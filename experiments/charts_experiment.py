"""
Usage:
  python experiment.py [mode] [build] [query] [declaration] [csv] [options]
"""
import subprocess, os, shlex, re, csv, sys, time
import pandas as pd
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

BUILD = (sys.argv[1].lower() if len(sys.argv) > 2 else "release")
QUERY = sys.argv[3] if len(sys.argv) > 3 else "src/targets/experiments/crypto/q3.txt"
DECL = sys.argv[4] if len(sys.argv) > 4 else "src/targets/experiments/crypto/crypto.core"
CSV_ORDERED = sys.argv[5] if len(sys.argv) > 5 else "src/targets/experiments/crypto/CSV/crypto.csv"
CSV = sys.argv[5] if len(sys.argv) > 5 else "src/targets/experiments/crypto/CSV/crypto.csv"
OPTIONS = sys.argv[6] if len(sys.argv) > 6 else "src/targets/experiments/crypto/crypto_quarantine.core"
DIR = "Debug" if BUILD == "debug" else "Release"
MOUNT_FLAGS = ["-v", f"{PROJECT_ROOT}:/workspace", "-w", "/workspace"]
ENV_FLAG = ["-e", "TRACY_NO_INVARIANT_CHECK=1"]
PLATFORM_FLAG = ["--platform", "linux/amd64"]
IMG_LOCAL = "core-dev"

CSV_PATH = os.path.join(PROJECT_ROOT, CSV)
QUERY_PATH = os.path.join(PROJECT_ROOT, QUERY)
OPTIONS_PATH = os.path.join(PROJECT_ROOT, OPTIONS)
CMD_WITHOUT_QUARANTINE = [f"/CORE/build/{DIR}/offline", "--query", f"/workspace/{QUERY}", "--declaration", f"/workspace/{DECL}", "--csv", f"/workspace/{CSV_ORDERED}"]
CMD_WITH_QUARANTINE = [f"/CORE/build/{DIR}/offline", "--query", f"/workspace/{QUERY}", "--declaration", f"/workspace/{DECL}", "--csv", f"/workspace/{CSV}", "--options", f"/workspace/{OPTIONS}"]

def count_events(csv_path):
    with open(csv_path) as f:
        return sum(1 for _ in f) - 1
    
def extract_events(output):
    received_order = []
    sent_order = []
    complex_events = []
    
    for line in output.splitlines():
        if "QUARANTINE RECEIVE: event time=" in line:
            match = re.search(r"time=(\d+)", line)
            if match:
                received_order.append(int(match.group(1)))
        
        if "QUARANTINE SEND: event time=" in line or "QUARANTINE FORCE SEND EVENT: time=" in line:
            match = re.search(r"time=(\d+)", line)
            if match:
                sent_order.append(int(match.group(1)))
        
        # Extract complex events (query results)
        if line.strip().startswith('[') and '], ((' in line:
            match = re.search(r'^\[(\d+),(\d+)\],', line.strip())
            if match:
                time1, time2 = int(match.group(1)), int(match.group(2))
                complex_events.append([time1, time2])
                    
    return received_order, sent_order, complex_events

def run_test(description, cmd, query_contents, options_contents=None):
    drops = 0
    received = 0
    sent = 0
    avg_detection_delay = 0.0
    max_quarantine_size = 0
    max_quarantine_size_mb = 0.0
    max_quarantine_size_mb = 0.0

    t0 = time.perf_counter()
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    elapsed_time = time.perf_counter() - t0

    if options_contents is None:
        log_file = open(os.path.join(PROJECT_ROOT, "logs/logfile_experiment_direct.log"), "w")
        quarantine_file = open(os.path.join(PROJECT_ROOT, "logs/logfile_quarantine.log"), "w")
    elif options_contents is not None:
        quarantine_file = open(os.path.join(PROJECT_ROOT, "logs/logfile_quarantine.log"), "w")
        result_log_file = open(os.path.join(PROJECT_ROOT, "logs/logfile_experiment_wait.log"), "w")

    for line in result.stdout.splitlines():
        if options_contents is None:
            if line.startswith('['):
                log_file.write(f"{line.split(') )')[0]}" + ") )\n")
            if line.startswith("Drops: "):
                match = re.search(r"(\d+)", line)
                if match:
                    drops = int(match.group(1))
            elif line.startswith("Average detection delay: "):
                match = re.search(r"([\d.]+)", line) 
                if match:
                    avg_detection_delay = float(match.group(1))
                    quarantine_file.write(f"{line}\n")
            else:
                quarantine_file.write(f"{line}\n")
        elif options_contents is not None:
            if line.startswith("STREAMING"):
                quarantine_file.write(f"\n{line}\n")
            elif line.startswith('['):
                result_log_file.write(f"{line.split(') )')[0]}" + ") )\n")
            else:
                if line.startswith("Number of events DROPPED"):
                    match = re.search(r"\d+", line)
                    if match:
                        drops = int(match.group())
                elif line.startswith("Number of events RECEIVED"):
                    match = re.search(r"\d+", line)
                    if match:
                        received = int(match.group())
                elif line.startswith("Number of events SENT"):
                    match = re.search(r"\d+", line)
                    if match:
                        sent = int(match.group())
                elif line.startswith("Average detection delay: "):
                    match = re.search(r"([\d.]+)", line) 
                    if match:
                        avg_detection_delay = float(match.group(1))
                elif line.startswith("Maximum quarantine size: "):
                    match = re.search(r"([\d.]+)", line) 
                    if match:
                        max_quarantine_size = int(match.group(1))
                elif line.startswith("Maximum quarantine buffer size (MB): "):
                    match = re.search(r"([\d.]+)", line) 
                    if match:
                        max_quarantine_size_mb = float(match.group(1))
                quarantine_file.write(f"{line}\n")
    
    if options_contents is None:
        num_results = sum(1 for line in result.stdout.splitlines() if line.strip().startswith('['))
        return num_results, elapsed_time, drops, avg_detection_delay
    
    received_order, sent_order, complex_events = extract_events(result.stdout)

    return received_order, sent_order, complex_events, elapsed_time, drops, avg_detection_delay, max_quarantine_size, max_quarantine_size_mb

