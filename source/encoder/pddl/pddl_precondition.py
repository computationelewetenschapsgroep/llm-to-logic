## Created by Omik Acharya
from .pddl_literal import PDDLLiteral

class PDDLPrecondition(PDDLLiteral):
    def __init__(self, operator: str, arguments: list = None, variables: list[tuple[str, str]] = None):
        self.operator = operator.lower()
        self.arguments = arguments or []
        self.variables = variables or []

    def to_pddl(self) -> str:
        if self.operator in {"forall", "exists"}:
            var_str = " ".join(f"{v} - {t}" for v, t in self.variables)
            return f"({self.operator} ({var_str}) {self.arguments[0].to_pddl()})"
        if self.operator == "not":
            return f"(not {self.arguments[0].to_pddl()})"
        if self.operator in {"and", "or", "imply"}:
            return f"({self.operator} {' '.join(arg.to_pddl() for arg in self.arguments)})"
        return f"({self.operator} {' '.join(arg.to_pddl() for arg in self.arguments)})"

    def __repr__(self):
        return f"PDDLPrecondition({self.operator}, {self.arguments}, {self.variables})"