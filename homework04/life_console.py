import curses
import time
from typing import Any

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        """Инициализировать консольный интерфейс"""
        super().__init__(life)
        self.screen = None

    def draw_borders(self, screen: Any) -> None:
        """Отобразить рамку"""
        screen.clear()
        screen.border(0)

    def draw_grid(self, screen: Any) -> None:
        """Отобразить состояние клеток"""
        start_y = 1
        start_x = 1

        rows, cols = screen.getmaxyx()

        for y in range(self.life.rows):
            if y >= rows - 2:
                break
            for x in range(self.life.cols):
                if x >= cols - 2:
                    break

                if self.life.curr_generation[y][x] == 1:
                    try:
                        screen.addch(start_y + y, start_x + x, "■")
                    except curses.error:
                        pass
                else:
                    try:
                        screen.addch(start_y + y, start_x + x, " ")
                    except curses.error:
                        pass

        info = f"Поколение: {self.life.generations} | Клавиша 'q' для выхода"
        try:
            screen.addstr(rows - 1, 2, info[: cols - 4])
        except curses.error:
            pass

        screen.refresh()

    def handle_input(self, screen: Any, key: int) -> bool:
        """Обработать ввод пользователя"""
        if key == ord("q") or key == ord("Q"):
            return False
        if key == 27:  # ESC
            return False
        if key == ord(" "):  # Пауза по пробелу
            screen.nodelay(False)  # Блокирующий ввод для паузы
            rows, cols = screen.getmaxyx()
            pause_msg = "Пауза. Нажмите любую клавишу для продолжения..."
            try:
                screen.addstr(rows - 1, 2, pause_msg[: cols - 4])
                screen.refresh()
            except curses.error:
                pass
            screen.getch()  # Ждем любую клавишу
            screen.nodelay(True)  # Возвращаем неблокирующий ввод
        return True

    def run(self) -> None:
        """Запустить основной цикл игры"""
        self.screen = curses.initscr()
        try:
            # Настройки curses
            curses.curs_set(0)  # Скрываем курсор
            self.screen.nodelay(True)  # Неблокирующий ввод
            self.screen.timeout(100)  # Таймаут для обновления экрана (100 мс)

            # Включаем поддержку цветов (если доступно)
            if curses.has_colors():
                curses.start_color()
                curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

            running = True

            while (running and self.life.is_changing
                   and not self.life.is_max_generations_exceeded):
                self.draw_borders(self.screen)
                self.draw_grid(self.screen)

                try:
                    key = self.screen.getch()
                    if key != -1:  # -1 означает отсутствие ввода
                        running = self.handle_input(self.screen, key)
                except curses.error:
                    pass

                # Выполняем один шаг игры
                self.life.step()

                # Небольшая задержка для удобства восприятия
                time.sleep(0.1)

            # Отображаем финальное состояние
            self.draw_borders(self.screen)
            self.draw_grid(self.screen)

            # Сообщение о завершении
            rows, cols = self.screen.getmaxyx()
            if not self.life.is_changing:
                message = "Игра завершена: стабильная конфигурация достигнута."
            elif self.life.is_max_generations_exceeded:
                message = (f"Игра завершена: достигнут лимит "
                           f"{self.life.max_generations} поколений.")
            else:
                message = "Игра завершена пользователем."

            try:
                self.screen.addstr(rows - 1, 2, message[: cols - 4])
                self.screen.refresh()
                self.screen.getch()  # Ждем любую клавишу перед выходом
            except curses.error:
                pass

        finally:
            curses.endwin()
