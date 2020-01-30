import numpy as np
from matplotlib.pyplot import plot, xlabel, ylabel, grid, savefig, legend
from operator import itemgetter
from random import sample, seed


seed(1)


LOOPS = 100
MIN_SIZE = 10
MAX_SIZE = 30
STEP = 5


def sort_matrix(matrix):
    for i in range(len(matrix)):
        sub = matrix[i:, i:]
        min_row = sub.sum(axis=1).argmin() + i
        copy = matrix[i].copy()
        matrix[i] = matrix[min_row]
        matrix[min_row] = copy
        sub = matrix[i:, i:]
        columns = [(i, sub[:, i].sum()) for i in range(len(sub)) if sub[0, i] == 1]
        if columns:
            max_col = max(columns, key=itemgetter(1))[0] + i
            copy = matrix[:, i].copy()
            matrix[:, i] = matrix[:, max_col]
            matrix[:, max_col] = copy
    return matrix


def filter_matrix(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i].sum() == 1:
            matrix[i] = np.zeros((1, n))
    for i in range(n):
        if matrix[:, i].sum() == 1:
            matrix[:, i] = np.zeros((n, 1))
    return matrix


def check_conflicts(matrix):
    matrix = filter_matrix(sort_matrix(matrix))
    return any(not matrix[:i, i:].any() and matrix[-i:, :-i].any() for i in range(1, len(matrix)))


if __name__ == "__main__":
    result = []
    for n in range(MIN_SIZE, MAX_SIZE + 1, 5):
        probabilities = []
        for percent in range(1, 101):
            total = 0
            for _ in range(LOOPS):
                m = [[0] * n for _ in range(n)]
                for x in sample(range(n * n), round(n * n * percent / 100)):
                    m[x // n][x % n] = 1
                total += check_conflicts(np.matrix(m))
            probabilities.append(total * 100 / LOOPS)
        result.append(probabilities)

    x = [*range(1, 101)]

    for i, (y, color) in enumerate(zip(result, "rgbcm")):
        plot(x, y, f"{color}-", label=f"{i * STEP + MIN_SIZE}")

    grid()
    ylabel("Probability, %")
    xlabel("Connectivity, %")
    legend()

    savefig("result2.png")
