"""Validate customer records without loading or changing source data."""

from copy import deepcopy
from numbers import Real


def _is_number(value):
    """Return whether value is a supported numeric value, excluding booleans."""
    return isinstance(value, Real) and not isinstance(value, bool)


def validate_records(records):
    """Separate customer records into valid and invalid lists.

    Invalid entries contain a copy of the original record and a rejection reason.
    The input records are never modified.

    Args:
        records: An iterable of customer record dictionaries.

    Returns:
        A tuple of ``(valid_records, invalid_records)``.
    """
    valid_records = []
    invalid_records = []
    seen_customer_ids = set()

    for record in records:
        reasons = []

        if not isinstance(record, dict):
            invalid_records.append(
                {
                    "record": deepcopy(record),
                    "reason": "Customer record must be an object."
                }
            )
            continue

        if "customer_id" not in record:
            reasons.append("customer_id is required.")
        elif not isinstance(record["customer_id"], int) or isinstance(
            record["customer_id"], bool
        ):
            reasons.append("customer_id must be an integer.")

        if "income" not in record:
            reasons.append("income is required.")
        elif not _is_number(record["income"]):
            reasons.append("income must be an integer or float.")
        elif record["income"] < 0:
            reasons.append("income must be greater than or equal to zero.")

        if "transactions" not in record:
            reasons.append("transactions is required.")
        elif not _is_number(record["transactions"]):
            reasons.append("transactions must be an integer or float.")
        elif record["transactions"] < 0:
            reasons.append(
                "transactions must be greater than or equal to zero."
            )

        customer_id = record.get("customer_id")
        if (
            not reasons
            and customer_id in seen_customer_ids
        ):
            reasons.append(f"customer_id {customer_id} must be unique.")

        if reasons:
            invalid_records.append(
                {
                    "record": deepcopy(record),
                    "reason": " ".join(reasons)
                }
            )
        else:
            seen_customer_ids.add(customer_id)
            valid_records.append(deepcopy(record))

    return valid_records, invalid_records