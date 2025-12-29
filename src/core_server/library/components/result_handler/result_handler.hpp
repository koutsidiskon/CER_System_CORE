#pragma once

#include <Loop.h>
#include <WebSocket.h>
#include <WebSocketProtocol.h>
#include <quill/Frontend.h>
#include <quill/LogMacros.h>
#include <quill/Logger.h>

#include <iostream>
#include <iomanip>
#include <list>
#include <memory>
#include <mutex>
#include <optional>
#include <stdexcept>
#include <string>
#include <tracy/Tracy.hpp>
#include <utility>
#include <chrono>
#include <vector>

#include "core_server/internal/coordination/query_catalog.hpp"
#include "core_server/internal/evaluation/enumeration/tecs/enumerator.hpp"
#include "core_server/library/components/user_data.hpp"
#include "result_handler_types.hpp"
#include "shared/datatypes/aliases/port_number.hpp"
#include "shared/datatypes/enumerator.hpp"
#include "shared/networking/message_broadcaster/zmq_message_broadcaster.hpp"
#include "shared/serializer/cereal_serializer.hpp"

namespace CORE::Library::Components {

class ResultHandler {
  ResultHandlerType result_handler_type;
  std::optional<const Internal::QueryCatalog> query_catalog;

 protected:
  quill::Logger* logger = quill::Frontend::get_logger("root");

 public:
  explicit ResultHandler(ResultHandlerType result_handler_type)
      : result_handler_type(result_handler_type) {}

  void set_query_catalog(const Internal::QueryCatalog& query_catalog) {
    this->query_catalog.emplace(query_catalog);
  }

  const Internal::QueryCatalog& get_query_catalog() {
    if (!query_catalog.has_value()) {
      throw std::runtime_error("Query catalog is not set");
    }
    return query_catalog.value();
  }

  void operator()(std::optional<Internal::tECS::Enumerator>&& enumerator) {
    handle_complex_event(std::move(enumerator));
  }

  virtual void start() = 0;

  virtual void
  handle_complex_event(std::optional<Internal::tECS::Enumerator>&& enumerator) = 0;

  ResultHandlerType get_result_handler_type() const { return result_handler_type; }

  virtual std::string get_identifier() const = 0;

  virtual ~ResultHandler() = default;
};

class OfflineResultHandler : public ResultHandler {
 private:
  size_t total_events = 0;
  double total_detection_delay = 0.0;

 public:
  OfflineResultHandler() : ResultHandler(ResultHandlerType::OFFLINE) {}

  ~OfflineResultHandler() override {
    // Print summary when handler is destroyed
    if (total_events > 0) {
      std::cout << "\n=== FINAL SUMMARY ===\n";
      std::cout << "Total events processed: " << total_events << "\n";
      std::cout << "Average detection delay: " << std::fixed << std::setprecision(9) 
                << (total_detection_delay / total_events) << "s\n";
      std::cout << "====================\n";
    }
  }

  void handle_complex_event(
    std::optional<Internal::tECS::Enumerator>&& internal_enumerator) override {
    ZoneScopedN("OfflineResultHandler::handle_complex_event");

    if (!internal_enumerator.has_value()) {
        // End of processing signal, but summary will be printed in destructor
        return;
    }
    
    auto& enumerator = internal_enumerator.value();
    const auto& detection_times = enumerator.get_detection_times();
    
    size_t event_index = 0;
    for (const auto& event : enumerator) {
        // Get print time immediately after enumeration of this event
        auto print_time = std::chrono::duration_cast<std::chrono::nanoseconds>(
            std::chrono::high_resolution_clock::now().time_since_epoch()).count();
        
        // Get the time when the last event arrived at CORE (from received_time of EventWrapper)
        auto last_event_arrival_time = detection_times[event_index];
        
        // Convert to string
        std::string event_string = event.to_string<true>();
        
      
        uint64_t last_event_time = 0;
        uint64_t last_arrive_time = 0;
        
    
        size_t last_attributes_pos = event_string.rfind("attributes: [");
        
        if (last_attributes_pos != std::string::npos) {
        
            size_t numbers_start = last_attributes_pos + 13; 
            // Extract the first number (event_time)
            size_t first_space = event_string.find(' ', numbers_start);
            if (first_space != std::string::npos) {
                std::string event_time_str = event_string.substr(numbers_start, first_space - numbers_start);
                last_event_time = std::stoull(event_time_str);
                
                // Extract the second number (arrive_time)
                size_t second_space = event_string.find(' ', first_space + 1);
                if (second_space != std::string::npos) {
                    std::string arrive_time_str = event_string.substr(first_space + 1, second_space - first_space - 1);
                    last_arrive_time = std::stoull(arrive_time_str);
                }
            }
        }
        
        // Calculate delays
        uint64_t system_arrival_delay = 0;     // arrive_time - event_time (from data, in seconds)
        uint64_t processing_delay_ns = 0;      // print_time - last_event_arrival_time (measured in real-time, in ns)
        double detection_delay = 0.0;          // system_arrival_delay + processing_delay (in seconds)
        
        if (last_event_time > 0 && last_arrive_time > 0) {
            // System Arrival Delay: time for event to arrive at CORE (from data, in seconds)
            system_arrival_delay = last_arrive_time - last_event_time;
            
            // Processing Delay: time from when last event arrived at CORE until print (measured in real-time)
            processing_delay_ns = print_time - last_event_arrival_time;
            
            // Convert processing_delay to seconds and add to system_arrival_delay
            double processing_delay_s = static_cast<double>(processing_delay_ns) / 1000000000.0;
            detection_delay = system_arrival_delay + processing_delay_s;
        }
        
        total_detection_delay += detection_delay;
        total_events++;
        
        // Print individual event details
        std::cout << "Event " << total_events << ":\n";
        std::cout << "  System Arrival Delay (network): " << system_arrival_delay << "s\n";
        std::cout << "  Processing Delay (CORE processing): " << processing_delay_ns << "ns (" 
                  << std::fixed << std::setprecision(9) << static_cast<double>(processing_delay_ns) / 1000000000.0 << "s)\n";
        std::cout << "  Detection Delay (Total): " << std::fixed << std::setprecision(9) << detection_delay << "s\n";
        std::cout << "  " << event_string << "\n\n";
        
        event_index++;
    }
  }

