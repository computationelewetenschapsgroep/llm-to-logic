from ..pddl import PDDLPredicateDef
from ..pddl import Type
from ..pddl import PDDLPredicate
from .feature_action import FeatureAction
from .feature_event import FeatureEvent

from ..pddl import PDDLParam, PDDLNumericFluent, PDDLNumericValue, PDDLLiteral
from ..pddl import PDDLEvent, PDDLProcess
from ..pddl import PDDLPrecondition
from .variant import Variant
from typing import List



class TransporterState(PDDLProcess):
    def __init__(self, name):
        super().__init__(name)

    def register_process(self, parameters: List[PDDLParam], precondition: PDDLPrecondition, effects: List[PDDLLiteral]):
        self.add_parameters(parameters)
        self.add_precondition(precondition)
        self.add_effects(effects)

class AssemblyLine(PDDLProcess):
    ## this models the discharge
    def __init__(self, name):
        super().__init__(name)
    


# Pickup Needs to make sure that order is in accordance!
class PickupAction(FeatureAction):
    
    def __init__(
        self,
        variant: Variant,
        types: dict[str:Type],
        constants: dict[str:PDDLParam],
        predicates: dict[str:PDDLPredicateDef],
        functions: dict[str:PDDLPredicateDef],
    ) -> None:
        super().__init__(variant, types, constants, predicates, functions)

        ## need to model transported and equipment compatibility for pickup
        ## need to model the maximum capacity of the transporter

        self.location_t = self.register_type("location")
        self.pickup_location_t = self.register_type("pickup_location", self.location_t)
        self.transporter_location_t = self.register_type("transporter_location", self.location_t) 
        self.resource_options_t = self.register_type("resource_options")
        self.transporter_t = self.register_type("transporter", self.transporter_location_t)
        self.equipment_part_t = self.register_type("equipment_part", self.pickup_location_t)
        self.equipment_availability_t = self.register_type("equipment_availability")
        self.transporter_availability_t = self.register_type("transporter_availability")
        self.order_t = self.register_type("order")
        #self.trip_type_t = self.register_type("trip_type")

        self.transporter = PDDLParam("?tp", self.transporter_t)
        self.equipment = PDDLParam("?eqp", self.equipment_part_t)
        self.equipment_availabile = PDDLParam("?eavl", self.equipment_availability_t)
        self.transporter_available = PDDLParam("?tavl", self.transporter_availability_t)

        self.pickup_location = PDDLParam("?ploc", self.pickup_location_t)
        self.transporter_location = PDDLParam("?tloc", self.transporter_location_t)

        self.prev_equipment = PDDLParam("?prev_eqp", self.equipment_part_t)
        self.complete_order = PDDLParam("?complete_order", self.order_t)

        # part 1, part 2, whole
        self.assembly_order = self.register_predicate("assembly-order", self.prev_equipment, self.equipment, self.complete_order)
        self.incorporated = self.register_predicate("incorporated", self.prev_equipment, self.complete_order)

        self.on_transporter = self.register_predicate("on", self.equipment, self.transporter)
        self.at_location = self.register_predicate("eq", self.pickup_location, self.transporter_location)
        self.is_compatible = self.register_predicate("compatible", self.equipment, self.transporter)
        self.available_for_pickup  = self.register_predicate("is", self.transporter, self.transporter_available)

    def add_basic(self, a):
        a.add_parameter(self.transporter)
        a.add_parameter(self.equipment)
        a.add_parameter(self.pickup_location)
        a.add_parameter(self.transporter_location)

        a.add_parameter(self.prev_equipment)
        a.add_parameter(self.complete_order)
        
        # imply_precondition = PDDLPrecondition(
        #     operator="imply", 
        #     arguments=[
        #         self.assembly_order.inst(self.prev_equipment, self.equipment, self.complete_order),
        #         self.incorporated.inst(self.prev_equipment, self.complete_order)
        #     ]
        # )
        # a.add_precondition(
        #     PDDLPrecondition("forall", [imply_precondition], variables=[(self.prev_equipment, self.equipment_part_t)])
        # )
        # updated implementation!
        a.begin_precondition("forall", variables=[(self.prev_equipment, self.equipment_part_t)])        
        a.begin_precondition("imply")
        a.add_precondition(
            predicate_symbol="assembly_order",
            arguments=[self.prev_equipment, self.equipment, self.complete_order]
        )
        a.add_precondition(
            predicate_symbol="incorporated",
            arguments=[self.prev_equipment, self.complete_order]
        )        


"""
(forall (?prev - assembly)
				     (imply
				        (remove-order ?prev ?part ?whole)
					(incorporated ?prev ?whole))))
"""



    #         (:event manufactured
    #     :parameters (?eqp - equipment_part)
    #     :precondition (and
    #         (not (equipment_availability ?avl))
    
    #     )
    #     :effect (
    #         (assign (equipment_availability ?avl) (True))
    #     )
    # )


    #   (:action BUILD-WALL
    #     :parameters (?s - site ?b - bricks)
    #     :precondition (and
    #         
    #         (equipment_availability ?avl)
    #        
    #     )
    #     :effect (and
    #         (walls-built ?s)
    #         (material-used ?b)
    #     )
    #     ; :expansion ;deprecated
    # )


