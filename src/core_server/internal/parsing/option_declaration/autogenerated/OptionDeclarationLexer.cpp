
// Generated from OptionDeclarationLexer.g4 by ANTLR 4.12.0


#include "OptionDeclarationLexer.h"


using namespace antlr4;



using namespace antlr4;

namespace {

struct OptionDeclarationLexerStaticData final {
  OptionDeclarationLexerStaticData(std::vector<std::string> ruleNames,
                          std::vector<std::string> channelNames,
                          std::vector<std::string> modeNames,
                          std::vector<std::string> literalNames,
                          std::vector<std::string> symbolicNames)
      : ruleNames(std::move(ruleNames)), channelNames(std::move(channelNames)),
        modeNames(std::move(modeNames)), literalNames(std::move(literalNames)),
        symbolicNames(std::move(symbolicNames)),
        vocabulary(this->literalNames, this->symbolicNames) {}

  OptionDeclarationLexerStaticData(const OptionDeclarationLexerStaticData&) = delete;
  OptionDeclarationLexerStaticData(OptionDeclarationLexerStaticData&&) = delete;
  OptionDeclarationLexerStaticData& operator=(const OptionDeclarationLexerStaticData&) = delete;
  OptionDeclarationLexerStaticData& operator=(OptionDeclarationLexerStaticData&&) = delete;

