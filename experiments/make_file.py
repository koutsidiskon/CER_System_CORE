import pandas as pd
import random
from collections import defaultdict

def create_unordered_file(input_file, output_file, disorder_percent=0.10):
    # Read the input CSV file
    df = pd.read_csv(input_file)
    
    # Group rows by stock_time and keep track of their original order
    time_groups = defaultdict(list)
    for idx, row in df.iterrows():
        time_groups[row['stock_time']].append((idx, row))
    
    # Convert to list of (time, [rows]) and sort by time
    sorted_groups = sorted(time_groups.items(), key=lambda x: x[0])
    total_groups = len(sorted_groups)
    
    # Calculate how many groups to move (10% of total groups)
    num_groups_to_move = max(1, int(total_groups * disorder_percent))
    
    # Select random groups to move
    groups_to_move = set(random.sample(range(total_groups), num_groups_to_move))
    
    # Create two lists: one for fixed groups and one for groups to be moved
    fixed_groups = []
    moving_groups = []
    
    for i, (time, rows) in enumerate(sorted_groups):
        if i in groups_to_move:
            moving_groups.append(rows)
        else:
            fixed_groups.append(rows)
    
    # Create the new order by interleaving fixed and moving groups
    new_order = []
    fixed_idx = 0
    moving_idx = 0
    total_fixed = len(fixed_groups)
    total_moving = len(moving_groups)
    
    # Distribute moving groups more evenly among fixed groups
    while fixed_idx < total_fixed or moving_idx < total_moving:
        # Add a fixed group
        if fixed_idx < total_fixed:
            new_order.extend([idx for idx, _ in fixed_groups[fixed_idx]])
            fixed_idx += 1
        
        # Add a moving group if available
        if moving_idx < total_moving and fixed_idx < total_fixed:
            new_order.extend([idx for idx, _ in moving_groups[moving_idx]])
            moving_idx += 1
    
    # If there are remaining moving groups, add them at the end
    while moving_idx < total_moving:
        new_order.extend([idx for idx, _ in moving_groups[moving_idx]])
        moving_idx += 1
    
    # Create the new dataframe with the new order
    result_df = df.iloc[new_order].reset_index(drop=True)
    
    # Save to output file
    result_df.to_csv(output_file, index=False)
    print(f"Created file with {disorder_percent*100}% disorder: {output_file}")

if __name__ == "__main__":
    # Define file paths
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, 'src', 'targets', 'experiments', 'stocks', 'stock_data.csv')
    output_file = os.path.join(base_dir, 'src', 'targets', 'experiments', 'unordered_stocks', 'test.csv')
    
    # Create the file with 10% disorder
    create_unordered_file(input_file, output_file, disorder_percent=0.20)