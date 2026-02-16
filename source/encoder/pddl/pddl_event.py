## Created by Omik Acharya
from typing import List

from .pddl_literal import PDDLLiteral
from .pddl_param import PDDLParam
from .pddl_precondition import PDDLPrecondition

class PDDLEvent:
    def __init__(self, name: str):
        self.name = name
        self.parameters : list[PDDLParam] = []
        self.precondition : PDDLPrecondition  = None
        self.effects : list[PDDLLiteral] = []

    def add_parameter(self, p: PDDLParam):
        self.parameters.append(p)
        return p

    def add_precondition(self, l: PDDLPrecondition):
        self.precondition = l

    def add_effect(self, l: PDDLLiteral):
        self.effects.append(l)

    def add_effects(self, l:  List[PDDLLiteral]):
        self.effects += l    


    def add_parameters(self, p: list[PDDLParam]):
        self.parameters += p

    # def add_precondition(self, l:  List[PDDLLiteral]):
        # self.preconditions += l

    def __str__(self):
        return f"PDDLEvent({self.name}, {self.parameters}, {self.precondition}, {self.effects})"

    def to_pddl(self) -> str:
        s = f"\t(:event {self.name}\n"
        s += f"\t\t:parameters ({' '.join(param.to_pddl() for param in self.parameters)})\n"
        # s += "\t\t:precondition (and\n\t\t\t"
        # s += '\n\t\t\t'.join(precondition.to_pddl() for precondition in self.preconditions)
        s += "\t\t:precondition "
        s += self.precondition.to_pddl() + "\n"
        s += "\n\t\t)\n"
        s += "\t\t:effect (and\n\t\t\t"
        s += '\n\t\t\t'.join(effect.to_pddl() for effect in self.effects)
        s += "\n\t\t)\n\t)\n\n\n"
        return s