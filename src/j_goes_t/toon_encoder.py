from j_goes_t.toon_tree import (
    ArrayNode,
    BoolNode,
    NullNode,
    NumberNode,
    ObjectNode,
    StringNode,
)


class TOONEncoder:
    """Encode a TOON tree into TOON format."""

    def __init__(self, toon_tree):
        self.toon_tree = toon_tree

    def encode(self):
        """Encode the TOON tree."""
        if isinstance(self.toon_tree, ObjectNode):
            return self._encode_object(self.toon_tree)

        if isinstance(self.toon_tree, ArrayNode):
            return self._encode_array(self.toon_tree)

    def _encode_object(self, node: ObjectNode, indent: int = 0):
        """Encode an object node."""
        lines = []
        prefix = "  " * indent

        for key, value in node.members.items():
            if isinstance(value, (StringNode, NumberNode)):
                lines.append(f"{prefix}{key}: {value.value}")

            elif isinstance(value, BoolNode):
                lines.append(f"{prefix}{key}: {str(value.value).lower()}")

            elif isinstance(value, NullNode):
                lines.append(f"{prefix}{key}: null")

            elif isinstance(value, ObjectNode):
                lines.append(f"{prefix}{key}:")
                nested = self._encode_object(value, indent + 1)
                lines.extend(nested.splitlines())

            elif isinstance(value, ArrayNode) and not value.elements:
                lines.append(f"{prefix}{key}: []")

            elif isinstance(value, ArrayNode):
                lines.extend(self._encode_tabular_array(key, value, indent))

        return "\n".join(lines)

    def _encode_array(self, node: ArrayNode):
        """Encode an array node."""
        values = []

        for element in node.elements:
            if isinstance(element, (StringNode, NumberNode)):
                values.append(str(element.value))

        return f"[{len(node.elements)}]: {','.join(values)}"

    def _encode_tabular_array(
        self,
        key: str,
        node: ArrayNode,
        indent: int = 0,
    ):
        """Encode an array of objects in tabular form."""
        objects = node.elements
        columns = list(objects[0].members.keys())

        prefix = "  " * indent
        header = f"{prefix}{key}[{len(objects)}]{{{','.join(columns)}}}:"

        lines = [header]

        for obj in objects:
            values = []

            for column in columns:
                value = obj.members[column]
                values.append(str(value.value))

            lines.append(f"{prefix}  {','.join(values)}")

        return lines