  std::vector<antlr4::dfa::DFA> decisionToDFA;
  antlr4::atn::PredictionContextCache sharedContextCache;
  const std::vector<std::string> ruleNames;
  const std::vector<std::string> channelNames;
  const std::vector<std::string> modeNames;
  const std::vector<std::string> literalNames;
  const std::vector<std::string> symbolicNames;
  const antlr4::dfa::Vocabulary vocabulary;
  antlr4::atn::SerializedATNView serializedATN;
  std::unique_ptr<antlr4::atn::ATN> atn;
};

::antlr4::internal::OnceFlag optiondeclarationlexerLexerOnceFlag;
OptionDeclarationLexerStaticData *optiondeclarationlexerLexerStaticData = nullptr;

void optiondeclarationlexerLexerInitialize() {
  assert(optiondeclarationlexerLexerStaticData == nullptr);
  auto staticData = std::make_unique<OptionDeclarationLexerStaticData>(
    std::vector<std::string>{
      "WS", "K_CREATE", "K_QUARANTINE", "K_FIXED_TIME", "K_NEW_FIXED_TIME", 
      "K_BOUNDED_TIME", "K_DYNAMIC_TIME", "K_DIRECT", "K_HOURS", "K_MINUTES", 
      "K_SECONDS", "LEFT_CURLY_BRACKET", "RIGHT_CURLY_BRACKET", "COMMA", 
      "DOUBLE_LITERAL", "INTEGER_LITERAL", "NUMERICAL_EXPONENT", "IDENTIFIER", 
      "UNEXPECTED_CHAR", "DIGIT", "A", "B", "C", "D", "E", "F", "G", "H", 
      "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", 
      "W", "X", "Y", "Z"
    },
    std::vector<std::string>{
      "DEFAULT_TOKEN_CHANNEL", "HIDDEN"
    },
    std::vector<std::string>{
      "DEFAULT_MODE"
    },
    std::vector<std::string>{
      "", "", "", "", "", "", "", "", "", "", "", "", "'{'", "'}'", "','"
    },
    std::vector<std::string>{
      "", "WS", "K_CREATE", "K_QUARANTINE", "K_FIXED_TIME", "K_NEW_FIXED_TIME", 
      "K_BOUNDED_TIME", "K_DYNAMIC_TIME", "K_DIRECT", "K_HOURS", "K_MINUTES", 
      "K_SECONDS", "LEFT_CURLY_BRACKET", "RIGHT_CURLY_BRACKET", "COMMA", 
      "DOUBLE_LITERAL", "INTEGER_LITERAL", "NUMERICAL_EXPONENT", "IDENTIFIER", 
      "UNEXPECTED_CHAR"
    }
  );
  static const int32_t serializedATNSegment[] = {
  	4,0,19,323,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
  	6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,2,14,
  	7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,7,20,2,21,
  	7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,2,27,7,27,2,28,
  	7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,7,33,2,34,7,34,2,35,
  	7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,39,2,40,7,40,2,41,7,41,2,42,
  	7,42,2,43,7,43,2,44,7,44,2,45,7,45,1,0,4,0,95,8,0,11,0,12,0,96,1,0,1,
  	0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,
  	1,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,
  	4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,
  	1,5,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,
  	6,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,3,8,183,8,8,1,9,1,9,
  	1,9,1,9,1,9,1,9,1,9,3,9,192,8,9,1,10,1,10,1,10,1,10,1,10,1,10,1,10,3,
  	10,201,8,10,1,11,1,11,1,12,1,12,1,13,1,13,1,14,1,14,1,14,1,14,1,14,3,
  	14,214,8,14,1,14,1,14,4,14,218,8,14,11,14,12,14,219,1,14,3,14,223,8,14,
  	1,14,1,14,4,14,227,8,14,11,14,12,14,228,1,14,1,14,3,14,233,8,14,1,15,
  	4,15,236,8,15,11,15,12,15,237,1,16,1,16,3,16,242,8,16,1,16,4,16,245,8,
  	16,11,16,12,16,246,1,17,1,17,1,17,1,17,5,17,253,8,17,10,17,12,17,256,
  	9,17,1,17,1,17,1,17,5,17,261,8,17,10,17,12,17,264,9,17,3,17,266,8,17,
  	1,18,1,18,1,19,1,19,1,20,1,20,1,21,1,21,1,22,1,22,1,23,1,23,1,24,1,24,
  	1,25,1,25,1,26,1,26,1,27,1,27,1,28,1,28,1,29,1,29,1,30,1,30,1,31,1,31,
  	1,32,1,32,1,33,1,33,1,34,1,34,1,35,1,35,1,36,1,36,1,37,1,37,1,38,1,38,
  	1,39,1,39,1,40,1,40,1,41,1,41,1,42,1,42,1,43,1,43,1,44,1,44,1,45,1,45,
  	0,0,46,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,23,12,25,13,
  	27,14,29,15,31,16,33,17,35,18,37,19,39,0,41,0,43,0,45,0,47,0,49,0,51,
  	0,53,0,55,0,57,0,59,0,61,0,63,0,65,0,67,0,69,0,71,0,73,0,75,0,77,0,79,
  	0,81,0,83,0,85,0,87,0,89,0,91,0,1,0,31,3,0,9,10,13,13,32,32,1,0,96,96,
  	3,0,65,90,95,95,97,122,4,0,48,57,65,90,95,95,97,122,1,0,48,57,2,0,65,
  	65,97,97,2,0,66,66,98,98,2,0,67,67,99,99,2,0,68,68,100,100,2,0,69,69,
  	101,101,2,0,70,70,102,102,2,0,71,71,103,103,2,0,72,72,104,104,2,0,73,
  	73,105,105,2,0,74,74,106,106,2,0,75,75,107,107,2,0,76,76,108,108,2,0,
  	77,77,109,109,2,0,78,78,110,110,2,0,79,79,111,111,2,0,80,80,112,112,2,
  	0,81,81,113,113,2,0,82,82,114,114,2,0,83,83,115,115,2,0,84,84,116,116,
  	2,0,85,85,117,117,2,0,86,86,118,118,2,0,87,87,119,119,2,0,88,88,120,120,
  	2,0,89,89,121,121,2,0,90,90,122,122,312,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,
  	0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,
  	0,17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,0,0,0,23,1,0,0,0,0,25,1,0,0,0,0,27,
  	1,0,0,0,0,29,1,0,0,0,0,31,1,0,0,0,0,33,1,0,0,0,0,35,1,0,0,0,0,37,1,0,
  	0,0,1,94,1,0,0,0,3,100,1,0,0,0,5,107,1,0,0,0,7,118,1,0,0,0,9,129,1,0,
  	0,0,11,144,1,0,0,0,13,157,1,0,0,0,15,170,1,0,0,0,17,177,1,0,0,0,19,184,
  	1,0,0,0,21,193,1,0,0,0,23,202,1,0,0,0,25,204,1,0,0,0,27,206,1,0,0,0,29,
  	232,1,0,0,0,31,235,1,0,0,0,33,239,1,0,0,0,35,265,1,0,0,0,37,267,1,0,0,
  	0,39,269,1,0,0,0,41,271,1,0,0,0,43,273,1,0,0,0,45,275,1,0,0,0,47,277,
  	1,0,0,0,49,279,1,0,0,0,51,281,1,0,0,0,53,283,1,0,0,0,55,285,1,0,0,0,57,
  	287,1,0,0,0,59,289,1,0,0,0,61,291,1,0,0,0,63,293,1,0,0,0,65,295,1,0,0,
  	0,67,297,1,0,0,0,69,299,1,0,0,0,71,301,1,0,0,0,73,303,1,0,0,0,75,305,
  	1,0,0,0,77,307,1,0,0,0,79,309,1,0,0,0,81,311,1,0,0,0,83,313,1,0,0,0,85,
  	315,1,0,0,0,87,317,1,0,0,0,89,319,1,0,0,0,91,321,1,0,0,0,93,95,7,0,0,
  	0,94,93,1,0,0,0,95,96,1,0,0,0,96,94,1,0,0,0,96,97,1,0,0,0,97,98,1,0,0,
  	0,98,99,6,0,0,0,99,2,1,0,0,0,100,101,3,45,22,0,101,102,3,75,37,0,102,
  	103,3,49,24,0,103,104,3,41,20,0,104,105,3,79,39,0,105,106,3,49,24,0,106,
  	4,1,0,0,0,107,108,3,73,36,0,108,109,3,81,40,0,109,110,3,41,20,0,110,111,
  	3,75,37,0,111,112,3,41,20,0,112,113,3,67,33,0,113,114,3,79,39,0,114,115,
  	3,57,28,0,115,116,3,67,33,0,116,117,3,49,24,0,117,6,1,0,0,0,118,119,3,
  	51,25,0,119,120,3,57,28,0,120,121,3,87,43,0,121,122,3,49,24,0,122,123,
  	3,47,23,0,123,124,5,95,0,0,124,125,3,79,39,0,125,126,3,57,28,0,126,127,
  	3,65,32,0,127,128,3,49,24,0,128,8,1,0,0,0,129,130,3,67,33,0,130,131,3,
  	49,24,0,131,132,3,85,42,0,132,133,5,95,0,0,133,134,3,51,25,0,134,135,
  	3,57,28,0,135,136,3,87,43,0,136,137,3,49,24,0,137,138,3,47,23,0,138,139,
  	5,95,0,0,139,140,3,79,39,0,140,141,3,57,28,0,141,142,3,65,32,0,142,143,
  	3,49,24,0,143,10,1,0,0,0,144,145,3,43,21,0,145,146,3,69,34,0,146,147,
  	3,81,40,0,147,148,3,67,33,0,148,149,3,47,23,0,149,150,3,49,24,0,150,151,
  	3,47,23,0,151,152,5,95,0,0,152,153,3,79,39,0,153,154,3,57,28,0,154,155,
  	3,65,32,0,155,156,3,49,24,0,156,12,1,0,0,0,157,158,3,47,23,0,158,159,
  	3,89,44,0,159,160,3,67,33,0,160,161,3,41,20,0,161,162,3,65,32,0,162,163,
  	3,57,28,0,163,164,3,45,22,0,164,165,5,95,0,0,165,166,3,79,39,0,166,167,
  	3,57,28,0,167,168,3,65,32,0,168,169,3,49,24,0,169,14,1,0,0,0,170,171,
  	3,47,23,0,171,172,3,57,28,0,172,173,3,75,37,0,173,174,3,49,24,0,174,175,
  	3,45,22,0,175,176,3,79,39,0,176,16,1,0,0,0,177,178,3,55,27,0,178,179,
  	3,69,34,0,179,180,3,81,40,0,180,182,3,75,37,0,181,183,3,77,38,0,182,181,
  	1,0,0,0,182,183,1,0,0,0,183,18,1,0,0,0,184,185,3,65,32,0,185,186,3,57,
  	28,0,186,187,3,67,33,0,187,188,3,81,40,0,188,189,3,79,39,0,189,191,3,
  	49,24,0,190,192,3,77,38,0,191,190,1,0,0,0,191,192,1,0,0,0,192,20,1,0,
  	0,0,193,194,3,77,38,0,194,195,3,49,24,0,195,196,3,45,22,0,196,197,3,69,
  	34,0,197,198,3,67,33,0,198,200,3,47,23,0,199,201,3,77,38,0,200,199,1,
  	0,0,0,200,201,1,0,0,0,201,22,1,0,0,0,202,203,5,123,0,0,203,24,1,0,0,0,
  	204,205,5,125,0,0,205,26,1,0,0,0,206,207,5,44,0,0,207,28,1,0,0,0,208,
  	209,3,31,15,0,209,210,5,46,0,0,210,211,3,33,16,0,211,233,1,0,0,0,212,
  	214,3,31,15,0,213,212,1,0,0,0,213,214,1,0,0,0,214,215,1,0,0,0,215,217,
  	5,46,0,0,216,218,3,39,19,0,217,216,1,0,0,0,218,219,1,0,0,0,219,217,1,
  	0,0,0,219,220,1,0,0,0,220,233,1,0,0,0,221,223,3,31,15,0,222,221,1,0,0,
  	0,222,223,1,0,0,0,223,224,1,0,0,0,224,226,5,46,0,0,225,227,3,39,19,0,
  	226,225,1,0,0,0,227,228,1,0,0,0,228,226,1,0,0,0,228,229,1,0,0,0,229,230,
  	1,0,0,0,230,231,3,33,16,0,231,233,1,0,0,0,232,208,1,0,0,0,232,213,1,0,
  	0,0,232,222,1,0,0,0,233,30,1,0,0,0,234,236,3,39,19,0,235,234,1,0,0,0,
  	236,237,1,0,0,0,237,235,1,0,0,0,237,238,1,0,0,0,238,32,1,0,0,0,239,241,
  	3,49,24,0,240,242,5,45,0,0,241,240,1,0,0,0,241,242,1,0,0,0,242,244,1,
  	0,0,0,243,245,3,39,19,0,244,243,1,0,0,0,245,246,1,0,0,0,246,244,1,0,0,
  	0,246,247,1,0,0,0,247,34,1,0,0,0,248,254,5,96,0,0,249,253,8,1,0,0,250,
  	251,5,96,0,0,251,253,5,96,0,0,252,249,1,0,0,0,252,250,1,0,0,0,253,256,
  	1,0,0,0,254,252,1,0,0,0,254,255,1,0,0,0,255,257,1,0,0,0,256,254,1,0,0,
  	0,257,266,5,96,0,0,258,262,7,2,0,0,259,261,7,3,0,0,260,259,1,0,0,0,261,
  	264,1,0,0,0,262,260,1,0,0,0,262,263,1,0,0,0,263,266,1,0,0,0,264,262,1,
  	0,0,0,265,248,1,0,0,0,265,258,1,0,0,0,266,36,1,0,0,0,267,268,9,0,0,0,
  	268,38,1,0,0,0,269,270,7,4,0,0,270,40,1,0,0,0,271,272,7,5,0,0,272,42,
  	1,0,0,0,273,274,7,6,0,0,274,44,1,0,0,0,275,276,7,7,0,0,276,46,1,0,0,0,
  	277,278,7,8,0,0,278,48,1,0,0,0,279,280,7,9,0,0,280,50,1,0,0,0,281,282,
  	7,10,0,0,282,52,1,0,0,0,283,284,7,11,0,0,284,54,1,0,0,0,285,286,7,12,
  	0,0,286,56,1,0,0,0,287,288,7,13,0,0,288,58,1,0,0,0,289,290,7,14,0,0,290,
  	60,1,0,0,0,291,292,7,15,0,0,292,62,1,0,0,0,293,294,7,16,0,0,294,64,1,
  	0,0,0,295,296,7,17,0,0,296,66,1,0,0,0,297,298,7,18,0,0,298,68,1,0,0,0,
  	299,300,7,19,0,0,300,70,1,0,0,0,301,302,7,20,0,0,302,72,1,0,0,0,303,304,
  	7,21,0,0,304,74,1,0,0,0,305,306,7,22,0,0,306,76,1,0,0,0,307,308,7,23,
  	0,0,308,78,1,0,0,0,309,310,7,24,0,0,310,80,1,0,0,0,311,312,7,25,0,0,312,
  	82,1,0,0,0,313,314,7,26,0,0,314,84,1,0,0,0,315,316,7,27,0,0,316,86,1,
  	0,0,0,317,318,7,28,0,0,318,88,1,0,0,0,319,320,7,29,0,0,320,90,1,0,0,0,
  	321,322,7,30,0,0,322,92,1,0,0,0,17,0,96,182,191,200,213,219,222,228,232,
  	237,241,246,252,254,262,265,1,6,0,0
  };
  staticData->serializedATN = antlr4::atn::SerializedATNView(serializedATNSegment, sizeof(serializedATNSegment) / sizeof(serializedATNSegment[0]));

  antlr4::atn::ATNDeserializer deserializer;
  staticData->atn = deserializer.deserialize(staticData->serializedATN);

  const size_t count = staticData->atn->getNumberOfDecisions();
  staticData->decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    staticData->decisionToDFA.emplace_back(staticData->atn->getDecisionState(i), i);
  }
  optiondeclarationlexerLexerStaticData = staticData.release();
}

}

