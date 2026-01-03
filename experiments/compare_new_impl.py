"""
Compare new implementation vs Direct and Fixed-Time quarantine.
Usage:
  python compare_new_impl.py

Edit the DATA section to plug in your actual results.
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

# ==================== DATA (EDIT THESE) ====================
# Quarantine buffer sizes (seconds) used in your runs
QUARANTINE_TIMES = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]

# Data for multiple datasets
# Each dataset has metrics for three implementations: Direct, Fixed-Time, Individual per event
# Metrics: num_results, num_drops, exec_time

DATASETS = {
    "Fires": {
        "Direct": {
            "num_results": [20258,20258,20258,20258,20258,20258,20258,20258,20258,20258,20258,20258,20258,20258,20258],
            "num_drops":   [79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434,79434],
            "exec_time":   [4.50,4.61,4.52,4.55,4.66,4.64,4.56,4.42,5.05,4.53,4.53,4.88,4.80,4.60,4.51],
        },
        "Fixed-Time": {
            "num_results": [28640,28640,28640,28640,28640,28640,29210,29670,30197,30634,30808,30851,30862,30867,30870],
            "num_drops":   [14524,14519,14501,14459,14396,14241,11085,8213,4512,1574,472,175,75,34,24],
            "exec_time":   [4.98,4.93,5.18,4.92,4.93,4.88,4.96,4.72,4.86,4.65,4.71,5.20,4.70,4.73,4.80],
        },
        "Individual per event": {
            'num_results': [30855,30855,30855,30855,30855,30855,30855,30855,30855,30855,30855,30859,30865,30867,30870],
            'num_drops': [108,108,108,108,108,108,108,108,108,108,108,88,52,33,24],
            "exec_time":   [4.95,4.90,4.99,4.91,4.91,5.13,5.20,4.97,5.09,5.04,4.85,4.82,5.09,5.03,5.12],
        },
    },
    "Aviation": {
        "Direct": {
            "num_results": [45,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
            "num_drops":   [336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293,336293],
            "exec_time":   [12.02,12.31,11.75,12.05,12.28,12.13,11.98,11.87,12.05,11.82,12.09,12.40,12.12,11.84,12.46],
        },
        "Fixed-Time": {
            "num_results": [53,53,53,53,53,53,69,101,163,197,225,247,257,257,257],
            "num_drops":   [313826,313826,313826,313826,313826,313826,274143,215379,126483,60387,21780,7209,2342,631,140],
            "exec_time":   [12.01,11.64,12.98,13.34,12.22,12.19,11.66,11.82,12.65,12.69,13.36,16.32,17.42,15.95,14.70],
        },
        "Individual per event": {
            'num_results': [257,257,257,257,257,257,257,257,257,257,257,257,257,257,257],
            'num_drops': [33,33,33,33,33,33,33,29,29,17,17,17,17,17,17],
            "exec_time":   [13.06,13.28,13.07,13.31,12.88,13.05,12.92,13.32,13.15,12.96,13.09,13.06,13.16,12.81,13.72],
        },
    },
    "Crypto": {
        "Direct": {
            "num_results": [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
            "num_drops":   [1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280,1739280],
            "exec_time":   [14.20,14.03,13.74,13.97,13.81,14.13,14.04,13.81,14.41,14.29,14.42,14.81,13.82,13.91,14.50],
        },
        "Fixed-Time": {
            "num_results": [5840,5840,5851,5851,5875,6077,6176,6458,6984,8373,10105,12102,14987,15575,15662],
            "num_drops":   [537992,537814,537226,536837,534910,526003,509382,486391,452175,362680,257363,135701,32900,7470,1342],
            "exec_time":   [17.85,17.30,16.20,16.54,16.29,16.40,18.49,16.14,17.06,18.06,19.09,18.32,18.04,19.64,19.03],
        },
        "Individual per event": {
            'num_results': [15676,15676,15676,15676,15676,15676,15676,15676,15676,15676,15676,15676,15676,15676,15684],
            'num_drops': [1024,1024,1024,1024,1024,1024,1024,1024,1024,1024,1024,1024,1021,1015,456],
            "exec_time":   [22.89,20.13,20.11,18.89,19.20,19.11,18.91,19.42,18.98,18.89,19.37,19.74,19.35,19.14,19.10],
        },
    },
}
# ===========================================================

OUTPUT_DIR = "compared_with_original"


def build_tables():
    # Build tables for each dataset
    all_dataset_tables = {}
    for dataset_name, implementations in DATASETS.items():
        tables = {}
        for metric in ["num_results", "num_drops", "exec_time"]:
            data = {"Quarantine Time (s)": QUARANTINE_TIMES}
            for impl_name, metrics in implementations.items():
                data[impl_name] = metrics[metric]
            tables[metric] = pd.DataFrame(data)
        all_dataset_tables[dataset_name] = tables
    return all_dataset_tables


def save_excel(all_dataset_tables, path):
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for dataset_name, tables in all_dataset_tables.items():
            tables["num_results"].to_excel(writer, sheet_name=f"{dataset_name}_Results", index=False)
            tables["num_drops"].to_excel(writer, sheet_name=f"{dataset_name}_Drops", index=False)
            tables["exec_time"].to_excel(writer, sheet_name=f"{dataset_name}_ExecTime", index=False)
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
