from j_goes_t.toon_encoder import TOONEncoder

from j_goes_t.json_analyser import JSONAnalyser
from j_goes_t.json_parser import JSONParser


def test_encode_simple_object(tmp_path):
    json_file = tmp_path / "simple.json"
    json_file.write_text(
        '{"name": "Isildur", "age": 30}',
        encoding="utf-8",
    )

    parser = JSONParser(json_file)
    python_tree = parser.parse()

    analyser = JSONAnalyser(python_tree)
    toon_tree = analyser.analyse()

    encoder = TOONEncoder(toon_tree)
    toon = encoder.encode()

    assert toon == "name: Isildur\nage: 30"


def test_encode_primitive_array(tmp_path):
    json_file = tmp_path / "array.json"
    json_file.write_text(
        '["Isildur", "Elendil", "Aragorn"]',
        encoding="utf-8",
    )

    parser = JSONParser(json_file)
    python_tree = parser.parse()

    analyser = JSONAnalyser(python_tree)
    toon_tree = analyser.analyse()

    encoder = TOONEncoder(toon_tree)
    toon = encoder.encode()

    assert toon == "[3]: Isildur,Elendil,Aragorn"


def test_encode_boolean_and_null(tmp_path):
    json_file = tmp_path / "values.json"
    json_file.write_text(
        '{"active": true, "deleted": false, "value": null}',
        encoding="utf-8",
    )

    parser = JSONParser(json_file)
    python_tree = parser.parse()

    analyser = JSONAnalyser(python_tree)
    toon_tree = analyser.analyse()

    encoder = TOONEncoder(toon_tree)
    toon = encoder.encode()

    assert toon == ("active: true\ndeleted: false\nvalue: null")


def test_encode_nested_object(tmp_path):
    json_file = tmp_path / "nested.json"
    json_file.write_text(
        """
    {
    "name": "Aragorn",
    "attributes": {
    "age": 87,
    "king": true
    }
    }
    """,
        encoding="utf-8",
    )

    parser = JSONParser(json_file)
    python_tree = parser.parse()

    analyser = JSONAnalyser(python_tree)
    toon_tree = analyser.analyse()

    encoder = TOONEncoder(toon_tree)
    toon = encoder.encode()

    assert toon == ("name: Aragorn\nattributes:\n  age: 87\n  king: true")


def test_encode_empty_array(tmp_path):
    json_file = tmp_path / "empty_array.json"
    json_file.write_text(
        '{"items": []}',
        encoding="utf-8",
    )

    parser = JSONParser(json_file)
    python_tree = parser.parse()

    analyser = JSONAnalyser(python_tree)
    toon_tree = analyser.analyse()

    encoder = TOONEncoder(toon_tree)
    toon = encoder.encode()

    assert toon == "items: []"


def test_encode_tabular_array(tmp_path):
    json_file = tmp_path / "users.json"
    json_file.write_text(
        """
    {
    "users": [
    {"id": 1, "name": "Ada"},
    {"id": 2, "name": "Bob"}
    ]
    }
    """,
        encoding="utf-8",
    )

    parser = JSONParser(json_file)
    python_tree = parser.parse()

    analyser = JSONAnalyser(python_tree)
    toon_tree = analyser.analyse()

    encoder = TOONEncoder(toon_tree)
    toon = encoder.encode()

    assert toon == ("users[2]{id,name}:\n  1,Ada\n  2,Bob")
