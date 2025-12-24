"""
Модуль консольного интерфейса для игры "Жизнь".
Использует библиотеку curses для отображения в терминале.
"""

import curses
import time
from typing import Optional

from life import GameOfLife
from ui import UI


class Console(UI):
    """Консольный интерфейс для игры "Жизнь" с использованием curses."""

    def __init__(self, life: GameOfLife) -> None:
        """Инициализировать консольный интерфейс"""
        super().__init__(life)
        self.screen: Optional[curses.window] = None # type: ignore

    def draw_borders(self, screen: curses.window) -> None:
        """Отобразить рамку"""
        screen.clear()
        screen.border(0)

    def draw_grid(self, screen: curses.window) -> None: # type: ignore
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
                    except curses.error:  # pylint: disable=no-member
                        pass
                else:
                    try:
                        screen.addch(start_y + y, start_x + x, " ")
                    except curses.error:  # pylint: disable=no-member
                        pass

        info = f"Поколение: {self.life.generations} | Клавиша 'q' для выхода"
        try:
            screen.addstr(rows - 1, 2, info[: cols - 4])
        except curses.error:  # pylint: disable=no-member
            pass

        screen.refresh()

    def handle_input(self, screen: curses.window, key: int) -> bool:
        """Обработать ввод пользователя."""
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
            except curses.error:  # pylint: disable=no-member
                pass
            screen.getch()  # Ждем любую клавишу
            screen.nodelay(True)  # Возвращаем неблокирующий ввод
        return True

    def run(self) -> None:
        """Запустить основной цикл игры"""
        screen = curses.initscr()
        self.screen = screen  # Присваиваем значение после инициализации

        try:
            # Настройки curses
            curses.curs_set(0)  # Скрываем курсор  # pylint: disable=no-member
            screen.nodelay(True)  # Неблокирующий ввод
            screen.timeout(100)  # Таймаут для обновления экрана (100 мс)

            # Включаем поддержку цветов (если доступно)
            if curses.has_colors():  # pylint: disable=no-member
                curses.start_color()
                curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # pylint: disable=no-member

            running = True

            while (running and self.life.is_changing and
                   not self.life.is_max_generations_exceeded):
                self.draw_borders(screen)
                self.draw_grid(screen)

                try:
                    key = screen.getch()
                    if key != -1:  # -1 означает отсутствие ввода
                        running = self.handle_input(screen, key)
                except curses.error:  # pylint: disable=no-member
                    pass

                # Выполняем один шаг игры
                self.life.step()

                # Небольшая задержка для удобства восприятия
                time.sleep(0.1)

            # Отображаем финальное состояние
            self.draw_borders(screen)
            self.draw_grid(screen)

            # Сообщение о завершении
            rows, cols = screen.getmaxyx()
            if not self.life.is_changing:
                message = "Игра завершена: стабильная конфигурация достигнута."
            elif self.life.is_max_generations_exceeded:
                message = (
                    f"Игра завершена: достигнут лимит "
                    f"{self.life.max_generations} поколений."
                )
            else:
                message = "Игра завершена пользователем."

            try:
                screen.addstr(rows - 1, 2, message[: cols - 4])
                screen.refresh()
                screen.getch()  # Ждем любую клавишу перед выходом
            except curses.error:  # pylint: disable=no-member
                pass

        finally:
            curses.endwin()  # pylint: disable=no-member
