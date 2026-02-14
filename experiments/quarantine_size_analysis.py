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

# Quarantine time axis (seconds)
QUARANTINE_TIMES: List[int] = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384]

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
            "size_mb": [0.0034, 0.0034, 0.0034, 0.0034, 0.0034, 0.0034, 0.0037, 0.0041, 0.0049, 0.0082, 0.0219, 0.0357, 0.0676, 0.1278, 0.1386],
            "num_events": [9, 9, 9, 9, 9, 9, 10, 11, 13, 22, 59, 96, 182, 344, 373],
        },
        "AVG": {
            "size_mb": [0.0082, 0.0082, 0.0082, 0.0082, 0.0082, 0.0082, 0.0082, 0.0082, 0.0082, 0.0082, 0.0219, 0.0357, 0.0676, 0.1278, 0.1386],
            "num_events": [22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 59, 96, 182, 344, 373],
        },
        "p99": {
            "size_mb": [0.1274, 0.1274, 0.1274, 0.1274, 0.1274, 0.1274, 0.1274, 0.1274, 0.1274, 0.1274, 0.1274, 0.1274, 0.1274, 0.1419, 0.1419],
            "num_events": [343, 343, 343, 343, 343, 343, 343, 343, 343, 343, 343, 343, 343, 382, 382],
        },
        "EMA on max": {
            "size_mb": [0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1527],
            "num_events": [388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 411],
        },
        "max": {
            "size_mb": [0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1527],
            "num_events": [388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 411],
        },
        "jump_and_decay": {
            "size_mb": [0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1527],
            "num_events": [388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 411],
        },
        "Individual per event": {
            "size_mb": [0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1441, 0.1519],
            "num_events": [388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 388, 409],
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
            "size_mb": [0.2420, 0.2420, 0.2420, 0.2420, 0.2420, 0.2420, 0.2758, 0.3875, 0.6664, 1.4783, 2.8295, 4.4478, 5.9230, 9.3298, 11.4781],
            "num_events": [394, 394, 394, 394, 394, 394, 449, 631, 1085, 2407, 4607, 7242, 9644, 15191, 18689],
        },
        "AVG": {
            "size_mb": [0.2420, 0.2420, 0.2420, 0.2420, 0.2420, 0.2420, 4.8519, 5.3672, 5.3672, 5.3672, 5.3672, 5.4077, 5.9230, 9.3298, 11.4781],
            "num_events": [394, 394, 394, 394, 394, 394, 7900, 8739, 8739, 8739, 8739, 8805, 9644, 15191, 18689],
        },
        "p99": {
            "size_mb": [11.6335, 11.6335, 11.6335, 11.6335, 11.6335, 11.6335, 11.6335, 11.6335, 11.6335, 11.6335, 11.6335, 11.6335, 11.6335, 11.6335, 11.6335],
            "num_events": [18942, 18942, 18942, 18942, 18942, 18942, 18942, 18942, 18942, 18942, 18942, 18942, 18942, 18942, 18942],
        },
        "EMA on max": {
            "size_mb": [11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584],
            "num_events": [19471, 19471, 19471, 19471, 19471, 19471, 19471, 19471, 19471, 19471, 19471, 19471, 19471, 19471, 19471],
        },
        "max": {
            "size_mb": [11.9517, 11.9517, 11.9517, 11.9517, 11.9517, 11.9517, 11.9517, 11.9517, 11.9517, 11.9517, 11.9517, 11.9517, 11.9517, 11.9517, 11.9517],
            "num_events": [19460, 19460, 19460, 19460, 19460, 19460, 19460, 19460, 19460, 19460, 19460, 19460, 19460, 19460, 19460],
        },
        "jump_and_decay": {
            "size_mb": [11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584, 11.9584],
            "num_events": [19471, 19471, 19471, 19471, 19471, 19471, 19471, 19471, 19471, 19471, 19471, 19471, 19471, 19471, 19471],
        },
        "Individual per event": {
            "size_mb": [19.1737, 19.1737, 19.1737, 19.1737, 19.1737, 19.1737, 19.1737, 19.1737, 19.1737, 19.1737, 19.1737, 19.1737, 19.1737, 19.1737, 19.1737],
            "num_events": [31219, 31219, 31219, 31219, 31219, 31219, 31219, 31219, 31219, 31219, 31219, 31219, 31219, 31219, 31219],
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
            "size_mb": [2.3252, 2.4965, 2.4969, 2.4969, 2.6783, 2.6783, 3.7993, 3.8240, 5.6635, 6.5762, 14.9135, 28.3903, 95.6450, 149.9255, 252.7562],
            "num_events": [5090, 5465, 5466, 5466, 5863, 5863, 8317, 8371, 12398, 14396, 32647, 62149, 209376, 328201, 553307],
        },
        "AVG": {
            "size_mb": [8.5282, 8.5282, 8.5282, 8.5282, 8.5282, 8.5282, 8.5282, 8.5282, 8.5282, 8.8927, 17.7489, 28.3903, 95.6450, 149.9255, 252.7562],
            "num_events": [18669, 18669, 18669, 18669, 18669, 18669, 18669, 18669, 18669, 19467, 38854, 62149, 209376, 328201, 553307],
        },
        "p99": {
            "size_mb": [18.5506, 18.5506, 18.5506, 18.5506, 18.5506, 18.5506, 18.5506, 18.5506, 18.5506, 19.8297, 32.3440, 44.5687, 95.6450, 149.9255, 252.7562],
            "num_events": [40609, 40609, 40609, 40609, 40609, 40609, 40609, 40609, 40609, 43409, 70804, 97565, 209376, 328201, 553307],
        },
        "EMA on max": {
            "size_mb": [38.0422, 38.0422, 38.0422, 38.0422, 38.0422, 38.0422, 38.0422, 38.0422, 38.0422, 38.0422, 38.0422, 64.4107, 98.4252, 149.9255, 252.7562],
            "num_events": [83278, 83278, 83278, 83278, 83278, 83278, 83278, 83278, 83278, 83278, 83278, 141001, 215462, 328201, 553307],
        },
        "max": {
            "size_mb": [38.9746, 38.9746, 38.9746, 38.9746, 38.9746, 38.9746, 38.9746, 38.9746, 38.9746, 38.9746, 38.9746, 64.4102, 106.4975, 149.9255, 252.7562],
            "num_events": [85319, 85319, 85319, 85319, 85319, 85319, 85319, 85319, 85319, 85319, 85319, 141000, 233133, 328201, 553307],
        },
        "jump_and_decay": {
            "size_mb": [38.9746, 38.9746, 38.9746, 38.9746, 38.9746, 38.9746, 38.9746, 38.9746, 38.9746, 38.9746, 38.9746, 64.4107, 106.5020, 149.9255, 252.7562],
            "num_events": [85319, 85319, 85319, 85319, 85319, 85319, 85319, 85319, 85319, 85319, 85319, 141001, 233143, 328201, 553307],
        },
        "Individual per event": {
            "size_mb": [253.9169, 253.9169, 253.9169, 253.9169, 253.9169, 253.9169, 253.9169, 253.9169, 253.9169, 253.9169, 253.9169, 253.9169, 253.9169, 253.9169, 280.8025],
            "num_events": [555848, 555848, 555848, 555848, 555848, 555848, 555848, 555848, 555848, 555848, 555848, 555848, 555848, 555848, 614703],
        },
    },
}
# ===========================================================

