import os
import subprocess
import csv
import time

# Размеры матриц
MATRIX_SIZES = [200, 400, 800, 1200, 1600, 2000]

# Размеры блоков (threads per block)
BLOCK_SIZES = [8, 16, 32]

RESULTS_FILE = 'stats_cuda.csv'
EXECUTABLE = './main_cuda.exe'


def generate_matrices(size):
    print(f"    Generating {size}x{size} matrices...")
    result = subprocess.run(
        f"python gen_data.py {size}",
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode == 0


def run_cuda(block_size):
    result = subprocess.run(
        f"{EXECUTABLE} {block_size}",
        shell=True,
        capture_output=True,
        text=True,
        timeout=300
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
    print("CUDA Matrix Multiplication Benchmark")
    print("=" * 60)

    if not os.path.exists(EXECUTABLE):
        print(f"ERROR: {EXECUTABLE} not found!")
        print("Compile with: nvcc -o main_cuda.exe main_cuda.cu")
        return

    results = []

    for size in MATRIX_SIZES:
        print(f"\n>>> Matrix size: {size}x{size}")

        if not generate_matrices(size):
            print(f"    Failed to generate matrices for size {size}")
            continue

        for block_size in BLOCK_SIZES:
            print(f"    Block size: {block_size}x{block_size}")

            times = []
            for run in range(3):
                print(f"        Run {run + 1}/3...", end=" ")
                t = run_cuda(block_size)
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
                    'BlockSize': block_size,
                    'Time_sec': avg_time,
                    'Operations': size ** 3
                })

    if results:
        with open(RESULTS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Size', 'BlockSize', 'Time_sec', 'Operations'])
            writer.writeheader()
            writer.writerows(results)

        print("\n" + "=" * 60)
        print(f"Results saved to {RESULTS_FILE}")

        print("\nSUMMARY:")
        print("-" * 60)
        for r in results:
            print(f"  {r['Size']}x{r['Size']} | Block {r['BlockSize']} | {r['Time_sec']:.4f} sec")
    else:
        print("\nNo results collected!")


if __name__ == "__main__":
    main()