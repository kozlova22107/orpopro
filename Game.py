from Grid import Grid
import pygame
import sys

from Widget import Widgets


class Game:
    def __init__(self, board_size, bombs_cnt):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Minesweeper")
        if board_size < 10 or board_size > 50:
            board_size = 24
        if bombs_cnt <= 0 or bombs_cnt >= board_size ** 2:
            bombs_cnt = int(board_size ** 2 // 8)
        self.screen = pygame.display.set_mode((600, 720))
        self.timer = Widgets(["0"], 0, 0, 600, 60)
        self.grid = Grid(0, 60, 600, 600, board_size, bombs_cnt)
        self.buttons = Widgets(["Exit", "New game"], 0, 660, 600, 60)
        self.is_win = False

    def run(self):
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        time = start_time
        was_boom = False
        while True:
            clock.tick(60)
            # ввод
            for event in pygame.event.get():
                buttons_out = self.buttons.manip(event)
                if event.type == pygame.QUIT or "Exit" in buttons_out:
                    pygame.quit()
                    sys.exit()
                if "New game" in buttons_out:
                    return
                # Обрабатываем нажатие кнопок мыши
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()  # получаем позицию
                    if event.button == 1:  # Левая кнопка
                        if self.grid.push(*pos):
                            was_boom = True

                    elif event.button == 3:  # Правая кнопка
                        self.grid.set_flag(*pos)
            # обновляем таймер
            time = (pygame.time.get_ticks() - start_time) // 1000

            self.timer.widgets[0].change_text(str(time))
            # отрисовываем
            self.timer.draw(self.screen)
            self.grid.draw(self.screen)
            self.buttons.draw(self.screen)
            pygame.display.flip()

            # проверка конца игры
            if self.grid.is_win():
                self.is_win = True
                self.draw_win()
                break
            elif was_boom:
                self.draw_loose()
                break

    def draw_win(self):
        self.timer.widgets[0].change_text("ALL CLEAN! TIME: " + self.timer.widgets[0].last_text)

        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        while True:
            clock.tick(60)
            # ввод
            for event in pygame.event.get():
                buttons_out = self.buttons.manip(event)
                if event.type == pygame.QUIT or "Exit" in buttons_out:
                    pygame.quit()
                    sys.exit()
                if "New game" in buttons_out:
                    return
            # отрисовываем
            self.timer.draw(self.screen)
            self.grid.draw_true(self.screen)
            self.buttons.draw(self.screen)
            pygame.display.flip()

    def draw_loose(self):
	    self.timer.widgets[0].change_text("BOOOM!")

	    clock = pygame.time.Clock()
	    start_time = pygame.time.get_ticks()
	    while True:
	        clock.tick(60)
	        # ввод
	        for event in pygame.event.get():
	            buttons_out = self.buttons.manip(event)
	            if event.type == pygame.QUIT or "Exit" in buttons_out:
	                pygame.quit()
	                sys.exit()
	            if "New game" in buttons_out:
	                return
	        # отрисовываем
	        self.timer.draw(self.screen)
	        self.grid.draw_true(self.screen)
	        self.buttons.draw(self.screen)
	        pygame.display.flip()
