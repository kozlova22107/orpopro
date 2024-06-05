import pygame.display
import sys
from Widget import Widgets, Entry
class Menu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Minesweaper")

        self.screen = pygame.display.set_mode((600, 400))
        self.size_field_rules = Widgets(["Enter size field from 10 to 50"], 0, 50, 600, 100)
        self.bombs_cnt_rules = Widgets(["Enter bombs count"], 0, 50, 600, 100)
        self.entry_field = Entry(0, 150, 600, 100)
        self.size_field_buttons = Widgets(["Exit" ,"Continue"], 0, 250, 600, 100)
        self.bombs_cnt_buttons = Widgets(["Back" ,"Start"], 0, 250, 600, 100)

        self.size_field = 0
        self.bombs_cnt = 0

    def draw_enter_size_field(self):
        clock = pygame.time.Clock()
        is_start = False
        while not is_start:
            clock.tick(60)
            # ввод
            for event in pygame.event.get():
                buttons_out = self.size_field_buttons.manip(event)
                if event.type == pygame.QUIT or "Exit" in buttons_out:
                    pygame.quit()
                    sys.exit()
                elif "Continue" in buttons_out:
                    is_start = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_start = True
                self.entry_field.manip(event)
            # отрисовка
            self.size_field_rules.draw(self.screen)
            self.entry_field.draw(self.screen)
            self.size_field_buttons.draw(self.screen)
            pygame.display.flip()

        if self.entry_field.text.isdigit():
            self.size_field = int(self.entry_field.text)
        self.entry_field.text = ""
        self.draw_enter_bombs_cnt()

    def draw_enter_bombs_cnt(self):
        clock = pygame.time.Clock()
        is_start = False
        while not is_start:
            clock.tick(60)
            # ввод
            for event in pygame.event.get():
                buttons_out = self.bombs_cnt_buttons.manip(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif "Back" in buttons_out:
                    self.draw_enter_size_field()
                    return
                elif "Start" in buttons_out:

                    is_start = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_start = True
                self.entry_field.manip(event)
            # отрисовка
            self.bombs_cnt_rules.draw(self.screen)
            self.entry_field.draw(self.screen)
            self.bombs_cnt_buttons.draw(self.screen)
            pygame.display.flip()
        if self.entry_field.text.isdigit():
            self.bombs_cnt = int(self.entry_field.text)


    def run(self):
        self.draw_enter_size_field()

    def get_size(self):
        return self.size_field, self.bombs_cnt