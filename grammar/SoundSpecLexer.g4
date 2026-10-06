lexer grammar SoundSpecLexer;

// --- KEYWORDS ---
TRACK     : 'track';
EFFECT    : 'effect';
MIX       : 'mix';
BPM       : 'bpm';
WAVE      : 'wave';
DELAY     : 'delay';
DECAY     : 'decay';
NOTES     : 'notes';

// --- VALORES TIPADOS Y ENUMS ---
WAVE_TYPE    : 'SAWTOOTH' | 'SINE' | 'SQUARE' | 'TRIANGLE';
NOTE         : [A-G][#b]?[0-8];
FRACTION     : [0-9]+ '/' [0-9]+;
TIME_MS      : [0-9]+ 'ms';

// --- OPERADORES Y SÍMBOLOS ---
PIPE_OP      : '->';
ASSIGN       : '=';
COLON        : ':';
SEMI         : ';';
COMMA        : ',';
LBRACE       : '{';
RBRACE       : '}';
LBRACK       : '[';
RBRACK       : ']';

// --- LITERALES NUMÉRICOS E IDENTIFICADORES ---
FLOAT : [0-9]+ '.' [0-9]+;
INT   : [0-9]+;
ID    : [a-zA-Z_][a-zA-Z0-9_]*;

// --- REGLAS AUXILIARES ---
WS           : [ \t\r\n]+ -> skip;
COMMENT      : '//' ~[\r\n]* -> skip;
