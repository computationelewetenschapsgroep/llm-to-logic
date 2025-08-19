## Created by Omik Acharya
from .pddl_literal import PDDLLiteral
from .pddl_precondition import PDDLPrecondition

class PreconditionNode:
    def __init__(self, operator: str = None, arguments: list = None, variables: list[tuple[str, str]] = None):
        self.operator = operator
        self.arguments = arguments or []
        self.variables = variables or []
        self.children: list[PreconditionNode] = []

    def __repr__(self):
        if self.children:
            return f"Node(op={self.operator}, vars={self.variables}, children={self.children})"
        return f"Leaf(pred={self.operator}, args={self.arguments}, vars={self.variables})"

class PDDLPreconditionSyntaxTree:
    def __init__(self):
        self.root: PreconditionNode | None = None
        self.current: PreconditionNode | None = None
        self.stack: list[PreconditionNode | None] = []

    def add_operator(self, operator: str, variables: list[tuple[str, str]] = None):
        """
        Begin a logical or quantifier operator node. Supported operators: and, or, not, imply, forall, exists.
        Must be closed with end_operator().
        """
        node = PreconditionNode(operator.lower(), variables=variables or [])
        if self.root is None:
            self.root = node
        else:
            self.current.children.append(node)
        self.stack.append(self.current)
        self.current = node

    def end_operator(self):
        """
        Close the most recently opened operator node and return to its parent.
        """
        self.current = self.stack.pop()

    def add_condition(self, predicate_symbol: str, arguments: list[str], variables: list[tuple[str, str]] = None):
        """
        Add a leaf predicate under the current operator context (or as root if none).
        """
        leaf = PreconditionNode(predicate_symbol.lower(), arguments, variables or [])
        if self.root is None:
            self.root = leaf
        else:
            self.current.children.append(leaf)

    def to_pddl_precondition(self) -> PDDLPrecondition:
        """
        Convert the built syntax tree into a nested PDDLPrecondition object.
        """
        if self.root is None:
            raise ValueError("Empty syntax tree: no preconditions added")
        return self._node_to_precondition(self.root)

    def _node_to_precondition(self, node: PreconditionNode) -> PDDLPrecondition:
        op = node.operator
        # Quantifiers: forall, exists
        if op in {"forall", "exists"}:
            if not node.children:
                raise ValueError(f"Quantifier '{op}' must have one child expression")
            inner = self._node_to_precondition(node.children[0])
            return PDDLPrecondition(op, [inner], variables=node.variables)
        # Negation
        if op == "not":
            if not node.children:
                raise ValueError("'not' operator must wrap one expression")
            inner = self._node_to_precondition(node.children[0])
            return PDDLPrecondition(op, [inner])
        # Logical connectives: and, or, imply
        if op in {"and", "or", "imply"}:
            args = [self._node_to_precondition(child) for child in node.children]
            return PDDLPrecondition(op, args)
        # Leaf predicate
        return PDDLPrecondition(op, node.arguments)

"""
    # Example 1: Simple AND of two predicates
    tree1 = PDDLPreconditionSyntaxTree()
    tree1.add_operator("and")
    tree1.add_condition("at", ["robot1", "room1"])
    tree1.add_condition("has-key", ["robot1"])
    tree1.end_operator()
    pre1 = tree1.to_pddl_precondition()
    print(pre1.to_pddl())  # => (and (at robot1 room1) (has-key robot1))

    # Example 2: Universal quantification with nested AND
    tree2 = PDDLPreconditionSyntaxTree()
    tree2.add_operator("forall")
    tree2.root.variables = [("?x", "room")]
    tree2.add_operator("and")
    tree2.add_condition("clear", ["?x"])
    tree2.add_operator("not")
    tree2.add_condition("locked", ["?x"])
    tree2.end_operator()  # end not
    tree2.end_operator()  # end and
    tree2.end_operator()  # end forall
    pre2 = tree2.to_pddl_precondition()
    print(pre2.to_pddl())
    # => (forall (?x - room) (and (clear ?x) (not (locked ?x))))
"""