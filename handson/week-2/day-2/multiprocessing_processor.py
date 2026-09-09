"""Process customer risk calculations across multiple CPU processes."""

import multiprocessing as mp
import os

import numpy as np

from feature_engineering import calculate_features
from risk_calculator import calculate_risk_score


def _process_chunk(records_chunk):
    """Calculate features and risk results for one records chunk."""
    features = calculate_features(records_chunk)
    return calculate_risk_score(features)


def _empty_result():
    """Return the standard result shape for an empty input."""
    return {
        "customer_ids": np.array([], dtype=int),
        "risk_scores": np.array([], dtype=float),
        "risk_levels": np.array([], dtype="U6"),
    }


def process_in_parallel(records, number_of_processes=None):
    """Process customer records in parallel and combine the risk results.

    Args:
        records: Iterable of validated customer record dictionaries.
        number_of_processes: Optional pool size. Defaults to the available
            CPU count.

    Returns:
        A dictionary containing combined customer IDs, risk scores, and risk
        levels in the same order as the input records.

    Raises:
        ValueError: If ``number_of_processes`` is not a positive integer.
    """
    records = list(records)
    if not records:
        return _empty_result()

    if number_of_processes is None:
        number_of_processes = os.cpu_count() or 1
    if not isinstance(number_of_processes, int) or isinstance(
        number_of_processes, bool
    ) or number_of_processes < 1:
        raise ValueError("number_of_processes must be a positive integer.")

    process_count = min(number_of_processes, len(records))
    chunk_size = (len(records) + process_count - 1) // process_count
    chunks = [
        records[start : start + chunk_size]
        for start in range(0, len(records), chunk_size)
    ]

    # A pool is useful here when each chunk performs genuinely CPU-bound work
    # that does not release the GIL. For purely numerical array operations,
    # NumPy vectorization is usually preferable because it avoids process and
    # serialization overhead. The pool is created inside this function, and
    # the worker is module-level, so Windows spawn can import it safely.
    with mp.Pool(processes=process_count) as pool:
        chunk_results = pool.map(_process_chunk, chunks)

    return {
        "customer_ids": np.concatenate(
            [result["customer_ids"] for result in chunk_results]
        ),
        "risk_scores": np.concatenate(
            [result["risk_scores"] for result in chunk_results]
        ),
        "risk_levels": np.concatenate(
            [result["risk_levels"] for result in chunk_results]
        ),
    }
