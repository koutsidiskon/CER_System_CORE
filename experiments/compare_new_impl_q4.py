"""
Compare new implementation vs Direct and Fixed-Time quarantine.
Usage:
  python compare_new_impl.py

Edit the DATA section to plug in your actual results.
"""
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# ==================== DATA (EDIT THESE) ====================
# Quarantine buffer sizes (seconds) used in your runs
QUARANTINE_TIMES = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]

# Data for multiple datasets
# Each dataset has metrics for three implementations: Direct, Fixed-Time, Individual per event
# Metrics: num_results, num_drops, exec_time, detection_delay
IMPLEMENTATIONS = ["Direct", "Fixed-Time", "jump_and_decay", "max", "Individual per event", "Sorted"]

# Color scheme for consistent coloring across all plots
COLORS = {
    "Direct": "#1f77b4",  
    "Fixed-Time": "#ff7f0e",  
    "jump_and_decay": "#2ca02c",  
    "max": "#d62728",  
    "Individual per event": "#9467bd",  
    "Sorted": "#8c564b",  
    "BoundedWaitTimePolicy": "#e377c2", 
    "NewFixedTimePolicy": "#7f7f7f",  
    "WaitFixedTimePolicy": "#bcbd22",  
}

DATASETS = {
    "Fires": {
        "Direct": {
            "num_results": [],
            "num_drops":   [],
            "exec_time":   [],
            "detection_delay": [],
        },
        "Fixed-Time": {
            "num_results": [],
            "num_drops":   [],
            "exec_time":   [],
            "detection_delay": [],
        },
        "jump_and_decay": {
            "num_results": [], 
            "num_drops": [], 
            "exec_time": [],
            "detection_delay": []
        },
        "max": {
            "num_results": [], 
            "num_drops": [], 
            "exec_time": [],
            "detection_delay": []
        },
        "Individual per event": {
            'num_results': [],
            'num_drops': [],
            "exec_time":   [],
            "detection_delay": [],
        },
        "Sorted": {
            "num_results": [],
            "num_drops": [],
            "exec_time": [],
            "detection_delay": [],
        },
    },
    "Aviation": {
        "Direct": {
            "num_results": [],
            "num_drops":   [],
            "exec_time":   [],
            "detection_delay": [],
        },
        "Fixed-Time": {
            "num_results": [],
            "num_drops":   [],
            "exec_time":   [],
            "detection_delay": [],
        },
        "jump_and_decay": {
            "num_results": [], 
            "num_drops": [], 
            "exec_time": [],
            "detection_delay": []
        },
        "max": {
            "num_results": [], 
            "num_drops": [], 
            "exec_time": [],
            "detection_delay": []
        },
        "Individual per event": {
            'num_results': [],
            'num_drops': [],
            "exec_time":   [],
            "detection_delay": [],
        },
        "Sorted": {
            "num_results": [],
            "num_drops": [],
            "exec_time": [],
            "detection_delay": [],
        },
    },
    "Crypto": {
        "Direct": {
            "num_results": [],
            "num_drops":   [],
            "exec_time":   [],
            "detection_delay": [],
        },
        "Fixed-Time": {
            "num_results": [],
            "num_drops":   [],
            "exec_time":   [],
            "detection_delay": [],
        },
        "jump_and_decay": {
            "num_results": [], 
            "num_drops": [], 
            "exec_time": [],
            "detection_delay": []
        },
        "max": {
            "num_results": [], 
            "num_drops": [], 
            "exec_time": [],
            "detection_delay": []
        },
        "Individual per event": {
            'num_results': [],
            'num_drops': [],
            "exec_time":   [],
            "detection_delay": [],
        },
        "Sorted": {
            "num_results": [],
            "num_drops": [],
            "exec_time": [],
            "detection_delay": [],
        },
    },
}
# ===========================================================

OUTPUT_DIR = "compared_with_original"