OUTPUT_DIR = "quarantine_size"


def _validate_dataset(dataset_name: str, policy_data: Dict[str, Dict[str, List[float]]]) -> None:
    for policy, metrics in policy_data.items():
        if "size_mb" not in metrics or "num_events" not in metrics:
            raise ValueError(f"{dataset_name}/{policy} must contain 'size_mb' and 'num_events'.")
        if len(metrics["size_mb"]) != len(metrics["num_events"]):
            raise ValueError(
                f"{dataset_name}/{policy} has mismatched lengths: "
                f"size_mb={len(metrics['size_mb'])}, num_events={len(metrics['num_events'])}"
            )


def _is_all_zero_axis(axis: List[float]) -> bool:
    return len(axis) > 0 and all(val == 0 for val in axis)


def _get_size_axis(dataset_name: str, policy_data: Dict[str, Dict[str, List[float]]]) -> List[float]:
    if not policy_data:
        raise ValueError(f"{dataset_name} has no policy data.")

    first_policy = next(iter(policy_data))
    size_axis = policy_data[first_policy]["size_mb"]

    for policy, metrics in policy_data.items():
        axis = metrics["size_mb"]
        if not _is_all_zero_axis(axis):
            size_axis = axis
            first_policy = policy
            break

    for policy, metrics in policy_data.items():
        axis = metrics["size_mb"]
        if axis != size_axis:
            if _is_all_zero_axis(axis) and len(axis) == len(size_axis):
                continue
            raise ValueError(
                f"{dataset_name}/{policy} has a different 'size_mb' axis than '{first_policy}'."
            )

    return size_axis


def _annotate_min_max_at_key_times(x_pos, series_values, key_indices) -> None:
    if not series_values or not x_pos:
        return

    def _format(v):
        return f"{int(v)}" if float(v).is_integer() else f"{v:.4f}"

    for idx in key_indices:
        if idx < 0 or idx >= len(x_pos):
            continue
        vals_at_idx = [vals[idx] for vals in series_values if len(vals) > idx]
        if not vals_at_idx:
            continue
        min_val = min(vals_at_idx)
        max_val = max(vals_at_idx)
        max_offset = (0, 12) if max_val == 0 else (0, 8)
        min_offset = (0, -6) if min_val == 0 else (0, -12)
        plt.annotate(
            _format(max_val),
            (x_pos[idx], max_val),
            textcoords="offset points",
            xytext=max_offset,
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold",
            color="black",
        )
        if min_val != max_val:
            plt.annotate(
                _format(min_val),
                (x_pos[idx], min_val),
                textcoords="offset points",
                xytext=min_offset,
                ha="center",
                va="top",
                fontsize=8,
                fontweight="bold",
                color="black",
            )


