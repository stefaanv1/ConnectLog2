# free tiles retrieved to put in the board

import pygame

from dataclasses import dataclass
from enum import Enum
from typing import Self

class TileState(Enum):
    ON = 1
    OFF = 2
    TOGGLE = 3

# position of the tile in the grid
@dataclass
class TilePos:
    x: int = 0
    y: int = 0

    def __hash__(self):
        return self.x*10 + self.y

    def is_neighbour(self: Self, other: Self) -> bool:
        if self == other:
            return False
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1

class Tiles(object):
    colors = ["yellow2", "palevioletred1", "skyblue1", "olivedrab", "thistle4", 
              "teal", "orange", "purple", "navajowhite2", "darkblue", 
              "gold3", "sienna1", "blue", "springgreen2", "pink",
              "turquoise", "darkgreen", "orchid4", "red", "green",
              "saddlebrown", "seagreen"]
    MIN_NBR = 1
    MAX_NBR = 60
    @staticmethod
    def get_tile(number: int) -> pygame.sprite.Sprite:
        # gauge number, TODO: give out-of-range error instead
        number = min(Tiles.MAX_NBR, number)
        number = max(Tiles.MIN_NBR, number)
        return Tile(number, Tiles.colors[(number - 1) % len(Tiles.colors)])

    
class Tile(pygame.sprite.Sprite): 
    WIDTH = HEIGHT = 80
    def __init__(self: Self, number: int, color: str):
        super().__init__() 
  
        self.color = color
        self.number = number
        self.highlighted = False
        self.marked = False
        self.image = pygame.Surface([Tile.WIDTH, Tile.HEIGHT]) 
        self.__draw_sprite()
  
        self.rect = self.image.get_rect() 

    def get_number(self: Self) -> int:
        return self.number

    @staticmethod
    def update(*args, **kwargs):
        tile = args[0]
        tile.rect.update(kwargs["pos"], (Tile.WIDTH, Tile.HEIGHT))

    def highlight(self: Self, state: TileState):
        if state == TileState.ON:
            self.highlighted = True
        elif state == TileState.OFF:
            self.highlighted = False
        else: # State.TOGGLE
            self.highlighted = not self.highlighted
        self.__draw_sprite()

    def mark(self: Self, state: TileState):
        if state == TileState.ON:
            self.marked = True
        elif state == TileState.OFF:
            self.marked = False
        else: # State.TOGGLE
            self.marked = not self.marked
        self.__draw_sprite()

    def is_marked(self: Self):
        return self.marked

    def get_rect(self: Self) -> pygame.Rect:
        return self.rect

    def __draw_sprite(self: Self):
        # use unused color for transparency
        unused_color = "grey20"
        self.image.fill(pygame.Color(unused_color))
        self.image.set_colorkey(unused_color)
        pygame.draw.rect(self.image, self.color, pygame.Rect(0, 0, Tile.WIDTH, Tile.HEIGHT), width = 0, border_radius = 7) 
  
        font = pygame.font.Font(None, 60)
        text_color = pygame.Color("white") if not self.marked else pygame.Color("black")
        text = font.render(str(self.number), True, text_color)
        text_rect = text.get_rect(center=(Tile.WIDTH/2, Tile.HEIGHT/2))
        self.image.blit(text, text_rect)

        if self.highlighted:
            pygame.draw.rect(self.image, pygame.Color("white"), pygame.Rect(0, 0, Tile.WIDTH, Tile.HEIGHT), width = 2, border_radius = 7)







