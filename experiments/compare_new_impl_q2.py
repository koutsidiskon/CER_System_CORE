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
IMPLEMENTATIONS = ["Direct", "Fixed-Time", "Individual per event"]

DATASETS = {
    "Fires": {
        "Direct": {
            "num_results": [1043,1043,1043,1043,1043,1043,1043,1043,1043,1043,1043,1043,1043,1043,1043],
            "num_drops":   [79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434],
            "exec_time":   [9.89, 9.69, 9.75, 9.80, 9.90, 9.74, 9.82, 9.75, 9.73, 9.75, 9.76, 9.80, 9.45, 9.48, 9.48],
            "detection_delay": [214.63087, 214.63087, 214.63087, 214.63087, 214.63087, 214.63087, 214.63087, 214.63087, 214.63087, 214.63087, 214.63087, 214.63087, 214.63087, 214.63087, 214.63087],
        },
        "Fixed-Time": {
            "num_results": [2058, 2058, 2058, 2058, 2058, 2058, 2114, 2153, 2186, 2199, 2200, 2200, 2200, 2200, 2200],
            "num_drops":   [14524, 14519, 14501, 14459, 14396, 14241, 11085, 8213, 4512, 1574, 472, 175, 75, 34, 24],
            "exec_time":   [10.49, 10.32, 10.33, 10.64, 10.31, 10.24, 10.35, 10.99, 10.58, 10.77, 10.38, 11.09, 10.42, 11.12, 10.37],
            "detection_delay": [213.67347, 213.67347, 213.67347, 213.67347, 213.67347, 213.67347, 213.54778, 214.19415, 214.55627, 215.00682, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273],
        },
        "jump_and_decay": {
            "num_results": [2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200], 
            "num_drops": [130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 111, 55, 34, 24], 
            "exec_time": [9.47, 9.37, 10.04, 9.43, 9.37, 9.38, 9.37, 9.45, 9.41, 9.40, 9.40, 9.41, 9.39, 9.41, 9.48],
            "detection_delay": [215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273]
        },
        "max": {
            "num_results": [2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200], 
            "num_drops": [131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 112, 55, 34, 24], 
            "exec_time": [10.46, 10.81, 10.53, 10.98, 10.47, 10.91, 10.54, 11.04, 11.24, 10.66, 11.78, 11.46, 11.05, 11.51, 10.92],
            "detection_delay": [215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273]
        },
        "Individual per event": {
            'num_results': [2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200, 2200],
            'num_drops': [108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 88, 52, 33, 24],
            "exec_time":   [9.88, 9.92, 9.37, 9.94, 9.43, 9.81, 9.92, 9.26, 10.01, 9.27, 9.93, 9.96, 8.98, 9.76, 9.27],
            "detection_delay": [215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273, 215.07273],
        },
    },
    "Aviation": {
        "Direct": {
            "num_results": [336,336,336,336,336,336,336,336,336,336,336,336,336,336,336],
            "num_drops":   [336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293],
            "exec_time":   [12.40, 12.14, 12.47, 12.12, 12.11, 12.70, 12.21, 12.41, 12.32, 12.42, 12.06, 12.45, 12.17, 12.12, 12.72],
            "detection_delay": [0.53571, 0.53572, 0.53571, 0.53571, 0.53571, 0.53571, 0.53571, 0.53571, 0.53571, 0.53571, 0.53571, 0.53571, 0.53571, 0.53571, 0.53571],
        },
        "Fixed-Time": {
            "num_results": [356, 356, 356, 356, 356, 356, 396, 433, 510, 568, 619, 637, 646, 648, 648],
            "num_drops":   [313826, 313826, 313826, 313826, 313826, 313826, 274143, 215379, 126483, 60387, 21780, 7209, 2342, 631, 140],
            "exec_time":   [12.59, 13.14, 13.23, 12.64, 13.31, 13.01, 12.81, 12.81, 13.25, 12.72, 13.16, 12.86, 12.63, 12.99, 12.67],
            "detection_delay": [5.89888, 5.89888, 5.89888, 5.89888, 5.89888, 5.89888, 45.61761, 91.03926, 279.88235, 548.76761, 959.90307, 1192.74725, 1396.16099, 1479.53704, 1479.53704],
        },
        "jump_and_decay": {
            "num_results": [648, 648, 648, 648, 648, 648, 648, 648, 648, 648, 648, 648, 648, 648, 648], 
            "num_drops": [147, 147, 147, 147, 147, 147, 147, 141, 141, 135, 135, 117, 103, 74, 58], 
            "exec_time": [11.86, 12.29, 11.66, 11.67, 11.68, 12.18, 11.85, 11.81, 11.97, 11.94, 11.31, 11.67, 11.61, 11.56, 11.51],
            "detection_delay": [1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704]
        },
        "max": {
            "num_results": [648, 648, 648, 648, 648, 648, 648, 648, 648, 648, 648, 648, 648, 648, 648], 
            "num_drops": [148, 148, 148, 148, 148, 148, 148, 142, 142, 136, 136, 118, 104, 77, 58], 
            "exec_time": [12.92, 12.93, 12.22, 12.28, 12.36, 12.27, 12.28, 12.37, 12.12, 12.07, 12.06, 13.49, 12.48, 12.05, 12.02],
            "detection_delay": [1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704]
        },
        "Individual per event": {
            'num_results': [648, 648, 648, 648, 648, 648, 648, 648, 648, 648, 648, 648, 648, 648, 648],
            'num_drops': [33, 33, 33, 33, 33, 33, 33, 29, 29, 17, 17, 17, 17, 17, 17],
            "exec_time":   [11.56, 11.75, 12.20, 11.84, 11.76, 11.56, 11.71, 12.20, 11.41, 12.35, 11.83, 11.31, 11.74, 11.25, 11.57],
            "detection_delay": [1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704, 1479.53704],
        },
    },
    "Crypto": {
        "Direct": {
            "num_results": [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],
            "num_drops":   [1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280],
            "exec_time":   [14.62, 14.31, 13.98, 14.32, 14.23, 14.57, 14.20, 14.34, 14.39, 14.09, 14.76, 14.43, 14.14, 14.30, 14.79],
            "detection_delay": [25.62500, 25.62500, 25.62500, 25.62500, 25.62500, 25.62500, 25.62500, 25.62500, 25.62500, 25.62500, 25.62500, 25.62500, 25.62500, 25.62500, 25.62500],
        },
        "Fixed-Time": {
            "num_results": [7074, 7077, 7092, 7096, 7128, 7315, 7545, 7857, 8349, 9705, 11303, 13280, 15646, 16182, 16305],
            "num_drops":   [537992, 537814, 537226, 536837, 534910, 526003, 509382, 486391, 452175, 362680, 257363, 135701, 32900, 7470, 1342],
            "exec_time":   [16.46, 16.64, 16.97, 17.21, 16.82, 16.61, 16.51, 16.72, 16.81, 17.18, 17.07, 17.49, 17.69, 17.44, 18.25],
            "detection_delay": [439.22745, 440.12830, 441.40496, 441.93503, 444.18462, 454.43814, 470.52485, 496.21191, 522.61636, 600.70850, 731.38202, 1022.56589, 2260.46363, 3060.26258, 3302.17326],
        },
        "jump_and_decay": {
            "num_results": [13655, 13655, 13655, 13655, 13655, 13655, 13655, 13655, 13655, 13655, 13878, 14485, 15764, 16231, 16307], 
            "num_drops": [119379, 119379, 119379, 119379, 119379, 119379, 119379, 119379, 119379, 119379, 110818, 82589, 27918, 5533, 1210], 
            "exec_time": [15.12, 15.11, 15.11, 15.71, 17.35, 15.91, 16.12, 15.83, 15.71, 15.77, 15.79, 15.85, 16.06, 16.17, 16.29],
            "detection_delay": [1270.20469, 1270.20469, 1270.20469, 1270.20469, 1270.20469, 1270.20469, 1270.20469, 1270.20469, 1270.20469, 1270.20469, 1283.22828, 1491.44018, 2454.40700, 3142.47637, 3301.96081]
        },
        "max": {
            "num_results": [13599, 13599, 13599, 13599, 13599, 13599, 13599, 13599, 13599, 13599, 13812, 14485, 15764, 16194, 16307], 
            "num_drops": [123070, 123070, 123070, 123070, 123070, 123070, 123070, 123070, 123070, 123070, 114730, 82589, 27918, 6739, 1210], 
            "exec_time": [16.63, 16.27, 16.59, 16.46, 16.34, 16.43, 17.07, 16.92, 16.63, 16.67, 16.44, 17.34, 17.38, 17.15, 17.11],
            "detection_delay": [1266.55239, 1266.55239, 1266.55239, 1266.55239, 1266.55239, 1266.55239, 1266.55239, 1266.55239, 1266.55239, 1266.55239, 1277.96880, 1491.44018, 2454.40700, 3079.38780, 3301.96081]
        },
        "Individual per event": {
            'num_results': [16308, 16308, 16308, 16308, 16308, 16308, 16308, 16308, 16308, 16308, 16308, 16308, 16308, 16308, 16326],
            'num_drops': [1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1021, 1015, 456],
            "exec_time":   [16.54, 16.88, 16.95, 17.03, 16.79, 16.76, 16.44, 16.47, 16.67, 16.49, 16.59, 16.50, 16.48, 16.53, 16.41],
            "detection_delay": [3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3311.84817, 3314.30651],
        },
    },
}
# ===========================================================

