![](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54)


# j-goes-t

**j-goes-t** is a Python library for converting data between **JSON** and **TOON** (Token-Oriented Object Notation).

The project is designed with a focus on **structured data representation, token efficiency, and reliable round-trip conversion**, with potential applications in workflows involving Large Language Models (LLMs).

## Project Status

🚧 **Early development**

The initial implementation focuses on parsing JSON and representing its structure internally. The TOON encoder and decoder are being developed incrementally using a **test-driven development (TDD)** approach.

## Goals

The main goals of the project are:

* Parse JSON into an internal object representation.
* Encode JSON data into TOON.
* Decode TOON back into JSON-compatible data.
* Preserve the structure and values of the original data.
* Support **round-trip conversion**:

```text
JSON → TOON → JSON
```

* Investigate and measure the potential **token savings** of TOON representations, particularly when data is processed by LLMs.

## Design

The library is being developed with an object-oriented architecture, separating the main responsibilities into components such as:

* **JSON parser** — analyzes JSON syntax and builds an internal representation.
* **JSON tree** — represents the structure of JSON data.
* **TOON encoder** — converts the internal representation into TOON.
* **TOON decoder** — reconstructs the data from TOON.
* **Tests** — verify each component independently and validate complete round-trip conversions.

The project initially avoids dependencies such as Pandas in order to keep the core implementation simple and independent. Pandas may be considered later as an **optional optimization** for tabular data.

## Example

The intended workflow is approximately:

```python
from j_goes_t import ...

data = {
    "name": "Alice",
    "age": 30,
    "languages": ["Python", "C++"]
}

toon = encode(data)
restored = decode(toon)
```

The exact public API is still under development.

## Development

The project requires **Python 3.12 or newer**.

Clone the repository and install the development dependencies according to the project configuration.

Tests are executed with:

```bash
pytest
```

## License

This project is released under the **MIT License**.
