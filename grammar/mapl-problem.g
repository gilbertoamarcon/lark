%import common.WS
%ignore WS
%ignore COMMENT 

number				: /[0-9]+(.[0-9]+)?/
id					: /[a-zA-Z][a-zA-Z0-9_]*/
COMMENT				: "//" /(.)+\n/

deadline			: number
type				: id
agent				: id
object				: id
capability_name		: id
predicate			: id
numeric				: id
function			: id
action				: id
var					: id

?start				: problem

problem				: "Problem" "{" agents objects agent_capabilities worldstate initialstate goalstate "}"

agents				: "Agents" "{" agent_type* "}"
agent_type			: type agent ("," agent)* ";"

objects				: "Objects" "{" object_type* "}"
object_type			: type object ("," object)* ";"

agent_capabilities	: "AgentCapabilities" "{" agentcap* "}"
agentcap			: "(" agent_list ")" "{" capability_dict "}" ";"
agent_list			: agent ("," agent)* 

capability_dict		: capability*
capability			: capability_name ":" number ","


worldstate			: "WorldState"		"{" (predicates | numerics | functions)* "}"
initialstate		: "InitialState"	"{" (predicates | numerics | functions)* "}"
goalstate			: "Goal"			"{" (predicates | numerics | func_subgoal)* "}"

predicates			: predicate		"("  object ("," object)* ")" ";"
numerics			: numeric		"(" (object ("," object)*)* ")" "=" number ";"
functions 			: function		"("  object ("," object)* ")" "=" ("undefined" | object) ";"

func_subgoal		: function		"("  object ("," object)* ")" "==" ("undefined" | object) ";"


