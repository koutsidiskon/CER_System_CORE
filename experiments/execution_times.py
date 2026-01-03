"""
Execution Time Analysis for Different Implementations and Datasets
Usage:
  python execution_times.py
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.patheffects as pe

def load_execution_times():
    """
    Define execution times for each implementation across different datasets.
    Times are in seconds for different quarantine buffer sizes.
    """
    
    # Quarantine times tested (in seconds)
    quarantine_times = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]
    
    # ============================================================
    # CRYPTO DATASET (1,756,833 events)
    # ============================================================
    crypto_data = {
        'dataset': 'Crypto (1.76M events)',
        'implementations': {
            'MAX (window max)': {
                'times': [21.06,20.40,20.27,21.62,21.93,21.17,23.44,26.52,21.94,19.00,18.57,18.56,20.09,19.01,21.04],
            },
            'EMA on max (α=0.1)': {
                'times': [19.00,19.04,18.97,19.41,18.34,18.70,18.86,18.48,18.50,18.47,19.06,19.01,19.35,19.42,19.39],
            },
            'Jump-and-Decay (α=0.1)': {
                'times': [21.21,20.86,21.26,21.13,21.16,20.54,20.78,20.76,21.24,20.46,21.14,21.44,21.32,21.24,23.09],
            },
            'p99 + EMA (α=0.1)': {
                'times': [49.90,51.39,49.21,49.03,49.61,49.30,48.80,49.41,49.58,49.47,50.37,51.92,53.66,56.20,55.70],
            },
            'Mean (window average)': {
                'times': [17.68,18.09,17.35,17.43,17.22,17.49,17.95,17.74,17.44,17.86,17.68,19.09,19.72,19.57,20.01],
            },
            'Individual quarantine per event type': {
                'times': [22.89,20.13,20.11,18.89,19.20,19.11,18.91,19.42,18.98,18.89,19.37,19.74,19.35,19.14,19.10],
            },
        }
    }
    
    # ============================================================
    # AVIATION DATASET (1,005,411 events)
    # ============================================================
    aviation_data = {
        'dataset': 'Aviation (1.0M events)',
        'implementations': {
            'MAX (window max)': {
                'times': [13.13,13.24,13.36,12.96,13.21,13.79,13.12,13.39,13.14,13.17,13.01,13.56,13.14,13.08,13.19],
            },
            'EMA on max (α=0.1)': {
                'times': [13.79,13.08,13.32,13.09,13.33,13.82,12.98,12.90,13.16,13.71,13.23,13.42,13.07,13.01,13.68],
            },
            'Jump-and-Decay (α=0.1)': {
                'times': [14.41,14.15,14.61,15.59,15.55,14.42,14.44,14.17,13.99,13.97,14.13,14.06,14.01,14.10,14.35],
            },
            'p99 + EMA (α=0.1)': {
                'times': [24.80,24.75,26.05,24.69,24.71,24.36,24.94,24.51,24.46,24.48,24.28,24.33,24.37,24.41,24.19],
            },
            'Mean (window average)': {
                'times': [12.04,12.08,12.10,11.98,12.40,12.09,12.26,12.27,12.97,12.50,12.39,12.47,12.48,12.28,12.29],
            },
            'Individual quarantine per event type': {
                'times': [13.06,13.28,13.07,13.31,12.88,13.05,12.92,13.32,13.15,12.96,13.09,13.06,13.16,12.81,13.72],
            },
        }
    }
    
    # ============================================================
    # FIRES DATASET (563,684 events)
    # ============================================================
    fires_data = {
        'dataset': 'Fires (563K events)',
        'implementations': {
            'MAX (window max)': {
                'times': [4.92,4.84,5.33,4.94,4.78,4.99,4.97,5.20,5.06,4.80,4.90,4.94,4.80,5.03,4.98],
            },
            'EMA on max (α=0.1)': {
                'times': [5.57,5.32,5.20,5.21,5.13,5.19,5.30,5.23,5.42,5.26,5.30,5.10,5.27,5.24,5.42],
            },
            'Jump-and-Decay (α=0.1)': {
                'times': [6.26,5.36,5.16,5.15,5.22,5.23,5.14,5.40,5.28,5.25,5.29,5.13,5.15,5.43,5.27],
            },
            'p99 + EMA (α=0.1)': {
                'times': [13.92,13.73,13.28,12.88,12.92,12.94,12.88,13.19,13.70,13.59,13.13,13.07,13.45,14.07,14.50],
            },
            'Mean (window average)': {
                'times': [4.67,4.64,4.60,4.48,4.62,4.40,4.83,4.66,4.57,4.43,4.54,4.73,4.68,4.41,4.75],
            },
            'Individual quarantine per event type': {
                'times': [4.95,4.90,4.99,4.91,4.91,5.13,5.76,4.97,5.09,5.04,4.85,4.82,5.09,5.03,5.12],
            },
        }
    }
    
    return {
        'quarantine_times': quarantine_times,
        'datasets': [crypto_data, aviation_data, fires_data]
    }


def create_execution_time_table(data):
    """Create a comprehensive execution time table"""
    
    # Get all implementation names (assuming all datasets have same implementations)
    implementations = list(data['datasets'][0]['implementations'].keys())
    quarantine_times = data['quarantine_times']
    
    # Create a table for each dataset
    tables = {}
    for dataset_info in data['datasets']:
        dataset_name = dataset_info['dataset']
        table_data = {'Quarantine Time (s)': quarantine_times}
        
        for impl_name in implementations:
            if impl_name in dataset_info['implementations']:
                table_data[impl_name] = dataset_info['implementations'][impl_name]['times']
        
        tables[dataset_name] = pd.DataFrame(table_data)
    
    return tables


def plot_execution_times_by_dataset(data):
    """Create plots showing execution times for each dataset"""
    
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown']
    markers = ['o', 's', '^', 'D', 'v', 'p']
    quarantine_times = data['quarantine_times']
    x_pos = range(len(quarantine_times))
    
    # Create a plot for each dataset
    for dataset_info in data['datasets']:
        dataset_name = dataset_info['dataset']
        implementations = dataset_info['implementations']
        
        plt.figure(figsize=(14, 7))
        
        for idx, (impl_name, impl_data) in enumerate(implementations.items()):
            plt.plot(x_pos, impl_data['times'],
                    marker=markers[idx % len(markers)], linestyle='-', linewidth=2,
                    color=colors[idx % len(colors)], label=impl_name, markersize=7)
        
        plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=9, rotation=45)
        plt.title(f'Execution Time Comparison - {dataset_name}', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Quarantine Buffer Size (s)', fontsize=12)
        plt.ylabel('Execution Time (seconds)', fontsize=12)
        plt.legend(fontsize=9, loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filename = os.path.join('execution time', f"execution_times_{dataset_name.split()[0].lower()}.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {filename}")


def plot_all_datasets_comparison(data):
    """Create comparison plots showing all datasets together for each implementation"""
    
    implementations = list(data['datasets'][0]['implementations'].keys())
    quarantine_times = data['quarantine_times']
    x_pos = range(len(quarantine_times))
    
    # Colors for each dataset
    dataset_colors = ['tab:blue', 'tab:orange', 'tab:green']
    dataset_markers = ['o', 's', '^']
    
    # Create a plot for each implementation
    for impl_name in implementations:
        plt.figure(figsize=(12, 6))
        
        for idx, dataset_info in enumerate(data['datasets']):
            dataset_name = dataset_info['dataset']
            times = dataset_info['implementations'][impl_name]['times']
            
            plt.plot(x_pos, times,
                    marker=dataset_markers[idx], linestyle='-', linewidth=2,
                    color=dataset_colors[idx], label=dataset_name, markersize=7)
        
        plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=9, rotation=45)
        plt.title(f'Execution Time: {impl_name} Across Datasets', fontsize=13, fontweight='bold', pad=12)
        plt.xlabel('Quarantine Buffer Size (s)', fontsize=11)
        plt.ylabel('Execution Time (seconds)', fontsize=11)
        plt.legend(fontsize=10, loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        safe_name = impl_name.replace(' ', '_').replace('(', '').replace(')', '').replace('=', '').replace('α', 'alpha').replace('.', '')
        filename = os.path.join('execution time', f"execution_times_by_impl_{safe_name}.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {filename}")


def plot_execution_times_heatmap(data):
    """Create heatmap showing execution times"""
    
    implementations = list(data['datasets'][0]['implementations'].keys())
    quarantine_times = data['quarantine_times']
    
    for dataset_info in data['datasets']:
        dataset_name = dataset_info['dataset']
        
        # Prepare data for heatmap
        times_matrix = []
        for impl_name in implementations:
            times_matrix.append(dataset_info['implementations'][impl_name]['times'])
        
        times_matrix = np.array(times_matrix)
        
        # Create heatmap (larger figure, high-contrast perceptual colormap)
        fig, ax = plt.subplots(figsize=(18, 10))
        im = ax.imshow(times_matrix, cmap='magma', aspect='auto')
        
        # Set ticks
        ax.set_xticks(np.arange(len(quarantine_times)))
        ax.set_yticks(np.arange(len(implementations)))
        ax.set_xticklabels(quarantine_times, fontsize=12, color='black')

        # Shorten long implementation names for readability
        def _short_name(name: str) -> str:
            return name.replace('Individual quarantine per event type', 'Per-event quarantine')

        ax.set_yticklabels([_short_name(impl) for impl in implementations], fontsize=12, color='black')
        ax.tick_params(colors='black')
        
        # Rotate x labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Execution Time (s)', rotation=270, labelpad=24, fontsize=13)
        cbar.ax.yaxis.set_tick_params(color='black')
        plt.setp(cbar.ax.get_yticklabels(), color='black')
        
        # Add text annotations
        # Choose text color based on relative value for better contrast
        vmax = np.max(times_matrix)
        mid = vmax * 0.55
        for i in range(len(implementations)):
            for j in range(len(quarantine_times)):
                val = times_matrix[i, j]
                ax.text(
                    j,
                    i,
                    f'{val:.1f}',
                    ha="center",
                    va="center",
                    color='white',
                    fontsize=11,
                    fontweight='bold',
                    path_effects=[pe.withStroke(linewidth=2, foreground='black')]
                )
        
        ax.set_title(f'Execution Time Heatmap - {dataset_name}', fontsize=14, fontweight='bold', pad=15, color='black')
        ax.set_xlabel('Quarantine Buffer Size (s)', fontsize=14, labelpad=10)
        ax.set_ylabel('Implementation', fontsize=14, labelpad=10)
        
        plt.tight_layout()
        filename = os.path.join('execution time', f"execution_times_heatmap_{dataset_name.split()[0].lower()}.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {filename}")


def print_summary_statistics(tables):
    """Print summary statistics for execution times"""
    
    print("\n" + "="*120)
    print("EXECUTION TIME SUMMARY STATISTICS")
    print("="*120)
    
    for dataset_name, df in tables.items():
        print(f"\n{dataset_name}")
        print("-" * 120)
        
        # Calculate statistics for each implementation
        stats_data = []
        for col in df.columns[1:]:  # Skip 'Quarantine Time (s)' column
            times = df[col].values
            stats_data.append({
                'Implementation': col,
                'Min (s)': f"{np.min(times):.2f}",
                'Max (s)': f"{np.max(times):.2f}",
                'Mean (s)': f"{np.mean(times):.2f}",
                'Median (s)': f"{np.median(times):.2f}",
                'Std Dev': f"{np.std(times):.2f}"
            })
        
        stats_df = pd.DataFrame(stats_data)
        print(stats_df.to_string(index=False))
        print()


def save_to_excel(tables, filename='execution_times.xlsx'):
    """Save all execution time tables to an Excel file"""
    
    filepath = os.path.join('execution time', filename)
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        for dataset_name, df in tables.items():
            sheet_name = dataset_name.split()[0]  # Use first word as sheet name
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"✓ Saved execution times to: {filepath}")


def print_tables(tables):
    """Print execution time tables"""
    
    print("\n" + "="*120)
    print("EXECUTION TIME TABLES (in seconds)")
    print("="*120)
    
    for dataset_name, df in tables.items():
        print(f"\n{dataset_name}")
        print("-" * 120)
        print(df.to_string(index=False))
        print()


if __name__ == "__main__":
    # Create output directory
    output_dir = 'execution time'
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*120)
    print("EXECUTION TIME ANALYSIS TOOL")
    print("="*120)
    
    # Load execution time data
    data = load_execution_times()
    print(f"\nLoaded execution time data for {len(data['datasets'])} datasets:")
    for dataset_info in data['datasets']:
        impl_count = len(dataset_info['implementations'])
        print(f"  • {dataset_info['dataset']}: {impl_count} implementations")
    
    # Create tables
    tables = create_execution_time_table(data)
    
    # Print tables
    print_tables(tables)
    
    # Print summary statistics
    print_summary_statistics(tables)
    
    # Save to Excel
    try:
        save_to_excel(tables)
    except ImportError:
        print("\n⚠ openpyxl not installed. Skipping Excel export.")
        print("  Install with: pip install openpyxl")
    
    # Create visualizations (per-dataset only; skip cross-dataset impl plots)
    print("\nGenerating execution time plots (per dataset only)...")
    plot_execution_times_by_dataset(data)
    # plot_all_datasets_comparison(data)  # intentionally skipped per user request
    plot_execution_times_heatmap(data)
    
    print("\n" + "="*120)
    print("DONE! Check the generated PNG files and Excel spreadsheet.")
    print("="*120 + "\n")
