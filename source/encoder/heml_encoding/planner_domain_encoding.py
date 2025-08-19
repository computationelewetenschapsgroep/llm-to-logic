from .feature_action import FeatureAction
from .feature_event import FeatureEvent
from .feature_process import FeatureProcess
#from .planner_complete_action import BelugaCompleteAction
#from .factory_actions import DeliverToHangarAction, GetFromHangarAction
#from .planner_actions import LoadBelugaAction, UnloadBelugaAction
#from .probabilistic_actions import ProceedToNextBeluga
from ..pddl import PDDLDomain
from .factory_actions import GetFromWarehouse
from .variant import Variant

class DomainEncoding:

    def __init__(self, variant: Variant) -> None:

        self.domain = PDDLDomain()

        if not variant.classic:
            self.domain.requirements.append(":fluents")

        if variant.probabilistic:
            self.domain.requirements.append(":probabilistic-effects")
            self.domain.requirements.append(":conditional-effects")
            self.domain.requirements.append(":negative-preconditions")

        self.constants = {}
        self.types = {}
        self.predicates = {}
        self.functions = {}

        feature_event_collection = [
            # ManufacturingEvent
        ]
        for feature_event_con in feature_event_collection:
            fe:FeatureEvent = feature_event_con(
                variant, self.types, self.constants, self.predicates, self.functions
            )
            self.domain.events.append(fe)
        
        feature_process_collection = [
            # ManufacturingProcess
        ]
        for feature_process_con in feature_process_collection:
            fp:FeatureProcess = feature_process_con(
                variant, self.types, self.constants, self.predicates, self.functions
            )
            self.domain.processes.append(fp)

        feature_actions_collection = [
            # GetFromManufacturer, 
            GetFromWarehouse
        ]

        # if not variant.probabilistic:
        #     feature_actions_collection.append(BelugaCompleteAction)

        for feature_action_con in feature_actions_collection:
            fa: FeatureAction = feature_action_con(
                variant, self.types, self.constants, self.predicates, self.functions
            )
            self.domain.actions.append(fa.create_PDDL_action())

        # if variant.probabilistic:
        #     fa = ProceedToNextBeluga(
        #         variant,
        #         beluga_problem,
        #         self.types,
        #         self.constants,
        #         self.predicates,
        #         self.functions,
        #     )
        #     self.domain.actions.extend(fa.create_PDDL_action())

        self.domain.types = self.types
        self.domain.constants = self.constants
        self.domain.predicates = self.predicates
        self.domain.functions = self.functions