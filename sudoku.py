import random
import itertools

n = 3


def __gen_grid():
    return [[((i * n + i // n + j) % (n * n) + 1) for j in range(n * n)] for i in range(n * n)]


def __transpose(grid):
    return list(map(list, zip(*grid)))


def __swap_rows1(grid):
    area = random.randrange(0, n, 1)
    line1 = random.randrange(0, n, 1)
    line2 = random.randrange(0, n, 1)
    while line1 == line2:
        line2 = random.randrange(0, n, 1)

    n1 = area * n + line1
    n2 = area * n + line2
    grid[n1], grid[n2] = grid[n2], grid[n1]
    return grid


def __swap_cols1(grid):
    grid = __transpose(grid)
    grid = __swap_rows1(grid)
    return __transpose(grid)


def __swap_rows2(grid):
    area1 = random.randrange(0, n, 1)
    area2 = random.randrange(0, n, 1)
    while area1 == area2:
        area2 = random.randrange(0, n, 1)

    for i in range(0, n):
        n1, n2 = area1 * n + i, area2 * n + i
        grid[n1], grid[n2] = grid[n2], grid[n1]
    return grid


def __swap_cols2(grid):
    grid = __transpose(grid)
    grid = __swap_rows2(grid)
    return __transpose(grid)


def __sieve(grid):
    for i in range(1, 35):
        x = random.randrange(0, n**4, 1)
        grid[x // n**2][x % n**2] = 0
    return grid


def gen_grid():
    transfromations = [__transpose, __swap_rows1, __swap_rows2, __swap_cols1, __swap_cols2]
    grid = __gen_grid()
    for i in range(1, 100):
        transformation = transfromations[random.randrange(0, len(transfromations), 1)]
        grid = transformation(grid)
    grid = __sieve(grid)
    return list(itertools.chain.from_iterable(grid))


def __check_rows(grid):
    for i in range(n**2):
        if set(grid[i * n**2:(i + 1) * n**2]) != set(range(1, 10)):
            return False
    return True


def __check_cols(grid):
    for i in range(n**2):
        if set(grid[i::n**2]) != set(range(1, 10)):
            return False
    return True


def __check_squares(grid):
    for i in range(n):
        for j in range(n):
            square = []
            for index in range(81):
                if (index // n**2) // n == j and (index % n**2) // n == i:
                    square.append(grid[index])
            if set(square) != set(range(1, 10)):
                return False
    return True


def check_grid(grid):
    return __check_rows(grid) and __check_cols(grid) and __check_squares(grid)