def _annotate_first_last_extremes(x_pos, all_solutions_values):
    """Annotate global min/max at first, middle, and last x positions across all solutions."""
    if not all_solutions_values or not x_pos:
        return
    
    def format_val(v):
        return f'{int(v)}' if v == int(v) else f'{v:.2f}'
    
    # Get values at first position (x=0)
    first_vals = [vals[0] for vals in all_solutions_values if len(vals) > 0]
    # Get values at middle position
    mid_idx = len(x_pos) // 2
    mid_vals = [vals[mid_idx] for vals in all_solutions_values if len(vals) > mid_idx]
    # Get values at last position (x=last)
    last_vals = [vals[-1] for vals in all_solutions_values if len(vals) > 0]
    
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


def build_tables():
    # Build tables for each dataset and derived summaries
    all_dataset_tables = {}
    for dataset_name, implementations in DATASETS.items():
        tables = {}
        # Core metrics tables
        for metric in ["num_results", "num_drops", "exec_time", "detection_delay"]:
            data = {"Quarantine Time (s)": QUARANTINE_TIMES}
            for impl_name in IMPLEMENTATIONS:
                data[impl_name] = implementations.get(impl_name, {}).get(metric, [])
            tables[metric] = pd.DataFrame(data)

        # Derived: percent of Sorted results
        if "Sorted" in tables["num_results"].columns:
            sorted_series = pd.Series(
                tables["num_results"]["Sorted"].values,
                index=range(len(QUARANTINE_TIMES))
            )
            pct_data = {"Quarantine Time (s)": QUARANTINE_TIMES}
            for impl in [i for i in IMPLEMENTATIONS if i != "Sorted"]:
                impl_series = pd.Series(
                    tables["num_results"][impl].values,
                    index=range(len(QUARANTINE_TIMES))
                )
                pct = (impl_series / sorted_series * 100).replace([np.inf, -np.inf], np.nan)
                pct_data[f"{impl} (% of Sorted)"] = pct.values.tolist()
            tables["sorted_pct"] = pd.DataFrame(pct_data)

        # Derived: combined jump (diff) and decay (% change) for all metrics per implementation
        jnd_data = {"Quarantine Time (s)": QUARANTINE_TIMES}
        for metric in ["num_results", "num_drops", "exec_time", "detection_delay"]:
            metric_df = tables[metric]
            for col in metric_df.columns[1:]:
                series = pd.Series(metric_df[col].values)
                jump = series.diff().fillna(0).values.tolist()
                with np.errstate(divide='ignore', invalid='ignore'):
                    decay = series.pct_change().replace([np.inf, -np.inf], np.nan).fillna(0).multiply(100).values.tolist()
                jnd_data[f"{metric} - {col} Jump"] = jump
                jnd_data[f"{metric} - {col} Decay (%)"] = decay
        tables["jump_and_decay"] = pd.DataFrame(jnd_data)

        # Derived: max per metric per implementation
        max_rows = []
        for metric in ["num_results", "num_drops", "exec_time", "detection_delay"]:
            row = {"Metric": metric}
            for impl in IMPLEMENTATIONS:
                vals = tables[metric][impl].values if impl in tables[metric] else []
                row[impl] = float(pd.Series(vals).max()) if len(vals) > 0 else float('nan')
            max_rows.append(row)
        tables["max"] = pd.DataFrame(max_rows)

        all_dataset_tables[dataset_name] = tables
    return all_dataset_tables


def save_excel(all_dataset_tables, path):
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for dataset_name, tables in all_dataset_tables.items():
            tables["num_results"].to_excel(writer, sheet_name=f"{dataset_name}_Results", index=False)
            tables["num_drops"].to_excel(writer, sheet_name=f"{dataset_name}_Drops", index=False)
            tables["exec_time"].to_excel(writer, sheet_name=f"{dataset_name}_ExecTime", index=False)
            tables["detection_delay"].to_excel(writer, sheet_name=f"{dataset_name}_DetDelay", index=False)
            tables["jump_and_decay"].to_excel(writer, sheet_name=f"{dataset_name}_JumpAndDecay", index=False)
            tables["max"].to_excel(writer, sheet_name=f"{dataset_name}_Max", index=False)
    print(f"✓ Saved Excel: {path}")


def save_excel_pct(all_dataset_tables, path):
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for dataset_name, tables in all_dataset_tables.items():
            if "sorted_pct" in tables:
                df = tables["sorted_pct"].copy()
                for col in df.columns[1:]:
                    df[col] = df[col].apply(lambda x: f"{x:.4f}" if pd.notna(x) else x)
                df.to_excel(writer, sheet_name=f"{dataset_name}", index=False)
    print(f"✓ Saved Excel: {path}")


