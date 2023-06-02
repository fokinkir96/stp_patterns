import unittest
import numpy as np


class Generate:
    def __init__(self, n, m, f2):
        self.n = n
        self.m = m
        self.f2 = f2

    def generate_matrix(self):
        A = np.random.randint(0, 10, size=(self.n, self.m))
        B = np.random.randint(0, 10, size=(self.n, self.m))
        with open(self.f2, 'w') as f:
            for row in A:
                f.write(" ".join(map(str, row)) + "\n")
            f.write("\n")
            for row in B:
                f.write(" ".join(map(str, row)) + "\n")


class Sum:
    def __init__(self, f0, f1):
        self.f0 = f0
        self.f1 = f1

    def read_matrix(self):
        with open(self.f0, 'r') as f:
            A = []
            B = []
            matrix = A
            for line in f:
                if line.strip() == "":
                    matrix = B
                    continue
                matrix.append(list(map(int, line.strip().split())))
        return np.array(A), np.array(B)

    def save_matrix(self, matrix):
        with open(self.f1, 'w') as f:
            for row in matrix:
                f.write(" ".join(map(str, row)) + "\n")

    def sum_matrix(self):
        A, B = self.read_matrix()
        C = A + B
        self.save_matrix(C)


class GenerateAdapter(Generate):
    def __init__(self, n, m, f2):
        super().__init__(n, m, f2)
        self._sum = Sum(f2, 'result.txt')

    def generate_matrix(self):
        super().generate_matrix()
        self._sum.sum_matrix()

# g = GenerateAdapter(3, 3, 'f2.txt')
# g.generate_matrix()


class TestGenerateAdapter(unittest.TestCase):

    def test_sum_matrices(self):
        n, m = 3, 3
        g = GenerateAdapter(n, m, 'f2.txt')
        g.generate_matrix()
        s = Sum('f2.txt', 'f1.txt')

        A, B = s.read_matrix()
        C = np.loadtxt("result.txt", dtype=int)

        self.assertEqual((A+B).tolist(), C.tolist(), f"Expected {A + B}, but got {C}")


unittest.main()