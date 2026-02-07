"""
Quarantine size analysis (MB vs number of events) across datasets and policies.

Usage:
  python quarantine_size_analysis.py

Edit the DATA section to plug in your actual results.
"""
import os
from typing import Dict, List

import pandas as pd
import matplotlib.pyplot as plt

# ==================== DATA (EDIT THESE) ====================
# Quarantine sizes (MB) used in your runs
QUARANTINE_SIZES_MB: List[float] = [1, 2, 4, 8, 16, 32, 64]

# Policies to plot (order controls legend order)
POLICIES: List[str] = [
    "Direct",
    "Fixed-Time",
    "jump_and_decay",
    "max",
    "Individual per event",
    "Sorted",
]

# Color scheme for consistent coloring across all plots
COLORS = {
    "Direct": "#1f77b4",
    "Fixed-Time": "#ff7f0e",
    "jump_and_decay": "#2ca02c",
    "max": "#d62728",
    "Individual per event": "#9467bd",
    "Sorted": "#8c564b",
}

# DATASETS structure:
# DATASETS[dataset_name][policy_name] = {
#     "size_mb": [...],      # quarantine size in MB for each point
#     "num_events": [...],    # number of events inside quarantine
# }
DATASETS: Dict[str, Dict[str, Dict[str, List[float]]]] = {
    "Fires": {
        "Direct": {
            "size_mb": [1, 2, 4, 8, 16, 32, 64],
            "num_events": [0, 0, 0, 0, 0, 0, 0],
        },
        "Fixed-Time": {
            "size_mb": [1, 2, 4, 8, 16, 32, 64],
            "num_events": [0, 0, 0, 0, 0, 0, 0],
        },
    },
    "Aviation": {
        "Direct": {
            "size_mb": [1, 2, 4, 8, 16, 32, 64],
            "num_events": [0, 0, 0, 0, 0, 0, 0],
        },
        "Fixed-Time": {
            "size_mb": [1, 2, 4, 8, 16, 32, 64],
            "num_events": [0, 0, 0, 0, 0, 0, 0],
        },
    },
}
# ===========================================================

OUTPUT_DIR = "compared_with_original"


def _validate_dataset(dataset_name: str, policy_data: Dict[str, Dict[str, List[float]]]) -> None:
    for policy, metrics in policy_data.items():
        if "size_mb" not in metrics or "num_events" not in metrics:
            raise ValueError(f"{dataset_name}/{policy} must contain 'size_mb' and 'num_events'.")
        if len(metrics["size_mb"]) != len(metrics["num_events"]):
            raise ValueError(
                f"{dataset_name}/{policy} has mismatched lengths: "
                f"size_mb={len(metrics['size_mb'])}, num_events={len(metrics['num_events'])}"
            )


def build_tables() -> Dict[str, pd.DataFrame]:
    tables = {}
    for dataset_name, policy_data in DATASETS.items():
        _validate_dataset(dataset_name, policy_data)

        # Ensure we have a unified size axis. Use QUARANTINE_SIZES_MB by default.
        data = {"Quarantine Size (MB)": QUARANTINE_SIZES_MB}
        for policy in POLICIES:
            series = policy_data.get(policy, {}).get("num_events", [])
            data[policy] = series
        tables[dataset_name] = pd.DataFrame(data)
    return tables


def save_excel(tables: Dict[str, pd.DataFrame], path: str) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for dataset_name, df in tables.items():
            df.to_excel(writer, sheet_name=f"{dataset_name}", index=False)
    print(f"✓ Saved Excel: {path}")


def plot_lines(df: pd.DataFrame, dataset_name: str) -> None:
    x = list(range(len(df["Quarantine Size (MB)"])))
    plt.figure(figsize=(12, 6))

    series_names = [c for c in df.columns[1:]]
    for col in series_names:
        y_vals = df[col].values
        color = COLORS.get(col, None)
        plt.plot(x, y_vals, marker="o", linewidth=2, label=col, markersize=6, color=color)

    plt.xticks(x, df["Quarantine Size (MB)"], rotation=45, fontsize=8)
    plt.xlabel("Quarantine Size (MB)", fontsize=11)
    plt.ylabel("Events Inside Quarantine", fontsize=11)
    plt.title(f"Events Inside vs Quarantine Size - {dataset_name}", fontsize=13, fontweight="bold", pad=12)
    plt.grid(True)
    plt.legend(fontsize=9, loc="best")
    plt.tight_layout()

    safe_name = dataset_name.lower().replace(" ", "_")
    out_path = os.path.join(OUTPUT_DIR, f"quarantine_size_{safe_name}.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {out_path}")


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    tables = build_tables()

    excel_path = os.path.join(OUTPUT_DIR, "quarantine_size_tables.xlsx")
    save_excel(tables, excel_path)

    for dataset_name, df in tables.items():
        plot_lines(df, dataset_name)


if __name__ == "__main__":
    main()
