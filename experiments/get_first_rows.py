#!/usr/bin/env python3
import pandas as pd
import sys

def get_first_rows(input_file, output_file=None, num_rows=1000):
    """
    Extract the first 'num_rows' from a CSV file and save to a new file.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str, optional): Path to save the output. If None, adds '_first_<num_rows>' to input filename.
        num_rows (int, optional): Number of rows to extract. Defaults to 1000.
    """
    # Read the first 'num_rows' rows
    df = pd.read_csv(input_file, nrows=num_rows)
    
    # If output_file is not provided, create a default name
    if output_file is None:
        import os
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_first_{num_rows}{ext}"
    
    # Save to new file
    df.to_csv(output_file, index=False)
    print(f"Successfully saved first {num_rows} rows to {output_file}")

import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level from the script directory (to reach the CORE- root)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Default settings
INPUT_FILE = os.path.join(PROJECT_ROOT, 'src', 'targets', 'experiments', 'fires', 'CSV', 'Fire_department_4depts.csv')
OUTPUT_FILE = os.path.join(PROJECT_ROOT, 'src', 'targets', 'experiments', 'fires', 'CSV', 'Fire_department_4depts_first_10.csv')
NUM_ROWS = 100

if __name__ == "__main__":
    # Use the default settings
    get_first_rows(INPUT_FILE, OUTPUT_FILE, NUM_ROWS)
