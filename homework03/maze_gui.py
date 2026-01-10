"""
GUI для визуализации лабиринта.
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Union

from .maze import add_path_to_grid, bin_tree_maze, solve_maze


def draw_cell(x_coord: int, y_coord: int, color: str, size: int = 10) -> None:
    """
    Рисует одну ячейку лабиринта.

    :param x_coord: координата X на канвасе
    :param y_coord: координата Y на канвасе
    :param color: цвет заливки
    :param size: размер ячейки
    """
    x_coord *= size
    y_coord *= size
    x1 = x_coord + size
    y1 = y_coord + size
    canvas.create_rectangle(x_coord, y_coord, x1, y1, fill=color)


def draw_maze(grid: List[List[Union[str, int]]], size: int = 10) -> None:
    """
    Рисует весь лабиринт.

    :param grid: лабиринт в виде матрицы
    :param size: размер ячейки
    """
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == "■":
                color = "black"
            elif cell == "X":
                color = "green"
            else:
                color = "white"
            draw_cell(y, x, color, size)


def show_solution():
    """Показывает решение лабиринта."""
    maze, path = solve_maze(GRID)
    maze = add_path_to_grid(GRID, path)
    if path:
        draw_maze(maze, CELL_SIZE)
    else:
        tk.messagebox.showinfo("Message", "No solutions")


if __name__ == "__main__":
    global GRID, CELL_SIZE
    N, M = 40, 50
    CELL_SIZE = 15
    GRID = bin_tree_maze(N, M)
    temp_maze, temp_path = solve_maze(GRID)
    while not temp_path:
        GRID = bin_tree_maze(N, M)
        temp_maze, temp_path = solve_maze(GRID)

    window = tk.Tk()
    window.title("Maze")
    window.geometry(f"{N * CELL_SIZE + 100}x{M * CELL_SIZE + 100}")

    canvas = tk.Canvas(window, width=M * CELL_SIZE, height=N * CELL_SIZE)
    canvas.pack()

    draw_maze([list(map(str, row)) for row in GRID], CELL_SIZE)
    ttk.Button(window, text="Solve", command=show_solution).pack(pady=20)

    window.mainloop()
