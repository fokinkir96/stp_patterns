import numpy as np
from abc import ABC, abstractmethod


class MatrixOperation(ABC):
    def read_matrix(self, file_path):
        with open(file_path, 'r') as f:
            A = []
            B = []
            matrix = A
            for line in f:
                if line.strip() == '':
                    matrix = B
                    continue
                matrix.append(list(map(int, line.strip().split())))
        return np.array(A), np.array(B)

    def save_matrix(self, file_path, matrix):
        with open(file_path, 'w') as f:
            if isinstance(matrix, np.float64):
                f.write(str(matrix) + "\n")
                return
            for row in matrix:
                f.write(" ".join(map(str, row)) + "\n")

    @abstractmethod
    def perform_operation(self, A, B):
        pass

    def execute(self, file_input, file_output):
        A, B = self.read_matrix(file_input)
        result = self.perform_operation(A, B)
        self.save_matrix(file_output, result)


class TransposeMatrix(MatrixOperation):
    def perform_operation(self, A, _):
        return A.T


class AddMatrix(MatrixOperation):
    def perform_operation(self, A, B):
        return A + B


class MatrixDeterminant(MatrixOperation):
    def perform_operation(self, A, _):
        return np.linalg.det(A)


operation_map = {
    'transpose': TransposeMatrix,
    'add': AddMatrix,
    'determinant': MatrixDeterminant
}

operation_name = 'add'
f1 = 'f2.txt'
f2 = 'result.txt'

operation = operation_map[operation_name]()
operation.execute(f1, f2)
