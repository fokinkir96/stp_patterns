from abc import ABC, abstractmethod
from Logger import Logger


class Matrix:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.data])


class MatrixOps(ABC):
    @abstractmethod
    def execute(self, matrix1, matrix2=None):
        pass


class MatrixAdd(MatrixOps):
    def execute(self, matrix1, matrix2=None):
        result = [[matrix1.data[i][j] + matrix2.data[i][j] for j in range(len(matrix1.data[0]))] for i in range(len(matrix1.data))]
        return Matrix(result)


class MatrixTranspose(MatrixOps):
    def execute(self, matrix1, matrix2=None):
        result = [[matrix1.data[j][i] for j in range(len(matrix1.data))] for i in range(len(matrix1.data[0]))]
        return Matrix(result)


class MatrixDeterminant(MatrixOps):
    def execute(self, matrix1, matrix2=None):
        if len(matrix1.data) != len(matrix1.data[0]):
            raise ValueError("Matrix must be square")
        return self._determinant(matrix1.data)

    def _determinant(self, matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        elif len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            result = 0
            for i in range(len(matrix)):
                submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
                result += matrix[0][i] * (-1) ** i * self._determinant(submatrix)
            return result


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class ReadCommand(Command):
    def __init__(self, filename):
        self.filename = filename

    def execute(self):
        with open(self.filename, "r") as file:
            data = [list(map(int, line.strip().split())) for line in file.readlines()]
        return Matrix(data)


class WriteCommand(Command):
    def __init__(self, matrix, filename):
        self.matrix = matrix
        self.filename = filename

    def execute(self):
        with open(self.filename, "w") as file:
            file.write(str(self.matrix))


class MatrixOperationCommand(Command):
    def __init__(self, operation, matrix1, matrix2=None):
        self.operation = operation
        self.matrix1 = matrix1
        self.matrix2 = matrix2

    def execute(self):
        return self.operation.execute(self.matrix1, self.matrix2)


class Invoker:
    def __init__(self):
        self.command = ''
        self.logger = Logger()

    def add_command(self, command):
        self.command = command

    def execute_command(self):
        self.logger.log(f"Выполнена команда {self.command.__class__.__name__}")
        return self.command.execute()


operation_symbol = input('Введите команду: ')
input_filenames = 'input.txt input1.txt'
output_filename = 'output.txt'

if operation_symbol == "+":
    operation = MatrixAdd()
elif operation_symbol == "t":
    operation = MatrixTranspose()
elif operation_symbol == "d":
    operation = MatrixDeterminant()
else:
    print("Неизвестная операция")
    exit()

invoker = Invoker()

matrices = []
input_filenames = input_filenames.split()
for filename in input_filenames:
    read_command = ReadCommand(filename)
    invoker.add_command(read_command)
    matrix = invoker.execute_command()
    matrices.append(matrix)

matrix_operation_command = MatrixOperationCommand(operation, *matrices)
invoker.add_command(matrix_operation_command)
result_matrix = invoker.execute_command()

write_command = WriteCommand(result_matrix, output_filename)
invoker.add_command(write_command)
invoker.execute_command()
