import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"),
                             (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            grid = [[random.randint(0, 1) for _ in range(self.cell_width)]
                    for _ in range(self.cell_height)]
        else:
            grid = [[0 for _ in range(self.cell_width)]
                    for _ in range(self.cell_height)]

        return grid
    def draw_grid(self) -> None:
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                if self.grid[y][x] == 1:
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("white")

                rect_x = x * self.cell_size
                rect_y = y * self.cell_size

                pygame.draw.rect(
                    self.screen,
                    color,
                    (rect_x, rect_y, self.cell_size, self.cell_size)
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        neighbours = []

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < self.cell_height and 0 <= new_col < self.cell_width:
                    neighbours.append(self.grid[new_row][new_col])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = [[0 for _ in range(self.cell_width)]
                    for _ in range(self.cell_height)]

        for y in range(self.cell_height):
            for x in range(self.cell_width):
                neighbours_values = self.get_neighbours((y, x))

                live_neighbours = sum(neighbours_values)

                current_cell = self.grid[y][x]

                if current_cell == 1:
                    if live_neighbours == 2 or live_neighbours == 3:
                        new_grid[y][x] = 1
                    else:
                        new_grid[y][x] = 0
                else:
                    if live_neighbours == 3:
                        new_grid[y][x] = 1
                    else:
                        new_grid[y][x] = 0
        return new_grid