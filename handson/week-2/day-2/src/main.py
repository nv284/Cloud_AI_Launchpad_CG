"""Run the complete customer risk-scoring pipeline."""

import json
import os
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_loader import load_data
from feature_engineering import calculate_features
from multiprocessing_processor import process_in_parallel
from validator import validate_records


DATA_FILE = PROJECT_ROOT / "data" / "customers.json"
RESULTS_FILE = PROJECT_ROOT / "data" / "customer_risk_results.json"


def run_pipeline():
    """Load, validate, process, and save customer risk results."""
    start_time = time.perf_counter()

    records = load_data(DATA_FILE)
    valid_records, invalid_records = validate_records(records)

    # Feature engineering uses NumPy arrays for the large numerical steps.
    features = calculate_features(valid_records)
    del features

    worker_count = min(os.cpu_count() or 1, len(valid_records))
    processed = process_in_parallel(
        valid_records,
        number_of_processes=worker_count or 1,
    )

    records_by_id = {
        record["customer_id"]: record for record in valid_records
    }
    final_results = [
        {
            "customer_id": int(customer_id),
            "income": records_by_id[int(customer_id)]["income"],
            "transactions": records_by_id[int(customer_id)]["transactions"],
            "risk_score": round(float(risk_score), 2),
            "risk_category": str(risk_category),
        }
        for customer_id, risk_score, risk_category in zip(
            processed["customer_ids"],
            processed["risk_scores"],
            processed["risk_levels"],
        )
    ]

    with RESULTS_FILE.open("w", encoding="utf-8") as results_file:
        json.dump(final_results, results_file, indent=4)
        results_file.write("\n")

    processing_time = time.perf_counter() - start_time
    print(f"Total records loaded: {len(records)}")
    print(f"Valid records: {len(valid_records)}")
    print(f"Invalid records: {len(invalid_records)}")
    print(f"Number of processed records: {len(final_results)}")
    print(f"Number of multiprocessing workers: {worker_count}")
    print(f"Processing time: {processing_time:.4f} seconds")
    print("First 5 results:")
    print(json.dumps(final_results[:5], indent=4))

    return final_results


if __name__ == "__main__":
    run_pipeline()
