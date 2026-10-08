from j_goes_t.toon_tree import (
    ArrayNode,
    BoolNode,
    NullNode,
    NumberNode,
    ObjectNode,
    StringNode,
)


class JSONAnalyser:
    """Analyse a Python tree and create a TOON tree."""

    def __init__(self, python_tree):
        self.python_tree = python_tree

    def analyse(self):
        return self._analyse_node(self.python_tree)

    def _analyse_node(self, node):
        if isinstance(node, dict):
            return ObjectNode(
                {key: self._analyse_node(value) for key, value in node.items()}
            )

        if isinstance(node, str):
            return StringNode(node)

        if isinstance(node, bool):
            return BoolNode(node)

        if isinstance(node, (int, float)):
            return NumberNode(node)

        if node is None:
            return NullNode()

        if isinstance(node, list):
            return ArrayNode([self._analyse_node(value) for value in node])

        raise TypeError(f"Unsupported JSON type: {type(node).__name__}")