def build_tables() -> Dict[str, pd.DataFrame]:
    tables = {}
    for dataset_name, policy_data in DATASETS.items():
        _validate_dataset(dataset_name, policy_data)

        rows = []
        for policy in POLICIES:
            metrics = policy_data.get(policy)
            if not metrics:
                continue
            for idx, (size_mb, num_events) in enumerate(
                zip(metrics["size_mb"], metrics["num_events"])
            ):
                quarantine_time = QUARANTINE_TIMES[idx] if idx < len(QUARANTINE_TIMES) else None
                rows.append(
                    {
                        "Policy": policy,
                        "Quarantine Time (s)": quarantine_time,
                        "Quarantine Size (MB)": size_mb,
                        "Events Inside Quarantine": num_events,
                    }
                )
        tables[dataset_name] = pd.DataFrame(
            rows,
            columns=[
                "Policy",
                "Quarantine Time (s)",
                "Quarantine Size (MB)",
                "Events Inside Quarantine",
            ],
        )
    return tables


def save_excel(tables: Dict[str, pd.DataFrame], path: str) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for dataset_name, df in tables.items():
            df.to_excel(writer, sheet_name=f"{dataset_name}", index=False)
    print(f"✓ Saved Excel: {path}")


def plot_lines(df: pd.DataFrame, dataset_name: str) -> None:
    safe_name = dataset_name.lower().replace(" ", "_")
    x_pos = list(range(len(QUARANTINE_TIMES)))

    plt.figure(figsize=(12, 6))
    size_series = []
    for policy in POLICIES:
        policy_df = df[df["Policy"] == policy].sort_values("Quarantine Time (s)")
        if policy_df.empty:
            continue
        if len(policy_df) != len(QUARANTINE_TIMES):
            raise ValueError(
                f"{dataset_name}/{policy} has {len(policy_df)} points, expected {len(QUARANTINE_TIMES)}."
            )
        color = COLORS.get(policy, None)
        y_vals = policy_df["Quarantine Size (MB)"].values
        size_series.append(y_vals)
        plt.plot(
            x_pos,
            y_vals,
            marker="o",
            linewidth=2,
            label=policy,
            markersize=6,
            color=color,
        )

    plt.xlabel("Quarantine Time (s)", fontsize=11)
    plt.ylabel("Quarantine Size (MB)", fontsize=11)
    plt.title(f"Quarantine Size vs Quarantine Time - {dataset_name}", fontsize=13, fontweight="bold", pad=12)
    plt.xlim(-0.5, len(x_pos) - 0.5)
    key_indices = [0, len(QUARANTINE_TIMES) // 2, len(QUARANTINE_TIMES) - 1]
    _annotate_min_max_at_key_times(x_pos, size_series, key_indices)
    plt.xticks(x_pos, QUARANTINE_TIMES, rotation=45, fontsize=8)
    plt.grid(True)
    plt.legend(fontsize=8, loc="center left", bbox_to_anchor=(1.02, 0.5), borderaxespad=0)
    plt.tight_layout()

    mb_out_path = os.path.join(OUTPUT_DIR, f"quarantine_size_mb_{safe_name}.png")
    plt.savefig(mb_out_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {mb_out_path}")

    plt.figure(figsize=(12, 6))
    max_series = []
    for policy in POLICIES:
        policy_df = df[df["Policy"] == policy].sort_values("Quarantine Time (s)")
        if policy_df.empty:
            continue
        if len(policy_df) != len(QUARANTINE_TIMES):
            raise ValueError(
                f"{dataset_name}/{policy} has {len(policy_df)} points, expected {len(QUARANTINE_TIMES)}."
            )
        color = COLORS.get(policy, None)
        y_vals = policy_df["Events Inside Quarantine"].cummax().values
        max_series.append(y_vals)
        plt.plot(
            x_pos,
            y_vals,
            marker="o",
            linewidth=2,
            label=policy,
            markersize=6,
            color=color,
        )

    plt.xlabel("Quarantine Time (s)", fontsize=11)
    plt.ylabel("Max Events Inside Quarantine", fontsize=11)
    plt.title(
        f"Max Events Inside Quarantine vs Quarantine Time - {dataset_name}",
        fontsize=13,
        fontweight="bold",
        pad=12,
    )
    plt.xlim(-0.5, len(x_pos) - 0.5)
    _annotate_min_max_at_key_times(x_pos, max_series, key_indices)
    plt.xticks(x_pos, QUARANTINE_TIMES, rotation=45, fontsize=8)
    plt.grid(True)
    plt.legend(fontsize=8, loc="center left", bbox_to_anchor=(1.02, 0.5), borderaxespad=0)
    plt.tight_layout()

    max_out_path = os.path.join(OUTPUT_DIR, f"quarantine_max_events_{safe_name}.png")
    plt.savefig(max_out_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {max_out_path}")


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    tables = build_tables()

    excel_path = os.path.join(OUTPUT_DIR, "quarantine_size_tables.xlsx")
    save_excel(tables, excel_path)

    for dataset_name, df in tables.items():
        plot_lines(df, dataset_name)


if __name__ == "__main__":
    main()
