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

?start				: problem

problem				: "Problem" "{" objects worldstate initialstate goalstate"}"

objects				: "Objects" "{" object_type* "}"
object_type			: type object_list ";"
object_list			: object ("," object)* 

worldstate			: "WorldState"		"{" (predicates | numerics | functions)* "}"
initialstate		: "InitialState"	"{" (predicates | numerics | functions)* "}"
goalstate			: "Goal"			"{" (predicates | numerics | func_subgoal)* "}"

predicates			: predicate			"(" object_list ")" ";"
numerics			: numeric			"(" object_list* ")" "=" number ";"
functions 			: function			"(" object_list ")" "=" ("undefined" | object) ";"

func_subgoal		: function			"(" object_list ")" "==" ("undefined" | object) ";"


