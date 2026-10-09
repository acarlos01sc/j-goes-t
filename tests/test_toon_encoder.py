from j_goes_t.json_analyser import JSONAnalyser
from j_goes_t.json_parser import JSONParser
from j_goes_t.toon_encoder import TOONEncoder


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


def test_encode_root_number(tmp_path):
    json_file = tmp_path / "number.json"
    json_file.write_text("42", encoding="utf-8")

    parser = JSONParser(json_file)
    python_tree = parser.parse()

    analyser = JSONAnalyser(python_tree)
    toon_tree = analyser.analyse()

    encoder = TOONEncoder(toon_tree)
    toon = encoder.encode()

    assert toon == "42"


def test_encode_root_string(tmp_path):
    json_file = tmp_path / "string.json"
    json_file.write_text('"hello"', encoding="utf-8")

    parser = JSONParser(json_file)
    python_tree = parser.parse()

    analyser = JSONAnalyser(python_tree)
    toon_tree = analyser.analyse()

    encoder = TOONEncoder(toon_tree)
    toon = encoder.encode()

    assert toon == "hello"


def test_encode_root_boolean(tmp_path):
    json_file = tmp_path / "boolean.json"
    json_file.write_text("true", encoding="utf-8")

    parser = JSONParser(json_file)
    python_tree = parser.parse()

    analyser = JSONAnalyser(python_tree)
    toon_tree = analyser.analyse()

    encoder = TOONEncoder(toon_tree)
    toon = encoder.encode()

    assert toon == "true"


def test_encode_root_null(tmp_path):
    json_file = tmp_path / "null.json"
    json_file.write_text("null", encoding="utf-8")

    parser = JSONParser(json_file)
    python_tree = parser.parse()

    analyser = JSONAnalyser(python_tree)
    toon_tree = analyser.analyse()

    encoder = TOONEncoder(toon_tree)
    toon = encoder.encode()

    assert toon == "null"


def test_encode_mixed_array(tmp_path):
    json_file = tmp_path / "mixed_array.json"
    json_file.write_text(
        "[10, true, null]",
        encoding="utf-8",
    )

    parser = JSONParser(json_file)
    python_tree = parser.parse()

    analyser = JSONAnalyser(python_tree)
    toon_tree = analyser.analyse()

    encoder = TOONEncoder(toon_tree)
    toon = encoder.encode()

    assert toon == "[3]: 10,true,null"


def test_encode_nested_array(tmp_path):
    """Encode an array containing another array."""
    json_file = tmp_path / "nested_array.json"
    json_file.write_text("[1, [2, 3]]", encoding="utf-8")

    parser = JSONParser(json_file)
    analyser = JSONAnalyser(parser.parse())
    encoder = TOONEncoder(analyser.analyse())

    result = encoder.encode()

    assert result == "[2]:\n  - 1\n  - [2]: 2,3"


def test_encode_root_array_of_objects(tmp_path):
    """Encode an array of objects as the root node."""
    json_data = '[{"id": 1, "name": "Ada"}, {"id": 2, "name": "Bob"}]'
    json_file = tmp_path / "users.json"
    json_file.write_text(json_data, encoding="utf-8")

    parser = JSONParser(json_file)
    analyser = JSONAnalyser(parser.parse())
    encoder = TOONEncoder(analyser.analyse())

    result = encoder.encode()

    assert result == "[2]{id,name}:\n  1,Ada\n  2,Bob"


def test_encode_array_of_objects_with_different_keys(tmp_path):
    """Encode an array of objects with different keys using list form."""
    json_data = '[{"id": 1, "name": "Ada"}, {"id": 2, "age": 30}]'
    json_file = tmp_path / "non_uniform_objects.json"
    json_file.write_text(json_data, encoding="utf-8")

    parser = JSONParser(json_file)
    analyser = JSONAnalyser(parser.parse())
    encoder = TOONEncoder(analyser.analyse())

    result = encoder.encode()

    assert result == ("[2]:\n  - id: 1\n    name: Ada\n  - id: 2\n    age: 30")


def test_get_tabular_columns_with_nested_object(tmp_path):
    """Discover tabular columns, including nested object fields."""
    json_data = '{"id": 1, "customer": {"name": "Ada", "country": "UK"}}'
    json_file = tmp_path / "nested_customer.json"
    json_file.write_text(json_data, encoding="utf-8")

    parser = JSONParser(json_file)
    analyser = JSONAnalyser(parser.parse())
    encoder = TOONEncoder(analyser.analyse())

    columns = encoder._get_tabular_columns(encoder.toon_tree)

    assert columns == [
        ("id", None),
        (
            "customer",
            [
                ("name", None),
                ("country", None),
            ],
        ),
    ]


def test_get_tabular_columns_with_deeply_nested_objects(tmp_path):
    """Discover tabular columns recursively in nested objects."""
    json_data = (
        '{"id": 1, "customer": {'
        '"name": "Ada", '
        '"address": {'
        '"city": "London", '
        '"country": "UK"'
        "}"
        "}}"
    )
    json_file = tmp_path / "deeply_nested_customer.json"
    json_file.write_text(json_data, encoding="utf-8")

    parser = JSONParser(json_file)
    analyser = JSONAnalyser(parser.parse())
    encoder = TOONEncoder(analyser.analyse())

    columns = encoder._get_tabular_columns(encoder.toon_tree)

    assert columns == [
        ("id", None),
        (
            "customer",
            [
                ("name", None),
                (
                    "address",
                    [
                        ("city", None),
                        ("country", None),
                    ],
                ),
            ],
        ),
    ]


def test_encode_array_of_objects_with_nested_objects(tmp_path):
    """Encode an array of objects containing uniform nested objects."""
    json_data = (
        '[{"id": 1, "customer": {"name": "Ada", "country": "UK"}},'
        ' {"id": 2, "customer": {"name": "Bob", "country": "US"}}]'
    )
    json_file = tmp_path / "nested_objects.json"
    json_file.write_text(json_data, encoding="utf-8")

    parser = JSONParser(json_file)
    analyser = JSONAnalyser(parser.parse())
    encoder = TOONEncoder(analyser.analyse())

    result = encoder.encode()

    assert result == ("[2]{id,customer{name,country}}:\n  1,Ada,UK\n  2,Bob,US")


def test_encode_tabular_array_with_different_key_order(tmp_path):
    """Encode uniform objects whose keys appear in different orders."""
    json_data = '[{"id": 1, "name": "Ada"}, {"name": "Bob", "id": 2}]'
    json_file = tmp_path / "different_key_order.json"
    json_file.write_text(json_data, encoding="utf-8")

    parser = JSONParser(json_file)
    analyser = JSONAnalyser(parser.parse())
    encoder = TOONEncoder(analyser.analyse())

    result = encoder.encode()

    assert result == "[2]{id,name}:\n  1,Ada\n  2,Bob"


def test_encode_array_with_incompatible_nested_types(tmp_path):
    """Encode incompatible nested structures using list form."""
    json_data = '[{"id": 1, "value": {"name": "Ada"}}, {"id": 2, "value": [10, 20]}]'
    json_file = tmp_path / "incompatible_nested_types.json"
    json_file.write_text(json_data, encoding="utf-8")

    parser = JSONParser(json_file)
    analyser = JSONAnalyser(parser.parse())
    encoder = TOONEncoder(analyser.analyse())

    result = encoder.encode()

    assert result == (
        "[2]:\n  - id: 1\n    value:\n      name: Ada\n  - id: 2\n    value: [2]: 10,20"
    )
