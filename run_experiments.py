import os
import re
import subprocess
import csv


MATRIX_SIZES = [10, 50, 100, 500, 1000]

OUTPUT_CSV = 'stats.csv'

EXECUTABLE = './main'


def execute_command(command, description):
    """Выполняет shell-команду и возвращает результат"""
    print(f"{description}...")

    process = subprocess.run(command, shell=True, capture_output=True, text=True)

    if process.returncode != 0:
        print(f"    ERROR: {process.stderr.strip()}")
        return False, ""

    return True, process.stdout


def main():
    print("STARTING EXPERIMENTS")
    print("=" * 50)


    if not os.path.exists(EXECUTABLE):
        print(f"Executable not found: {EXECUTABLE}")
        print("Compile with: g++ -std=c++11 main.cpp -o main")
        return

    results = []

    for size in MATRIX_SIZES:
        print(f"\n>>> Testing N = {size}")


        success, _ = execute_command(
            f"python gen_data.py {size}",
            f"Generating {size}x{size} matrices"
        )
        if not success:
            continue


        success, program_output = execute_command(
            EXECUTABLE,
            "Computing matrix product"
        )
        if not success:
            continue


        time_match = re.search(r"Computation time:\s*([\d.]+)\s*seconds", program_output)
        exec_time = float(time_match.group(1)) if time_match else 0.0
        print(f"    Execution time: {exec_time} seconds")


        total_ops = size ** 3
        print(f"    Total operations: {total_ops:,}")

        # Верификация результата
        success, verify_output = execute_command(
            "python check_result.py",
            "Verifying result correctness"
        )

        if success and "VALID" in verify_output:
            status = "PASSED"
            print("    Status: PASSED")
        else:
            status = "FAILED"
            print("    Status: FAILED")

        results.append({
            'Size': size,
            'Time_sec': exec_time,
            'Operations': total_ops,
            'Status': status
        })


    if results:
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Size', 'Time_sec', 'Operations', 'Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print("\n" + "=" * 50)
        print(f"Results saved to {OUTPUT_CSV}")


        print("\nSummary:")
        print("-" * 50)
        for r in results:
            print(f"  {r['Size']}x{r['Size']}: {r['Time_sec']:.4f} sec ({r['Status']})")
        print("=" * 50)


if __name__ == "__main__":
    main()