  void start() override {}

  // Always returns "offline" as the identifier
  std::string get_identifier() const override { return "offline"; }
};

class OnlineResultHandler : public ResultHandler {
 public:
  std::unique_ptr<Internal::ZMQMessageBroadcaster> broadcaster;
  Types::PortNumber port{};

  explicit OnlineResultHandler(Types::PortNumber assigned_port)
      : port(assigned_port),
        ResultHandler(ResultHandlerType::ONLINE),
        broadcaster{nullptr} {}

  void start() override {
    broadcaster = std::make_unique<Internal::ZMQMessageBroadcaster>(
      "tcp://*:" + std::to_string(port));
    LOG_INFO(logger, "Starting broadcaster at port {}", port);
  }

  void handle_complex_event(
    std::optional<Internal::tECS::Enumerator>&& internal_enumerator) override {
    Types::Enumerator enumerator;
    if (internal_enumerator.has_value()) {
      enumerator = get_query_catalog().convert_enumerator(
        std::move(internal_enumerator.value()));
    }
    std::string serialized_enumerator{
      Internal::CerealSerializer<Types::Enumerator>::serialize(enumerator)};

    broadcaster->broadcast(serialized_enumerator);
  }

  // Returns the port as the identifier
  std::string get_identifier() const override { return std::to_string(port); }
};

class WebSocketResultHandler : public ResultHandler {
  std::shared_ptr<std::list<uWS::WebSocket<false, true, UserData>*>> ws_clients;
  std::mutex& ws_clients_mutex;
  UniqueWebSocketQueryId query_id;
  uWS::Loop* uws_loop;

 public:
  explicit WebSocketResultHandler(
    std::shared_ptr<std::list<uWS::WebSocket<false, true, UserData>*>> ws_clients,
    std::mutex& ws_clients_mutex,
    uWS::Loop* uws_loop,
    UniqueWebSocketQueryId query_id)
      : ws_clients(ws_clients),
        ws_clients_mutex(ws_clients_mutex),
        uws_loop(uws_loop),
        query_id(query_id),
        ResultHandler(ResultHandlerType::WEBSOCKET) {}

  void start() override {}

  void handle_complex_event(
    std::optional<Internal::tECS::Enumerator>&& internal_enumerator) override {
    if (!internal_enumerator.has_value()) {  // NOLINT
      return;
    }

    std::string result_json = "[";
    for (const auto& complex_event : internal_enumerator.value()) {
      result_json += complex_event.to_json(get_query_catalog());
      result_json += ",";
    }
    result_json = result_json.substr(0, result_json.size() - 1);
    result_json += "]";

    uws_loop->defer([this, result_json]() {
      std::lock_guard<std::mutex> lock(ws_clients_mutex);
      for (auto& ws_client : *ws_clients) {
        ws_client->send(result_json, uWS::OpCode::TEXT);  // NOLINT
      }
    });
    // Send the result to all connected clients
  }

  std::string get_identifier() const override { return std::to_string(query_id); }
};

}  // namespace CORE::Library::Components
