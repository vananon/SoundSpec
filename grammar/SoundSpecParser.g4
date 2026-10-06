parser grammar SoundSpecParser;
options { tokenVocab=SoundSpecLexer; }

program    : statement+ EOF ;
statement  : trackDecl | effectDecl | mixRule ;

trackDecl  : TRACK ID LBRACE trackProp+ RBRACE ;
trackProp  : BPM COLON INT SEMI
           | WAVE COLON WAVE_TYPE SEMI
           | NOTES COLON noteList SEMI ;
noteList   : LBRACK noteItem (COMMA noteItem)* RBRACK ;
noteItem   : NOTE COLON? FRACTION ;

effectDecl : EFFECT ID LBRACE effectProp+ RBRACE ;
effectProp : DELAY COLON TIME_MS SEMI
           | DECAY COLON FLOAT SEMI ;

mixRule    : MIX ID ASSIGN ID (PIPE_OP ID)* SEMI ;
