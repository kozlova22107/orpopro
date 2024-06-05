import pygame


class Widget:
    def __init__(self, text, rect, bg_color, font_color):
        self.bg_rect = rect
        self.bg_color = bg_color
        self.font_color = font_color
        self.font = pygame.font.Font(None, 32)
        self.text = self.font.render(text, True, self.font_color)
        self.text_rect = self.text.get_rect(center=self.bg_rect.center)

    def change_text(self, text):
        self.last_text = text
        self.text = self.font.render(text, True, self.font_color)
        self.text_rect = self.text.get_rect(center=self.bg_rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.bg_rect)
        screen.blit(self.text, self.text_rect)


class Widgets:
    def __init__(self, widgets, x, y, w, h, bg_color=(0, 0, 0), font_color=(255, 255, 255)):
        self.widgets = []
        self.text_in_widget = widgets
        self.height_sprite, self.width_sprite = h, w // len(widgets)
        for ind, text in enumerate(widgets):
            rect = pygame.rect.Rect(x + ind * self.width_sprite,
                                    y,
                                    self.width_sprite,
                                    self.height_sprite)
            self.widgets.append(Widget(text, rect, bg_color, font_color))

    def manip(self, event):
        result = []
        if event.type == pygame.MOUSEBUTTONDOWN:
            for ind, widget in enumerate(self.widgets):
                if widget.bg_rect.collidepoint(event.pos):
                    result.append(self.text_in_widget[ind])
        return result

    def draw(self, screen):
        for widget in self.widgets:
            widget.draw(screen)


class Entry:
    def __init__(self, x, y, w, h, bg_color=(0, 0, 0), font_color=(255, 255, 255)):
        self.text_label = None
        self.bg_rect = pygame.rect.Rect(x, y, w, h)
        self.bg_color = bg_color
        self.font_color = font_color
        self.font = pygame.font.Font(None, 32)
        self.text = ""
        self.text_label = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_label.get_rect(center=self.bg_rect.center)

    def manip(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if event.unicode.isdigit():
                    self.text += event.unicode
            self.text_label = self.font.render(self.text, True, self.font_color)
            self.text_rect = self.text_label.get_rect(center=self.bg_rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.bg_rect)
        screen.blit(self.text_label, self.text_rect)