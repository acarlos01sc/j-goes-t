import json

from j_goes_t.json_analyser import JSONAnalyser
from j_goes_t.json_parser import JSONParser
from j_goes_t.toon_encoder import TOONEncoder


def convert_json_to_toon(json_content: str) -> str:
    """Convert a JSON string to TOON using the complete pipeline."""
    python_tree = JSONParser(json_content).parse()
    toon_tree = JSONAnalyser(python_tree).analyse()
    return TOONEncoder(toon_tree).encode()


def test_encode_empty_array_at_root(tmp_path):
    """An empty JSON array at the root must encode as []."""
    json_file = tmp_path / "empty_array.json"
    json_file.write_text(json.dumps([]), encoding="utf-8")

    python_tree = JSONParser(json_file).parse()
    toon_tree = JSONAnalyser(python_tree).analyse()
    result = TOONEncoder(toon_tree).encode()

    assert result == "[]"


def test_encode_array_with_empty_objects(tmp_path):
    """An array containing empty objects must preserve both elements."""
    json_file = tmp_path / "empty_objects.json"
    json_file.write_text("[{}, {}]", encoding="utf-8")

    python_tree = JSONParser(json_file).parse()
    toon_tree = JSONAnalyser(python_tree).analyse()
    result = TOONEncoder(toon_tree).encode()

    assert result == "[2]:\n  -\n  -"
