import numpy as np

from risk_calculator import calculate_risk_score


def test_all_risk_scores_are_between_zero_and_one_hundred():
    features = {
        "customer_ids": np.array([1, 2, 3]),
        "income_score": np.array([0.0, 0.5, 1.0]),
        "transaction_score": np.array([1.0, 0.5, 0.0]),
        "transaction_to_income_ratio": np.array([1.0, 0.5, 0.0]),
    }

    result = calculate_risk_score(features)

    assert np.all((result["risk_scores"] >= 0) & (result["risk_scores"] <= 100))


def test_low_risk_input_produces_low_score():
    features = {
        "customer_ids": np.array([1]),
        "income_score": np.array([1.0]),
        "transaction_score": np.array([0.0]),
        "transaction_to_income_ratio": np.array([0.0]),
    }

    result = calculate_risk_score(features)

    assert result["risk_scores"][0] < 40
    assert result["risk_levels"][0] == "LOW"


def test_high_risk_input_produces_high_score():
    features = {
        "customer_ids": np.array([1]),
        "income_score": np.array([0.0]),
        "transaction_score": np.array([1.0]),
        "transaction_to_income_ratio": np.array([1.0]),
    }

    result = calculate_risk_score(features)

    assert result["risk_scores"][0] >= 70
    assert result["risk_levels"][0] == "HIGH"


def test_number_of_risk_scores_matches_number_of_customers():
    customer_ids = np.array([101, 102, 103, 104])
    features = {
        "customer_ids": customer_ids,
        "income_score": np.array([0.2, 0.4, 0.6, 0.8]),
        "transaction_score": np.array([0.8, 0.6, 0.4, 0.2]),
        "transaction_to_income_ratio": np.array([0.7, 0.5, 0.3, 0.1]),
    }

    result = calculate_risk_score(features)

    assert len(result["risk_scores"]) == len(customer_ids)
    assert len(result["risk_levels"]) == len(customer_ids)


def test_numpy_arrays_are_supported():
    features = {
        "customer_ids": np.array([1, 2]),
        "income_score": np.array([0.25, 0.75]),
        "transaction_score": np.array([0.75, 0.25]),
        "transaction_to_income_ratio": np.array([0.6, 0.2]),
    }

    result = calculate_risk_score(features)

    assert isinstance(result["customer_ids"], np.ndarray)
    assert isinstance(result["risk_scores"], np.ndarray)
    assert isinstance(result["risk_levels"], np.ndarray)


def test_risk_scores_are_finite():
    features = {
        "customer_ids": np.array([1, 2, 3]),
        "income_score": np.array([0.0, 0.5, 1.0]),
        "transaction_score": np.array([0.0, 0.5, 1.0]),
        "transaction_to_income_ratio": np.array([0.0, 0.5, 1.0]),
    }

    result = calculate_risk_score(features)

    assert np.all(np.isfinite(result["risk_scores"]))
