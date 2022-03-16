grammar logo3d;

program: procedure* EOF;

procedure:  PROC  ID  PAROPEN  parameters? PARCLOSE IS
            block
            END
            ;

parameters: ID (COMMA parameters)?
            ;

block: statement*
       ;

statement: ID
        | varAssig
        | io
        | conditional
        | call
        | whileLoop
        | forLoop
        ;

varAssig: ID ASSIGN expression
          ;

io: RD ID
    | WR expression
    ;

term: ID
      | MINUS? NUM
      ;

call:  ID PAROPEN arguments? PARCLOSE
       ;

arguments: expression (COMMA arguments)?
           ;

conditional:  IF relational THEN
              block
              (ELSE block)?
              END
              ;

whileLoop:  WHILE relational DO
            block
            END
            ;

forLoop:  FOR ID FROM term TO term DO
          block
          END
          ;

expression:  expression MULT expression
            | expression DIV expression
            | expression PLUS expression
            | expression MINUS expression
            | PAROPEN expression PARCLOSE
            | term
            ;

relational:  expression LT expression
            | expression GT expression
            | expression LEQ expression
            | expression GEQ expression
            | expression EQ expression
            | expression DIF expression
            | expression
            ;

PLUS:	'+';
MINUS:	'-';
MULT:	'*';
DIV:	'/';

GT:	'>';
LT:	'<';
GEQ:	'>=';
LEQ:	'<=';
EQ:	'==';
DIF:	'!=';

ASSIGN:	':=';

RD:	'>>';
WR: '<<';

PAROPEN:	'(';
PARCLOSE:	')';
COMMA:	',';

IF:	'IF';
THEN:	'THEN';
ELSE:	'ELSE';

WHILE:	'WHILE';
DO:	'DO';
FOR:	'FOR';
FROM:	'FROM';
TO:	'TO';

PROC:	'PROC';
IS: 'IS';

END:	'END';

NUM :  [0-9]+ ('.' [0-9]+)?;

ID: [a-zA-Z_][a-zA-Z0-9_]*;

COMMENT:  '//' ~[\r\n]* -> skip;

WS:	[ \t\r\n]+ -> skip;
