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
            "num_results": [23,23,23,23,23,23,23,23,23,23,23,23,23,23,23],
            "num_drops":   [79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434],
            "exec_time":   [9.90, 9.85, 9.87, 9.84, 9.86, 9.79, 9.84, 9.79, 9.83, 9.80, 9.86, 9.74, 9.57, 9.66, 9.76],
            "detection_delay": [240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000, 240.00000],
        },
        "Fixed-Time": {
            "num_results": [44, 44, 44, 44, 44, 44, 44, 44, 46, 46, 46, 46, 46, 46, 46],
            "num_drops":   [14524, 14519, 14501, 14459, 14396, 14241, 11085, 8213, 4512, 1574, 472, 175, 75, 34, 24],
            "exec_time":   [10.59, 10.59, 10.53, 10.73, 10.63, 10.52, 10.57, 10.65, 10.79, 10.85, 10.75, 11.37, 10.67, 10.84, 10.72],
            "detection_delay": [216.81818, 216.81818, 216.81818, 216.81818, 216.81818, 216.81818, 216.81818, 216.81818, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478],
        },
        "jump_and_decay": {
            "num_results": [46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46], 
            "num_drops": [130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 130, 111, 55, 34, 24], 
            "exec_time": [9.45, 9.31, 9.44, 9.47, 9.40, 11.07, 9.66, 10.07, 9.60, 10.01, 10.06, 9.46, 10.06, 9.70, 9.46],
            "detection_delay": [220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478]
        },
        "max": {
            "num_results": [46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46], 
            "num_drops": [131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 112, 55, 34, 24], 
            "exec_time": [9.72, 9.34, 9.25, 9.68, 9.16, 9.08, 9.01, 9.15, 9.13, 9.24, 9.07, 9.07, 9.12, 9.14, 9.17],
            "detection_delay": [220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478]
        },
        "Individual per event": {
            'num_results': [46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46],
            'num_drops': [108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 88, 52, 33, 24],
            "exec_time":   [9.60, 9.96, 9.35, 9.88, 9.42, 9.78, 9.94, 9.25, 9.90, 9.30, 9.36, 9.06, 9.38, 9.13, 9.86],
            "detection_delay": [220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478, 220.43478],
        },
    },
    "Aviation": {
        "Direct": {
            "num_results": [265,265,265,265,265,265,265,265,265,265,265,265,265,265,265],
            "num_drops":   [336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293],
            "exec_time":   [12.66, 12.44, 12.50, 12.98, 12.55, 12.87, 13.13, 12.65, 12.72, 12.81, 12.99, 12.80, 12.90, 13.09, 12.72],
            "detection_delay": [0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642, 0.22642],
        },
        "Fixed-Time": {
            "num_results": [282, 282, 282, 282, 282, 282, 316, 341, 399, 440, 473, 487, 492, 493, 493],
            "num_drops":   [313826, 313826, 313826, 313826, 313826, 313826, 274143, 215379, 126483, 60387, 21780, 7209, 2342, 631, 140],
            "exec_time":   [12.84, 12.56, 12.76, 12.50, 12.54, 12.57, 12.64, 12.75, 13.07, 13.50, 13.30, 13.34, 13.55, 13.37, 13.12],
            "detection_delay": [6.17021, 6.17021, 6.17021, 6.17021, 6.17021, 6.17021, 45.00000, 79.17889, 256.99248, 480.81818, 809.04863, 1044.39425, 1203.65854, 1252.08925, 1252.08925],
        },
        "jump_and_decay": {
            "num_results": [493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493], 
            "num_drops": [147, 147, 147, 147, 147, 147, 147, 141, 141, 135, 135, 117, 103, 74, 58], 
            "exec_time": [11.67, 11.69, 11.67, 11.74, 12.13, 11.95, 12.33, 11.94, 11.78, 11.83, 12.48, 12.37, 12.41, 11.89, 11.55],
            "detection_delay": [1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1251.83579, 1252.08925, 1252.08925]
        },
        "max": {
            "num_results": [493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493], 
            "num_drops": [148, 148, 148, 148, 148, 148, 148, 142, 142, 136, 136, 118, 104, 77, 58], 
            "exec_time": [12.16, 12.15, 12.14, 12.18, 12.23, 11.87, 12.07, 12.13, 12.16, 12.08, 12.23, 12.25, 12.25, 12.18, 12.25],
            "detection_delay": [1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925]
        },
        "Individual per event": {
            'num_results': [493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493, 493],
            'num_drops': [33, 33, 33, 33, 33, 33, 33, 29, 29, 17, 17, 17, 17, 17, 17],
            "exec_time":   [12.02, 12.19, 12.27, 11.56, 12.21, 12.28, 12.25, 11.63, 12.08, 12.01, 11.56, 11.90, 11.90, 11.57, 11.33],
            "detection_delay": [1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925, 1252.08925],
        },
    },
    "Crypto": {
        "Direct": {
            "num_results": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            "num_drops":   [1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280],
            "exec_time":   [14.76, 14.62, 14.38, 14.68, 14.52, 14.82, 14.60, 14.41, 14.33, 14.62, 14.29, 14.93, 14.61, 14.35, 14.60],
            "detection_delay": [13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000, 13.00000],
        },
        "Fixed-Time": {
            "num_results": [1314, 1314, 1317, 1318, 1324, 1375, 1446, 1515, 1618, 2012, 2392, 2926, 3656, 3849, 3886],
            "num_drops":   [537992, 537814, 537226, 536837, 534910, 526003, 509382, 486391, 452175, 362680, 257363, 135701, 32900, 7470, 1342],
            "exec_time":   [17.66, 16.83, 16.54, 16.71, 17.01, 16.97, 16.93, 16.82, 16.80, 16.87, 16.89, 16.87, 17.61, 18.29, 18.39],
            "detection_delay": [369.95129, 369.95129, 370.75323, 371.44993, 373.55891, 393.05891, 422.87483, 446.67261, 470.48022, 577.06113, 707.93144, 982.69036, 2086.65099, 2827.87789, 2933.38420],
        },
        "jump_and_decay": {
            "num_results": [2988, 2988, 2988, 2988, 2988, 2988, 2988, 2988, 2988, 2988, 3055, 3228, 3701, 3863, 3887], 
            "num_drops": [119379, 119379, 119379, 119379, 119379, 119379, 119379, 119379, 119379, 119379, 110818, 82589, 27918, 5533, 1210], 
            "exec_time": [14.93, 15.38, 14.89, 15.34, 14.84, 16.03, 15.27, 15.35, 15.20, 15.53, 15.11, 15.38, 15.69, 15.74, 15.69],
            "detection_delay": [1185.47289, 1185.47289, 1185.47289, 1185.47289, 1185.47289, 1185.47289, 1185.47289, 1185.44270, 1185.47289, 1185.47289, 1189.73944, 1368.78408, 2333.45988, 2894.75123, 2932.63288]
        },
        "max": {
            "num_results": [2971, 2971, 2971, 2971, 2971, 2971, 2971, 2971, 2971, 2971, 3036, 3228, 3701, 3857, 3887], 
            "num_drops": [123070, 123070, 123070, 123070, 123070, 123070, 123070, 123070, 123070, 123070, 114730, 82589, 27918, 6739, 1210], 
            "exec_time": [15.35, 15.32, 15.29, 15.29, 15.63, 15.40, 15.47, 15.57, 15.53, 15.53, 15.67, 15.55, 15.76, 16.20, 16.06],
            "detection_delay": [1177.95490, 1177.95490, 1177.95490, 1177.95490, 1177.96742, 1177.95490, 1177.95490, 1177.95490, 1177.95490, 1177.95490, 1182.73814, 1368.78408, 2333.45988, 2858.24190, 2932.63288]
        },
        "Individual per event": {
            'num_results': [3889, 3889, 3889, 3889, 3889, 3889, 3889, 3889, 3889, 3889, 3889, 3889, 3889, 3889, 3898],
            'num_drops': [1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1021, 1015, 456],
            "exec_time":   [16.49, 16.65, 16.48, 16.59, 16.65, 16.54, 16.47, 16.55, 16.60, 16.07, 16.43, 16.27, 16.43, 16.26, 16.35],
            "detection_delay": [2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2932.78041, 2966.86301],
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
