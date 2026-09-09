from pathlib import Path

import numpy as np
import pytest

from data_loader import load_data
from feature_engineering import calculate_features
from validator import validate_records


DATA_FILE = Path(__file__).parents[1] / "data" / "test_customers.json"


@pytest.fixture(scope="module")
def feature_context():
    records = load_data(DATA_FILE)
    valid_records, invalid_records = validate_records(records)
    features = calculate_features(valid_records)
    return valid_records, invalid_records, features


def test_income_score_is_calculated_correctly(feature_context):
    valid_records, _, features = feature_context
    incomes = np.asarray(
        [record["income"] for record in valid_records], dtype=float
    )
    expected = incomes / incomes.max()

    np.testing.assert_allclose(features["income_score"], expected)


def test_transaction_score_is_calculated_correctly(feature_context):
    valid_records, _, features = feature_context
    transactions = np.asarray(
        [record["transactions"] for record in valid_records], dtype=float
    )
    expected = transactions / transactions.max()

    np.testing.assert_allclose(features["transaction_score"], expected)


def test_transaction_to_income_ratio_is_calculated_correctly(feature_context):
    valid_records, _, features = feature_context
    incomes = np.asarray(
        [record["income"] for record in valid_records], dtype=float
    )
    transactions = np.asarray(
        [record["transactions"] for record in valid_records], dtype=float
    )
    expected = np.divide(
        transactions,
        incomes,
        out=np.zeros_like(transactions),
        where=incomes != 0,
    )

    np.testing.assert_allclose(
        features["transaction_to_income_ratio"], expected
    )


def test_feature_values_are_numpy_arrays(feature_context):
    _, _, features = feature_context

    assert isinstance(features["customer_ids"], np.ndarray)
    assert isinstance(features["income_score"], np.ndarray)
    assert isinstance(features["transaction_score"], np.ndarray)
    assert isinstance(
        features["transaction_to_income_ratio"], np.ndarray
    )


def test_feature_count_matches_valid_customer_count(feature_context):
    valid_records, invalid_records, features = feature_context

    assert invalid_records
    assert len(features["customer_ids"]) == len(valid_records)
    assert len(features["income_score"]) == len(valid_records)
    assert len(features["transaction_score"]) == len(valid_records)
    assert len(features["transaction_to_income_ratio"]) == len(valid_records)


def test_zero_income_does_not_cause_division_by_zero(feature_context):
    valid_records, _, features = feature_context
    zero_income_indexes = [
        index
        for index, record in enumerate(valid_records)
        if record["income"] == 0
    ]

    assert zero_income_indexes
    assert np.all(
        features["transaction_to_income_ratio"][zero_income_indexes] == 0
    )
