"""
Графический интерфейс для игры "Жизнь" с использованием PyGame.
"""

# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-branches
# pylint: disable=no-member

import pygame

from life import GameOfLife
from ui import UI


class GUI(UI):
    """Графический интерфейс для игры "Жизнь"."""

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        """Инициализировать графический интерфейс.

        Args:
            life: Игровая логика "Жизни"
            cell_size: Размер клетки в пикселях
            speed: Скорость игры (FPS)
        """
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen: pygame.Surface = None  # type: ignore
        self.paused = False
        self.dragging = False
        self.running = True

        # Вычисляем размеры окна
        self.width = life.cols * cell_size
        self.height = life.rows * cell_size

    def draw_lines(self) -> None:
        """Нарисовать сетку игрового поля."""
        if self.screen is None:
            return

        for x_coord in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"),
                (x_coord, 0), (x_coord, self.height)
            )
        for y_coord in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"),
                (0, y_coord), (self.width, y_coord)
            )

    def draw_grid(self) -> None:
        """Нарисовать клетки игрового поля."""
        if self.screen is None:
            return

        for y_coord in range(self.life.rows):
            for x_coord in range(self.life.cols):
                is_alive = self.life.curr_generation[y_coord][x_coord]
                color = pygame.Color("green") if is_alive else pygame.Color("white")

                # Рисуем прямоугольник с небольшим отступом для видимости сетки
                padding = 1
                rect = pygame.Rect(
                    x_coord * self.cell_size + padding,
                    y_coord * self.cell_size + padding,
                    self.cell_size - 2 * padding,
                    self.cell_size - 2 * padding,
                )
                pygame.draw.rect(self.screen, color, rect)

    def toggle_cell(self, pos: tuple) -> None:
        """Переключить состояние клетки по координатам мыши.

        Args:
            pos: Координаты мыши (x, y)
        """
        x_coord, y_coord = pos
        grid_x = x_coord // self.cell_size
        grid_y = y_coord // self.cell_size

        if 0 <= grid_x < self.life.cols and 0 <= grid_y < self.life.rows:
            current_state = self.life.curr_generation[grid_y][grid_x]
            self.life.curr_generation[grid_y][grid_x] = 1 - current_state

    def draw_info(self) -> None:
        """Отображение информации о состоянии игры."""
        if self.screen is None:
            return

        font = pygame.font.Font(None, 24)

        # Информация о поколении
        gen_text = f"Поколение: {self.life.generations}"
        if self.life.max_generations != float("inf"):
            gen_text += f" / {self.life.max_generations}"

        # Состояние игры
        if self.paused:
            state_text = "ПАУЗА - ПРОБЕЛ: продолжить | ЛКМ: рисовать | ESC: выйти"
        else:
            state_text = "ИГРА - ПРОБЕЛ: пауза | ESC: выйти"

        # Если игра завершена
        if not self.life.is_changing:
            state_text = "СТАБИЛЬНАЯ КОНФИГУРАЦИЯ - ESC: выйти"
        elif self.life.is_max_generations_exceeded:
            state_text = (
                f"ДОСТИГНУТ ЛИМИТ ({self.life.max_generations} поколений) "
                "- ESC: выйти"
            )

        # Отрисовываем текст
        gen_surface = font.render(gen_text, True, pygame.Color("black"))
        state_surface = font.render(state_text, True, pygame.Color("black"))

        # Фон для текста
        pygame.draw.rect(
            self.screen, pygame.Color("white"), (0, 0, self.width, 50)
        )

        self.screen.blit(gen_surface, (10, 10))
        self.screen.blit(state_surface, (10, 35))

    def run(self) -> None:
        """Запустить основной цикл игры."""
        pygame.init()

        self.screen = pygame.display.set_mode(
            (self.width, self.height + 50)
        )  # +50 для панели информации
        pygame.display.set_caption("Game of Life")

        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                    elif event.key == pygame.K_SPACE:
                        # Пауза/продолжение игры
                        self.paused = not self.paused

                    elif event.key == pygame.K_r and self.paused:
                        # Сброс игры (только в паузе)
                        self.life = GameOfLife(
                            (self.life.rows, self.life.cols),
                            randomize=True,
                            max_generations=self.life.max_generations,
                        )

                    elif event.key == pygame.K_c and self.paused:
                        # Очистка поля (только в паузе)
                        self.life.curr_generation = self.life.create_grid(
                            randomize=False
                        )

                elif event.type == pygame.MOUSEBUTTONDOWN and self.paused:
                    # Рисование клеток в режиме паузы
                    if event.button == 1:  # Левая кнопка мыши
                        self.dragging = True
                        self.toggle_cell(event.pos)

                elif event.type == pygame.MOUSEBUTTONUP and self.paused:
                    # Прекращаем рисование
                    if event.button == 1:  # Левая кнопка мыши
                        self.dragging = False

                elif (
                    event.type == pygame.MOUSEMOTION
                    and self.paused
                    and self.dragging
                ):
                    # Рисование при перетаскивании
                    self.toggle_cell(event.pos)

            if self.screen is None:
                continue

            # Заполняем фон
            self.screen.fill(pygame.Color("white"))

            # Отрисовываем игровое поле
            game_surface = pygame.Surface((self.width, self.height))
            game_surface.fill(pygame.Color("white"))

            # Сохраняем и восстанавливаем состояние отсечения
            old_clip = self.screen.get_clip()
            self.screen.set_clip((0, 50, self.width, self.height))

            # Рисуем сетку и клетки на game_surface
            self.draw_grid()
            self.draw_lines()

            # Копируем game_surface на основной экран
            self.screen.blit(
                self.screen.subsurface((0, 0, self.width, self.height)),
                (0, 50)
            )
            self.screen.set_clip(old_clip)

            # Отрисовываем информацию
            self.draw_info()

            # Обновляем состояние игры
            should_update = (
                not self.paused
                and self.life.is_changing
                and not self.life.is_max_generations_exceeded
            )
            if should_update:
                self.life.step()

            # Обновляем экран
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()