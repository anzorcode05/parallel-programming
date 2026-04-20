import numpy as np
import sys


def read_matrix_from_file(filename):
    """Читает матрицу из файла (формат: первая строка - размер)"""
    with open(filename, 'r') as f:
        size = int(f.readline().strip())
        matrix = []
        for line in f:
            if line.strip():
                row = [float(x) for x in line.split()]
                matrix.append(row)
    return matrix


def main():
    print("VERIFICATION IN PROGRESS...")

    try:
        matrix_a = read_matrix_from_file('data/matrixA.txt')
        matrix_b = read_matrix_from_file('data/matrixB.txt')
        matrix_result = read_matrix_from_file('data/matrixC.txt')

        np_a = np.array(matrix_a)
        np_b = np.array(matrix_b)
        np_result = np.array(matrix_result)

        expected = np_a @ np_b  # матричное умножение через @ (современный синтаксис)

        if np.allclose(np_result, expected, rtol=1e-5, atol=1e-8):
            print("RESULT: VALID (PASSED)")
            return 0
        else:
            print("RESULT: INVALID (FAILED)")
            max_diff = np.max(np.abs(np_result - expected))
            print(f"Maximum difference: {max_diff}")
            return 1

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return 1
    except Exception as e:
        print(f"Verification error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())