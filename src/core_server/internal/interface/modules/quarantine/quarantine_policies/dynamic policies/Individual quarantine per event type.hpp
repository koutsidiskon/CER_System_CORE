#pragma once

#include <atomic>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <mutex>
#include <optional>
#include <ratio>
#include <set>
#include <string>
#include <deque>
#include <numeric>
#include <tracy/Tracy.hpp>
#include <utility>
#include <algorithm>

#include "base_policy.hpp"
#include "core_server/internal/coordination/catalog.hpp"
#include "quill/LogMacros.h"
#include "shared/datatypes/aliases/port_number.hpp"
#include "shared/datatypes/eventWrapper.hpp"
#include "shared/datatypes/value.hpp"

namespace CORE::Internal::Interface::Module::Quarantine {

class DynamicTimePolicy: public BasePolicy {
  std::mutex events_lock;
    std::set<Types::EventWrapper> events;
    std::chrono::duration<int64_t, std::nano> time_to_wait;
    std::chrono::time_point<std::chrono::system_clock> last_save = std::chrono::system_clock::now();
    int drops = 0;
    int received_events = 0;
    int sent_events = 0;
    size_t max_quarantine_size = 0;
    size_t current_quarantine_bytes = 0;
    size_t max_quarantine_bytes = 0;
    std::optional<int64_t> last_received_event_time;
    bool end_of_stream_received = false;
    std::map<Types::UniqueEventTypeId, double> dynamic_time_per_event_type;
    std::map<Types::UniqueEventTypeId, std::deque<double>> latencies_per_type;

    double safety_margin = 1.5;  
    double learning_rate = 0.1;
    const double max_quarantine_ns = 1000000.0 * 1e9;
    
    std::deque<double> recent_latencies; 
    size_t window_size = 500;  

    Types::IntValue last_time_sent = Types::IntValue::create_lower_bound();

 public:
  DynamicTimePolicy(Catalog& catalog,
                 std::atomic<Types::PortNumber>& next_available_inproc_port,
                 std::chrono::duration<int64_t, std::nano> time_to_wait,
                 double safety_margin = 1.5,
                 size_t latency_window_size = 500)
    : BasePolicy(catalog, next_available_inproc_port),
      time_to_wait(time_to_wait),
      safety_margin(safety_margin),
      window_size(latency_window_size) {
    this->start();
  }
  
  void set_latency_window_size(size_t new_size) {
      std::lock_guard<std::mutex> lock(events_lock);
      window_size = new_size;
      while (recent_latencies.size() > window_size) {
          recent_latencies.pop_front();
      }
  }

  ~DynamicTimePolicy() { this->handle_destruction(); }

  void save_events_to_disk() {
    if (events.empty()) {
      return;
    }
    std::string out = "[";

    for (auto& event : events) {
      out += event.to_json() + ",\n";
    }

    // Remove the last comma and newline
    out = out.substr(0, out.size() - 2);

    out += "]";

    std::string filename = "events_"
                           + std::to_string(last_save.time_since_epoch().count()) + "_"
                           + std::to_string(
                             events.begin()->get_event_reference().get_event_type_id())
                           + ".json";

    std::ofstream myfile(filename);

    myfile << out;

    myfile.close();
  }

  void receive_event(Types::EventWrapper&& event) override {
    std::lock_guard<std::mutex> lock(events_lock);
    received_events++;

    auto type_id = event.get_unique_event_type_id();

    last_received_event_time = event.get_attribute_at_index<Types::IntValue>(1).val;
    auto event_gen_time = event.get_primary_time().val; 
    
    if (event_gen_time < last_time_sent.val) {
      drops++;

      std::cout << event.get_event_reference().to_string() << std::endl;
      
      LOG_WARNING(logger,
                 "Dropping out-of-order event. Current: {}, New: {}",
                 last_time_sent.val,
                 event.get_primary_time().val);
      return;
    }
    
    double current_latency_sec = last_received_event_time.value() - event_gen_time;
    double current_latency_ns = current_latency_sec * 1e9;
    
    if (current_latency_ns >= 0) {
      latencies_per_type[type_id].push_back(current_latency_ns);
     
      if (latencies_per_type[type_id].size() > window_size) {
          latencies_per_type[type_id].pop_front();
      }
      
      if (!latencies_per_type[type_id].empty()) {
          double window_max = *std::max_element(
              latencies_per_type[type_id].begin(), 
              latencies_per_type[type_id].end()
          );

          if (window_max > dynamic_time_per_event_type[type_id]) {
            dynamic_time_per_event_type[type_id] = window_max;
          } else {
            dynamic_time_per_event_type[type_id] = (1.0 - learning_rate) * dynamic_time_per_event_type[type_id] + learning_rate * window_max;
          }
      }
    }

    const std::size_t event_size_bytes = event.size_bytes();
    events.insert(std::move(event));
    current_quarantine_bytes += event_size_bytes;
    if (events.size() > max_quarantine_size) {
      max_quarantine_size = events.size();
    }
    if (current_quarantine_bytes > max_quarantine_bytes) {
      max_quarantine_bytes = current_quarantine_bytes;
    }
    try_add_tuples_to_send_queue();
  }

  bool is_events_empty() override {
    std::lock_guard<std::mutex> lock(events_lock);
    while (!events.empty()) {
        auto iter = events.begin();
        sent_events++;
        auto internal_node = events.extract(iter);
      current_quarantine_bytes -= internal_node.value().size_bytes();
        this->send_event_queue.enqueue(std::move(internal_node.value()));
    }
    end_of_stream_received = true;
    return true;
}

 protected:
  /**
   * Tries to add received tuples to send queue according to specific policy
   */
  void try_add_tuples_to_send_queue() override {
    if (!last_received_event_time || events.empty()) {
        return;
    }

    for (auto iter = events.begin(); iter != events.end();) {
      const auto& event = *iter;
      auto event_arrival_time = const_cast<Types::EventWrapper&>(event).get_attribute_at_index<Types::IntValue>(1).val;
      
      double current_lateness_ns = (last_received_event_time.value() - event_arrival_time) * 1e9;  
      
      double dynamic_quarantine_ns = std::clamp(
        dynamic_time_per_event_type[event.get_unique_event_type_id()] * safety_margin,
        static_cast<double>(time_to_wait.count()),
        max_quarantine_ns
      );
      
      if ((current_lateness_ns > dynamic_quarantine_ns) || end_of_stream_received) {
        sent_events++;
        
        assert(event.get_primary_time().val >= last_time_sent.val
                && "Event time is not after last time sent");
        
        auto internal_node = events.extract(iter++);
        current_quarantine_bytes -= internal_node.value().size_bytes();
        last_time_sent = internal_node.value().get_primary_time();
        this->send_event_queue.enqueue(std::move(internal_node.value()));
      } else {
          break;
      }
    }
  }


  void force_add_tuples_to_send_queue() override {
    std::cout << "Number of events RECEIVED by quarantine: " << received_events << std::endl;
    std::cout << "Number of events SENT by quarantine: " << sent_events << std::endl;
    std::cout << "Number of events DROPPED by quarantine: " << drops << std::endl;
    std::cout << "Maximum quarantine size: " << max_quarantine_size << std::endl;
    const double bytes_per_mb = 1024.0 * 1024.0;
    std::cout << "Maximum quarantine buffer size (MB): "
              << (static_cast<double>(max_quarantine_bytes) / bytes_per_mb)
              << std::endl;
  }
};
}  // namespace CORE::Internal::Interface::Module::Quarantine
