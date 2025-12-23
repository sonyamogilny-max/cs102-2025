import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.clear()
        screen.border(0)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        start_y = 1
        start_x = 1

        for y in range(self.life.rows):
            if y >= curses.LINES - 2:
                break
            for x in range(self.life.cols):
                if x >= curses.COLS - 2:
                    break

                if self.life.curr_generation[y][x] == 1:
                    try:
                        screen.addch(start_y + y, start_x + x, '■')
                    except curses.error:
                        pass
                else:
                    try:
                        screen.addch(start_y + y, start_x + x, ' ')
                    except curses.error:
                        pass

        info = f"Поколение: {self.life.generations} | Клавиша 'q' для выхода"
        try:
            screen.addstr(curses.LINES - 1, 2, info[:curses.COLS - 4])
        except curses.error:
            pass

        screen.refresh()

    def run(self) -> None:
        screen = curses.initscr()
        try:
            # Настройки curses
            curses.curs_set(0)  # Скрываем курсор
            screen.nodelay(1)  # Неблокирующий ввод
            screen.timeout(100)  # Таймаут для обновления экрана (100 мс)

            # Включаем поддержку цветов (если доступно)
            if curses.has_colors():
                curses.start_color()
                curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

            running = True

            while running and self.life.is_changing and not self.life.is_max_generations_exceeded:
                self.draw_borders(screen)
                self.draw_grid(screen)

                try:
                    key = screen.getch()

                    if key == ord('q') or key == ord('Q'):
                        running = False

                    elif key == 27:  # ESC
                        running = False

                    # Пауза по пробелу
                    elif key == ord(' '):
                        screen.nodelay(0)  # Блокирующий ввод для паузы
                        screen.addstr(curses.LINES - 1, 2, "Пауза. Нажмите любую клавишу для продолжения...")
                        screen.refresh()
                        screen.getch()  # Ждем любую клавишу
                        screen.nodelay(1)  # Возвращаем неблокирующий ввод

                except curses.error:
                    pass

                # Выполняем один шаг игры
                self.life.step()

                # Небольшая задержка для удобства восприятия
                time.sleep(0.1)

            # Отображаем финальное состояние
            self.draw_borders(screen)
            self.draw_grid(screen)

            # Сообщение о завершении
            if not self.life.is_changing:
                message = "Игра завершена: стабильная конфигурация достигнута."
            elif self.life.is_max_generations_exceeded:
                message = f"Игра завершена: достигнут лимит {self.life.max_generations} поколений."
            else:
                message = "Игра завершена пользователем."

            try:
                screen.addstr(curses.LINES - 1, 2, message[:curses.COLS - 4])
                screen.refresh()
                screen.getch()  # Ждем любую клавишу перед выходом
            except curses.error:
                pass

        finally:
            curses.endwin()
