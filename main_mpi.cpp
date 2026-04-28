#include <iostream>
#include <vector>
#include <chrono>
#include <fstream>
#include <mpi.h>

using namespace std;


vector<vector<double>> multiplyBlock(
    const vector<vector<double>>& firstBlock,
    const vector<vector<double>>& second,
    int startRow, int endRow, int dimension) {

    vector<vector<double>> resultBlock(endRow - startRow, vector<double>(dimension, 0.0));

    for (int i = startRow; i < endRow; i++) {
        for (int k = 0; k < dimension; k++) {
            double tmp = firstBlock[i - startRow][k];
            for (int j = 0; j < dimension; j++) {
                resultBlock[i - startRow][j] += tmp * second[k][j];
            }
        }
    }

    return resultBlock;
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
    MPI_Init(&argc, &argv);

    int rank, numProcesses;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &numProcesses);

    int dimension;
    vector<vector<double>> matrixA, matrixB, matrixC;

    double startTime = 0.0, endTime = 0.0;


    if (rank == 0) {
        int dim1, dim2;
        matrixA = loadMatrix("data/matrixA.txt", dim1);
        matrixB = loadMatrix("data/matrixB.txt", dim2);

        if (dim1 <= 0 || dim2 <= 0 || dim1 != dim2) {
            cerr << "ERROR: Invalid matrix dimensions" << endl;
            MPI_Abort(MPI_COMM_WORLD, 1);
        }

        dimension = dim1;
        cout << "Matrix size: " << dimension << "x" << dimension << endl;
        cout << "Processes: " << numProcesses << endl;

        startTime = MPI_Wtime();
    }


    MPI_Bcast(&dimension, 1, MPI_INT, 0, MPI_COMM_WORLD);


    vector<double> flatB(dimension * dimension);
    if (rank == 0) {
        for (int i = 0; i < dimension; i++)
            for (int j = 0; j < dimension; j++)
                flatB[i * dimension + j] = matrixB[i][j];
    }
    MPI_Bcast(flatB.data(), dimension * dimension, MPI_DOUBLE, 0, MPI_COMM_WORLD);


    vector<vector<double>> localB(dimension, vector<double>(dimension));
    for (int i = 0; i < dimension; i++)
        for (int j = 0; j < dimension; j++)
            localB[i][j] = flatB[i * dimension + j];


    int rowsPerProcess = dimension / numProcesses;
    int remainder = dimension % numProcesses;

    int startRow = rank * rowsPerProcess;
    if (rank < remainder) {
        startRow += rank;
        rowsPerProcess++;
    } else {
        startRow += remainder;
    }
    int endRow = startRow + rowsPerProcess;


    vector<vector<double>> localA(rowsPerProcess, vector<double>(dimension));

    if (rank == 0) {
        for (int i = startRow; i < endRow; i++) {
            for (int j = 0; j < dimension; j++) {
                localA[i - startRow][j] = matrixA[i][j];
            }
        }


        for (int p = 1; p < numProcesses; p++) {
            int pRowsPerProcess = dimension / numProcesses;
            int pStartRow = p * pRowsPerProcess;
            int pRemainder = dimension % numProcesses;
            if (p < pRemainder) {
                pStartRow += p;
                pRowsPerProcess++;
            } else {
                pStartRow += pRemainder;
            }

            for (int i = pStartRow; i < pStartRow + pRowsPerProcess; i++) {
                MPI_Send(matrixA[i].data(), dimension, MPI_DOUBLE, p, i, MPI_COMM_WORLD);
            }
        }
    } else {

        for (int i = startRow; i < endRow; i++) {
            MPI_Recv(localA[i - startRow].data(), dimension, MPI_DOUBLE, 0, i, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }
    }


    vector<vector<double>> localResult(rowsPerProcess, vector<double>(dimension, 0.0));

    for (int i = 0; i < rowsPerProcess; i++) {
        for (int k = 0; k < dimension; k++) {
            double tmp = localA[i][k];
            for (int j = 0; j < dimension; j++) {
                localResult[i][j] += tmp * localB[k][j];
            }
        }
    }


    vector<vector<double>> fullResult;
    if (rank == 0) {
        fullResult.resize(dimension, vector<double>(dimension));

        // Копируем свою часть
        for (int i = startRow; i < endRow; i++) {
            for (int j = 0; j < dimension; j++) {
                fullResult[i][j] = localResult[i - startRow][j];
            }
        }


        for (int p = 1; p < numProcesses; p++) {
            int pRowsPerProcess = dimension / numProcesses;
            int pStartRow = p * pRowsPerProcess;
            int pRemainder = dimension % numProcesses;
            if (p < pRemainder) {
                pStartRow += p;
                pRowsPerProcess++;
            } else {
                pStartRow += pRemainder;
            }

            for (int i = pStartRow; i < pStartRow + pRowsPerProcess; i++) {
                MPI_Recv(fullResult[i].data(), dimension, MPI_DOUBLE, p, i, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            }
        }
    } else {

        for (int i = startRow; i < endRow; i++) {
            MPI_Send(localResult[i - startRow].data(), dimension, MPI_DOUBLE, 0, i, MPI_COMM_WORLD);
        }
    }

    if (rank == 0) {
        endTime = MPI_Wtime();
        storeMatrix("data/matrixC.txt", fullResult, dimension);

        cout << "Computation time: " << (endTime - startTime) << " seconds" << endl;
        cout << "Result saved to data/matrixC.txt" << endl;
    }

    MPI_Finalize();
    return 0;
}