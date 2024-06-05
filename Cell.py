import pygame


class Cell:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.bomb = False
        self.state_visual = "idle"

    @staticmethod
    def load_resources(w, h):
        source = "sprites/"
        Cell.grow_sprite = pygame.transform.scale(pygame.image.load(source + "grow.png"), (w, h))
        Cell.idle_sprite = pygame.transform.scale(pygame.image.load(source + "idle.png"), (w, h))
        Cell.flag_sprite = pygame.transform.scale(pygame.image.load(source + "flag.png"), (w, h))
        Cell.bomb_sprite = pygame.transform.scale(pygame.image.load(source + "bomb.png"), (w, h))
        Cell.number_sprites = [pygame.transform.scale(pygame.image.load(source + f"number_{i}.png"), (w, h)) for i in
                               range(1, 9)]

    def is_bomb(self):
        return self.bomb

    def set_bomb(self):
        self.bomb = True

    def set_flag(self):
        if not self.state_visual.isdigit() and not self.state_visual == "grow":
            if self.state_visual == "flag":
                self.state_visual = "idle"
            else:
                self.state_visual = "flag"

    def set_num(self, n):
        self.state_visual = str(n)

    def push(self) -> bool:
        if self.bomb:
            return True
        self.state_visual = "grow"
        return False

    def is_excavated(self):
        if self.state_visual == "grow" or self.state_visual.isdigit():
            return True
        return False

    def draw(self, window):
        if self.state_visual == "flag":
            window.blit(self.flag_sprite, self.rect.topleft)
        elif self.state_visual.isdigit():
            window.blit(self.number_sprites[int(self.state_visual) - 1], self.rect.topleft)
        elif self.state_visual == "idle":
            window.blit(self.idle_sprite, self.rect.topleft)
        elif self.state_visual == "grow":
            window.blit(self.grow_sprite, self.rect.topleft)

    def draw_true(self, window):
        if self.bomb:
            window.blit(self.bomb_sprite, self.rect.topleft)
        else:
            window.blit(self.grow_sprite, self.rect.topleft)