def plot_lines(tables, metric, ylabel, filename, dataset_name):
    df = tables[metric]
    x = list(range(len(df["Quarantine Time (s)"])))
    plt.figure(figsize=(12, 6))
    series_names = [c for c in df.columns[1:] if c != "Sorted"]
    y_series = []
    for col in series_names:
        y_vals = df[col].values
        y_series.append(y_vals)
        color = COLORS.get(col, None)
        plt.plot(x, y_vals, marker="o", linewidth=2, label=col, markersize=6, color=color)

    _annotate_first_last_extremes(x, y_series)
    plt.xticks(x, df["Quarantine Time (s)"], rotation=45, fontsize=8)
    plt.xlabel("Quarantine Time (s)", fontsize=11)
    plt.ylabel(ylabel, fontsize=11)
    plt.title(f"{ylabel} vs Quarantine Time - {dataset_name}", fontsize=13, fontweight='bold', pad=12)
    if metric == "exec_time":
        plt.ylim(bottom=0)
    plt.grid(True)
    plt.legend(fontsize=9, loc='best')
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {out_path}")


def plot_drops_enhanced(tables, dataset_name):
    """Create enhanced drops plot with better visibility for differences"""
    df = tables["num_drops"]
    x = list(range(len(df["Quarantine Time (s)"])))
    
    # Single plot with log scale for better visibility of differences
    plt.figure(figsize=(12, 6))
    series_names = [c for c in df.columns[1:] if c != "Sorted"]
    y_series = []
    for col in series_names:
        plotted_vals = [v + 1 for v in df[col]]
        y_series.append(plotted_vals)
        color = COLORS.get(col, None)
        plt.plot(x, plotted_vals, marker="o", linewidth=2, label=col, markersize=6, color=color)

    _annotate_first_last_extremes(x, [df[col].values for col in series_names])
    plt.xticks(x, df["Quarantine Time (s)"], rotation=45, fontsize=8)
    plt.xlabel("Quarantine Time (s)", fontsize=11)
    plt.ylabel("Dropped Events (log scale, +1)", fontsize=11)
    plt.title(f"Dropped Events vs Quarantine Time (Log Scale) - {dataset_name}", fontsize=13, fontweight='bold', pad=12)
    plt.yscale('log')
    plt.grid(True, which="both")
    plt.legend(fontsize=9, loc='best')
    plt.tight_layout()
    
    safe_name = dataset_name.lower().replace(" ", "_")
    out_path = os.path.join(OUTPUT_DIR, f"compare_{safe_name}_drops_enhanced.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {out_path}")


def plot_lines_top3(tables, metric, ylabel, filename, dataset_name):
    """Plot top 3 quarantine implementations (jump_and_decay, max, Individual per event)"""
    df = tables[metric]
    # Filter out Direct and Fixed-Time columns
    cols_to_plot = [col for col in df.columns[1:] if col not in ["Direct", "Fixed-Time", "Sorted"]]
    x = list(range(len(df["Quarantine Time (s)"])))
    plt.figure(figsize=(12, 6))
    series_names = cols_to_plot
    y_series = []
    for col in series_names:
        y_vals = df[col].values
        y_series.append(y_vals)
        color = COLORS.get(col, None)
        plt.plot(x, y_vals, marker="o", linewidth=2, label=col, markersize=6, color=color)

    _annotate_first_last_extremes(x, y_series)
    plt.xticks(x, df["Quarantine Time (s)"], rotation=45, fontsize=8)
    plt.xlabel("Quarantine Time (s)", fontsize=11)
    plt.ylabel(ylabel, fontsize=11)
    plt.title(f"{ylabel} vs Quarantine Time (Top 3) - {dataset_name}", fontsize=13, fontweight='bold', pad=12)
    if metric == "exec_time":
        plt.ylim(bottom=0)
    plt.grid(True)
    plt.legend(fontsize=9, loc='best')
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {out_path}")


