%import common.WS
%ignore WS
%ignore COMMENT 

// Token Regex
number			: /[0-9]+(.[0-9]+)?/
id				: /[a-zA-Z][a-zA-Z0-9_]*/
when			: /@(start|end|overall)/
COMMENT			: "//" /(.)+\n/

// Token ids and numbers
deadline		: number
type			: id
object			: id
predicate		: id
numeric			: id
function		: id
action			: id
var				: id

// Starting node
?start			: domain

// The domain
domain			: "domain" "{" types worlddef statedef actiondefs "}"

// Main sections
types			: "types" type_list_curl	-> list_strip
worlddef		: "world" "{" ( predicatedef | numericdef | functiondef )* "}"
statedef		: "state" "{" ( predicatedef | numericdef | functiondef )* "}"
actiondefs		: actiondef*

// Relation types
predicatedef	: "predicate" predicate		type_list_squa ";"
numericdef		: "numeric" numeric			type_list_squa ";"
functiondef		: "function" type function	type_list_squa ";"
actiondef		: "action" action type_var_list "{" actiondur? cost? conditionsdef effectsdef "}"

// Lists
var_list		: "(" ( var			( "," var		)* )? ")"
type_list_squa	: "(" ( type		( "," type		)* )? ")"
type_list_curl	: "{" ( type		( "," type		)* )? "}"
type_var_list	: "(" ( type var	( "," type var	)* )? ")"

// Action body
actiondur		: "duration" ":"	distribution ";"
cost			: "cost" ":"		distribution ";"
conditionsdef	: "conditions" ":"	conditions*
effectsdef		: "effects" ":"		effect*


// Probability distributions
distribution	: "constant"	exp			-> distribution_constant
				| "uniform"		exp exp		-> distribution_uniform
				| "normal"		exp exp		-> distribution_normal
				| "exponential"	exp			-> distribution_exponential

// Numerical expressions
exp				: numeric var_list			-> exp_numeric
				| exp "*" exp				-> mul
				| exp "/" exp				-> div
				| exp "+" exp				-> add
				| exp "-" exp				-> sub
				| "(" exp ")"				-> list_strip
				| number					-> list_strip

// Temporal conditions
conditions		: when ":" ( pred_cond | func_cond | num_cond | varsdiff ) ";"
effect			: when ":" ( func_assign | pred_eff | ( numeric_assign | increase | decrease ) )";"


// Conditions

pred_cond		: ( pred_cond_pos | pred_cond_neg )		-> list_strip
pred_cond_pos	: predicate var_list
pred_cond_neg	: "!" predicate var_list


func_cond		: ( func_cond_pos | func_cond_neg )		-> list_strip
func_cond_pos	: function var_list "=" ( var | "undefined" )
func_cond_neg	: "!" function var_list "=" ( var | "undefined" )

num_cond		: numeric var_list ( "<=" | ">=" | "==" | "<" | ">" ) number

varsdiff		: var "!=" var




// Effects

func_assign		: function var_list "=" ( var | "undefined" )

pred_eff		: ( pred_eff_pos | pred_eff_neg )		-> list_strip
pred_eff_pos	: predicate var_list
pred_eff_neg	: "!" predicate var_list

numeric_assign	: numeric var_list "=" exp
increase		: ( "increase" ) numeric var_list exp
decrease		: ( "decrease" ) numeric var_list exp




