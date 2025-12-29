"""
Compare multiple solutions with pandas DataFrames and multi-line plots
Usage:
  python compare_solutions.py
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_solution_data():
    """
    Define your different solutions here.
    Each solution should have data for different quarantine times.
    """
    
    # Example: Solution 1 - Dynamic Policy with MAX
    solution1 = {
        'name': 'MAX (window max)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [30853,30853,30853,30853,30853,30853,30853,30853,30853,30853,30853,30854,30865,30867,30870],
        'num_drops': [131,131,131,131,131,131,131,131,131,131,131,112,55,34,24],
    }
    
    # Example: Solution 2 - Dynamic Policy with a=0.1
    solution2 = {
        'name': 'EMA on max (α=0.1)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [30853,30853,30853,30853,30853,30853,30853,30853,30853,30853,30853,30854,30865,30867,30870],
        'num_drops': [133,133,133,133,133,133,133,133,133,133,133,112,56,34,24],
    }
    
    # Example: Solution 3 - ADAPTIVE Policy
    solution3 = {
        'name': 'Jump-and-Decay (α=0.1)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [30853,30853,30853,30853,30853,30853,30853,30853,30853,30853,30853,30854,30865,30867,30870],
        'num_drops': [130,130,130,130,130,130,130,130,130,130,130,111,55,34,24],
    }
    
    # Example: Solution 4 - HYBRID Policy
    solution4 = {
        'name': 'p99 + EMA (α=0.1)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [30831,30831,30831,30831,30831,30831,30831,30831,30831,30831,30831,30851,30862,30867,30870],
        'num_drops': [255,255,255,255,255,255,255,255,255,255,255,141,67,34,24],
    }
    
    # Example: Solution 5 - DIRECT (baseline)
    solution5 = {
    }
    
    return [solution1,solution2,solution3,solution4]


def create_comparison_dataframe(solutions):
    """Create a pandas DataFrame for each metric comparing all solutions"""
    
    # Get quarantine times (assuming all solutions use the same times)
    quarantine_times = solutions[0]['quarantine_times']
    
    # Create DataFrames for each metric
    dfs = {}
    metrics = ['num_results', 'num_drops']
    
    for metric in metrics:
        data = {'Quarantine Time (s)': quarantine_times}
        for solution in solutions:
            data[solution['name']] = solution[metric]
        dfs[metric] = pd.DataFrame(data)
    
    return dfs


def plot_all_solutions(dfs, solutions):
    """Create multi-line plots comparing all solutions"""
    
    # Define colors for each solution
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown']
    markers = ['o', 's', '^', 'D', 'v', 'p']
    
    # Get quarantine times from the first solution
    quarantine_times = solutions[0]['quarantine_times']
    
    # ======= Results Found Comparison =======
    plt.figure(figsize=(15, 8))
    x_pos = range(len(quarantine_times))
    
    for idx, solution in enumerate(solutions):
        plt.plot(x_pos, solution['num_results'], 
                marker=markers[idx], linestyle='-', linewidth=2,
                color=colors[idx], label=solution['name'], markersize=8)
    
    # Set x-ticks to show the actual quarantine times
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title('Complex Events Found Comparison Across Solutions', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Quarantine Time (s)', fontsize=12)
    plt.ylabel('Number of Results', fontsize=12)
    plt.legend(fontsize=10, loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("comparison_results.png", dpi=300, bbox_inches='tight')
    print("✓ Saved: comparison_results.png")
    
    # ======= Drops Comparison (IMPORTANT!) =======
    plt.figure(figsize=(15, 8))
    x_pos = range(len(quarantine_times))
    
    for idx, solution in enumerate(solutions):
        plt.plot(x_pos, solution['num_drops'], 
                marker=markers[idx], linestyle='-', linewidth=2,
                color=colors[idx], label=solution['name'], markersize=8)
    
    # Set x-ticks to show the actual quarantine times
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title('Dropped Events Comparison Across Solutions', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Quarantine Time (s)', fontsize=12)
    plt.ylabel('Number of Dropped Events', fontsize=12)
    plt.legend(fontsize=10, loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("comparison_drops.png", dpi=300, bbox_inches='tight')
    print("✓ Saved: comparison_drops.png")
    
    # ======= Combined Dashboard (2 subplots) =======
    fig, axes = plt.subplots(1, 2, figsize=(18, 7))
    fig.suptitle('Comparison Dashboard - All Solutions', fontsize=16, fontweight='bold', y=0.98)
    
    x_pos = range(len(quarantine_times))
    
    # Results Found
    for idx, solution in enumerate(solutions):
        axes[0].plot(x_pos, solution['num_results'], 
                       marker=markers[idx], linestyle='-', linewidth=2,
                       color=colors[idx], label=solution['name'], markersize=7)
    
    axes[0].set_xticks(x_pos)
    axes[0].set_xticklabels([str(t) for t in quarantine_times], fontsize=8, rotation=45)
    axes[0].set_title('Complex Events Found', fontweight='bold', fontsize=12)
    axes[0].set_xlabel('Quarantine Time (s)', fontsize=11)
    axes[0].set_ylabel('Number of Results', fontsize=11)
    axes[0].legend(fontsize=9, loc='best')
    axes[0].grid(True)
    
    # Drops
    for idx, solution in enumerate(solutions):
        axes[1].plot(x_pos, solution['num_drops'], 
                       marker=markers[idx], linestyle='-', linewidth=2,
                       color=colors[idx], label=solution['name'], markersize=7)
    
    axes[1].set_xticks(x_pos)
    axes[1].set_xticklabels([str(t) for t in quarantine_times], fontsize=8, rotation=45)
    axes[1].set_title('Dropped Events', fontweight='bold', fontsize=12)
    axes[1].set_xlabel('Quarantine Time (s)', fontsize=11)
    axes[1].set_ylabel('Number of Drops', fontsize=11)
    axes[1].legend(fontsize=9, loc='best')
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.savefig("comparison_dashboard.png", dpi=300, bbox_inches='tight')
    print("✓ Saved: comparison_dashboard.png")


def print_comparison_tables(dfs):
    """Print comparison tables for each metric"""
    
    metrics = {
        'num_results': 'Number of Results Found',
        'num_drops': 'Number of Dropped Events'
    }
    
    print("\n" + "="*100)
    print("COMPARISON TABLES")
    print("="*100)
    
    for metric_key, metric_name in metrics.items():
        print(f"\n{metric_name}:")
        print("-" * 100)
        print(dfs[metric_key].to_string(index=False))
        print()


def save_to_excel(dfs, filename='solution_comparison.xlsx'):
    """Save all comparison tables to an Excel file with multiple sheets"""
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        dfs['num_results'].to_excel(writer, sheet_name='Results Found', index=False)
        dfs['num_drops'].to_excel(writer, sheet_name='Drops', index=False)
    
    print(f"✓ Saved comparison data to: {filename}")


if __name__ == "__main__":
    print("\n" + "="*100)
    print("MULTI-SOLUTION COMPARISON TOOL")
    print("="*100)
    
    # Load data for all solutions
    solutions = load_solution_data()
    print(f"\nLoaded {len(solutions)} solutions for comparison:")
    for i, sol in enumerate(solutions, 1):
        print(f"  {i}. {sol['name']}")
    
    # Create comparison DataFrames
    dfs = create_comparison_dataframe(solutions)
    
    # Print comparison tables
    print_comparison_tables(dfs)
    
    # Save to Excel
    try:
        save_to_excel(dfs)
    except ImportError:
        print("\n⚠ openpyxl not installed. Skipping Excel export.")
        print("  Install with: pip install openpyxl")
    
    # Create all comparison plots
    print("\nGenerating comparison plots...")
    plot_all_solutions(dfs, solutions)
    
    print("\n" + "="*100)
    print("DONE! Check the generated PNG files.")
    print("="*100 + "\n")
