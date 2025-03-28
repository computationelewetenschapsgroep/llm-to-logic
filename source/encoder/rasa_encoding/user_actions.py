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
        self.name = "check-balance"
        self.user_t = self.register_type("user")
        self.account_t = self.register_type("account", self.user_t)
        self.balance_t = self.register_type("balance", self.account_t)
        self.account = PDDLParam("?a", self.account_t)
        self.user = PDDLParam("?u", self.user_t)
        self.balance = PDDLParam("?b", self.balance_t)
        self.of = self.register_predicate("of", self.account, self.user)
        self.foor = self.register_predicate("for", self.balance, self.account)

    def add_basic(self, a):
            a.add_parameter(self.account)
            a.add_parameter(self.user)
            a.add_precondition(self.of.inst(self.account,self.user))
            a.add_effect(self.foor.inst(self.balance,self.account))

      


