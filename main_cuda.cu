#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <cuda_runtime.h>

using namespace std;


__global__ void matrixMulKernel(const double* A, const double* B, double* C, int N) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < N && col < N) {
        double sum = 0.0;
        for (int k = 0; k < N; k++) {
            sum += A[row * N + k] * B[k * N + col];
        }
        C[row * N + col] = sum;
    }
}


vector<double> loadMatrix(const string& path, int& N) {
    ifstream file(path);
    if (!file.is_open()) {
        cerr << "ERROR: Cannot open file " << path << endl;
        exit(1);
    }

    file >> N;
    vector<double> matrix(N * N);
    for (int i = 0; i < N * N; i++) {
        file >> matrix[i];
    }
    return matrix;
}


void saveMatrix(const string& path, const vector<double>& matrix, int N) {
    ofstream file(path);
    if (!file.is_open()) {
        cerr << "ERROR: Cannot write to file " << path << endl;
        exit(1);
    }

    file << N << endl;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            file << matrix[i * N + j] << " ";
        }
        file << endl;
    }
}

int main(int argc, char* argv[]) {
    // Параметры сетки блоков
    int blockSize = 16;
    if (argc > 1) {
        blockSize = atoi(argv[1]);
    }

    int dimA, dimB;
    vector<double> h_A = loadMatrix("data/matrixA.txt", dimA);
    vector<double> h_B = loadMatrix("data/matrixB.txt", dimB);

    if (dimA <= 0 || dimB <= 0 || dimA != dimB) {
        cout << "ERROR: Invalid matrix dimensions" << endl;
        return 1;
    }

    int N = dimA;
    cout << "Matrix size: " << N << "x" << N << endl;
    cout << "Block size: " << blockSize << "x" << blockSize << endl;


    size_t bytes = N * N * sizeof(double);


    double *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, bytes);
    cudaMalloc(&d_B, bytes);
    cudaMalloc(&d_C, bytes);


    cudaMemcpy(d_A, h_A.data(), bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B.data(), bytes, cudaMemcpyHostToDevice);


    dim3 threadsPerBlock(blockSize, blockSize);
    dim3 numBlocks((N + blockSize - 1) / blockSize, (N + blockSize - 1) / blockSize);

    cout << "Grid size: " << numBlocks.x << "x" << numBlocks.y << " blocks" << endl;


    auto start = chrono::high_resolution_clock::now();


    matrixMulKernel<<<numBlocks, threadsPerBlock>>>(d_A, d_B, d_C, N);
    cudaDeviceSynchronize();

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;


    vector<double> h_C(N * N);
    cudaMemcpy(h_C.data(), d_C, bytes, cudaMemcpyDeviceToHost);


    saveMatrix("data/matrixC.txt", h_C, N);

    cout << "Computation time: " << elapsed.count() << " seconds" << endl;
    cout << "Result saved to data/matrixC.txt" << endl;


    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);

    return 0;
}