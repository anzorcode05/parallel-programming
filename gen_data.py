import random
import sys
import os


def create_random_matrix(n, filepath):
    """Генерирует случайную квадратную матрицу размера n и сохраняет в файл"""
    random.seed(2025 + n)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w') as f:
        f.write(f"{n}\n")
        for _ in range(n):
            row = [str(random.randint(1, 50)) for _ in range(n)]
            f.write(" ".join(row) + "\n")


if __name__ == "__main__":
    matrix_size = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    print(f"Generating {matrix_size}x{matrix_size} matrices...")
    create_random_matrix(matrix_size, "data/matrixA.txt")
    create_random_matrix(matrix_size, "data/matrixB.txt")
    print("Generation complete!")