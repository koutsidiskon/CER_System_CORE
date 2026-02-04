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

# Color scheme for consistent coloring across all plots
COLORS = {
    "MAX (window max)": "#d62728",  
    "EMA on max (α=0.1)": "#e377c2",  
    "Jump-and-Decay (α=0.1)": "#2ca02c",  
    "p99 + EMA (α=0.1)": "#7f7f7f",  
    "Mean (window average)": "#bcbd22", 
    "Individual quarantine per event type": "#9467bd", 
}

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

def _annotate_first_last(x_pos, solutions_data, metric_key):
    """Annotate first (x=0) and last (x=-1) points for all solutions with min/max highlight."""
    x_pos = list(x_pos)
    if not x_pos:
        return
    
    # Get values at first and last positions
    first_vals = [(sol['name'], sol[metric_key][0], sol.get('_color', 'black')) for sol in solutions_data]
    last_vals = [(sol['name'], sol[metric_key][-1], sol.get('_color', 'black')) for sol in solutions_data]
    
    # Find min and max at first position
    first_min = min(first_vals, key=lambda x: x[1])
    first_max = max(first_vals, key=lambda x: x[1])
    
    # Annotate first position
    offset = 0
    for name, val, color in first_vals:
        label = f'{val:.2f}'
        if (name, val, color) == first_min:
            label = f'Min: {val:.2f}'
        elif (name, val, color) == first_max:
            label = f'Max: {val:.2f}'
        plt.annotate(label, (x_pos[0], val), textcoords="offset points", xytext=(0, offset),
                    ha='center', va='bottom' if offset >= 0 else 'top', fontsize=7, color=color, fontweight='bold')
        offset += 8
    
    # Find min and max at last position
    last_min = min(last_vals, key=lambda x: x[1])
    last_max = max(last_vals, key=lambda x: x[1])
    
    # Annotate last position
    offset = 0
    for name, val, color in last_vals:
        label = f'{val:.2f}'
        if (name, val, color) == last_min:
            label = f'Min: {val:.2f}'
        elif (name, val, color) == last_max:
            label = f'Max: {val:.2f}'
        plt.annotate(label, (x_pos[-1], val), textcoords="offset points", xytext=(0, offset),
                    ha='center', va='bottom' if offset >= 0 else 'top', fontsize=7, color=color, fontweight='bold')
        offset += 8