if __name__ == "__main__":
    if subprocess.call(["docker", "image", "inspect", IMG_LOCAL], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):
        print("Building local image (core-dev)…")
        subprocess.run([
            "docker", "buildx", "build", *PLATFORM_FLAG,
            "--target", "build", "-t", IMG_LOCAL, ".",
            "--load"
        ], check=True, cwd=PROJECT_ROOT)

    with open(QUERY_PATH, 'r') as f:
        query_contents = '  '.join(line.strip() + '\n' for line in f)

    with open(OPTIONS_PATH, 'r') as f:
        options_contents = '  '.join(line.strip() + '\n' for line in f)

    print("\nQuery:\n  " + query_contents)

    match = re.search(r'DYNAMIC_TIME\s+(\d+)\s+seconds', options_contents)
    number = None
    quarantine_times = []
    if match:
        number = int(match.group(1))
    
    x = number
    while x >= 1:
        quarantine_times.append(int(x))
        x /= 2
        '''if x > 512:
            x /= 2
        else:
            x /= 8'''

    '''x = number
    for i in range(4):
        quarantine_times.append(int(x))
        x *= 2'''

    quarantine_times = sorted(quarantine_times)
    print(f"\nQuarantine times to test: {quarantine_times}\n")

    execution_time = []
    throughput = []
    numOfResults = []
    numOfDrops = []
    avgDetectionDelays = []
    maxQuarantineSizes = []
    maxQuarantineSizesMB = []
    
    results_labels = ["Execution Time (s)", "Throughput (results/s)", "Number of Results", "Number of Drops", "Average Detection Delay (s)"]

    cmd_direct = ["docker", "run", "--rm", *PLATFORM_FLAG, *ENV_FLAG, *MOUNT_FLAGS, IMG_LOCAL, *CMD_WITHOUT_QUARANTINE]
    num_results_direct, direct_core_time, direct_drops, direct_avg_detection_delay = run_test("DIRECT Policy (No Quarantine)", cmd_direct, query_contents)

    for i in quarantine_times:
        options_contents = re.sub(r'DYNAMIC_TIME\s+\d+\s+seconds',
                    f'DYNAMIC_TIME {i} seconds',
                    options_contents)

        with open(OPTIONS_PATH, "w") as f:
            f.write(options_contents)

        cmd_wait = ["docker", "run", "--rm", *PLATFORM_FLAG, *ENV_FLAG, *MOUNT_FLAGS, IMG_LOCAL, *CMD_WITH_QUARANTINE]
        received_wait, sent_wait, events_wait, core_time, drops, avg_detection_delay, max_quarantine_size, max_quarantine_size_mb = run_test("WAIT Quarantine Policy", cmd_wait, query_contents, options_contents)
        execution_time.append(round(core_time,2))
        throughput.append(round((num_results_direct / core_time),2))
        numOfResults.append(len(events_wait))
        numOfDrops.append(drops)
        avgDetectionDelays.append(round(avg_detection_delay,5))
        maxQuarantineSizes.append(max_quarantine_size)
        maxQuarantineSizesMB.append(max_quarantine_size_mb)
    
    print("== Quarantine Time ==", end="")
    for i in range(len(results_labels)):
        print(f"== {results_labels[i]} ==", end="")
    print()
    print(f"       direct        ", end="")
    print(f"         {round(direct_core_time,2)}        ", end="")
    print(f"              {round(num_results_direct / direct_core_time,2)}            ", end="")
    print(f"          {num_results_direct}            ", end="")
    print(f"       {direct_drops}            ", end="")
    for i in range(len(quarantine_times)):
        print()
        if quarantine_times[i] < 10:
            print(f"       {quarantine_times[i]}s          ", end="")
            print(f"           {execution_time[i]}       ", end="")
            print(f"              {throughput[i]}        ", end="")
            print(f"              {numOfResults[i]}       ", end="")
            print(f"              {numOfDrops[i]}            ", end="")
        else:
            print(f"       {quarantine_times[i]}s         ", end="")
            print(f"           {execution_time[i]}       ", end="")
            print(f"              {throughput[i]}        ", end="")
            print(f"              {numOfResults[i]}       ", end="")
            print(f"              {numOfDrops[i]}            ", end="")
    print()

    # ======= Execution Time =======
    plt.figure(figsize=(15,8))
    
    # Use evenly spaced x-positions
    x_pos = range(len(quarantine_times))
    
    # Plot with evenly spaced x-positions
    plt.plot(x_pos, execution_time, 'o-', color='tab:orange', label='WAIT Policy')
    
    # Add value labels on top of each point
    y_min, y_max = min(execution_time), max(execution_time)
    y_range = y_max - y_min if y_max > y_min else 1
    offset = y_range * 0.02  # Reduced from 5% to 2% of the y-range as offset
    
    for x, y in zip(x_pos, execution_time):
        plt.text(x, y + offset, f"{y:.2f}", 
                ha='center', fontsize=9, va='bottom')
    
    # Set x-ticks to show the actual quarantine times
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title(f'Execution Time vs Quarantine Fixed Time\n(DIRECT: {direct_core_time:.2f}s)', pad=10)
    plt.xlabel('Quarantine Fixed Time (s)')
    plt.ylabel('Execution Time (s)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig("Execution Time.png", dpi=300, bbox_inches='tight')
    #plt.show()

    # ======= Throughput =======
    plt.figure(figsize=(15,8))
    
    # Plot with evenly spaced x-positions
    x_pos = range(len(quarantine_times))
    plt.plot(x_pos, throughput, 'o-', color='tab:blue', label='WAIT Policy')
    
    # Add value labels on top of each point
    y_min, y_max = min(throughput), max(throughput)
    y_range = y_max - y_min if y_max > y_min else 1
    offset = y_range * 0.02  # Reduced from 5% to 2% of the y-range as offset
    
    for x, y in zip(x_pos, throughput):
        plt.text(x, y + offset, f"{y:.2f}", 
                ha='center', fontsize=9, va='bottom')
    
    # Set x-ticks to show the actual quarantine times
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title(f'Query Throughput vs Quarantine Fixed Time\n(DIRECT: {num_results_direct/direct_core_time:.2f} results/s)', pad=10)
    plt.xlabel('Quarantine Fixed Time (s)')
    plt.ylabel('Throughput (results/sec)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig("Throughput.png", dpi=300, bbox_inches='tight')
    #plt.show()

    # ======= Results Found =======
    plt.figure(figsize=(15,8))
    
    # Plot with evenly spaced x-positions
    x_pos = range(len(quarantine_times))
    plt.plot(x_pos, numOfResults, 'o-', color='tab:green', label='DYNAMIC Policy')
    
    # Add value labels on top of each point
    y_min, y_max = min(numOfResults), max(numOfResults)
    y_range = y_max - y_min if y_max > y_min else 1
    offset = y_range * 0.01  # Reduced from 5% to 1% of the y-range as offset
    
    for x, y in zip(x_pos, numOfResults):
        plt.text(x, y + offset, f"{y}", 
                ha='center', fontsize=9, va='bottom')
    
    # Set x-ticks to show the actual quarantine times
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title(f'Complex Events Found vs Quarantine Fixed Time\n(DIRECT: {num_results_direct} results)', pad=10)
    plt.xlabel('Quarantine Fixed Time (s)')
    plt.ylabel('Number of Results')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig("Results.png", dpi=300, bbox_inches='tight')
    #plt.show()

    # ======= Drops =======
    plt.figure(figsize=(15,8))
    
    # Plot with evenly spaced x-positions
    x_pos = range(len(quarantine_times))
    plt.plot(x_pos, numOfDrops, 'o-', color='tab:red', label='Dropped Events')
    
    # Add value labels on top of each point
    y_min, y_max = min(numOfDrops), max(numOfDrops)
    y_range = y_max - y_min if y_max > y_min else 1
    offset = y_range * 0.01  # Reduced from 5% to 1% of the y-range as offset
    
    for x, y in zip(x_pos, numOfDrops):
        plt.text(x, y + offset, f"{y}", 
                ha='center', fontsize=9, va='bottom')
    
    # Set x-ticks to show the actual quarantine times
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title(f'Dropped Events vs Quarantine Fixed Time\n(DIRECT: {direct_drops} drops)', pad=10)
    plt.xlabel('Quarantine Fixed Time (s)')
    plt.ylabel('Number of Dropped Events')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig("Dropped Events.png", dpi=300, bbox_inches='tight')
    #plt.show()

    # ======= Average Detection Delay =======
    plt.figure(figsize=(15,8))
    # Plot with evenly spaced x-positions
    x_pos = range(len(quarantine_times))
    plt.plot(x_pos, avgDetectionDelays, 'o-', color='tab:pink', label='DYNAMIC Policy')
    # Add value labels on top of each point
    y_min, y_max = min(avgDetectionDelays), max(avgDetectionDelays)
    y_range = y_max - y_min if y_max > y_min else 1
    offset = y_range * 0.02  # Reduced from 5% to
    for x, y in zip(x_pos, avgDetectionDelays):
        plt.text(x, y + offset, f"{y:.5f}", 
                ha='center', fontsize=9, va='bottom')
    # Set x-ticks to show the actual quarantine times
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title(f'Average Detection Delay vs Quarantine Fixed Time\n', pad=10)
    plt.xlabel('Quarantine Fixed Time (s)')
    plt.ylabel('Average Detection Delay (s)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig("Average Detection Delay.png", dpi=300, bbox_inches='tight')
    #plt.show()

    # ======= Maximum Quarantine Size =======
    plt.figure(figsize=(15,8))
    
    # Plot with evenly spaced x-positions
    x_pos = range(len(quarantine_times))
    plt.plot(x_pos, maxQuarantineSizes, 'o-', color='tab:purple', label='Max Quarantine Size')
    
    # Add value labels on top of each point
    y_min, y_max = min(maxQuarantineSizes), max(maxQuarantineSizes)
    y_range = y_max - y_min if y_max > y_min else 1
    offset = y_range * 0.02  # 2% of the y-range as offset
    
    for x, y in zip(x_pos, maxQuarantineSizes):
        plt.text(x, y + offset, f"{y}", 
                ha='center', fontsize=9, va='bottom')
    
    # Set x-ticks to show the actual quarantine times
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title(f'Maximum Quarantine Size vs Quarantine Fixed Time', pad=10)
    plt.xlabel('Quarantine Fixed Time (s)')
    plt.ylabel('Maximum Quarantine Size (events)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig("Maximum Quarantine Size.png", dpi=300, bbox_inches='tight')
    #plt.show() 

    # ======= Maximum Quarantine Size (MB) =======
    plt.figure(figsize=(15,8))

    # Plot with evenly spaced x-positions
    x_pos = range(len(quarantine_times))
    plt.plot(x_pos, maxQuarantineSizesMB, 'o-', color='tab:brown', label='Max Quarantine Size (MB)')

    # Add value labels on top of each point
    y_min, y_max = min(maxQuarantineSizesMB), max(maxQuarantineSizesMB)
    y_range = y_max - y_min if y_max > y_min else 1
    offset = y_range * 0.02  # 2% of the y-range as offset

    for x, y in zip(x_pos, maxQuarantineSizesMB):
        plt.text(x, y + offset, f"{y:.4f}",
                ha='center', fontsize=9, va='bottom')

    # Set x-ticks to show the actual quarantine times
    plt.xticks(x_pos, [str(t) for t in quarantine_times], fontsize=8, rotation=45)
    plt.title('Maximum Quarantine Size (MB) vs Quarantine Fixed Time', pad=10)
    plt.xlabel('Quarantine Fixed Time (s)')
    plt.ylabel('Maximum Quarantine Size (MB)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig("Maximum Quarantine Size (MB).png", dpi=300, bbox_inches='tight')
    #plt.show() 
    

    options_contents = re.sub(r'DYNAMIC_TIME\s+\d+\s+seconds',
                    f'DYNAMIC_TIME {number} seconds',
                    options_contents)
    
    with open(OPTIONS_PATH, "w") as f:
            f.write(options_contents)
    
    # Print all results as tuples
    print("\n" + "="*70)
    print("📊 RESULTS AS TUPLES")
    print("="*70)
    print(f"\nQuarantine Times: {tuple(quarantine_times)}")
    print(f"Execution Time (s): {tuple(execution_time)}")
    print(f"Throughput (results/s): {tuple(throughput)}")
    print(f"Number of Results: {tuple(numOfResults)}")
    print(f"Number of Drops: {tuple(numOfDrops)}")
    print(f"Average Detection Delays (s): {tuple(avgDetectionDelays)}")
    print(f"Maximum Quarantine Sizes: {tuple(maxQuarantineSizes)}")
    print(f"Maximum Quarantine Sizes (MB): {tuple(maxQuarantineSizesMB)}")
    print("="*70)
        
        
