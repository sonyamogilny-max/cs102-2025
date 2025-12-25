"""
GUI для визуализации лабиринта.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import List, Union

from .maze import add_path_to_grid, bin_tree_maze, solve_maze

# Глобальные переменные для GUI
GRID: List[List[Union[str, int]]] = []
CELL_SIZE: int = 10
CANVAS: tk.Canvas = None  # type: ignore


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
    CANVAS.create_rectangle(x_coord, y_coord, x1, y1, fill=color)


def draw_maze(grid: List[List[Union[str, int]]], size: int = 10) -> None:
    """
    Рисует весь лабиринт.

    :param grid: лабиринт в виде матрицы
    :param size: размер ячейки
    """
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == " ":
                color = "white"
            elif cell == "■":
                color = "black"
            elif cell == "X":
                color = "blue"
            elif cell == "*":
                color = "red"
            else:
                color = "white"  # для чисел или других символов

            # Передаем x и y в правильном порядке
            draw_cell(y, x, color, size)


def show_solution() -> None:
    """
    Находит и отображает решение лабиринта.
    """
    global GRID, CELL_SIZE, CANVAS  # noqa: PLW0603

    maze_with_path, path = solve_maze(GRID)
    maze_with_path = add_path_to_grid(GRID, path)

    if path:
        # Очищаем канвас и рисуем лабиринт с путем
        CANVAS.delete("all")
        draw_maze(maze_with_path, CELL_SIZE)
    else:
        messagebox.showinfo("Message", "No solutions")


def main() -> None:
    """
    Основная функция для запуска GUI.
    """
    global GRID, CELL_SIZE, CANVAS  # noqa: PLW0603

    rows, cols = 51, 77
    CELL_SIZE = 10
    GRID = bin_tree_maze(rows, cols)

    window = tk.Tk()
    window.title("Maze")
    window.geometry(f"{cols * CELL_SIZE + 100}x{rows * CELL_SIZE + 100}")

    CANVAS = tk.Canvas(window, width=cols * CELL_SIZE, height=rows * CELL_SIZE)
    CANVAS.pack()

    draw_maze(GRID, CELL_SIZE)
    ttk.Button(window, text="Solve", command=show_solution).pack(pady=20)

    window.mainloop()


if __name__ == "__main__":
    main()