def load_solution_data():
    """
    Define your different solutions here.
    Each solution should have data for different quarantine times.
    """
    
    # Example: Solution 1 - MAX (window max)
    solution1 = {
        'name': 'MAX (window max)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200], 
        'num_drops': [131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 112, 55, 34, 24], 
        'exec_time': [10.46, 10.81, 10.53, 10.98, 10.47, 10.91, 10.54, 11.04, 11.24, 10.66, 11.78, 11.46, 11.05, 11.51, 10.92],
        'detection_delay': [215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273],
    }
    
    # Example: Solution 2 - EMA on max (α=0.1)
    solution2 = {
        'name': 'EMA on max (α=0.1)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200],
        'num_drops': [133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 112, 56, 34, 24],
        'exec_time': [8.90, 8.86, 8.87, 8.87, 8.86, 8.85, 8.84, 8.82, 8.98, 8.76, 8.74, 8.96, 8.89, 9.00, 9.00],
        'detection_delay': [215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273],
    }
    
    # Example: Solution 3 - Jump-and-Decay (α=0.1)
    solution3 = {
        'name': 'Jump-and-Decay (α=0.1)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        "num_results": [2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200], 
        "num_drops": [130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 111, 55, 34, 24], 
        "exec_time": [9.47, 9.37, 10.04, 9.43, 9.37, 9.38, 9.37, 9.45, 9.41, 9.40, 9.40, 9.41, 9.39, 9.41, 9.48],
        "detection_delay": [215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273]
    }
    
    # Example: Solution 4 - p99 + EMA (α=0.1)
    solution4 = {
        'name': 'p99 + EMA (α=0.1)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200],
        'num_drops': [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 141, 67, 34, 24],
        'exec_time': [12.78, 12.74, 12.70, 12.69, 13.02, 12.88, 13.02, 13.29, 13.14, 14.22, 13.01, 12.72, 12.76, 12.74, 12.78],
        'detection_delay': [215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273],
    }
    
    # Example: Solution 5 - Mean (window average)
    solution5 = {
        'name': 'Mean (window average)',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [2199, 2199, 2199, 2199, 2199, 2199, 2199, 2199, 2199, 2200, 2200, 2200, 2200, 2200, 2200],
        'num_drops': [1659, 1659, 1659, 1659, 1659, 1659, 1659, 1659, 1659, 1534, 472, 175, 75, 34, 24],
        'exec_time': [9.60, 9.20, 9.35, 9.19, 9.16, 9.21, 9.17, 9.55, 9.34, 9.58, 9.60, 9.34, 9.73, 9.19, 9.18],
        'detection_delay': [215.03411, 215.03411, 215.03411, 215.03411, 215.03411, 215.03411, 215.03411, 215.03411, 215.03411, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273],
    }

    solution6 = {
        'name': 'Individual quarantine per event type',
        'quarantine_times': [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384],
        'num_results': [2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200],
        'num_drops': [108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 88, 52, 33, 24],
        "exec_time":   [9.88, 9.92, 9.37, 9.94, 9.43, 9.81, 9.92, 9.26, 10.01, 9.27, 9.93, 9.96, 8.98, 9.76, 9.27],
        "detection_delay": [215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273],
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
    markers = ['o', 's', '^', 'D', 'v', 'p']
    
    # Attach colors to solutions for annotation
    for idx, sol in enumerate(solutions):
        sol['_color'] = COLORS.get(sol['name'], 'tab:gray')
    
    # Get quarantine times from the first solution
    quarantine_times = solutions[0]['quarantine_times']
    
    # ======= Results Found Comparison =======
    plt.figure(figsize=(15, 8))
    x_pos = list(range(len(quarantine_times)))
    
    all_results = []
    for idx, solution in enumerate(solutions):
        color = COLORS.get(solution['name'], 'tab:gray')
        plt.plot(x_pos, solution['num_results'], 
                marker=markers[idx], linestyle='-', linewidth=2,
                color=color, label=solution['name'], markersize=8)
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
        color = COLORS.get(solution['name'], 'tab:gray')
        plt.plot(x_pos, solution['num_drops'], 
                marker=markers[idx], linestyle='-', linewidth=2,
                color=color, label=solution['name'], markersize=8)
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
        color = COLORS.get(solution['name'], 'tab:gray')
        plt.plot(x_pos, solution['exec_time'], 
                marker=markers[idx], linestyle='-', linewidth=2,
                color=color, label=solution['name'], markersize=8)
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
        color = COLORS.get(solution['name'], 'tab:gray')
        plt.plot(x_pos, solution['detection_delay'], 
                marker=markers[idx], linestyle='-', linewidth=2,
                color=color, label=solution['name'], markersize=8)
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
        color = COLORS.get(solution['name'], 'tab:gray')
        axes[0].plot(x_pos, solution['num_results'], 
                       marker=markers[idx], linestyle='-', linewidth=2,
                       color=color, label=solution['name'], markersize=7)
    
    axes[0].set_xticks(x_pos)
    axes[0].set_xticklabels([str(t) for t in quarantine_times], fontsize=8, rotation=45)
    axes[0].set_title('Complex Events Found', fontweight='bold', fontsize=12)
    axes[0].set_xlabel('Quarantine Time (s)', fontsize=11)
    axes[0].set_ylabel('Number of Results', fontsize=11)
    axes[0].legend(fontsize=9, loc='best')
    axes[0].grid(True)
    
    # Drops
    for idx, solution in enumerate(solutions):
        color = COLORS.get(solution['name'], 'tab:gray')
        axes[1].plot(x_pos, solution['num_drops'], 
                       marker=markers[idx], linestyle='-', linewidth=2,
                       color=color, label=solution['name'], markersize=7)
    
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
    markers = ['o', 's', '^', 'D']
    quarantine_times = top_solutions[0]['quarantine_times']
    x_pos = range(len(quarantine_times))

    # Results
    plt.figure(figsize=(12, 6))
    x_pos = list(range(len(quarantine_times)))
    all_results = []
    for idx, solution in enumerate(top_solutions):
        color = COLORS.get(solution['name'], 'tab:gray')
        plt.plot(x_pos, solution['num_results'],
                 marker=markers[idx % len(markers)], linestyle='-', linewidth=2,
                 color=color, label=solution['name'], markersize=7)
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
        color = COLORS.get(solution['name'], 'tab:gray')
        plt.plot(x_pos, solution['num_drops'],
                 marker=markers[idx % len(markers)], linestyle='-', linewidth=2,
                 color=color, label=solution['name'], markersize=7)
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
        color = COLORS.get(solution['name'], 'tab:gray')
        plt.plot(x_pos, solution['exec_time'],
                 marker=markers[idx % len(markers)], linestyle='-', linewidth=2,
                 color=color, label=solution['name'], markersize=7)
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
        color = COLORS.get(solution['name'], 'tab:gray')
        plt.plot(x_pos, solution['detection_delay'],
                 marker=markers[idx % len(markers)], linestyle='-', linewidth=2,
                 color=color, label=solution['name'], markersize=7)
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
