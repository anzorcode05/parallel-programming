import os
import subprocess
import csv
import time

MATRIX_SIZES = [200, 400, 800, 1200, 1600, 2000]
THREAD_COUNTS = [1, 2, 4, 8]

EXECUTABLE = './main.exe'
RESULTS_FILE = 'stats_omp.csv'


def generate_matrices(size):
    print(f"    Generating {size}x{size} matrices...")
    result = subprocess.run(
        f"python gen_data.py {size}",
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode == 0


def run_multiplication(threads):
    result = subprocess.run(
        f"{EXECUTABLE} {threads}",
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return None

    output = result.stdout
    for line in output.split('\n'):
        if 'Computation time:' in line:
            time_str = line.split(':')[1].strip().split()[0]
            return float(time_str)

    return None


def main():
    print("=" * 60)
    print("OpenMP Matrix Multiplication Benchmark")
    print("=" * 60)

    if not os.path.exists(EXECUTABLE):
        print(f"ERROR: {EXECUTABLE} not found!")
        print("Compile: g++ -fopenmp -std=c++11 main.cpp -o main.exe")
        return

    results = []

    for size in MATRIX_SIZES:
        print(f"\n>>> Matrix size: {size}x{size}")

        if not generate_matrices(size):
            print(f"    Failed to generate matrices for size {size}")
            continue

        for threads in THREAD_COUNTS:
            print(f"    Threads: {threads}")

            times = []
            for run in range(3):
                print(f"        Run {run + 1}/3...", end=" ")
                t = run_multiplication(threads)
                if t is not None:
                    times.append(t)
                    print(f"{t:.4f} sec")
                else:
                    print("FAILED")

            if times:
                avg_time = sum(times) / len(times)
                print(f"        Average: {avg_time:.4f} sec")

                results.append({
                    'Size': size,
                    'Threads': threads,
                    'Time_sec': avg_time,
                    'Operations': size ** 3
                })

    if results:
        with open(RESULTS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Size', 'Threads', 'Time_sec', 'Operations'])
            writer.writeheader()
            writer.writerows(results)

        print("\n" + "=" * 60)
        print(f"Results saved to {RESULTS_FILE}")

        print("\nSUMMARY:")
        print("-" * 50)
        for r in results:
            print(f"  {r['Size']}x{r['Size']} | {r['Threads']} threads | {r['Time_sec']:.4f} sec")
    else:
        print("\nNo results collected!")


if __name__ == "__main__":
    main()