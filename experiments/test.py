# compare_csv.py
import os
def compare_csv_files(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        lines1 = [line.strip() for line in f1.readlines()]
        lines2 = [line.strip() for line in f2.readlines()]

    len1, len2 = len(lines1), len(lines2)
    print(f"File 1: {file1} → {len1} lines")
    print(f"File 2: {file2} → {len2} lines\n")

    # Compare line by line
    min_len = min(len1, len2)
    differences = []

    for i in range(min_len):
        if lines1[i] != lines2[i]:
            differences.append((i + 1, lines1[i], lines2[i]))

    if len1 != len2:
        print("⚠️ The files have a different number of lines.\n")
        print(f"File 1 has {len1} lines, File 2 has {len2} lines.\n")

    if differences:
        print(f"❌ Found {len(differences)} differing lines:\n")
        #for line_num, line1, line2 in differences:
          #  print(f"Line {line_num}:")
          #  print(f"  File 1 → {line1}")
          # print(f"  File 2 → {line2}\n")
    else:
        print("✅ The files are identical (up to the shortest length).")


# Example usage
if __name__ == "__main__":
    file1 = "../src/targets/experiments/stocks/expected_results/other-q2_any.txt"
    file2 = "../logs/logfile_experiment_direct.log"
    compare_csv_files(file1, file2)
