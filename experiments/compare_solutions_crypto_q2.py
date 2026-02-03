"""
Compare multiple solutions with pandas DataFrames and multi-line plots
Usage:
  python compare_solutions.py
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

OUTPUT_DIR = "comparison"

def _annotate_first_last_extremes(x_pos, all_solutions_values):
    """Annotate global min/max at first, middle, and last x positions across all solutions."""
    if not all_solutions_values or not x_pos:
        return
    
    def format_val(v):
        return f'{int(v)}' if v == int(v) else f'{v:.2f}'
    
    # Get values at first position (x=0)
    first_vals = [vals[0] for vals in all_solutions_values if vals]
    # Get values at middle position
    mid_idx = len(x_pos) // 2
    mid_vals = [vals[mid_idx] for vals in all_solutions_values if vals]
    # Get values at last position (x=last)
    last_vals = [vals[-1] for vals in all_solutions_values if vals]
    
    first_x = x_pos[0]
    mid_x = x_pos[mid_idx]
    last_x = x_pos[-1]
    
    if first_vals:
        global_min_first = min(first_vals)
        global_max_first = max(first_vals)
        plt.annotate(format_val(global_max_first), (first_x, global_max_first),
                    textcoords="offset points", xytext=(0, 8), ha='center', va='bottom',
                    fontsize=8, fontweight='bold', color='black')
        if global_min_first != global_max_first:
            plt.annotate(format_val(global_min_first), (first_x, global_min_first),
                        textcoords="offset points", xytext=(0, -12), ha='center', va='top',
                        fontsize=8, fontweight='bold', color='black')
    
    if mid_vals:
        global_min_mid = min(mid_vals)
        global_max_mid = max(mid_vals)
        plt.annotate(format_val(global_max_mid), (mid_x, global_max_mid),
                    textcoords="offset points", xytext=(0, 8), ha='center', va='bottom',
                    fontsize=8, fontweight='bold', color='black')
        if global_min_mid != global_max_mid:
            plt.annotate(format_val(global_min_mid), (mid_x, global_min_mid),
                        textcoords="offset points", xytext=(0, -12), ha='center', va='top',
                        fontsize=8, fontweight='bold', color='black')
    
    if last_vals:
        global_min_last = min(last_vals)
        global_max_last = max(last_vals)
        plt.annotate(format_val(global_max_last), (last_x, global_max_last),
                    textcoords="offset points", xytext=(0, 8), ha='center', va='bottom',
                    fontsize=8, fontweight='bold', color='black')
        if global_min_last != global_max_last:
            plt.annotate(format_val(global_min_last), (last_x, global_min_last),
                        textcoords="offset points", xytext=(0, -12), ha='center', va='top',
                        fontsize=8, fontweight='bold', color='black')

def load_solution_data():
    """
    Define your different solutions here.
    Each solution should have data for different quarantine times.
    """
    
    # Example: Solution 1 - MAX (window max)
    solution1 = {
        'name': 'MAX (window max)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [13599, 13599, 13599, 13599, 13599, 13599, 13599, 13599, 13599, 13599, 13812, 14485, 15764, 16194, 16307],
        'num_drops': [123070, 123070, 123070, 123070, 123070, 123070, 123070, 123070, 123070, 123070, 114730, 82589, 27918, 6739, 1210],
        'exec_time': [16.63, 16.27, 16.59, 16.46, 16.34, 16.43, 17.07, 16.92, 16.63, 16.67, 16.44, 17.34, 17.38, 17.15, 17.11],
        'detection_delay': [1266.55239, 1266.55239, 1266.55239, 1266.55239, 1266.55239, 1266.55239, 1266.55239, 1266.55239, 1266.55239, 1266.55239, 1277.96880, 1491.44018, 2454.40700, 3079.38780, 3301.96081]
    }
    
    # Example: Solution 2 - EMA on max (α=0.1)
    solution2 = {
        'name': 'EMA on max (α=0.1)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [13560, 13560, 13560, 13560, 13560, 13560, 13560, 13560, 13560, 13560, 13810, 14386, 15759, 16231, 16307],
        'num_drops': [124751, 124751, 124751, 124751, 124751, 124751, 124751, 124751, 124751, 124748, 113954, 85670, 28117, 5533, 1210],
        'exec_time': [15.16, 15.21, 15.26, 15.47, 15.80, 15.49, 15.16, 15.14, 15.40, 15.34, 15.25, 15.57, 16.20, 15.81, 16.23],
        'detection_delay': [1221.80715, 1221.80715, 1221.80715, 1221.80715, 1221.80715, 1221.80715, 1221.80715, 1221.80715, 1221.80715, 1221.80715, 1239.08711, 1463.41096, 2445.39761, 3142.47637, 3301.96081],
    }
    
    # Example: Solution 3 - Jump-and-Decay (α=0.1)
    solution3 = {
        'name': 'Jump-and-Decay (α=0.1)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
            "num_results": [13655, 13655, 13655, 13655, 13655, 13655, 13655, 13655, 13655, 13655, 13878, 14485, 15764, 16231, 16307], 
            "num_drops": [119379, 119379, 119379, 119379, 119379, 119379, 119379, 119379, 119379, 119379, 110818, 82589, 27918, 5533, 1210], 
            "exec_time": [15.12, 15.11, 15.11, 15.71, 17.35, 15.91, 16.12, 15.83, 15.71, 15.77, 15.79, 15.85, 16.06, 16.17, 16.29],
            "detection_delay": [1270.20469, 1270.20469, 1270.20469, 1270.20469, 1270.20469, 1270.20469, 1270.20469, 1270.20469, 1270.20469, 1270.20469, 1283.22828, 1491.44018, 2454.40700, 3142.47637, 3301.96081]
    }
    
    # Example: Solution 4 - p99 + EMA (α=0.1)
    solution4 = {
        'name': 'p99 + EMA (α=0.1)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [12267, 12267, 12267, 12267, 12267, 12267, 12267, 12267, 12271, 12295, 12870, 14172, 15672, 16188, 16307],
        'num_drops': [189148, 189148, 189148, 189148, 189148, 189148, 189148, 189148, 189148, 188163, 162834, 96175, 31928, 7041, 1210],
        'exec_time': [40.21, 39.07, 38.82, 39.87, 39.58, 40.66, 40.48, 40.32, 39.89, 38.62, 39.11, 40.69, 41.95, 42.76, 43.60],
        'detection_delay': [895.60748, 895.60748, 895.60748, 895.60748, 895.60748, 895.60748, 895.60748, 895.60748, 895.60748, 897.93991, 1031.00319, 1343.20710, 2277.95680, 3064.05856, 3301.96081],
    }
    
    # Example: Solution 5 - Mean (window average)
    solution5 = {
        'name': 'Mean (window average)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [10231, 10231, 10231, 10231, 10231, 10231, 10231, 10231, 10238, 10616, 11602, 13322, 15646, 16181, 16305],
        'num_drops': [312196, 312196, 312196, 312196, 312196, 312196, 312196, 312179, 312020, 291123, 232520, 132496, 32899, 7378, 1342],
        'exec_time': [14.02, 14.13, 14.27, 14.13, 14.15, 14.73, 14.35, 14.41, 14.29, 14.86, 14.38, 14.94, 15.16, 15.18, 15.81],
        'detection_delay': [669.75916, 669.75916, 669.75916, 669.75916, 669.75916, 669.75916, 669.75916, 669.75916, 669.69135, 695.37180, 781.95363, 1031.15523, 2260.46363, 3064.91348, 3302.17326],
    }

    solution6 = {
        'name': 'Individual quarantine per event type',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [16308, 16308, 16308, 16308, 16308, 16308, 16308, 16308, 16308, 16308, 16308, 16308, 16308, 16308, 16326],
        'num_drops': [1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1021, 1015, 456],
        "exec_time":   [16.54, 16.88, 16.95, 17.03, 16.79, 16.76, 16.44, 16.47, 16.67, 16.49, 16.59, 16.50, 16.48, 16.53, 16.41],
        "detection_delay": [3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3314.30651],
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
    x_pos = list(range(len(quarantine_times)))
    
    all_results = []
    for idx, solution in enumerate(solutions):
        plt.plot(x_pos, solution['num_results'], 
                marker=markers[idx], linestyle='-', linewidth=2,
                color=colors[idx], label=solution['name'], markersize=8)
        all_results.append(solution['num_results'])
    
    _annotate_first_last_extremes(x_pos, all_results)
    
    # Set x-ticks to show the actual quarantine times
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title('Complex Events Found Comparison Across Solutions', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Quarantine Time (s)', fontsize=12)
    plt.ylabel('Number of Results', fontsize=12)
    plt.legend(fontsize=10, loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "comparison_results.png"), dpi=300, bbox_inches='tight')
    print("✓ Saved: comparison_results.png")
    
    # ======= Drops Comparison (IMPORTANT!) =======
    plt.figure(figsize=(15, 8))
    x_pos = list(range(len(quarantine_times)))
    
    all_drops = []
    for idx, solution in enumerate(solutions):
        plt.plot(x_pos, solution['num_drops'], 
                marker=markers[idx], linestyle='-', linewidth=2,
                color=colors[idx], label=solution['name'], markersize=8)
        all_drops.append(solution['num_drops'])
    
    _annotate_first_last_extremes(x_pos, all_drops)
    
    # Set x-ticks to show the actual quarantine times
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title('Dropped Events Comparison Across Solutions', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Quarantine Time (s)', fontsize=12)
    plt.ylabel('Number of Dropped Events', fontsize=12)
    plt.legend(fontsize=10, loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "comparison_drops.png"), dpi=300, bbox_inches='tight')
    print("✓ Saved: comparison_drops.png")
    
    # ======= Execution Time Comparison =======
    plt.figure(figsize=(15, 8))
    x_pos = list(range(len(quarantine_times)))
    
    all_exec_time = []
    for idx, solution in enumerate(solutions):
        plt.plot(x_pos, solution['exec_time'], 
                marker=markers[idx], linestyle='-', linewidth=2,
                color=colors[idx], label=solution['name'], markersize=8)
        all_exec_time.append(solution['exec_time'])
    
    _annotate_first_last_extremes(x_pos, all_exec_time)
    
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title('Execution Time Comparison Across Solutions', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Quarantine Time (s)', fontsize=12)
    plt.ylabel('Execution Time (s)', fontsize=12)
    plt.ylim(bottom=0)
    plt.legend(fontsize=10, loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "comparison_exec_time.png"), dpi=300, bbox_inches='tight')
    print("✓ Saved: comparison_exec_time.png")
    
    # ======= Detection Delay Comparison =======
    plt.figure(figsize=(15, 8))
    x_pos = list(range(len(quarantine_times)))
    
    all_detection_delay = []
    for idx, solution in enumerate(solutions):
        plt.plot(x_pos, solution['detection_delay'], 
                marker=markers[idx], linestyle='-', linewidth=2,
                color=colors[idx], label=solution['name'], markersize=8)
        all_detection_delay.append(solution['detection_delay'])
    
    _annotate_first_last_extremes(x_pos, all_detection_delay)
    
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title('Detection Delay Comparison Across Solutions', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Quarantine Time (s)', fontsize=12)
    plt.ylabel('Detection Delay (s)', fontsize=12)
    plt.legend(fontsize=10, loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "comparison_detection_delay.png"), dpi=300, bbox_inches='tight')
    print("✓ Saved: comparison_detection_delay.png")
    
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
    plt.savefig(os.path.join(OUTPUT_DIR, "comparison_dashboard.png"), dpi=300, bbox_inches='tight')
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
    x_pos = list(range(len(quarantine_times)))
    all_results = []
    for idx, solution in enumerate(top_solutions):
        plt.plot(x_pos, solution['num_results'],
                 marker=markers[idx % len(markers)], linestyle='-', linewidth=2,
                 color=colors[idx % len(colors)], label=solution['name'], markersize=7)
        all_results.append(solution['num_results'])
    _annotate_first_last_extremes(x_pos, all_results)
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title('Results: Key Solutions Comparison', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Quarantine Time (s)', fontsize=11)
    plt.ylabel('Number of Results', fontsize=11)
    plt.legend(fontsize=9, loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "comparison_results_top3.png"), dpi=300, bbox_inches='tight')
    print("✓ Saved: comparison_results_top3.png")

    # Drops
    plt.figure(figsize=(12, 6))
    all_drops = []
    for idx, solution in enumerate(top_solutions):
        plt.plot(x_pos, solution['num_drops'],
                 marker=markers[idx % len(markers)], linestyle='-', linewidth=2,
                 color=colors[idx % len(colors)], label=solution['name'], markersize=7)
        all_drops.append(solution['num_drops'])
    _annotate_first_last_extremes(x_pos, all_drops)
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title('Drops: Key Solutions Comparison', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Quarantine Time (s)', fontsize=11)
    plt.ylabel('Number of Dropped Events', fontsize=11)
    plt.legend(fontsize=9, loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "comparison_drops_top3.png"), dpi=300, bbox_inches='tight')
    print("✓ Saved: comparison_drops_top3.png")

    # Execution Time
    plt.figure(figsize=(12, 6))
    all_exec_time = []
    for idx, solution in enumerate(top_solutions):
        plt.plot(x_pos, solution['exec_time'],
                 marker=markers[idx % len(markers)], linestyle='-', linewidth=2,
                 color=colors[idx % len(colors)], label=solution['name'], markersize=7)
        all_exec_time.append(solution['exec_time'])
    _annotate_first_last_extremes(x_pos, all_exec_time)
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title('Execution Time: Key Solutions Comparison', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Quarantine Time (s)', fontsize=11)
    plt.ylabel('Execution Time (s)', fontsize=11)
    plt.ylim(bottom=0)
    plt.legend(fontsize=9, loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "comparison_exec_time_top3.png"), dpi=300, bbox_inches='tight')
    print("✓ Saved: comparison_exec_time_top3.png")

    # Detection Delay
    plt.figure(figsize=(12, 6))
    all_detection_delay = []
    for idx, solution in enumerate(top_solutions):
        plt.plot(x_pos, solution['detection_delay'],
                 marker=markers[idx % len(markers)], linestyle='-', linewidth=2,
                 color=colors[idx % len(colors)], label=solution['name'], markersize=7)
        all_detection_delay.append(solution['detection_delay'])
    _annotate_first_last_extremes(x_pos, all_detection_delay)
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title('Detection Delay: Key Solutions Comparison', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Quarantine Time (s)', fontsize=11)
    plt.ylabel('Detection Delay (s)', fontsize=11)
    plt.legend(fontsize=9, loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "comparison_detection_delay_top3.png"), dpi=300, bbox_inches='tight')
    print("✓ Saved: comparison_detection_delay_top3.png")


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
    os.makedirs(OUTPUT_DIR, exist_ok=True)
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
