# the board to be displayed, contains tile-sprites. uses a group to interface with pygame

from typing import Self, Tuple, Dict

import pygame

from tiles import Tile, Tiles, TilePos, TileState

class Board(object):
    SEP = 5 # space between tiles

    def __init__(self: Self, screen: pygame.Surface):
        self.__group = pygame.sprite.Group()
        self.__screen : pygame.Surface = screen
        self.__number_rows : int = 0
        self.__number_columns : int = 0
        self.__tiles = {}
        self.__marked_tiles = []
        self.__background : pygame.Surface = None

    def set_number_rows(self: Self, rows: int) -> None:
        self.__number_rows = rows

    def get_height(self: Self) -> int:
        return (Tile.HEIGHT + Board.SEP) * self.__number_rows - Board.SEP

    def get_width(self: Self) -> int:
        return (Tile.WIDTH + Board.SEP) * self.__number_columns - Board.SEP

    def set_number_columns(self: Self, cols: int) -> None:
        self.__number_columns = cols

    def empty(self: Self) -> None:
        self.__group.empty()

    def set_tile(self: Self, pos: TilePos, number: int) -> None:
        tile = Tiles.get_tile(number)
        Tile.update(tile, pos = (pos.x * (Tile.WIDTH + Board.SEP), pos.y * (Tile.HEIGHT + self.SEP)))
        self.__tiles[pos] = tile

    def remove_tile(self: Self, pos: TilePos):
        del self.__tiles[pos]

    def highlight(self: Self, pos: TilePos, state: TileState) -> None:
        if t := self.__tiles[pos]:
            t.highlight(state)

    def set_marked_tiles(self: Self, marked_tiles) -> None: 
        self.__marked_tiles = marked_tiles
        for p in self.__tiles:
            self.__tiles[p].mark(TileState.ON if p in self.__marked_tiles else TileState.OFF)

    def get_tile_rect(self: Self, pos: TilePos) -> pygame.Rect:
        if t := self.__tiles.get(pos):
            return t.get_rect() 
        else: 
            return None

    def __draw_background(self: Self) -> None:
        self.__background = pygame.Surface((self.get_width(), self.get_height()))
        self.__background.fill("grey")
        if len(self.__marked_tiles) > 1:
            centers = [(p.x * (Tile.WIDTH + Board.SEP) + Tile.WIDTH / 2, p.y * (Tile.HEIGHT + Board.SEP) + Tile.HEIGHT / 2) for p in self.__marked_tiles]
            for c1, c2 in zip(centers, centers[1:]):
                pygame.draw.line(self.__background, pygame.Color("black"), c1, c2, 7)
        self.__screen.blit(self.__background, self.__background.get_rect())

    def __put_tiles_in_group(self: Self) -> None:
        self.empty()
        for t in self.__tiles.values():
            self.__add_tile_sprite(t)

    def __add_tile_sprite(self: Self, t: pygame.sprite) -> None:
        self.__group.add(t)

    def draw(self: Self) -> None:
        self.__draw_background()
        self.__put_tiles_in_group()
        self.__group.draw(self.__screen)




