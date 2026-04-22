#include <iostream>
#include <vector>
#include <chrono>
#include <fstream>
#include <omp.h>

using namespace std;

vector<vector<double>> parallelMultiplyOpenMP(
    const vector<vector<double>>& first,
    const vector<vector<double>>& second,
    int dimension,
    int numThreads) {

    vector<vector<double>> result(dimension, vector<double>(dimension, 0.0));

    omp_set_num_threads(numThreads);

    #pragma omp parallel for
    for (int i = 0; i < dimension; i++) {
        for (int k = 0; k < dimension; k++) {
            double tmp = first[i][k];
            for (int j = 0; j < dimension; j++) {
                result[i][j] += tmp * second[k][j];
            }
        }
    }

    return result;
}

vector<vector<double>> loadMatrix(const string& path, int& size) {
    ifstream input(path);
    if (!input.is_open()) {
        cerr << "ERROR: Cannot open file " << path << endl;
        exit(1);
    }
    input >> size;
    vector<vector<double>> matrix(size, vector<double>(size, 0.0));
    for (int row = 0; row < size; row++)
        for (int col = 0; col < size; col++)
            input >> matrix[row][col];
    return matrix;
}

void storeMatrix(const string& path, const vector<vector<double>>& matrix, int size) {
    ofstream output(path);
    if (!output.is_open()) {
        cerr << "ERROR: Cannot write to file " << path << endl;
        exit(1);
    }
    output << size << endl;
    for (int row = 0; row < size; row++) {
        for (int col = 0; col < size; col++)
            output << matrix[row][col] << " ";
        output << endl;
    }
}

int main(int argc, char* argv[]) {
    int numThreads = 4;
    if (argc > 1) {
        numThreads = atoi(argv[1]);
    }

    int dim1, dim2;
    vector<vector<double>> firstMatrix = loadMatrix("data/matrixA.txt", dim1);
    vector<vector<double>> secondMatrix = loadMatrix("data/matrixB.txt", dim2);

    if (dim1 <= 0 || dim2 <= 0 || dim1 != dim2) {
        cout << "ERROR: Invalid matrix dimensions" << endl;
        return 1;
    }

    cout << "Matrix size: " << dim1 << "x" << dim1 << endl;
    cout << "Threads: " << numThreads << endl;

    auto start = chrono::high_resolution_clock::now();

    vector<vector<double>> result = parallelMultiplyOpenMP(firstMatrix, secondMatrix, dim1, numThreads);

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;

    storeMatrix("data/matrixC.txt", result, dim1);

    cout << "Computation time: " << elapsed.count() << " seconds" << endl;
    cout << "Result saved to data/matrixC.txt" << endl;

    return 0;
}