def plot_drops_enhanced_top3(tables, dataset_name):
    """Create enhanced drops plot for top 3 quarantine implementations"""
    df = tables["num_drops"]
    # Filter out Direct and Fixed-Time columns
    cols_to_plot = [col for col in df.columns[1:] if col not in ["Direct", "Fixed-Time", "Sorted"]]
    x = list(range(len(df["Quarantine Time (s)"])))
    
    # Single plot with log scale for better visibility of differences
    plt.figure(figsize=(12, 6))
    series_names = cols_to_plot
    y_series = []
    for col in series_names:
        plotted_vals = [v + 1 for v in df[col]]
        y_series.append(plotted_vals)
        color = COLORS.get(col, None)
        plt.plot(x, plotted_vals, marker="o", linewidth=2, label=col, markersize=6, color=color)

    _annotate_first_last_extremes(x, [df[col].values for col in series_names])
    plt.xticks(x, df["Quarantine Time (s)"], rotation=45, fontsize=8)
    plt.xlabel("Quarantine Time (s)", fontsize=11)
    plt.ylabel("Dropped Events (log scale, +1)", fontsize=11)
    plt.title(f"Dropped Events vs Quarantine Time (Log Scale, Top 3) - {dataset_name}", fontsize=13, fontweight='bold', pad=12)
    plt.yscale('log')
    plt.grid(True, which="both")
    plt.legend(fontsize=9, loc='best')
    plt.tight_layout()
    
    safe_name = dataset_name.lower().replace(" ", "_")
    out_path = os.path.join(OUTPUT_DIR, f"compare_{safe_name}_drops_enhanced_top3.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {out_path}")


def plot_all(all_dataset_tables):
    for dataset_name, tables in all_dataset_tables.items():
        safe_name = dataset_name.lower().replace(" ", "_")
        # Original plots with all implementations
        plot_lines(tables, "num_results", "Number of Results", f"compare_{safe_name}_results.png", dataset_name)
        plot_drops_enhanced(tables, dataset_name)
        plot_lines(tables, "exec_time", "Execution Time (s)", f"compare_{safe_name}_exec_time.png", dataset_name)
        plot_lines(tables, "detection_delay", "Detection Delay (s)", f"compare_{safe_name}_detection_delay.png", dataset_name)
        
        # Top 3 quarantine implementations plots
        plot_lines_top3(tables, "num_results", "Number of Results", f"compare_{safe_name}_results_top3.png", dataset_name)
        plot_drops_enhanced_top3(tables, dataset_name)
        plot_lines_top3(tables, "exec_time", "Execution Time (s)", f"compare_{safe_name}_exec_time_top3.png", dataset_name)
        plot_lines_top3(tables, "detection_delay", "Detection Delay (s)", f"compare_{safe_name}_detection_delay_top3.png", dataset_name)


def print_tables(all_dataset_tables):
    for dataset_name, tables in all_dataset_tables.items():
        print(f"\n{'='*80}")
        print(f"DATASET: {dataset_name}")
        print('='*80)
        print("\n=== Results ===")
        print(tables["num_results"].to_string(index=False))
        print("\n=== Drops ===")
        print(tables["num_drops"].to_string(index=False))
        print("\n=== Execution Time (s) ===")
        print(tables["exec_time"].to_string(index=False))
        print("\n=== Detection Delay (s) ===")
        print(tables["detection_delay"].to_string(index=False))
        print("\n=== Jump + Decay (num_results diff and % change) ===")
        print(tables["jump_and_decay"].to_string(index=False))
        print("\n=== Max values across quarantine times ===")
        print(tables["max"].to_string(index=False))
        if "sorted_pct" in tables:
            print("\n=== % Results vs Sorted (num_results) ===")
            print(tables["sorted_pct"].to_string(index=False))


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_dataset_tables = build_tables()
    print_tables(all_dataset_tables)
    excel_path = os.path.join(OUTPUT_DIR, "compare_new_impl.xlsx")
    save_excel(all_dataset_tables, excel_path)
    excel_pct_path = os.path.join(OUTPUT_DIR, "compare_new_impl_sorted_pct.xlsx")
    save_excel_pct(all_dataset_tables, excel_pct_path)
    plot_all(all_dataset_tables)
    print("\n" + "="*80)
    print("Done! Update the DATASETS section with your real measurements if needed.")
    print("="*80)
