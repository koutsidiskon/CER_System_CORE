# compare_csv.py
import os

def compare_csv_files(file1, file2):
    name1 = os.path.basename(file1)
    name2 = os.path.basename(file2)

    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        lines1 = [line.strip() for line in f1.readlines()]
        lines2 = [line.strip() for line in f2.readlines()]

    len1, len2 = len(lines1), len(lines2)
    print(f"File 1: {name1} → {len1} lines")
    print(f"File 2: {name2} → {len2} lines\n")

    # Compare line by line
    min_len = min(len1, len2)
    differences = []

    for i in range(min_len):
        if lines1[i] != lines2[i]:
            differences.append((i + 1, lines1[i], lines2[i]))

    if len1 != len2:
        print("⚠️ The files have a different number of lines.\n")
        print(f"{name1} has {len1} lines, {name2} has {len2} lines.\n")

    if differences:
        print(f"❌ Found {len(differences)} differing lines.\n")
    else:
        print("✅ The files are identical (up to the shortest length).")


def compare_lines_anywhere(file1, file2):
    name1 = os.path.basename(file1)
    name2 = os.path.basename(file2)

    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        lines1 = [line.strip() for line in f1.readlines() if line.strip()]
        lines2 = [line.strip() for line in f2.readlines() if line.strip()]

    set2 = set(lines2)
    found = []
    missing = []

    for i, line in enumerate(lines1, start=1):
        if line in set2:
            found.append(line)
        else:
            missing.append((i, line))

    print(f"File 1: {name1} → {len(lines1)} lines")
    print(f"File 2: {name2} → {len(lines2)} lines\n")

    print(f"✅ Found {len(found)} lines from {name1} also in {name2}.")
    print(f"❌ Missing {len(missing)} lines from {name1} not found in {name2}.\n")


# Example usage
if __name__ == "__main__":
    file1 = "../logs/logfile_experiment_direct.log"
    file2 = "../logs/logfile_experiment_wait.log"
    #compare_csv_files(file1, file2)
    compare_lines_anywhere(file1, file2)

