import pytest

from j_goes_t.json_parser import JSONParser


def test_validate_nonexistent_file():
    parser = JSONParser("nonexistent.json")

    with pytest.raises(FileNotFoundError):
        parser.validate()


def test_validate_valid_json(tmp_path):
    json_file = tmp_path / "valid.json"
    json_file.write_text('{"name": "Isildur"}', encoding="utf-8")

    parser = JSONParser(json_file)

    assert parser.validate() is True


def test_validate_invalid_json(tmp_path):
    json_file = tmp_path / "invalid.json"
    json_file.write_text('{"name": "Isildur"', encoding="utf-8")

    parser = JSONParser(json_file)

    assert parser.validate() is False


def test_parse_simple_object(tmp_path):
    json_file = tmp_path / "simple.json"
    json_file.write_text(
        '{"name": "Isildur", "age": 30}',
        encoding="utf-8",
    )

    parser = JSONParser(json_file)

    assert parser.parse() == {
        "name": "Isildur",
        "age": 30,
    }


def test_parse_simple_array(tmp_path):
    json_file = tmp_path / "array.json"
    json_file.write_text(
        '["Isildur", "Elendil", "Aragorn"]',
        encoding="utf-8",
    )

    parser = JSONParser(json_file)

    assert parser.parse() == [
        "Isildur",
        "Elendil",
        "Aragorn",
    ]


def test_parse_nested_object(tmp_path):
    json_file = tmp_path / "nested.json"
    json_file.write_text(
        '{"name": "Isildur", "father": {"name": "Elendil"}}',
        encoding="utf-8",
    )

    parser = JSONParser(json_file)

    assert parser.parse() == {
        "name": "Isildur",
        "father": {
            "name": "Elendil",
        },
    }


def test_parse_object_with_array(tmp_path):
    json_file = tmp_path / "object_array.json"
    json_file.write_text(
        '{"name": "Isildur", "children": ["Elendur", "Aratan", "Ciryon"]}',
        encoding="utf-8",
    )

    parser = JSONParser(json_file)

    assert parser.parse() == {
        "name": "Isildur",
        "children": [
            "Elendur",
            "Aratan",
            "Ciryon",
        ],
    }
