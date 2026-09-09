"""Load customer records from a JSON file."""

import json
from json import JSONDecodeError
from pathlib import Path


def load_data(file_path):
    """Load and return customer records from a JSON file.

    Args:
        file_path: Path to a JSON file containing a list of customer records.

    Returns:
        A list of customer records.

    Raises:
        FileNotFoundError: If the JSON file does not exist.
        ValueError: If the JSON is invalid or its root is not a list.
    """
    path = Path(file_path)

    try:
        with path.open("r", encoding="utf-8") as data_file:
            records = json.load(data_file)
    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Customer data file not found: {path}"
        ) from error
    except JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in customer data file '{path}' "
            f"at line {error.lineno}, column {error.colno}: {error.msg}"
        ) from error

    if not isinstance(records, list):
        raise ValueError(
            f"Customer data in '{path}' must contain a list of records."
        )

    if any(not isinstance(record, dict) for record in records):
        raise ValueError(
            f"Customer data in '{path}' must contain customer records as objects."
        )

    return records


if __name__ == "__main__":
    customers_file = Path(__file__).parent / "data" / "customers.json"
    customers = load_data(customers_file)
    print(f"Successfully loaded {len(customers)} customer records.")
