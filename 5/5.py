import threading
import random


class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance


class Logger(Singleton):
    def __init__(self):
        self.file = open("log.txt", "w", encoding="utf-8")

    def log(self, thread_name, i, j, value):
        self.file.write(f"{thread_name}: C[{i}][{j}] = {value}\n")
        self.file.flush()


def matrix_multiply_worker(A, B, C, i, j, logger):
    N = len(A)
    C[i][j] = sum(A[i][k] * B[k][j] for k in range(N))
    logger.log(threading.current_thread().name, i, j, C[i][j])


def matrix_multiply(A, B):
    N = len(A)
    C = [[0 for _ in range(N)] for _ in range(N)]
    logger = Logger()

    threads = []
    for i in range(N):
        for j in range(N):
            thread = threading.Thread(target=matrix_multiply_worker, args=(A, B, C, i, j, logger))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    return C


def generate_matrix(N):
    return [[random.randint(1, 10) for _ in range(N)] for _ in range(N)]


N = 3
A = generate_matrix(N)
B = generate_matrix(N)
C = matrix_multiply(A, B)
print("Matrix A:")
for row in A:
    print(row)
print("Matrix B:")
for row in B:
    print(row)
print("Matrix C:")
for row in C:
    print(row)
