from typing import List

from .pddl_literal import PDDLLiteral
from .pddl_param import PDDLParam
from .pddl_precondition import PDDLPrecondition
from .pddl_syntax_tree import PDDLPreconditionSyntaxTree

class PDDLAction:
    def __init__(self, name: str):
        self.name = name
        self.parameters : list[PDDLParam] = []
        self.precondition_syntax_tree: PDDLPreconditionSyntaxTree = PDDLPreconditionSyntaxTree() 
        self.effects : list[PDDLLiteral] = []

    def add_parameter(self, p: PDDLParam):
        self.parameters.append(p)
        return p

    def begin_precondition(self, operator: str, variables: List[tuple[str, str]] = None):
        self.precondition_syntax_tree.add_operator(operator, variables)

    def end_precondition(self):
        self.precondition_syntax_tree.end_operator()        

    def add_precondition(self, predicate_symbol: str, arguments: List[str], variables: List[tuple[str, str]] = None) -> None:
        self.precondition_syntax_tree.add_condition(predicate_symbol, arguments, variables)

    def add_effect(self, l: PDDLLiteral):
        self.effects.append(l)

    def add_parameters(self, p: list[PDDLParam]):
        self.parameters += p

    def add_effects(self, l:  List[PDDLLiteral]):
        self.effects += l

    def to_pddl(self) -> str:
        precondition = self.precondition_syntax_tree.to_pddl_precondition()

        s = f"\t(:action {self.name}\n"
        s += f"\t\t:parameters ({' '.join(param.to_pddl() for param in self.parameters)})\n"
        s += "\t\t:precondition "
        s += precondition.to_pddl() + "\n"
        # s += "\n\t\t)\n"
        # s += '\n\t\t\t'.join(precondition.to_pddl() for precondition in self.preconditions)
        s += "\t\t:effect (and\n\t\t\t"
        s += '\n\t\t\t'.join(effect.to_pddl() for effect in self.effects)
        s += "\n\t\t)\n\t)\n\n\n"
        return s