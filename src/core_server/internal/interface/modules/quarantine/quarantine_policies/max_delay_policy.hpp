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
#include <tracy/Tracy.hpp>
#include <utility>

#include "base_policy.hpp"
#include "core_server/internal/coordination/catalog.hpp"
#include "quill/LogMacros.h"
#include "shared/datatypes/aliases/port_number.hpp"
#include "shared/datatypes/eventWrapper.hpp"
#include "shared/datatypes/value.hpp"

namespace CORE::Internal::Interface::Module::Quarantine {

class MaxDelayPolicy: public BasePolicy {
  std::mutex events_lock;
  std::set<Types::EventWrapper> events;
  std::chrono::duration<int64_t, std::nano> time_to_wait;
  std::chrono::time_point<std::chrono::system_clock>
    last_save = std::chrono::system_clock::now();
  int drops = 0;
  int received_events = 0;
  int sent_events = 0;  
  std::optional<int64_t> last_received_event_time;
  bool end_of_stream_received = false;

  // Corresponds to the last time an event was sent
  Types::IntValue last_time_sent = Types::IntValue::create_lower_bound();

 public:
  MaxDelayPolicy(Catalog& catalog,
                      std::atomic<Types::PortNumber>& next_available_inproc_port,
                      std::chrono::duration<int64_t, std::nano> time_to_wait)
      : BasePolicy(catalog, next_available_inproc_port), time_to_wait(time_to_wait) {
    this->start();
  }

  ~MaxDelayPolicy() { this->handle_destruction(); }

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
    received_events++;
    ZoneScopedN("MaxDelayPolicy::receive_event");
    LOG_TRACE_L1(logger,
                 "Received event with id {} and time {} in "
                 "MaxDelayPolicy::receive_event",
                 event.get_unique_event_type_id(),
                 event.get_primary_time().val);

    std::lock_guard<std::mutex> lock(events_lock);



    if (event.get_primary_time().val < last_time_sent.val) {
      drops++;
      LOG_WARNING(logger,
                  "Dropping event with id {} and time {} in "
                  "MaxDelayPolicy::receive_event due to time being before last time "
                  "sent",
                  event.get_unique_event_type_id(),
                  event.get_primary_time().val);
      return;
    }
    last_received_event_time = event.get_attribute_at_index<Types::IntValue>(1).val;
    events.insert(std::move(event));
    try_add_tuples_to_send_queue(-1);
  }

  bool is_events_empty() override {
    std::lock_guard<std::mutex> lock(events_lock);
    while (!events.empty()) {
        auto iter = events.begin();
        sent_events++;
        auto internal_node = events.extract(iter);
        this->send_event_queue.enqueue(std::move(internal_node.value()));
    }
    end_of_stream_received = true;
    return true;
}

 protected:
  /**
   * Tries to add received tuples to send queue according to specific policy
   */
  void try_add_tuples_to_send_queue(size_t type_id) override {
    LOG_TRACE_L3(logger,
                 "Trying to add tuples to send queue in "
                 "MaxDelayPolicy::try_add_tuples_to_send");

    //std::lock_guard<std::mutex> lock(events_lock);
    
    for (auto iter = events.begin(); iter != events.end();) {
      const Types::EventWrapper& event = *iter;
      auto event_time = const_cast<Types::EventWrapper&>(event).get_attribute_at_index<Types::IntValue>(1).val;
      // Calculate delay using event timestamps
      auto duration = std::chrono::nanoseconds(last_received_event_time.value() * 1000000000LL) - std::chrono::nanoseconds(event_time * 1000000000LL);
      if ((duration > time_to_wait) || (end_of_stream_received)){
        sent_events++;
        LOG_TRACE_L1(logger,
                     "Adding event with id {} and time {} to send queue in "
                     "MaxDelayPolicy::try_add_tuples_to_send",
                     event.get_unique_event_type_id(),
                     event.get_primary_time().val);
        assert(event.get_primary_time().val >= last_time_sent.val
               && "Event time is not after last time sent");
        auto internal_node = events.extract(iter++);
        last_time_sent = internal_node.value().get_primary_time();
        this->send_event_queue.enqueue(std::move(internal_node.value()));
      } else {
        // If we couldn't remove the first event, stop trying
        return;
      }
    }
  }

  void force_add_tuples_to_send_queue() override {
    //std::lock_guard<std::mutex> lock(events_lock);
    /*for (auto iter = events.begin(); iter != events.end();) {
      
      sent_events++;
      auto internal_node = events.extract(iter++);
      this->send_event_queue.enqueue(std::move(internal_node.value()));
    }*/
    std::cout << "Number of events RECEIVED by quarantine: " << received_events << std::endl;
    std::cout << "Number of events SENT by quarantine: " << sent_events << std::endl;
    std::cout << "Number of events DROPPED by quarantine: " << drops << std::endl;
  }
};
}  // namespace CORE::Internal::Interface::Module::Quarantine
