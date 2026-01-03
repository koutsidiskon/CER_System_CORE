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
    
    # Example: Solution 1 - MAX (window max)
    solution1 = {
        'name': 'MAX (window max)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [12556,12556,12556,12556,12556,12556,12556,12556,12556,12556,12843,13670,15123,15579,15663],
        'num_drops': [123070,123070,123070,123070,123070,123070,123070,123070,123070,123070,114730,82589,27918,6739,1210],
    }
    
    # Example: Solution 2 - EMA on max (α=0.1)
    solution2 = {
        'name': 'EMA on max (α=0.1)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [12524,12524,12524,12524,12524,12524,12524,12524,12524,12524,12823,13550,15123,15600,15663],
        'num_drops': [124751,124751,124751,124751,124751,124751,124751,124751,124751,124751,113954,85670,28117,5533,1210],
    }
    
    # Example: Solution 3 - Jump-and-Decay (α=0.1)
    solution3 = {
        'name': 'Jump-and-Decay (α=0.1)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [12635,12635,12635,12635,12635,12635,12635,12635,12635,12635,12930,13670,15123,15600,15663],
        'num_drops': [119379,119379,119379,119379,119379,119379,119379,119379,119379,119379,110818,82589,27918,5533,1210],
    }
    
    # Example: Solution 4 - p99 + EMA (α=0.1)
    solution4 = {
        'name': 'p99 + EMA (α=0.1)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [11026,11026,11026,11026,11026,11026,11026,11026,11026,11053,11731,13193,15017,15576,15663],
        'num_drops': [188626,188626,188626,188626,188626,188626,188626,188626,188626,187641,162333,96168,31928,7041,1210],
    }
    
    # Example: Solution 5 - Mean (window average)
    solution5 = {
        'name': 'Mean (window average)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [8773,8773,8773,8773,8773,8773,8773,8773,8778,9170,10405,12157,14987,15575,15662],
        'num_drops': [312196,312196,312196,312196,312196,312196,312196,312179,312020,291123,232520,132496,32899,7378,1342],
    }

    solution6 = {
        'name': 'Individual quarantine per event type',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [15676,15676,15676,15676,15676,15676,15676,15676,15676,15676,15676,15676,15676,15676,15684],
        'num_drops': [1024,1024,1024,1024,1024,1024,1024,1024,1024,1024,1024,1024,1021,1015,456],
    }
    
    return [solution1,solution2,solution3,solution4,solution5,solution6]


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


def plot_top_three(solutions):
    """Plot results and drops for the key solutions (includes solution 6)."""
    top_names = [
        'MAX (window max)',
        'EMA on max (α=0.1)',
        'Jump-and-Decay (α=0.1)',
        'Individual quarantine per event type',
    ]
    top_solutions = [s for s in solutions if s['name'] in top_names]
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:brown']
    markers = ['o', 's', '^', 'D']
    quarantine_times = top_solutions[0]['quarantine_times']
    x_pos = range(len(quarantine_times))

    # Results
    plt.figure(figsize=(12, 6))
    for idx, solution in enumerate(top_solutions):
        plt.plot(x_pos, solution['num_results'],
                 marker=markers[idx % len(markers)], linestyle='-', linewidth=2,
                 color=colors[idx % len(colors)], label=solution['name'], markersize=7)
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title('Results: Key Solutions Comparison', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Quarantine Time (s)', fontsize=11)
    plt.ylabel('Number of Results', fontsize=11)
    plt.legend(fontsize=9, loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("comparison_results_top3.png", dpi=300, bbox_inches='tight')
    print("✓ Saved: comparison_results_top3.png")

    # Drops
    plt.figure(figsize=(12, 6))
    for idx, solution in enumerate(top_solutions):
        plt.plot(x_pos, solution['num_drops'],
                 marker=markers[idx % len(markers)], linestyle='-', linewidth=2,
                 color=colors[idx % len(colors)], label=solution['name'], markersize=7)
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title('Drops: Key Solutions Comparison', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Quarantine Time (s)', fontsize=11)
    plt.ylabel('Number of Dropped Events', fontsize=11)
    plt.legend(fontsize=9, loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("comparison_drops_top3.png", dpi=300, bbox_inches='tight')
    print("✓ Saved: comparison_drops_top3.png")


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
    plot_top_three(solutions)
    
    print("\n" + "="*100)
    print("DONE! Check the generated PNG files.")
    print("="*100 + "\n")
