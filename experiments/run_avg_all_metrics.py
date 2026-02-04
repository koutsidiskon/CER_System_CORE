#!/usr/bin/env python3
"""
Run experiment.py multiple times with different dynamic time values and calculate average metrics.
Combines execution time and detection delay analysis in a single script.

Usage:
  python run_avg_all_metrics.py [mode] [num_runs] [build] [query] [declaration] [csv] [options]
  
  mode: "direct", "wait", or "compare" (default: "compare")
  num_runs: number of times to run the experiment for each dynamic time (default: 10)
  build: "debug" or "release" (default: "release")
  
Examples:
  python run_avg_all_metrics.py wait 10
  python run_avg_all_metrics.py wait 10 release src/targets/experiments/crypto/q1.txt
  python run_avg_all_metrics.py compare 5 release
"""

import subprocess
import sys
import os
import re
import statistics

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT_SCRIPT = os.path.join(SCRIPT_DIR, "experiment.py")
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

# Parse command line arguments
MODE = sys.argv[1] if len(sys.argv) > 1 else "compare"
NUM_RUNS = int(sys.argv[2]) if len(sys.argv) > 2 else 10
BUILD = sys.argv[3] if len(sys.argv) > 3 else "release"
QUERY = sys.argv[4] if len(sys.argv) > 4 else "src/targets/experiments/aviation/q3.txt"
DECL = sys.argv[5] if len(sys.argv) > 5 else "src/targets/experiments/aviation/aviation.core"
CSV = sys.argv[6] if len(sys.argv) > 6 else "src/targets/experiments/aviation/CSV/aviation_sorted.csv"
OPTIONS = sys.argv[7] if len(sys.argv) > 7 else "src/targets/experiments/aviation/aviation_quarantine.core"

OPTIONS_PATH = os.path.join(PROJECT_ROOT, OPTIONS)

def extract_metrics_direct(output):
    """Extract metrics from direct mode output."""
    metrics = {
        'execution_time': None,
        'detection_delay': None
    }
    
    for line in output.splitlines():
        if "Query execution time" in line:
            match = re.search(r':\s*([\d.]+)s', line)
            if match:
                metrics['execution_time'] = float(match.group(1))
        if "Average detection delay" in line:
            match = re.search(r':\s*([\d.]+)', line)
            if match:
                metrics['detection_delay'] = float(match.group(1))
    
    return metrics

def extract_metrics_wait(output):
    """Extract metrics from wait mode output."""
    metrics = {
        'execution_time': None,
        'detection_delay': None
    }
    
    for line in output.splitlines():
        if "Query execution time" in line:
            match = re.search(r':\s*([\d.]+)s', line)
            if match:
                metrics['execution_time'] = float(match.group(1))
        if "Average detection delay" in line:
            match = re.search(r':\s*([\d.]+)', line)
            if match:
                metrics['detection_delay'] = float(match.group(1))
    
    return metrics

def extract_metrics_compare(output):
    """Extract metrics from compare mode output."""
    metrics = {
        'direct': {'execution_time': None, 'detection_delay': None},
        'wait': {'execution_time': None, 'detection_delay': None}
    }
    
    lines = output.splitlines()
    current_section = None
    
    for i, line in enumerate(lines):
        if "DIRECT Policy (No Quarantine)" in line:
            current_section = 'direct'
        elif "WAIT Quarantine Policy" in line:
            current_section = 'wait'
        
        if current_section == 'direct':
            if "Query execution time" in line and metrics['direct']['execution_time'] is None:
                match = re.search(r':\s*([\d.]+)s', line)
                if match:
                    metrics['direct']['execution_time'] = float(match.group(1))
            if "Average detection delay" in line and metrics['direct']['detection_delay'] is None:
                match = re.search(r':\s*([\d.]+)', line)
                if match:
                    metrics['direct']['detection_delay'] = float(match.group(1))
        
        elif current_section == 'wait':
            if "Query execution time" in line and metrics['wait']['execution_time'] is None:
                match = re.search(r':\s*([\d.]+)s', line)
                if match:
                    metrics['wait']['execution_time'] = float(match.group(1))
            if "Average detection delay" in line and metrics['wait']['detection_delay'] is None:
                match = re.search(r':\s*([\d.]+)', line)
                if match:
                    metrics['wait']['detection_delay'] = float(match.group(1))
    
    return metrics

