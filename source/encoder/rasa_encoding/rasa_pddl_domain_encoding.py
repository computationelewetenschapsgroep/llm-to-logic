from .feature_action import FeatureAction
from .user_actions import CheckBalance
from ..pddl.pddl_domain import PDDLDomain
from .variant import Variant

class DomainEncoding:
    def __init__(self, variant: Variant) -> None:
        self.domain = PDDLDomain()
        self.constants = {}
        self.types = {}
        self.predicates = {}
        self.functions = {}
        feature_actions_collection = [
            CheckBalance
        ]

        # self.constants = {}
        # self.types = {}
        # self.predicates = {}
        # self.functions = {}

        for feature_action_con in feature_actions_collection:
            fa: FeatureAction = feature_action_con(
                variant, self.types, self.constants, self.predicates, self.functions
            )
            self.domain.actions.append(fa.create_PDDL_action())

       