OUTPUT_DIR = "compared_with_original"


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


def plot_lines(tables, metric, ylabel, filename, dataset_name):
    df = tables[metric]
    x = range(len(df["Quarantine Time (s)"]))
    plt.figure(figsize=(14, 6))
    col_idx = 0
    for col in df.columns[1:]:
        y_vals = df[col].values
        plt.plot(x, y_vals, marker="o", linewidth=2, label=col, markersize=6)
        # Add labels at every point with decimal formatting
        # Alternate position for each line to avoid overlap
        va_position = 'bottom' if col_idx % 2 == 0 else 'top'
        for xi, yi in zip(x, y_vals):
            # Format with 2 decimals if value has decimals, otherwise as integer
            label = f'{yi:.2f}' if yi % 1 != 0 else f'{int(yi)}'
            plt.text(xi, yi, label, fontsize=7, ha='center', va=va_position)
        col_idx += 1
    plt.xticks(x, df["Quarantine Time (s)"], rotation=45)
    plt.xlabel("Quarantine Time (s)", fontsize=11)
    plt.ylabel(ylabel, fontsize=11)
    plt.title(f"{ylabel} vs Quarantine Time - {dataset_name}", fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {out_path}")


def plot_drops_enhanced(tables, dataset_name):
    """Create enhanced drops plot with better visibility for differences"""
    df = tables["num_drops"]
    x = range(len(df["Quarantine Time (s)"]))
    
    # Single plot with log scale for better visibility of differences
    plt.figure(figsize=(14, 6))
    col_idx = 0
    for col in df.columns[1:]:
        # Add 1 to handle zeros in log scale
        y_vals = [v + 1 for v in df[col]]
        plt.plot(x, y_vals, marker="o", linewidth=2, label=col, markersize=6)
        # Add labels at every point (show original value with decimal formatting)
        # Alternate position for each line to avoid overlap
        va_position = 'bottom' if col_idx % 2 == 0 else 'top'
        for xi, orig, yval in zip(x, df[col], y_vals):
            label = f'{orig:.2f}' if orig % 1 != 0 else f'{int(orig)}'
            plt.text(xi, yval, label, fontsize=7, ha='center', va=va_position)
        col_idx += 1
    plt.xticks(x, df["Quarantine Time (s)"], rotation=45)
    plt.xlabel("Quarantine Time (s)", fontsize=12)
    plt.ylabel("Dropped Events (log scale, +1)", fontsize=12)
    plt.title(f"Dropped Events vs Quarantine Time (Log Scale) - {dataset_name}", fontsize=13, fontweight='bold')
    plt.yscale('log')
    plt.grid(True, alpha=0.3, which="both")
    plt.legend(fontsize=10)
    plt.tight_layout()
    
    safe_name = dataset_name.lower().replace(" ", "_")
    out_path = os.path.join(OUTPUT_DIR, f"compare_{safe_name}_drops_enhanced.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {out_path}")


def plot_all(all_dataset_tables):
    for dataset_name, tables in all_dataset_tables.items():
        safe_name = dataset_name.lower().replace(" ", "_")
        plot_lines(tables, "num_results", "Number of Results", f"compare_{safe_name}_results.png", dataset_name)
        plot_drops_enhanced(tables, dataset_name)  # Only log scale drops plot
        plot_lines(tables, "exec_time", "Execution Time (s)", f"compare_{safe_name}_exec_time.png", dataset_name)
        plot_lines(tables, "detection_delay", "Detection Delay (s)", f"compare_{safe_name}_detection_delay.png", dataset_name)


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


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_dataset_tables = build_tables()
    print_tables(all_dataset_tables)
    excel_path = os.path.join(OUTPUT_DIR, "compare_new_impl.xlsx")
    save_excel(all_dataset_tables, excel_path)
    plot_all(all_dataset_tables)
    print("\n" + "="*80)
    print("Done! Update the DATASETS section with your real measurements if needed.")
    print("="*80)
