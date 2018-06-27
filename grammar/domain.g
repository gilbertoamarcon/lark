?start				: domain

domain				: "domain" "{" types worlddef statedef "}"
types				: "types" "{" type_list "}"
worlddef			: "world" "{" ( predicatedef | numericdef | functiondef )* "}"
statedef			: "state" "{" ( predicatedef | numericdef | functiondef )* "}"

predicatedef		: "predicate" predicate "(" type_list ")" ";"
numericdef			: "numeric" numeric "(" type_list ")" ";"
functiondef			: "function" type function "(" type_list ")" ";"

type_list			: ( type ( "," type )* )?




type				: id
object				: id
predicate			: id
numeric				: id
function			: id
deadline			: number


id					: /[a-zA-Z][a-zA-Z0-9_]*/
number				: /[0-9]+(.[0-9]+)?/
COMMENT				: "//" /(.)+\n/


%import common.WS
%ignore WS
%ignore COMMENT 

