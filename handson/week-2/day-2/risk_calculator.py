"""Calculate educational customer risk scores from engineered features."""

import numpy as np


def calculate_risk_score(features):
    """Calculate bounded risk scores and risk levels with NumPy arrays.

    Args:
        features: Mapping containing the feature arrays ``customer_ids``,
            ``income_score``, ``transaction_score``, and
            ``transaction_to_income_ratio``.

    Returns:
        A dictionary containing customer IDs, scores from 0 to 100, and risk
        levels (LOW, MEDIUM, or HIGH).
    """
    customer_ids = np.asarray(features["customer_ids"])
    income_score = np.asarray(features["income_score"], dtype=float)
    transaction_score = np.asarray(features["transaction_score"], dtype=float)
    transaction_to_income_ratio = np.asarray(
        features["transaction_to_income_ratio"], dtype=float
    )

    max_ratio = transaction_to_income_ratio.max(initial=0.0)
    normalized_ratio = np.divide(
        transaction_to_income_ratio,
        max_ratio,
        out=np.zeros_like(transaction_to_income_ratio),
        where=max_ratio != 0,
    )

    # Formula: risk score = 100 * (
    #     0.40 * (1 - income_score)
    #     + 0.40 * transaction_score
    #     + 0.20 * normalized transaction_to_income_ratio
    # ). Higher transaction activity and transaction-to-income ratios increase
    # risk, while a higher income score reduces risk.
    risk_scores = 100 * (
        0.40 * (1 - income_score)
        + 0.40 * transaction_score
        + 0.20 * normalized_ratio
    )
    risk_scores = np.clip(risk_scores, 0, 100)

    risk_levels = np.select(
        [risk_scores < 40, risk_scores < 70],
        ["LOW", "MEDIUM"],
        default="HIGH",
    )

    return {
        "customer_ids": customer_ids,
        "risk_scores": risk_scores,
        "risk_levels": risk_levels,
    }
