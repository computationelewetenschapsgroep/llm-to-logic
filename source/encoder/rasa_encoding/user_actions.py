from ..pddl.pddl_predicate_def import PDDLPredicateDef
from ..pddl.type import Type
from .feature_action import FeatureAction
from ..pddl import PDDLParam, PDDLNumericFluent, PDDLNumericValue
from .variant import Variant


class CheckBalance(FeatureAction):
    def __init__(
        self,
        variant: Variant,
        types: dict[str:Type],
        constants: dict[str:PDDLParam],
        predicates: dict[str:PDDLPredicateDef],
        functions: dict[str:PDDLPredicateDef],
    ) -> None:
        super().__init__(variant, types, constants, predicates, functions)
       
        self.user_t = self.register_type("user")
        self.account_t = self.register_type("account", self.user_t)
        self.account = PDDLParam("?a", self.account_t)
        self.user = PDDLParam("?u", self.user_t)
        self.of = self.register_predicate("of", self.account, self.user)


