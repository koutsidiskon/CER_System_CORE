
// Generated from OptionDeclarationParser.g4 by ANTLR 4.12.0

#pragma once


#include "antlr4-runtime.h"
#include "OptionDeclarationParserVisitor.h"


/**
 * This class provides an empty implementation of OptionDeclarationParserVisitor, which can be
 * extended to create a visitor which only needs to handle a subset of the available methods.
 */
class  OptionDeclarationParserBaseVisitor : public OptionDeclarationParserVisitor {
public:

  virtual std::any visitParse(OptionDeclarationParser::ParseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitError(OptionDeclarationParser::ErrorContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitOption_declaration(OptionDeclarationParser::Option_declarationContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFixed_time_policy(OptionDeclarationParser::Fixed_time_policyContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitBounded_time_policy(OptionDeclarationParser::Bounded_time_policyContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDirect_policy(OptionDeclarationParser::Direct_policyContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitNew_fixed_time_policy(OptionDeclarationParser::New_fixed_time_policyContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAvg_dynamic_time_policy(OptionDeclarationParser::Avg_dynamic_time_policyContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitJad_dynamic_time_policy(OptionDeclarationParser::Jad_dynamic_time_policyContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitMax_dynamic_time_policy(OptionDeclarationParser::Max_dynamic_time_policyContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitMax_ema_dynamic_time_policy(OptionDeclarationParser::Max_ema_dynamic_time_policyContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitP99_dynamic_time_policy(OptionDeclarationParser::P99_dynamic_time_policyContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPer_event_dynamic_time_policy(OptionDeclarationParser::Per_event_dynamic_time_policyContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStream_names(OptionDeclarationParser::Stream_namesContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTime_span(OptionDeclarationParser::Time_spanContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitHour_span(OptionDeclarationParser::Hour_spanContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitMinute_span(OptionDeclarationParser::Minute_spanContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSecond_span(OptionDeclarationParser::Second_spanContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStream_name(OptionDeclarationParser::Stream_nameContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAny_name(OptionDeclarationParser::Any_nameContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitNumber(OptionDeclarationParser::NumberContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitInteger(OptionDeclarationParser::IntegerContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDouble(OptionDeclarationParser::DoubleContext *ctx) override {
    return visitChildren(ctx);
  }


};

