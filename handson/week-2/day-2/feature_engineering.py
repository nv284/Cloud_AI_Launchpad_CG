"""Calculate numerical features for validated customer records."""

import numpy as np


def calculate_features(valid_records):
    """Return customer IDs and vectorized risk-related feature arrays.

    Income and transaction scores are normalized to the largest value in the
    supplied records. The transaction-to-income ratio is zero when income is
    zero, avoiding division by zero.

    Args:
        valid_records: Iterable of validated customer record dictionaries.

    Returns:
        A dictionary containing NumPy arrays for customer IDs and features.
    """
    customer_ids = np.asarray(
        [record["customer_id"] for record in valid_records]
    )
    incomes = np.asarray(
        [record["income"] for record in valid_records], dtype=float
    )
    transactions = np.asarray(
        [record["transactions"] for record in valid_records], dtype=float
    )

    max_income = incomes.max(initial=0.0)
    max_transactions = transactions.max(initial=0.0)

    income_score = np.divide(
        incomes,
        max_income,
        out=np.zeros_like(incomes),
        where=max_income != 0,
    )
    transaction_score = np.divide(
        transactions,
        max_transactions,
        out=np.zeros_like(transactions),
        where=max_transactions != 0,
    )
    transaction_to_income_ratio = np.divide(
        transactions,
        incomes,
        out=np.zeros_like(transactions),
        where=incomes != 0,
    )

    return {
        "customer_ids": customer_ids,
        "income_score": income_score,
        "transaction_score": transaction_score,
        "transaction_to_income_ratio": transaction_to_income_ratio,
    }
