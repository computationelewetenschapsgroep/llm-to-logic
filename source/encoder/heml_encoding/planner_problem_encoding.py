# from beluga_lib.problem_def import BelugaProblem
#from beluga_lib.beluga_problem import BelugaProblem
#from beluga_lib.rack import Rack
#from beluga_lib.flight_schedule import Flight
from ..pddl import PDDLDomain
from ..pddl import PDDLComment
from ..pddl import PDDLNumericValue
from ..pddl import PDDLProblem, PDDLParam, PDDLNumericFluent
from .variant import Variant
from ..pddl.utils import utils  as utils
#from beluga_lib.problem_state import BelugaProblemState
import copy

def encode(
    name: str,
    planning_problem: "PlanningProblem" = None,
    domain: PDDLDomain,
    variant: Variant,
    state : "PlanningProblemState" = None
) -> PDDLProblem:
    
    problem = PDDLProblem(name, "planning")

    

