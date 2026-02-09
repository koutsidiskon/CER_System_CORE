
// Generated from OptionDeclarationLexer.g4 by ANTLR 4.12.0

#pragma once


#include "antlr4-runtime.h"




class  OptionDeclarationLexer : public antlr4::Lexer {
public:
  enum {
    WS = 1, K_CREATE = 2, K_QUARANTINE = 3, K_FIXED_TIME = 4, K_NEW_FIXED_TIME = 5, 
    K_AVG_DYNAMIC_TIME = 6, K_JAD_DYNAMIC_TIME = 7, K_MAX_DYNAMIC_TIME = 8, 
    K_MAX_EMA_DYNAMIC_TIME = 9, K_P99_DYNAMIC_TIME = 10, K_PER_EVENT_DYNAMIC_TIME = 11, 
    K_BOUNDED_TIME = 12, K_DIRECT = 13, K_HOURS = 14, K_MINUTES = 15, K_SECONDS = 16, 
    LEFT_CURLY_BRACKET = 17, RIGHT_CURLY_BRACKET = 18, COMMA = 19, DOUBLE_LITERAL = 20, 
    INTEGER_LITERAL = 21, NUMERICAL_EXPONENT = 22, IDENTIFIER = 23, UNEXPECTED_CHAR = 24
  };

  explicit OptionDeclarationLexer(antlr4::CharStream *input);

  ~OptionDeclarationLexer() override;


  std::string getGrammarFileName() const override;

  const std::vector<std::string>& getRuleNames() const override;

  const std::vector<std::string>& getChannelNames() const override;

  const std::vector<std::string>& getModeNames() const override;

  const antlr4::dfa::Vocabulary& getVocabulary() const override;

  antlr4::atn::SerializedATNView getSerializedATN() const override;

  const antlr4::atn::ATN& getATN() const override;

  // By default the static state used to implement the lexer is lazily initialized during the first
  // call to the constructor. You can call this function if you wish to initialize the static state
  // ahead of time.
  static void initialize();

private:

  // Individual action functions triggered by action() above.

  // Individual semantic predicate functions triggered by sempred() above.

};