def read_options_file():
    """Read the options file contents."""
    with open(OPTIONS_PATH, 'r') as f:
        return f.read()

def write_options_file(contents):
    """Write the options file contents."""
    with open(OPTIONS_PATH, 'w') as f:
        f.write(contents)

def get_dynamic_times_from_options(options_contents):
    """Extract and calculate NEW_FIXED_TIME values to test from the options file."""
    match = re.search(r'NEW_FIXED_TIME\s+(\d+)\s+seconds', options_contents)
    if not match:
        return []
    
    number = int(match.group(1))
    dynamic_times = []
    
    x = number
    while x >= 1:
        dynamic_times.append(int(x))
        x /= 2
    
    return sorted(dynamic_times)

def update_dynamic_time(options_contents, dynamic_time):
    """Update the NEW_FIXED_TIME value in the options contents."""
    return re.sub(r'NEW_FIXED_TIME\s+\d+\s+seconds',
                  f'NEW_FIXED_TIME {dynamic_time} seconds',
                  options_contents)

def run_experiment(run_num, total_runs, dynamic_time=None):
    """Run a single experiment and return its metrics."""
    print(f"  Run {run_num}/{total_runs}...", end=" ", flush=True)
    
    cmd = [
        "python3",
        EXPERIMENT_SCRIPT,
        MODE,
        BUILD,
        QUERY,
        DECL,
        CSV,
        OPTIONS
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if MODE == "direct":
            metrics = extract_metrics_direct(result.stdout)
        elif MODE == "wait":
            metrics = extract_metrics_wait(result.stdout)
        elif MODE == "compare":
            metrics = extract_metrics_compare(result.stdout)
        else:
            print(f"❌ Unknown mode: {MODE}")
            return None
        
        print("✓")
        return metrics
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        return None

def calculate_statistics(values):
    """Calculate mean, std dev, min, max for a list of values."""
    if not values:
        return None
    
    return {
        'mean': statistics.mean(values),
        'stdev': statistics.stdev(values) if len(values) > 1 else 0.0,
        'min': min(values),
        'max': max(values),
        'median': statistics.median(values)
    }

def print_statistics_direct(all_metrics):
    """Print statistics for direct mode."""
    print("\n" + "="*70)
    print("📊 AGGREGATED RESULTS (DIRECT MODE)")
    print("="*70)
    
    execution_times = [m['execution_time'] for m in all_metrics if m['execution_time'] is not None]
    detection_delays = [m['detection_delay'] for m in all_metrics if m['detection_delay'] is not None]
    
    if execution_times:
        stats = calculate_statistics(execution_times)
        print(f"\n⏱️  Query execution time (seconds):")
        print(f"  Mean:   {stats['mean']:.2f}s")
        print(f"  StdDev: {stats['stdev']:.2f}s")
        print(f"  Min:    {stats['min']:.2f}s")
        print(f"  Max:    {stats['max']:.2f}s")
        print(f"  Median: {stats['median']:.2f}s")
    
    if detection_delays:
        stats = calculate_statistics(detection_delays)
        print(f"\n🎯 Average detection delay (seconds):")
        print(f"  Mean:   {stats['mean']:.5f}s")
        print(f"  StdDev: {stats['stdev']:.5f}s")
        print(f"  Min:    {stats['min']:.5f}s")
        print(f"  Max:    {stats['max']:.5f}s")
        print(f"  Median: {stats['median']:.5f}s")

def print_statistics_wait(all_metrics):
    """Print statistics for wait mode."""
    print("\n" + "="*70)
    print("📊 AGGREGATED RESULTS (WAIT MODE)")
    print("="*70)
    
    execution_times = [m['execution_time'] for m in all_metrics if m['execution_time'] is not None]
    detection_delays = [m['detection_delay'] for m in all_metrics if m['detection_delay'] is not None]
    
    if execution_times:
        stats = calculate_statistics(execution_times)
        print(f"\n⏱️  Query execution time (seconds):")
        print(f"  Mean:   {stats['mean']:.2f}s")
        print(f"  StdDev: {stats['stdev']:.2f}s")
        print(f"  Min:    {stats['min']:.2f}s")
        print(f"  Max:    {stats['max']:.2f}s")
        print(f"  Median: {stats['median']:.2f}s")
    
    if detection_delays:
        stats = calculate_statistics(detection_delays)
        print(f"\n🎯 Average detection delay (seconds):")
        print(f"  Mean:   {stats['mean']:.5f}s")
        print(f"  StdDev: {stats['stdev']:.5f}s")
        print(f"  Min:    {stats['min']:.5f}s")
        print(f"  Max:    {stats['max']:.5f}s")
        print(f"  Median: {stats['median']:.5f}s")

def print_statistics_compare(all_metrics):
    """Print statistics for compare mode."""
    print("\n" + "="*70)
    print("📊 AGGREGATED RESULTS (COMPARE MODE)")
    print("="*70)
    
    # Direct mode statistics
    print("\n" + "-"*70)
    print("🔵 DIRECT MODE STATISTICS")
    print("-"*70)
    
    direct_exec_times = [m['direct']['execution_time'] for m in all_metrics if m['direct']['execution_time'] is not None]
    direct_det_delays = [m['direct']['detection_delay'] for m in all_metrics if m['direct']['detection_delay'] is not None]
    
    if direct_exec_times:
        stats = calculate_statistics(direct_exec_times)
        print(f"\n⏱️  Execution time (seconds):")
        print(f"  Mean:   {stats['mean']:.2f}s")
        print(f"  StdDev: {stats['stdev']:.2f}s")
        print(f"  Min:    {stats['min']:.2f}s")
        print(f"  Max:    {stats['max']:.2f}s")
        print(f"  Median: {stats['median']:.2f}s")
    
    if direct_det_delays:
        stats = calculate_statistics(direct_det_delays)
        print(f"\n🎯 Detection delay (seconds):")
        print(f"  Mean:   {stats['mean']:.5f}s")
        print(f"  StdDev: {stats['stdev']:.5f}s")
        print(f"  Min:    {stats['min']:.5f}s")
        print(f"  Max:    {stats['max']:.5f}s")
        print(f"  Median: {stats['median']:.5f}s")
    
    # Wait mode statistics
    print("\n" + "-"*70)
    print("🟢 WAIT MODE STATISTICS")
    print("-"*70)
    
    wait_exec_times = [m['wait']['execution_time'] for m in all_metrics if m['wait']['execution_time'] is not None]
    wait_det_delays = [m['wait']['detection_delay'] for m in all_metrics if m['wait']['detection_delay'] is not None]
    
    if wait_exec_times:
        stats = calculate_statistics(wait_exec_times)
        print(f"\n⏱️  Execution time (seconds):")
        print(f"  Mean:   {stats['mean']:.2f}s")
        print(f"  StdDev: {stats['stdev']:.2f}s")
        print(f"  Min:    {stats['min']:.2f}s")
        print(f"  Max:    {stats['max']:.2f}s")
        print(f"  Median: {stats['median']:.2f}s")
    
    if wait_det_delays:
        stats = calculate_statistics(wait_det_delays)
        print(f"\n🎯 Detection delay (seconds):")
        print(f"  Mean:   {stats['mean']:.5f}s")
        print(f"  StdDev: {stats['stdev']:.5f}s")
        print(f"  Min:    {stats['min']:.5f}s")
        print(f"  Max:    {stats['max']:.5f}s")
        print(f"  Median: {stats['median']:.5f}s")

def main():
    print("="*70)
    print(f"🧪 RUNNING {NUM_RUNS} EXPERIMENTS PER DYNAMIC TIME VALUE")
    print("="*70)
    print(f"Mode:        {MODE.upper()}")
    print(f"Build:       {BUILD}")
    print(f"Query:       {QUERY}")
    print(f"Declaration: {DECL}")
    print(f"CSV:         {CSV}")
    print(f"Options:     {OPTIONS}")
    print("="*70)
    
    # Test different dynamic times for all modes
    if MODE in ["direct", "wait", "compare"]:
        # Read original options file
        original_options = read_options_file()
        
        # Get dynamic time values to test
        dynamic_times = get_dynamic_times_from_options(original_options)
        
        if not dynamic_times:
            print("❌ No NEW_FIXED_TIME found in options file!")
            sys.exit(1)
        
        print(f"\n📋 Dynamic times to test: {dynamic_times}")
        print(f"🔁 Running {NUM_RUNS} experiments for each dynamic time value\n")
        
        # Store averages for each dynamic time
        avg_exec_times = []
        avg_det_delays = []
        
        # Run experiments for each dynamic time
        for dynamic_time in dynamic_times:
            print(f"\n{'='*70}")
            print(f"⏱️  Testing NEW_FIXED_TIME = {dynamic_time} seconds")
            print(f"{'='*70}")
            
            # Update options file with new dynamic time
            updated_options = update_dynamic_time(original_options, dynamic_time)
            write_options_file(updated_options)
            
            # Run NUM_RUNS experiments
            all_metrics = []
            successful_runs = 0
            
            for i in range(1, NUM_RUNS + 1):
                metrics = run_experiment(i, NUM_RUNS, dynamic_time)
                if metrics:
                    all_metrics.append(metrics)
                    successful_runs += 1
            
            if successful_runs == 0:
                print(f"  ⚠️  No successful runs for dynamic_time={dynamic_time}")
                avg_exec_times.append(None)
                avg_det_delays.append(None)
                continue
            
            # Calculate averages for this dynamic time
            if MODE == "direct":
                exec_times = [m['execution_time'] for m in all_metrics if m['execution_time'] is not None]
                det_delays = [m['detection_delay'] for m in all_metrics if m['detection_delay'] is not None]
                
                if exec_times:
                    avg_time = statistics.mean(exec_times)
                    avg_exec_times.append(avg_time)
                    print(f"\n  ⏱️  Average execution time: {avg_time:.2f}s (from {successful_runs}/{NUM_RUNS} runs)")
                else:
                    avg_exec_times.append(None)
                
                if det_delays:
                    avg_delay = statistics.mean(det_delays)
                    avg_det_delays.append(avg_delay)
                    print(f"  🎯 Average detection delay: {avg_delay:.5f}s (from {successful_runs}/{NUM_RUNS} runs)")
                else:
                    avg_det_delays.append(None)
            
            elif MODE == "wait":
                exec_times = [m['execution_time'] for m in all_metrics if m['execution_time'] is not None]
                det_delays = [m['detection_delay'] for m in all_metrics if m['detection_delay'] is not None]
                
                if exec_times:
                    avg_time = statistics.mean(exec_times)
                    avg_exec_times.append(avg_time)
                    print(f"\n  ⏱️  Average execution time: {avg_time:.2f}s (from {successful_runs}/{NUM_RUNS} runs)")
                else:
                    avg_exec_times.append(None)
                
                if det_delays:
                    avg_delay = statistics.mean(det_delays)
                    avg_det_delays.append(avg_delay)
                    print(f"  🎯 Average detection delay: {avg_delay:.5f}s (from {successful_runs}/{NUM_RUNS} runs)")
                else:
                    avg_det_delays.append(None)
                    
            elif MODE == "compare":
                wait_exec_times = [m['wait']['execution_time'] for m in all_metrics if m['wait']['execution_time'] is not None]
                wait_det_delays = [m['wait']['detection_delay'] for m in all_metrics if m['wait']['detection_delay'] is not None]
                
                if wait_exec_times:
                    avg_time = statistics.mean(wait_exec_times)
                    avg_exec_times.append(avg_time)
                    print(f"\n  ⏱️  Average wait execution time: {avg_time:.2f}s (from {successful_runs}/{NUM_RUNS} runs)")
                else:
                    avg_exec_times.append(None)
                
                if wait_det_delays:
                    avg_delay = statistics.mean(wait_det_delays)
                    avg_det_delays.append(avg_delay)
                    print(f"  🎯 Average wait detection delay: {avg_delay:.5f}s (from {successful_runs}/{NUM_RUNS} runs)")
                else:
                    avg_det_delays.append(None)
        
        # Restore original options file
        write_options_file(original_options)
        
        # Print final results
        print("\n" + "="*70)
        print("📊 FINAL RESULTS: Average Execution Times & Detection Delays")
        print("="*70)
        print(f"\nDynamic Times: {tuple(dynamic_times)}")
        print(f"\nExecution Times (s):")
        print(f"  Values: {tuple(f'{t:.2f}' if t is not None else 'N/A' for t in avg_exec_times)}")
        print(f"\nDetection Delays (s):")
        print(f"  Values: {tuple(f'{d:.5f}' if d is not None else 'N/A' for d in avg_det_delays)}")
        print("="*70)
    
    else:
        print(f"\n❌ Unknown mode: {MODE}!")
        print("Available modes: direct, wait, compare")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("✨ EXPERIMENT COMPLETED")
    print("="*70)

if __name__ == "__main__":
    main()
