
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
      "WS", "K_CREATE", "K_QUARANTINE", "K_FIXED_TIME", "K_MAX_DELAY", "K_BOUNDED_TIME", 
      "K_DYNAMIC_TIME", "K_DIRECT", "K_HOURS", "K_MINUTES", "K_SECONDS", 
      "LEFT_CURLY_BRACKET", "RIGHT_CURLY_BRACKET", "COMMA", "DOUBLE_LITERAL", 
      "INTEGER_LITERAL", "NUMERICAL_EXPONENT", "IDENTIFIER", "UNEXPECTED_CHAR", 
      "DIGIT", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", 
      "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
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
      "", "WS", "K_CREATE", "K_QUARANTINE", "K_FIXED_TIME", "K_MAX_DELAY", 
      "K_BOUNDED_TIME", "K_DYNAMIC_TIME", "K_DIRECT", "K_HOURS", "K_MINUTES", 
      "K_SECONDS", "LEFT_CURLY_BRACKET", "RIGHT_CURLY_BRACKET", "COMMA", 
      "DOUBLE_LITERAL", "INTEGER_LITERAL", "NUMERICAL_EXPONENT", "IDENTIFIER", 
      "UNEXPECTED_CHAR"
    }
  );
  static const int32_t serializedATNSegment[] = {
  	4,0,19,318,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
  	6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,2,14,
  	7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,7,20,2,21,
  	7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,2,27,7,27,2,28,
  	7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,7,33,2,34,7,34,2,35,
  	7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,39,2,40,7,40,2,41,7,41,2,42,
  	7,42,2,43,7,43,2,44,7,44,2,45,7,45,1,0,4,0,95,8,0,11,0,12,0,96,1,0,1,
  	0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,
  	1,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,
  	4,1,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,
  	1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,7,1,7,1,
  	7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,3,8,178,8,8,1,9,1,9,1,9,1,9,1,9,1,9,1,9,
  	3,9,187,8,9,1,10,1,10,1,10,1,10,1,10,1,10,1,10,3,10,196,8,10,1,11,1,11,
  	1,12,1,12,1,13,1,13,1,14,1,14,1,14,1,14,1,14,3,14,209,8,14,1,14,1,14,
  	4,14,213,8,14,11,14,12,14,214,1,14,3,14,218,8,14,1,14,1,14,4,14,222,8,
  	14,11,14,12,14,223,1,14,1,14,3,14,228,8,14,1,15,4,15,231,8,15,11,15,12,
  	15,232,1,16,1,16,3,16,237,8,16,1,16,4,16,240,8,16,11,16,12,16,241,1,17,
  	1,17,1,17,1,17,5,17,248,8,17,10,17,12,17,251,9,17,1,17,1,17,1,17,5,17,
  	256,8,17,10,17,12,17,259,9,17,3,17,261,8,17,1,18,1,18,1,19,1,19,1,20,
  	1,20,1,21,1,21,1,22,1,22,1,23,1,23,1,24,1,24,1,25,1,25,1,26,1,26,1,27,
  	1,27,1,28,1,28,1,29,1,29,1,30,1,30,1,31,1,31,1,32,1,32,1,33,1,33,1,34,
  	1,34,1,35,1,35,1,36,1,36,1,37,1,37,1,38,1,38,1,39,1,39,1,40,1,40,1,41,
  	1,41,1,42,1,42,1,43,1,43,1,44,1,44,1,45,1,45,0,0,46,1,1,3,2,5,3,7,4,9,
  	5,11,6,13,7,15,8,17,9,19,10,21,11,23,12,25,13,27,14,29,15,31,16,33,17,
  	35,18,37,19,39,0,41,0,43,0,45,0,47,0,49,0,51,0,53,0,55,0,57,0,59,0,61,
  	0,63,0,65,0,67,0,69,0,71,0,73,0,75,0,77,0,79,0,81,0,83,0,85,0,87,0,89,
  	0,91,0,1,0,31,3,0,9,10,13,13,32,32,1,0,96,96,3,0,65,90,95,95,97,122,4,
  	0,48,57,65,90,95,95,97,122,1,0,48,57,2,0,65,65,97,97,2,0,66,66,98,98,
  	2,0,67,67,99,99,2,0,68,68,100,100,2,0,69,69,101,101,2,0,70,70,102,102,
  	2,0,71,71,103,103,2,0,72,72,104,104,2,0,73,73,105,105,2,0,74,74,106,106,
  	2,0,75,75,107,107,2,0,76,76,108,108,2,0,77,77,109,109,2,0,78,78,110,110,
  	2,0,79,79,111,111,2,0,80,80,112,112,2,0,81,81,113,113,2,0,82,82,114,114,
  	2,0,83,83,115,115,2,0,84,84,116,116,2,0,85,85,117,117,2,0,86,86,118,118,
  	2,0,87,87,119,119,2,0,88,88,120,120,2,0,89,89,121,121,2,0,90,90,122,122,
  	307,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,
  	1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,
  	0,0,0,23,1,0,0,0,0,25,1,0,0,0,0,27,1,0,0,0,0,29,1,0,0,0,0,31,1,0,0,0,
  	0,33,1,0,0,0,0,35,1,0,0,0,0,37,1,0,0,0,1,94,1,0,0,0,3,100,1,0,0,0,5,107,
  	1,0,0,0,7,118,1,0,0,0,9,129,1,0,0,0,11,139,1,0,0,0,13,152,1,0,0,0,15,
  	165,1,0,0,0,17,172,1,0,0,0,19,179,1,0,0,0,21,188,1,0,0,0,23,197,1,0,0,
  	0,25,199,1,0,0,0,27,201,1,0,0,0,29,227,1,0,0,0,31,230,1,0,0,0,33,234,
  	1,0,0,0,35,260,1,0,0,0,37,262,1,0,0,0,39,264,1,0,0,0,41,266,1,0,0,0,43,
  	268,1,0,0,0,45,270,1,0,0,0,47,272,1,0,0,0,49,274,1,0,0,0,51,276,1,0,0,
  	0,53,278,1,0,0,0,55,280,1,0,0,0,57,282,1,0,0,0,59,284,1,0,0,0,61,286,
  	1,0,0,0,63,288,1,0,0,0,65,290,1,0,0,0,67,292,1,0,0,0,69,294,1,0,0,0,71,
  	296,1,0,0,0,73,298,1,0,0,0,75,300,1,0,0,0,77,302,1,0,0,0,79,304,1,0,0,
  	0,81,306,1,0,0,0,83,308,1,0,0,0,85,310,1,0,0,0,87,312,1,0,0,0,89,314,
  	1,0,0,0,91,316,1,0,0,0,93,95,7,0,0,0,94,93,1,0,0,0,95,96,1,0,0,0,96,94,
  	1,0,0,0,96,97,1,0,0,0,97,98,1,0,0,0,98,99,6,0,0,0,99,2,1,0,0,0,100,101,
  	3,45,22,0,101,102,3,75,37,0,102,103,3,49,24,0,103,104,3,41,20,0,104,105,
  	3,79,39,0,105,106,3,49,24,0,106,4,1,0,0,0,107,108,3,73,36,0,108,109,3,
  	81,40,0,109,110,3,41,20,0,110,111,3,75,37,0,111,112,3,41,20,0,112,113,
  	3,67,33,0,113,114,3,79,39,0,114,115,3,57,28,0,115,116,3,67,33,0,116,117,
  	3,49,24,0,117,6,1,0,0,0,118,119,3,51,25,0,119,120,3,57,28,0,120,121,3,
  	87,43,0,121,122,3,49,24,0,122,123,3,47,23,0,123,124,5,95,0,0,124,125,
  	3,79,39,0,125,126,3,57,28,0,126,127,3,65,32,0,127,128,3,49,24,0,128,8,
  	1,0,0,0,129,130,3,65,32,0,130,131,3,41,20,0,131,132,3,87,43,0,132,133,
  	5,95,0,0,133,134,3,47,23,0,134,135,3,49,24,0,135,136,3,63,31,0,136,137,
  	3,41,20,0,137,138,3,89,44,0,138,10,1,0,0,0,139,140,3,43,21,0,140,141,
  	3,69,34,0,141,142,3,81,40,0,142,143,3,67,33,0,143,144,3,47,23,0,144,145,
  	3,49,24,0,145,146,3,47,23,0,146,147,5,95,0,0,147,148,3,79,39,0,148,149,
  	3,57,28,0,149,150,3,65,32,0,150,151,3,49,24,0,151,12,1,0,0,0,152,153,
  	3,47,23,0,153,154,3,89,44,0,154,155,3,67,33,0,155,156,3,41,20,0,156,157,
  	3,65,32,0,157,158,3,57,28,0,158,159,3,45,22,0,159,160,5,95,0,0,160,161,
  	3,79,39,0,161,162,3,57,28,0,162,163,3,65,32,0,163,164,3,49,24,0,164,14,
  	1,0,0,0,165,166,3,47,23,0,166,167,3,57,28,0,167,168,3,75,37,0,168,169,
  	3,49,24,0,169,170,3,45,22,0,170,171,3,79,39,0,171,16,1,0,0,0,172,173,
  	3,55,27,0,173,174,3,69,34,0,174,175,3,81,40,0,175,177,3,75,37,0,176,178,
  	3,77,38,0,177,176,1,0,0,0,177,178,1,0,0,0,178,18,1,0,0,0,179,180,3,65,
  	32,0,180,181,3,57,28,0,181,182,3,67,33,0,182,183,3,81,40,0,183,184,3,
  	79,39,0,184,186,3,49,24,0,185,187,3,77,38,0,186,185,1,0,0,0,186,187,1,
  	0,0,0,187,20,1,0,0,0,188,189,3,77,38,0,189,190,3,49,24,0,190,191,3,45,
  	22,0,191,192,3,69,34,0,192,193,3,67,33,0,193,195,3,47,23,0,194,196,3,
  	77,38,0,195,194,1,0,0,0,195,196,1,0,0,0,196,22,1,0,0,0,197,198,5,123,
  	0,0,198,24,1,0,0,0,199,200,5,125,0,0,200,26,1,0,0,0,201,202,5,44,0,0,
  	202,28,1,0,0,0,203,204,3,31,15,0,204,205,5,46,0,0,205,206,3,33,16,0,206,
  	228,1,0,0,0,207,209,3,31,15,0,208,207,1,0,0,0,208,209,1,0,0,0,209,210,
  	1,0,0,0,210,212,5,46,0,0,211,213,3,39,19,0,212,211,1,0,0,0,213,214,1,
  	0,0,0,214,212,1,0,0,0,214,215,1,0,0,0,215,228,1,0,0,0,216,218,3,31,15,
  	0,217,216,1,0,0,0,217,218,1,0,0,0,218,219,1,0,0,0,219,221,5,46,0,0,220,
  	222,3,39,19,0,221,220,1,0,0,0,222,223,1,0,0,0,223,221,1,0,0,0,223,224,
  	1,0,0,0,224,225,1,0,0,0,225,226,3,33,16,0,226,228,1,0,0,0,227,203,1,0,
  	0,0,227,208,1,0,0,0,227,217,1,0,0,0,228,30,1,0,0,0,229,231,3,39,19,0,
  	230,229,1,0,0,0,231,232,1,0,0,0,232,230,1,0,0,0,232,233,1,0,0,0,233,32,
  	1,0,0,0,234,236,3,49,24,0,235,237,5,45,0,0,236,235,1,0,0,0,236,237,1,
  	0,0,0,237,239,1,0,0,0,238,240,3,39,19,0,239,238,1,0,0,0,240,241,1,0,0,
  	0,241,239,1,0,0,0,241,242,1,0,0,0,242,34,1,0,0,0,243,249,5,96,0,0,244,
  	248,8,1,0,0,245,246,5,96,0,0,246,248,5,96,0,0,247,244,1,0,0,0,247,245,
  	1,0,0,0,248,251,1,0,0,0,249,247,1,0,0,0,249,250,1,0,0,0,250,252,1,0,0,
  	0,251,249,1,0,0,0,252,261,5,96,0,0,253,257,7,2,0,0,254,256,7,3,0,0,255,
  	254,1,0,0,0,256,259,1,0,0,0,257,255,1,0,0,0,257,258,1,0,0,0,258,261,1,
  	0,0,0,259,257,1,0,0,0,260,243,1,0,0,0,260,253,1,0,0,0,261,36,1,0,0,0,
  	262,263,9,0,0,0,263,38,1,0,0,0,264,265,7,4,0,0,265,40,1,0,0,0,266,267,
  	7,5,0,0,267,42,1,0,0,0,268,269,7,6,0,0,269,44,1,0,0,0,270,271,7,7,0,0,
  	271,46,1,0,0,0,272,273,7,8,0,0,273,48,1,0,0,0,274,275,7,9,0,0,275,50,
  	1,0,0,0,276,277,7,10,0,0,277,52,1,0,0,0,278,279,7,11,0,0,279,54,1,0,0,
  	0,280,281,7,12,0,0,281,56,1,0,0,0,282,283,7,13,0,0,283,58,1,0,0,0,284,
  	285,7,14,0,0,285,60,1,0,0,0,286,287,7,15,0,0,287,62,1,0,0,0,288,289,7,
  	16,0,0,289,64,1,0,0,0,290,291,7,17,0,0,291,66,1,0,0,0,292,293,7,18,0,
  	0,293,68,1,0,0,0,294,295,7,19,0,0,295,70,1,0,0,0,296,297,7,20,0,0,297,
  	72,1,0,0,0,298,299,7,21,0,0,299,74,1,0,0,0,300,301,7,22,0,0,301,76,1,
  	0,0,0,302,303,7,23,0,0,303,78,1,0,0,0,304,305,7,24,0,0,305,80,1,0,0,0,
  	306,307,7,25,0,0,307,82,1,0,0,0,308,309,7,26,0,0,309,84,1,0,0,0,310,311,
  	7,27,0,0,311,86,1,0,0,0,312,313,7,28,0,0,313,88,1,0,0,0,314,315,7,29,
  	0,0,315,90,1,0,0,0,316,317,7,30,0,0,317,92,1,0,0,0,17,0,96,177,186,195,
  	208,214,217,223,227,232,236,241,247,249,257,260,1,6,0,0
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
