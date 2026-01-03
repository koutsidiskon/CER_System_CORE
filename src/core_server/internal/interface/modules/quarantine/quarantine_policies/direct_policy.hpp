#pragma once

#include <atomic>
#include <tracy/Tracy.hpp>
#include <utility>

#include "base_policy.hpp"
#include "core_server/internal/coordination/catalog.hpp"
#include "shared/datatypes/aliases/port_number.hpp"
#include "shared/datatypes/eventWrapper.hpp"

namespace CORE::Internal::Interface::Module::Quarantine {

class DirectPolicy : public BasePolicy {
  Types::IntValue last_send_primary_time;
  int drops = 0;

 public:
  DirectPolicy(Catalog& catalog,
               std::atomic<Types::PortNumber>& next_available_inproc_port)
      : BasePolicy(catalog, next_available_inproc_port) {
    last_send_primary_time = 0;
    this->start();
  }

  ~DirectPolicy() { this->handle_destruction(); }

  void receive_event(Types::EventWrapper&& event) override {
    ZoneScopedN("DirectPolicy::receive_event");
    if (event.get_primary_time().val < last_send_primary_time.val) {
      drops++;
    } else {
      this->send_event_queue.enqueue(std::move(event));
      last_send_primary_time = event.get_primary_time().val;
    }
  }

  bool is_events_empty() override {
    return true;
  }

 protected:
  void try_add_tuples_to_send_queue() override {
    // No need to try to add tuples to send queue as they are directly sent
  }

  void force_add_tuples_to_send_queue() override {
    // No need to try to add tuples to send queue as they are directly sent
    std::cout << "Drops: " << drops << std::endl;
  }
};
}  // namespace CORE::Internal::Interface::Module::Quarantine
