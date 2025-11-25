#pragma once

#include <atomic>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <mutex>
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


    // std::chrono::time_point<std::chrono::system_clock>
    //   now = std::chrono::system_clock::now();
    //
    // std::chrono::duration<int64_t, std::nano> duration_since_last_save = now - last_save;
    // if (std::chrono::duration_cast<std::chrono::minutes>(duration_since_last_save).count()
    //     >= 15) {
    //   std::cout << "Saving events to disk in WaitFixedTimePolicy" << std::endl;
    //   save_events_to_disk();
    //   last_save = now;
    // }
    auto delay_ns = std::chrono::seconds(event.get_attribute_at_index<Types::IntValue>(5).val);

    if (event.get_primary_time().val < last_time_sent.val || delay_ns > time_to_wait) {
      drops++;
      LOG_WARNING(logger,
                  "Dropping event with id {} and time {} in "
                  "MaxDelayPolicy::receive_event due to time being before last time "
                  "sent",
                  event.get_unique_event_type_id(),
                  event.get_primary_time().val);
      return;
    }
    events.insert(std::move(event));
  }

  bool is_events_empty() override {
    std::lock_guard<std::mutex> lock(events_lock);
    return events.empty();
  }

 protected:
  /**
   * Tries to add received tuples to send queue according to specific policy
   */
  // Threshold for the number of events to process at once
  static constexpr size_t BATCH_SIZE = 2000;

  void try_add_tuples_to_send_queue() override {
    LOG_TRACE_L3(logger,
                "Trying to add tuples to send queue in "
                "MaxDelayPolicy::try_add_tuples_to_send");

    std::lock_guard<std::mutex> lock(events_lock);
    size_t current_size = events.size();
    
    if (current_size < BATCH_SIZE) {
        return;  // Not enough events to process
    }

    // Process all available events in batches of BATCH_SIZE
    while (!events.empty()) {
        size_t to_process = std::min(BATCH_SIZE, events.size());
        size_t processed = 0;
        auto iter = events.begin();
        
        LOG_TRACE_L1(logger, "Processing batch of {} events (remaining: {})", 
                    to_process, events.size());

        while (iter != events.end() && processed < to_process) {
            const Types::EventWrapper& event = *iter;
            auto next_iter = std::next(iter);  // Get next before modifying container
            
            sent_events++;
            LOG_TRACE_L2(logger,
                        "Adding event with id {} and time {} to send queue",
                        event.get_unique_event_type_id(),
                        event.get_primary_time().val);
            
            assert(event.get_primary_time().val >= last_time_sent.val
                  && "Event time is not after last time sent");
            
            auto internal_node = events.extract(iter);
            last_time_sent = internal_node.value().get_primary_time();
            this->send_event_queue.enqueue(std::move(internal_node.value()));
            
            processed++;
            iter = next_iter;
        }
    }
  }

  void force_add_tuples_to_send_queue() override {
    std::lock_guard<std::mutex> lock(events_lock);
    for (auto iter = events.begin(); iter != events.end();) {
      sent_events++;
      auto internal_node = events.extract(iter++);
      this->send_event_queue.enqueue(std::move(internal_node.value()));
    }
    std::cout << "Number of events RECEIVED by quarantine: " << received_events << std::endl;
    std::cout << "Number of events SENT by quarantine: " << sent_events << std::endl;
    std::cout << "Number of events DROPPED by quarantine: " << drops << std::endl;
  }
};
}  // namespace CORE::Internal::Interface::Module::Quarantine
