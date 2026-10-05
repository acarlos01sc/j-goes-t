from j_goes_t.json_analyser import JSONAnalyser
from j_goes_t.json_parser import JSONParser
from j_goes_t.toon_tree import (
    ArrayNode,
    ObjectNode,
    StringNode,
    NumberNode,
    BoolNode,
    NullNode,
)


def test_analyse_simple_object(tmp_path):
    json_file = tmp_path / "simple.json"
    json_file.write_text(
        '{"name": "Isildur", "age": 30}',
        encoding="utf-8",
    )

    parser = JSONParser(json_file)
    python_tree = parser.parse()

    analyser = JSONAnalyser(python_tree)
    toon_tree = analyser.analyse()

    assert isinstance(toon_tree, ObjectNode)

    assert isinstance(toon_tree.members["name"], StringNode)
    assert toon_tree.members["name"].value == "Isildur"

    assert isinstance(toon_tree.members["age"], NumberNode)
    assert toon_tree.members["age"].value == 30


def test_analyse_simple_array(tmp_path):
    json_file = tmp_path / "array.json"
    json_file.write_text(
        '["Isildur", "Elendil", "Aragorn"]',
        encoding="utf-8",
    )

    parser = JSONParser(json_file)
    python_tree = parser.parse()

    analyser = JSONAnalyser(python_tree)
    toon_tree = analyser.analyse()

    assert isinstance(toon_tree, ArrayNode)

    assert len(toon_tree.elements) == 3

    assert isinstance(toon_tree.elements[0], StringNode)
    assert toon_tree.elements[0].value == "Isildur"

    assert isinstance(toon_tree.elements[1], StringNode)
    assert toon_tree.elements[1].value == "Elendil"

    assert isinstance(toon_tree.elements[2], StringNode)
    assert toon_tree.elements[2].value == "Aragorn"


def test_analyse_boolean(tmp_path):
    json_file = tmp_path / "boolean.json"
    json_file.write_text(
        '{"active": true, "deleted": false}',
        encoding="utf-8",
    )

    parser = JSONParser(json_file)
    python_tree = parser.parse()

    analyser = JSONAnalyser(python_tree)
    toon_tree = analyser.analyse()

    assert isinstance(toon_tree, ObjectNode)

    assert isinstance(toon_tree.members["active"], BoolNode)
    assert toon_tree.members["active"].value is True

    assert isinstance(toon_tree.members["deleted"], BoolNode)
    assert toon_tree.members["deleted"].value is False


def test_analyse_null(tmp_path):
    json_file = tmp_path / "null.json"
    json_file.write_text(
        '{"value": null}',
        encoding="utf-8",
    )

    parser = JSONParser(json_file)
    python_tree = parser.parse()

    analyser = JSONAnalyser(python_tree)
    toon_tree = analyser.analyse()

    assert isinstance(toon_tree, ObjectNode)
    assert isinstance(toon_tree.members["value"], NullNode)


def test_analyse_nested_structure(tmp_path):
    json_file = tmp_path / "nested.json"
    json_file.write_text(
        """
        {
            "name": "Aragorn",
            "attributes": {
                "age": 87,
                "king": true
            },
            "weapons": [
                "Andúril",
                "Bow"
            ],
            "nickname": null
        }
        """,
        encoding="utf-8",
    )

    parser = JSONParser(json_file)
    python_tree = parser.parse()

    analyser = JSONAnalyser(python_tree)
    toon_tree = analyser.analyse()

    assert isinstance(toon_tree, ObjectNode)

    assert isinstance(toon_tree.members["name"], StringNode)
    assert toon_tree.members["name"].value == "Aragorn"

    attributes = toon_tree.members["attributes"]

    assert isinstance(attributes, ObjectNode)
    assert isinstance(attributes.members["age"], NumberNode)
    assert attributes.members["age"].value == 87
    assert isinstance(attributes.members["king"], BoolNode)
    assert attributes.members["king"].value is True

    weapons = toon_tree.members["weapons"]

    assert isinstance(weapons, ArrayNode)
    assert len(weapons.elements) == 2
    assert isinstance(weapons.elements[0], StringNode)
    assert weapons.elements[0].value == "Andúril"
    assert isinstance(weapons.elements[1], StringNode)
    assert weapons.elements[1].value == "Bow"

    assert isinstance(toon_tree.members["nickname"], NullNode)
