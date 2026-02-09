parser grammar OptionDeclarationParser;

options {
  tokenVocab = OptionDeclarationLexer;
}

parse
 : (option_declaration | error )* EOF
 ;

error
 : UNEXPECTED_CHAR
   {
     throw new RuntimeException("UNEXPECTED_CHAR=" + $UNEXPECTED_CHAR.text);
   }
 ;


option_declaration
 : K_CREATE K_QUARANTINE LEFT_CURLY_BRACKET quarantine_policy* RIGHT_CURLY_BRACKET
 ;

quarantine_policy
 : K_FIXED_TIME time_span LEFT_CURLY_BRACKET stream_names RIGHT_CURLY_BRACKET # fixed_time_policy
 | K_BOUNDED_TIME time_span LEFT_CURLY_BRACKET stream_names RIGHT_CURLY_BRACKET # bounded_time_policy
 | K_DIRECT LEFT_CURLY_BRACKET stream_names RIGHT_CURLY_BRACKET # direct_policy
 | K_NEW_FIXED_TIME time_span LEFT_CURLY_BRACKET stream_names RIGHT_CURLY_BRACKET # new_fixed_time_policy
 | K_AVG_DYNAMIC_TIME time_span LEFT_CURLY_BRACKET stream_names RIGHT_CURLY_BRACKET # avg_dynamic_time_policy
 | K_JAD_DYNAMIC_TIME time_span LEFT_CURLY_BRACKET stream_names RIGHT_CURLY_BRACKET # jad_dynamic_time_policy
 | K_MAX_DYNAMIC_TIME time_span LEFT_CURLY_BRACKET stream_names RIGHT_CURLY_BRACKET # max_dynamic_time_policy
 | K_MAX_EMA_DYNAMIC_TIME time_span LEFT_CURLY_BRACKET stream_names RIGHT_CURLY_BRACKET # max_ema_dynamic_time_policy
 | K_P99_DYNAMIC_TIME time_span LEFT_CURLY_BRACKET stream_names RIGHT_CURLY_BRACKET # p99_dynamic_time_policy
 | K_PER_EVENT_DYNAMIC_TIME time_span LEFT_CURLY_BRACKET stream_names RIGHT_CURLY_BRACKET # per_event_dynamic_time_policy
 ;

 stream_names
 : stream_name ( COMMA stream_name )*
 ;

time_span
 : hour_span? minute_span? second_span?
 ;

hour_span
 : integer K_HOURS
 ;

minute_span
 : integer K_MINUTES
 ;

second_span
 : integer K_SECONDS
 ;

stream_name
 : any_name
 ;

any_name
 : IDENTIFIER
 ;

number
 : integer
 | double
 ;

integer
 : INTEGER_LITERAL
 ;

double
 : DOUBLE_LITERAL
 ;
