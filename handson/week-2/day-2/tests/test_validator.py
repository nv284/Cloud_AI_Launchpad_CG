from pathlib import Path

import pytest

from data_loader import load_data
from validator import validate_records


DATA_FILE = Path(__file__).parents[1] / "data" / "test_customers.json"


@pytest.fixture(scope="module")
def validation_results():
    records = load_data(DATA_FILE)
    return validate_records(records)


def get_case(records, case_name):
    return next(record for record in records if record["test_case"] == case_name)


def get_reason(invalid_records, case_name):
    return next(
        item["reason"]
        for item in invalid_records
        if item["record"]["test_case"] == case_name
    )


def test_valid_record_is_accepted(validation_results):
    valid_records, invalid_records = validation_results

    assert get_case(valid_records, "Valid customer")["customer_id"] == 101
    assert not any(
        item["record"]["test_case"] == "Valid customer"
        for item in invalid_records
    )


@pytest.mark.parametrize(
    ("case_name", "expected_reason"),
    [
        ("Missing customer_id", "customer_id is required"),
        ("Missing income", "income is required"),
        ("Missing transactions", "transactions is required"),
        (
            "Negative income",
            "income must be greater than or equal to zero",
        ),
        (
            "Negative transactions",
            "transactions must be greater than or equal to zero",
        ),
        ("Invalid customer_id type", "customer_id must be an integer"),
        ("Invalid income type", "income must be an integer or float"),
        (
            "Invalid transactions type",
            "transactions must be an integer or float",
        ),
    ],
)
def test_invalid_record_is_rejected_with_rule_reason(
    validation_results, case_name, expected_reason
):
    _, invalid_records = validation_results

    reason = get_reason(invalid_records, case_name)

    assert expected_reason in reason, (
        f"Validation rule failed for '{case_name}': {reason}"
    )


def test_duplicate_customer_id_is_detected(validation_results):
    _, invalid_records = validation_results

    reason = get_reason(invalid_records, "Duplicate customer_id")

    assert "customer_id 101 must be unique" in reason, (
        f"Validation rule failed for duplicate customer_id: {reason}"
    )
