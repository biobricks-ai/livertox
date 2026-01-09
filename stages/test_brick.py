#!/usr/bin/env python3
"""
Test script to validate the livertox brick data.
"""

import sys
from pathlib import Path
import pandas as pd

def test_brick():
    brick_path = Path("brick")
    parquet_file = brick_path / "livertox.parquet"

    # Check file exists
    if not parquet_file.exists():
        print(f"FAIL: {parquet_file} does not exist")
        return False

    # Load and validate
    df = pd.read_parquet(parquet_file)

    # Check minimum records
    if len(df) < 100:
        print(f"FAIL: Expected at least 100 drug records, got {len(df)}")
        return False

    # Check required columns
    required_cols = ['drug_name', 'hepatotoxicity']
    for col in required_cols:
        if col not in df.columns:
            print(f"FAIL: Missing required column: {col}")
            return False

    # Check drug_name is not empty
    non_empty = df['drug_name'].notna() & (df['drug_name'] != '')
    if non_empty.sum() < 100:
        print(f"FAIL: Too few drugs with names: {non_empty.sum()}")
        return False

    print(f"PASS: LiverTox brick validated")
    print(f"  - Total records: {len(df)}")
    print(f"  - Columns: {list(df.columns)}")
    print(f"  - Sample drugs: {df['drug_name'].head(5).tolist()}")
    return True

if __name__ == "__main__":
    success = test_brick()
    sys.exit(0 if success else 1)
