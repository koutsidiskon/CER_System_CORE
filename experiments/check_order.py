import pandas as pd
import os

# Use the absolute path to the file
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                        'src/targets/experiments/unordered_stocks/test.csv')

# Read the CSV file
try:
    df = pd.read_csv(file_path)
    # Rest of your code...
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    print("Current working directory:", os.getcwd())
    print("Please check the file path and try again.")

# Check if 'stock_time' column exists
if 'stock_time' not in df.columns:
    print("Error: 'stock_time' column not found in the CSV file.")
    print("Available columns:", df.columns.tolist())
else:
    # Sort the DataFrame by 'stock_time' to get the expected order
    df_sorted = df.sort_values('stock_time')
    
    # Reset index to get the original positions
    df_sorted = df_sorted.reset_index(drop=True)
    df = df.reset_index(drop=True)
    
    # Compare the original order with the sorted order
    out_of_order = df['stock_time'] != df_sorted['stock_time']
    num_out_of_order = out_of_order.sum()
    total_events = len(df)
    
    print(f"Total number of events: {total_events}")
    print(f"Number of events out of order: {num_out_of_order}")
    print(f"Percentage of events out of order: {num_out_of_order / total_events * 100:.2f}%")
    
    # If you want to see the first few out-of-order events
    if num_out_of_order > 0:
        print("\nFirst few out-of-order events:")
        print(df[out_of_order].head())