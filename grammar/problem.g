?start				: problem

problem				: "Problem" "{" objects worldstate initialstate goal "}"

objects				: "Objects" "{" object_type* "}"
object_type			: type object ("," object)* ";"

worldstate			: "WorldState" "{"  (predicates | numerics | functions)* "}"
initialstate		: "InitialState" "{"  (predicates | numerics | functions)* "}"
goal				: "Goal" "{"  (predicates | functions | functions)* "}"

predicates			: predicate "(" object ("," object)* ")" ";"
numerics			: numeric "(" (object ("," object)*)* ")" "=" number ";"
functions 			: function "(" object ("," object)* ")" "=" ("undefined" | object) ";"


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

