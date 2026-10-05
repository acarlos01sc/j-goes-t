class Node:
    """Base class for nodes in a TOON tree."""


class ObjectNode(Node):
    """Node representing a JSON object."""

    def __init__(self, members):
        self.members = members


class ArrayNode(Node):
    """Node representing a JSON array."""

    def __init__(self, elements):
        self.elements = elements


class StringNode(Node):
    """Node representing a JSON string."""

    def __init__(self, value):
        self.value = value


class NumberNode(Node):
    """Node representing a JSON number."""

    def __init__(self, value):
        self.value = value


class BoolNode(Node):
    """Node representing a JSON boolean."""

    def __init__(self, value):
        self.value = value


class NullNode(Node):
    """Node representing a JSON null."""

    def __init__(self):
        pass
