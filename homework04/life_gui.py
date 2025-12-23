import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen = None
        self.paused = False
        self.dragging = False  # Для перетаскивания клеток
        self.running = True

        # Вычисляем размеры окна
        self.width = life.cols * cell_size
        self.height = life.rows * cell_size

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                color = pygame.Color("green") if self.life.curr_generation[y][x] else pygame.Color("white")

                # Рисуем прямоугольник с небольшим отступом для видимости сетки
                padding = 1
                rect = pygame.Rect(
                    x * self.cell_size + padding,
                    y * self.cell_size + padding,
                    self.cell_size - 2 * padding,
                    self.cell_size - 2 * padding
                )
                pygame.draw.rect(self.screen, color, rect)

    def toggle_cell(self, pos: tuple) -> None:
        """Переключить состояние клетки по координатам мыши"""
        x, y = pos
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size

        if 0 <= grid_x < self.life.cols and 0 <= grid_y < self.life.rows:
            self.life.curr_generation[grid_y][grid_x] = 1 - self.life.curr_generation[grid_y][grid_x]

    def draw_info(self) -> None:
        """Отображение информации о состоянии игры"""
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
            state_text = f"ДОСТИГНУТ ЛИМИТ ({self.life.max_generations} поколений) - ESC: выйти"

        # Отрисовываем текст
        gen_surface = font.render(gen_text, True, pygame.Color("black"))
        state_surface = font.render(state_text, True, pygame.Color("black"))

        # Фон для текста
        pygame.draw.rect(self.screen, pygame.Color("white"),
                         (0, 0, self.width, 50))

        self.screen.blit(gen_surface, (10, 10))
        self.screen.blit(state_surface, (10, 35))

    def run(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height + 50))  # +50 для панели информации
        pygame.display.set_caption("Game of Life")

        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False

                    elif event.key == K_SPACE:
                        # Пауза/продолжение игры
                        self.paused = not self.paused

                    elif event.key == K_r and self.paused:
                        # Сброс игры (только в паузе)
                        self.life = GameOfLife((self.life.rows, self.life.cols),
                                               randomize=True,
                                               max_generations=self.life.max_generations)

                    elif event.key == K_c and self.paused:
                        # Очистка поля (только в паузе)
                        self.life.curr_generation = self.life.create_grid(randomize=False)

                elif event.type == MOUSEBUTTONDOWN and self.paused:
                    # Рисование клеток в режиме паузы
                    if event.button == 1:  # Левая кнопка мыши
                        self.dragging = True
                        self.toggle_cell(event.pos)

                elif event.type == MOUSEBUTTONUP and self.paused:
                    # Прекращаем рисование
                    if event.button == 1:  # Левая кнопка мыши
                        self.dragging = False

                elif event.type == MOUSEMOTION and self.paused and self.dragging:
                    # Рисование при перетаскивании
                    self.toggle_cell(event.pos)

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
            self.screen.blit(self.screen.subsurface((0, 0, self.width, self.height)), (0, 50))
            self.screen.set_clip(old_clip)

            # Отрисовываем информацию
            self.draw_info()

            # Обновляем состояние игры, если не на паузе и игра продолжается
            if not self.paused and self.life.is_changing and not self.life.is_max_generations_exceeded:
                self.life.step()

            # Обновляем экран
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()
