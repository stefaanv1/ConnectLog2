# place to put extra information (e.g. score)

from typing import Self, Tuple
from math import log2
import locale
import pygame

class Status(pygame.sprite.Sprite):
    def __init__(self: Self, pos: Tuple[int, int], size: Tuple[int, int], font_color: str, bg_color: str): 
        super().__init__() 
  
        locale.setlocale(locale.LC_ALL, '')
        self.font_color: str = font_color
        self.bg_color: str = bg_color
        self.image: pygame.Surface = pygame.Surface(size) 
        self.rect: pygame.Rect = self.image.get_rect() 
        self.status_text: str = ""
        self.score: int = 0
        self.highest_tile: int = 0
        self._draw_sprite()
        self.rect.update(pos, size)
  
    def update(*args, **kwargs):
        pane = args[0]
        pane.rect.update(kwargs["pos"], pane.rect.size)

    def _draw_sprite(self: Self) -> None:
        self.image.fill(pygame.Color(self.bg_color))

        font = pygame.font.Font(None, 30)
        text: pygame.Surface = font.render(self.status_text, True, self.font_color)
        text_rect: pygame.Rect = text.get_rect()
        text_rect.top = 2
        text_rect.left = 5
        self.image.blit(text, text_rect)

        sc : str = f'Score: {self.score:n} ({int(log2(max(1, self.score)))})'
        text = font.render(sc, True, self.font_color)
        text_rect = text.get_rect()
        text_rect.top  = 35
        text_rect.left = 5
        self.image.blit(text, text_rect)

        ht : str = f'Highest tile: {2 ** self.highest_tile:n} (2^{self.highest_tile})'
        text = font.render(ht, True, self.font_color)
        text_rect = text.get_rect()
        text_rect.top  = 68
        text_rect.left = 5
        self.image.blit(text, text_rect)

    def set_text(self: Self, text: str) -> None:
        self.status_text = text
        self._draw_sprite()

    def set_score(self:Self, score: int) -> None:
        self.score = score
        self._draw_sprite()

    def set_highest_tile(self:Self, high: int) -> None:
        self.highest_tile = high
        self._draw_sprite()

class StatusPane:
    def __init__(self: Self, pos: Tuple[int, int], size: Tuple[int, int], font_color: str = "thistle4", bg_color: str = "ivory"): 
        super().__init__() 
        self.status = Status(pos, size, font_color, bg_color)
        self.group = pygame.sprite.Group()
        self.group.add(self.status)

    def draw(self: Self, surface: pygame.Surface) -> None:
        self.group.draw(surface)

    def set_text(self: Self, text: str) -> None:
        self.status.set_text(text)

    def set_score(self:Self, score: int) -> None:
        self.status.set_score(score)

    def set_highest_tile(self:Self, high: int) -> None:
        self.status.set_highest_tile(high)






