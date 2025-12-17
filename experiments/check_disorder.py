def check_disorder(test_file):
    import pandas as pd
    
    # Read the test file
    df_test = pd.read_csv(test_file)
    
    # Convert Time_A to integer for comparison
    df_test['Time_A'] = df_test['Time_A'].astype(int)
    
    # Check for out-of-order events
    out_of_order_events = 0
    prev_time = None
    
    for idx, row in df_test.iterrows():
        current_time = int(row['Time_A'])
        
        if prev_time is not None and current_time < prev_time:
            out_of_order_events += 1
            
        prev_time = current_time
    
    total_events = len(df_test)
    disorder_percent = (out_of_order_events / total_events) * 100 if total_events > 0 else 0
    
    print(f"\n--- Disorder Analysis ---")
    print(f"Total events: {total_events}")
    print(f"Out of order events: {out_of_order_events}")
    print(f"Disorder percentage: {disorder_percent:.2f}%")

if __name__ == "__main__":
    import os
    import sys
    
    # Default test file path (relative to the script's location)
    default_test_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'src', 'targets', 'experiments', 'maritime', '1M_unsorted2.csv'
    )
    
    # Use command line argument if provided, otherwise use default
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
    else:
        test_file = default_test_file
        print(f"Using default test file: {test_file}")
    
    if os.path.exists(test_file):
        check_disorder(test_file)
    else:
        print(f"Error: File not found: {test_file}")
        print("Please provide a valid file path as an argument.")
        print(f"Example: python {os.path.basename(__file__)} path/to/your/file.csv")
        sys.exit(1)