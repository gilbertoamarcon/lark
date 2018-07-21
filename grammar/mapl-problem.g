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
predicate_name		: id
task_name			: id
numeric				: id
function			: id
action				: id
var					: id

?start				: problem

problem				: "Problem" "{" agents objects agent_capabilities worldstate initialstate task_dict task_capabilities"}"

agents				: "Agents" "{" agent_type* "}"
agent_type			: type agent_list ";"
agent_list			: agent ("," agent)* 

objects				: "Objects" "{" object_type* "}"
object_type			: type object_list ";"
object_list			: object ("," object)* 

task_list			: task_name ("," task_name)* 

agent_capabilities	: "AgentCapabilities" "{" agentcap* "}"
agentcap			: "(" agent_list ")" "{" capability_dict "}" ";"

task_capabilities	: "TaskCapabilities" "{" taskcap* "}"
taskcap				: "(" task_list ")" "{" capability_dict "}" ";"

capability_dict		: capability*
capability			: capability_name ":" number ","


worldstate			: "WorldState"		"{" (predicates | numerics | functions)* "}"
initialstate		: "InitialState"	"{" (predicates | numerics | functions)* "}"
task_dict			: "Goal"			"{" task+ "}"
task				: task_name			"{" (predicates | numerics | func_subgoal)* "}" ";"

predicates			: predicate_name	"(" object_list ")" ";"
numerics			: numeric			"(" object_list* ")" "=" number ";"
functions 			: function			"(" object_list ")" "=" ("undefined" | object) ";"

func_subgoal		: function			"(" object_list ")" "==" ("undefined" | object) ";"