OptionDeclarationLexer::OptionDeclarationLexer(CharStream *input) : Lexer(input) {
  OptionDeclarationLexer::initialize();
  _interpreter = new atn::LexerATNSimulator(this, *optiondeclarationlexerLexerStaticData->atn, optiondeclarationlexerLexerStaticData->decisionToDFA, optiondeclarationlexerLexerStaticData->sharedContextCache);
}

OptionDeclarationLexer::~OptionDeclarationLexer() {
  delete _interpreter;
}

std::string OptionDeclarationLexer::getGrammarFileName() const {
  return "OptionDeclarationLexer.g4";
}

const std::vector<std::string>& OptionDeclarationLexer::getRuleNames() const {
  return optiondeclarationlexerLexerStaticData->ruleNames;
}

const std::vector<std::string>& OptionDeclarationLexer::getChannelNames() const {
  return optiondeclarationlexerLexerStaticData->channelNames;
}

const std::vector<std::string>& OptionDeclarationLexer::getModeNames() const {
  return optiondeclarationlexerLexerStaticData->modeNames;
}

const dfa::Vocabulary& OptionDeclarationLexer::getVocabulary() const {
  return optiondeclarationlexerLexerStaticData->vocabulary;
}

antlr4::atn::SerializedATNView OptionDeclarationLexer::getSerializedATN() const {
  return optiondeclarationlexerLexerStaticData->serializedATN;
}

const atn::ATN& OptionDeclarationLexer::getATN() const {
  return *optiondeclarationlexerLexerStaticData->atn;
}




void OptionDeclarationLexer::initialize() {
  ::antlr4::internal::call_once(optiondeclarationlexerLexerOnceFlag, optiondeclarationlexerLexerInitialize);
}
