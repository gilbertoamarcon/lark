%import common.WS
%ignore WS
%ignore COMMENT 

number				: /[0-9]+(.[0-9]+)?/
id					: /[a-zA-Z][a-zA-Z0-9_]*/
COMMENT				: "//" /(.)+\n/

deadline			: number
type				: id
object				: id
predicate			: id
numeric				: id
function			: id
action				: id
var					: id

?start				: domain

domain				: "domain" "{" types worlddef statedef actiondefs "}"

types				: "types" "{" type_list "}"
worlddef			: "world" "{" ( predicatedef | numericdef | functiondef )* "}"
statedef			: "state" "{" ( predicatedef | numericdef | functiondef )* "}"

predicatedef		: "predicate" predicate "(" type_list ")" ";"
numericdef			: "numeric" numeric "(" type_list ")" ";"
functiondef			: "function" type function "(" type_list ")" ";"

type_list			: ( type ( "," type )* )?
var_list			: "(" ( var ( "," var )* )? ")"
type_var_list		: type var ( "," type var )*

actiondefs			: actiondef*
actiondef			: "action" action "(" type_var_list ")" "{" actiondur? cost? conditionsdef effectsdef "}"

actiondur			: "duration" ":" distribution ";"
cost				: "cost" ":" distribution ";"

distribution		: "constant"	exp			-> distribution_constant
					| "uniform"		exp exp		-> distribution_uniform
					| "normal"		exp exp		-> distribution_normal
					| "exponential"	exp			-> distribution_exponential

exp					: numeric var_list			-> exp_numeric
					| exp "*" exp				-> mul
					| exp "/" exp				-> div
					| exp "+" exp				-> add
					| exp "-" exp				-> sub
					| "(" exp ")"
					| number

conditionsdef		: "conditions" ":" conditions*

conditions			: when ":" (pred_cond | func_cond | num_cond | varsdiff) ";"

pred_cond			: "!"? predicate var_list

func_cond			: "!"? function var_list "=" (var | "undefined")

num_cond			: numeric var_list ("<=" | ">=" | "==" | "<" | ">") number

varsdiff			: var "!=" var

effectsdef			: "effects" ":" effect*

effect				: when ":" (func_assign | pred_eff | numeric_eff )";"

func_assign			: function var_list "=" (var | "undefined")

pred_eff			: "!"? predicate var_list

numeric_eff			: numeric var_list "=" exp
					| ("increase" | "decrease") numeric var_list exp


when				: /@(start|end|overall)/


