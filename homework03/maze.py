from copy import deepcopy
from random import choice, randint, seed
from typing import List, Optional, Tuple, Union

import pandas as pd


#
#
def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    res = [row[:] for row in grid]
    row, col = coord
    direct = choice(["up", "right"])

    if direct == "right":
        if col + 2 < len(res[0]) and res[row][col + 1] == "■":
            res[row][col + 1] = " "
        elif row - 1 > 0 and res[row - 1][col] == "■":
            res[row - 1][col] = " "
    elif direct == "up":
        if row - 1 > 0 and res[row - 1][col] == "■":
            res[row - 1][col] = " "
        elif col + 2 < len(res[0]) and res[row][col + 1] == "■":
            res[row][col + 1] = " "

    return res


#
#
def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for cell in empty_cells:
        grid = remove_wall(grid, cell)

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    exits = []

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "X":
                exits.append((i, j))

    if len(exits) < 2:
        pass

    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    new_grid = [row.copy() for row in grid]

    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == k:
                neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

                for nx, ny in neighbors:
                    if 0 <= nx < rows and 0 <= ny < cols:
                        if grid[nx][ny] == 0 or grid[nx][ny] == " ":
                            new_grid[nx][ny] = k + 1

    return new_grid


def shortest_path(grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    if not grid:
        return None

    x, y = exit_coord
    rows = len(grid)
    cols = len(grid[0])

    # Получаем числовое значение в клетке выхода
    def cell_to_int(cell):
        if type(cell) == int:
            return cell
        elif type(cell) == str and cell.isdigit():
            return int(cell)
        return None

    exit_value = cell_to_int(grid[x][y])

    # Если клетка выхода содержит не число, пытаемся определить значение
    if exit_value is None:
        # Проверяем соседей
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                neighbor_val = cell_to_int(grid[nx][ny])
                if neighbor_val is not None and neighbor_val > 0:
                    exit_value = neighbor_val + 1
                    break
        else:
            return None

    if exit_value <= 0:
        return None

    # Восстанавливаем путь ОТ ВЫХОДА К ВХОДУ
    path = [(x, y)]
    current_val = exit_value
    cx, cy = x, y

    while current_val > 1:
        # Ищем следующую клетку
        next_found = False

        # Порядок проверки: вверх, вниз, влево, вправо
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy

            if 0 <= nx < rows and 0 <= ny < cols:
                neighbor_val = cell_to_int(grid[nx][ny])

                if neighbor_val == current_val - 1:
                    cx, cy = nx, ny
                    current_val = neighbor_val
                    path.append((cx, cy))
                    next_found = True
                    break

        if not next_found:
            return None

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    x, y = coord
    rows = len(grid)
    cols = len(grid[0])

    # функция для проверки, является ли клетка стенкой
    def is_wall(cell):
        return cell != " " and cell != "" and cell != "X"

    is_top = x == 0
    is_bottom = x == rows - 1
    is_left = y == 0
    is_right = y == cols - 1

    # Случай 1: Угловая клетка
    if (is_top and is_left) or (is_top and is_right) or (is_bottom and is_left) or (is_bottom and is_right):

        wall_count = 0

        if x == 0 and y == 0:
            if x + 1 < rows and is_wall(grid[x + 1][y]):
                wall_count += 1
            if y + 1 < cols and is_wall(grid[x][y + 1]):
                wall_count += 1

        elif x == 0 and y == cols - 1:
            if x + 1 < rows and is_wall(grid[x + 1][y]):
                wall_count += 1
            if y - 1 >= 0 and is_wall(grid[x][y - 1]):
                wall_count += 1

        elif x == rows - 1 and y == 0:
            if x - 1 >= 0 and is_wall(grid[x - 1][y]):
                wall_count += 1
            if y + 1 < cols and is_wall(grid[x][y + 1]):
                wall_count += 1

        elif x == rows - 1 and y == cols - 1:
            if x - 1 >= 0 and is_wall(grid[x - 1][y]):
                wall_count += 1
            if y - 1 >= 0 and is_wall(grid[x][y - 1]):
                wall_count += 1

        return wall_count == 2

    # Случай 2: Клетка на стенке (но не в углу)
    elif is_top or is_bottom or is_left or is_right:

        wall_count = 0

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if not (0 <= nx < rows and 0 <= ny < cols):
                wall_count += 1
            elif is_wall(grid[nx][ny]):
                wall_count += 1

        return wall_count == 4

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[List[Tuple[int, int]]]]:
    """

    :param grid:
    :return:
    """
    exits = get_exits(grid)
    if len(exits) < 2:
        return grid, exits
    else:
        entrance = exits[1]
        exit = exits[0]
        if encircled_exit(grid, exit):
            return grid, None
        else:
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == " ":
                        grid[i][j] = 0
            grid[entrance[0]][entrance[1]] = 1
            grid[exit[0]][exit[1]] = 0
            k = 1
            while grid[exit[0]][exit[1]] == 0:
                grid = make_step(grid, k)
                k += 1
            back = shortest_path(grid, exit)
            if back is None:
                return grid, None
            res = back[::-1]
            return grid, res


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[List[Tuple[int, int]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