class ManufacturingEvent(FeatureEvent):
    def __init__(self, name):
        super().__init__(name)

    def register_event(self, parameters: List[PDDLParam], precondition: PDDLPrecondition, effects: List[PDDLLiteral]):
        self.add_parameters(parameters)
        self.add_precondition(precondition)
        self.add_effects(effects)

class GetFromManufacturer(PickupAction):

    def __init__(
        self,
        variant: Variant,
        types: dict[str:Type],
        constants: dict[str:PDDLParam],
        predicates: dict[str:PDDLPredicateDef],
        functions: dict[str:PDDLPredicateDef],
    ) -> None:
        super().__init__(variant, types, constants, predicates, functions)
        self.name = "get-from-manufacturer"
        self.manufacturing_event = ManufacturingEvent("manufacturing-event")
        self.in_manufacturing = self.register_predicate("in",self.equipment, self.equipment_availabile)
        self.manufacturing_event.register_event([self.equipment], 
                                                PDDLPrecondition("", self.in_manufacturing.inst(self.equipment, self.equipment_availabile), []),
                                                [self.in_manufacturing.negated_inst(self.equipment, self.equipment_availabile)])
        self.transporter_state = TransporterState("transporter-process-state")
        self.transporter_state.register_process([self.transporter], 
                                                [self.available_for_pickup.inst(self.transporter, self.transporter_available)],
                                                [self.available_for_pickup.negated_inst(self.transporter, self.transporter_available)])


    def add_basic(self, a):
        super().add_basic(a)

        # a.add_precondition(self.at_location.inst(self.pickup_location, self.transporter_location))
        
        # a.add_precondition(self.manufacturing_event.effects)
        # a.add_precondition(self.transporter_state.effects)

        # Fix this later
        combined_precondition = PDDLPrecondition(
        "and", 
        [
            self.at_location.inst(self.pickup_location, self.transporter_location),
            self.manufacturing_event.effects,
            self.transporter_state.effects
        ]
        )
        a.add_precondition(combined_precondition)
        
        a.add_effect(self.on_transporter.inst(self.equipment, self.transporter))



class GetFromWarehouse(PickupAction):
    
    def __init__(
        self,
        variant: Variant,
        types: dict[str:Type],
        constants: dict[str:PDDLParam],
        predicates: dict[str:PDDLPredicateDef],
        functions: dict[str:PDDLPredicateDef],
    ) -> None:
        super().__init__(variant, types, constants, predicates, functions)
        self.name = "get-from-warehouse"

        self.batch_t = self.register_type("batch")
        self.batch_size_t = self.register_type("batch_size", self.batch_t)
        
        self.batch = PDDLParam("?b", self.batch_t)
        self.batch_size_limit = PDDLParam("?bsl", self.batch_size_t)
        
        self.batch_within_limit = self.register_predicate("within_size_limit", self.batch, self.batch_size_limit)
        self.valid_batch_composition = self.register_predicate("valid_composition", self.batch)
        self.batch_creation_possible = self.register_predicate("batch_possible", self.batch)

        self.current_batch_size = self.register_function("current_batch_size", self.batch)
        self.rebatch_equipment = RebatchEquipment("rebatch-equipment")
        
        self.rebatch_equipment.register_event(
            parameters=[self.batch, self.batch_size_limit], 
            precondition=[self.batch_within_limit.inst(self.batch, self.batch_size_limit),
                           self.valid_batch_composition.inst(self.batch)], 
            effects=[self.batch_creation_possible.inst(self.batch)]
        )
        
        self.transporter_state = TransporterState("transporter-process-state")
        self.transporter_state.register_process([self.transporter], 
                                                [self.available_for_pickup.inst(self.transporter, self.transporter_available)],
                                                [self.available_for_pickup.negated_inst(self.transporter, self.transporter_available)])

    def add_basic(self, a):
        super().add_basic(a)

        a.add_precondition(self.at_location.inst(self.pickup_location, self.transporter_location))
        a.add_precondition(self.available_for_pickup.inst(self.transporter, self.transporter_available))
        a.add_precondition(self.rebatch_equipment.effects)  # condition to see if rebatching possible   

        a.add_effect(self.on_transporter.inst(self.equipment, self.transporter))
    ### shold include the  logic for rebatching

class RebatchEquipment(PDDLEvent):
    def __init__(self, name):
        super().__init__(name)

    def register_event(self, parameters: List[PDDLParam], precondition: List[PDDLLiteral], effects: List[PDDLLiteral]):
        self.add_parameters(parameters)
        self.add_precondition(precondition)
        self.add_effects(effects) 

class DeliveryAction(FeatureAction):
    pass


class SiteDeliveryAction(FeatureAction):
    pass


class WarehouseDeliveryAction(FeatureAction):
    pass




####

### Pickup / Delivery   |  Warehouse              | Delivery Site   
### Manufacturer        | Yes (Marshalling Trip)  | Yes (Direct Shipment)
### Warehouse           | No                      | Yes (Feedering)
