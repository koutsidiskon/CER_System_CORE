import pandas as pd
import os

def check_disorder(original_file, test_file):
    # Read both files
    df_orig = pd.read_csv(original_file)
    df_test = pd.read_csv(test_file)
    
    # Create a mapping of (stock_time, event_type, name, price) to original index
    orig_mapping = {
        tuple(x): i for i, x in enumerate(zip(
            df_orig['stock_time'],
            df_orig['event_type'],
            df_orig['name'],
            df_orig['price'],
            df_orig['volume']
        ))
    }
    
    # Check for out-of-order events based on time
    out_of_order_time = 0
    prev_time = None
    
    for i, row in df_test.iterrows():
        current_time = row['stock_time']
        
        # Check if this event exists in the original file
        key = (row['stock_time'], row['event_type'], row['name'], row['price'], row['volume'])
        if key in orig_mapping:
            orig_pos = orig_mapping[key]
            
            # Check if time is out of order
            if prev_time is not None and current_time < prev_time:
                out_of_order_time += 1
                
        # Update previous time
        if prev_time is None or current_time != prev_time:
            prev_time = current_time
    
    total_events = len(df_orig)
    disorder_percent = (out_of_order_time / total_events) * 100
    
    print(f"Total events: {total_events}")
    print(f"Events with earlier timestamps appearing after later ones: {out_of_order_time}")
    print(f"Time-based disorder percentage: {disorder_percent:.4f}%")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    original_file = os.path.join(base_dir, 'src', 'targets', 'experiments', 'stocks', 'stock_data.csv')
    test_file = os.path.join(base_dir, 'src', 'targets', 'experiments', 'unordered_stocks', 'test.csv')
    
    check_disorder(original_file, test_file)