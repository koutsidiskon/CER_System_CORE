"""
Quarantine size analysis (MB vs number of events) across datasets and policies.

Usage:
  python quarantine_size_analysis.py
"""
import os
from typing import Dict, List

import pandas as pd
import matplotlib.pyplot as plt

# ==================== DATA ====================

# Policies to plot (order controls legend order)
POLICIES: List[str] = [
    "Direct",
    "Sorted",
    "Fixed-Time",
    "AVG",
    "p99",
    "EMA on max",
    "max",
    "jump_and_decay",
    "Individual per event",
]

# Color scheme for consistent coloring across all plots
COLORS = {
    "Direct": "#1f77b4",
    "Fixed-Time": "#ff7f0e",
    "jump_and_decay": "#2ca02c",
    "max": "#d62728",
    "Individual per event": "#9467bd",
    "Sorted": "#8c564b",
    "AVG": "#bcbd22",
    "EMA on max": "#e377c2",
    "p99": "#7f7f7f",
}

DATASETS: Dict[str, Dict[str, Dict[str, List[float]]]] = {
    "Fires": {
        "Direct": {
            "size_mb": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "num_events": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        },
        "Sorted": {
            "size_mb": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "num_events": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        },
        "Fixed-Time": {
            "size_mb": [0.0034, 0.0034, 0.0034, 0.0034, 0.0034, 0.0034, 0.0037, 0.0041, 0.0048, 0.0082, 0.0219, 0.0357, 0.0676, 0.1278, 0.1386],
            "num_events": [9, 9, 9, 9, 9, 9, 10, 11, 13, 22, 59, 96, 182, 344, 373],
        },
        "AVG": {
            "size_mb": [],
            "num_events": [],
        },
        "p99": {
            "size_mb": [],
            "num_events": [],
        },
        "EMA on max": {
            "size_mb": [],
            "num_events": [],
        },
        "max": {
            "size_mb": [],
            "num_events": [],
        },
        "jump_and_decay": {
            "size_mb": [],
            "num_events": [],
        },
        "Individual per event": {
            "size_mb": [],
            "num_events": [],
        },
    },
    "Aviation": {
        "Direct": {
            "size_mb": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "num_events": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        },
        "Sorted": {
            "size_mb": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "num_events": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        },
        "Fixed-Time": {
            "size_mb": [0.2420, 0.2420, 0.2420, 0.2420, 0.2420, 0.2420, 0.2758, 0.3875, 0.6664, 1.4783, 2.8295, 4.4478, 5.9230, 9.3298, 11.4782],
            "num_events": [394, 394, 394, 394, 394, 394, 449, 631, 1085, 2407, 4607, 7242, 9644, 15191, 18689],
        },
        "AVG": {
            "size_mb": [],
            "num_events": [],
        },
        "p99": {
            "size_mb": [],
            "num_events": [],
        },
        "EMA on max": {
            "size_mb": [],
            "num_events": [],
        },
        "max": {
            "size_mb": [],
            "num_events": [],
        },
        "jump_and_decay": {
            "size_mb": [],
            "num_events": [],
        },
        "Individual per event": {
            "size_mb": [],
            "num_events": [],
        },
    },
    "Crypto": {
        "Direct": {
            "size_mb": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "num_events": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        },
        "Sorted": {
            "size_mb": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "num_events": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        },
        "Fixed-Time": {
            "size_mb": [],
            "num_events": [],
        },
        "AVG": {
            "size_mb": [],
            "num_events": [],
        },
        "p99": {
            "size_mb": [],
            "num_events": [],
        },
        "EMA on max": {
            "size_mb": [],
            "num_events": [],
        },
        "max": {
            "size_mb": [],
            "num_events": [],
        },
        "jump_and_decay": {
            "size_mb": [],
            "num_events": [],
        },
        "Individual per event": {
            "size_mb": [],
            "num_events": [],
        },
    },
}
# ===========================================================

OUTPUT_DIR = os.path.join("experiments", "compared_with_original")


def _validate_dataset(dataset_name: str, policy_data: Dict[str, Dict[str, List[float]]]) -> None:
    for policy, metrics in policy_data.items():
        if "size_mb" not in metrics or "num_events" not in metrics:
            raise ValueError(f"{dataset_name}/{policy} must contain 'size_mb' and 'num_events'.")
        if len(metrics["size_mb"]) != len(metrics["num_events"]):
            raise ValueError(
                f"{dataset_name}/{policy} has mismatched lengths: "
                f"size_mb={len(metrics['size_mb'])}, num_events={len(metrics['num_events'])}"
            )


def _get_size_axis(dataset_name: str, policy_data: Dict[str, Dict[str, List[float]]]) -> List[float]:
    if not policy_data:
        raise ValueError(f"{dataset_name} has no policy data.")

    first_policy = next(iter(policy_data))
    size_axis = policy_data[first_policy]["size_mb"]

    for policy, metrics in policy_data.items():
        if metrics["size_mb"] != size_axis:
            raise ValueError(
                f"{dataset_name}/{policy} has a different 'size_mb' axis than '{first_policy}'."
            )

    return size_axis


def build_tables() -> Dict[str, pd.DataFrame]:
    tables = {}
    for dataset_name, policy_data in DATASETS.items():
        _validate_dataset(dataset_name, policy_data)

        size_axis = _get_size_axis(dataset_name, policy_data)
        data = {"Quarantine Size (MB)": size_axis}
        for policy in POLICIES:
            series = policy_data.get(policy, {}).get("num_events", [])
            if series == []:
                series = [None] * len(size_axis)
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
