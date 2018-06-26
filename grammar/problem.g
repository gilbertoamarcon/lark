?start				: problem

?problem			: "Problem" "{" objects worldstate initialstate goal "}"

objects				: "Objects" "{" (type object ("," object)* ";")* "}"
worldstate			: "WorldState" "{"  (predicates | numerics | functions)* "}"
initialstate		: "InitialState" "{"  (predicates | numerics | functions)* "}"
goal				: "Goal" "{"  (predicates | functions)* "}"

predicates			: predicate "(" object ("," object)* ")" ";"
numerics			: numeric "(" (object ("," object)*)* ")" "=" number ";"
functions 			: function "(" object ("," object)* ")" "=" ("undefined" | object) ";"


id					: /[a-zA-Z][a-zA-Z0-9_]*/
type				: id
object				: id
predicate			: id
numeric				: id
function			: id


deadline			: number
number				: /[0-9]+(.[0-9]+)?/
COMMENT				: "//" /(.)+\n/


%ignore COMMENT 
%import common.WS
%ignore WS

