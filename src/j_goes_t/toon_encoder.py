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
        return self._encode_node(self.toon_tree)

    def _encode_node(self, node):
        """Encode a TOON node according ti its type."""
        if isinstance(node, ObjectNode):
            return self._encode_object(node)

        if isinstance(node, ArrayNode):
            return self._encode_array(node)

        if isinstance(node, NumberNode):
            return str(node.value)

        if isinstance(node, StringNode):
            return node.value

        if isinstance(node, BoolNode):
            return str(node.value).lower()

        if isinstance(node, NullNode):
            return "null"

        raise TypeError(f"Unsupported TOON node type: {type(node).__name__}")

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
                if self._has_uniform_structure(value):
                    lines.extend(self._encode_tabular_array(key, value, indent))
                else:
                    encoded = self._encode_array(value)
                    encoded_lines = encoded.splitlines()

                    lines.append(f"{prefix}{key}: {encoded_lines[0]}")
                    lines.extend(f"{prefix}{line}" for line in encoded_lines[1:])

        return "\n".join(lines)

    def _get_tabular_columns(self, node: ObjectNode):
        """Discover tabular columns recursively in nested objects."""
        columns = []

        for key, value in node.members.items():
            if isinstance(value, ObjectNode):
                nested_columns = self._get_tabular_columns(value)
                columns.append((key, nested_columns))
            else:
                columns.append((key, None))

        return columns

    def _get_tabular_values(self, node: ObjectNode) -> list[str]:
        """Extract primitive values from an object recursively."""
        values = []

        for value in node.members.values():
            if isinstance(value, ObjectNode):
                values.extend(self._get_tabular_values(value))
            else:
                values.append(self._encode_node(value))

        return values

    def _has_uniform_structure(self, node: ArrayNode) -> bool:
        """Check whether an array satisfies TOON tabular requirements."""
        objects = node.elements

        if not objects or not all(
            isinstance(element, ObjectNode) for element in objects
        ):
            return False

        if any(not obj.members for obj in objects):
            return False

        first_keys = set(objects[0].members)

        if any(set(obj.members) != first_keys for obj in objects):
            return False

        primitive_types = (StringNode, NumberNode, BoolNode, NullNode)

        for key in objects[0].members:
            values = [obj.members[key] for obj in objects]

            if all(isinstance(value, primitive_types) for value in values):
                continue

            if all(isinstance(value, ObjectNode) for value in values):
                if not self._has_uniform_structure(ArrayNode(values)):
                    return False

                continue

            return False

        return True

    def _encode_array(self, node: ArrayNode):
        """Encode an array node."""
        if self._has_uniform_structure(node):
            return "\n".join(self._encode_tabular_array("", node))

        if all(
            isinstance(element, (StringNode, NumberNode, BoolNode, NullNode))
            for element in node.elements
        ):
            values = [self._encode_node(element) for element in node.elements]
            return f"[{len(node.elements)}]: {','.join(values)}"

        lines = [f"[{len(node.elements)}]:"]

        for element in node.elements:
            encoded = self._encode_node(element)
            element_lines = encoded.splitlines()

            lines.append(f"  - {element_lines[0]}")
            lines.extend(f"    {line}" for line in element_lines[1:])

        return "\n".join(lines)

    def _encode_tabular_array(
        self,
        key: str,
        node: ArrayNode,
        indent: int = 0,
    ):
        """Encode an array of objects in tabular form."""
        objects = node.elements
        columns = self._get_tabular_columns(objects[0])

        def encode_columns(columns):
            encoded_columns = []

            for column, nested_columns in columns:
                if nested_columns is None:
                    encoded_columns.append(column)
                else:
                    nested = encode_columns(nested_columns)
                    encoded_columns.append(f"{column}{{{nested}}}")

            return ",".join(encoded_columns)

        prefix = "  " * indent
        header = f"{prefix}{key}[{len(objects)}]{{{encode_columns(columns)}}}:"

        lines = [header]

        for obj in objects:
            values = []

            for column, nested_columns in columns:
                value = obj.members[column]

                if nested_columns is None:
                    values.append(self._encode_node(value))
                elif isinstance(value, ObjectNode):
                    values.extend(self._get_tabular_values(value))

            lines.append(f"{prefix}  {','.join(values)}")

        return lines
