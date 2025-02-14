# the board to be displayed, contains tile-sprites. uses a group to interface with pygame

from typing import Self, Tuple, Dict

import pygame

from tiles import Tile, Tiles, TilePos, TileState

class Board(object):
    SEP = 5 # space between tiles

    def __init__(self: Self, screen: pygame.Surface):
        self.group = pygame.sprite.Group()
        self.screen = screen
        self.number_rows = 0
        self.number_columns = 0
        self.__tiles = {}

    def set_number_rows(self: Self, rows: int) -> None:
        self.number_rows = rows

    def get_height(self: Self) -> int:
        return (Tile.HEIGHT + Board.SEP) * self.number_rows - Board.SEP

    def get_width(self: Self) -> int:
        return (Tile.WIDTH + Board.SEP) * self.number_columns - Board.SEP

    def set_number_columns(self: Self, cols: int) -> None:
        self.number_columns = cols

    def empty(self: Self) -> None:
        self.group.empty()

    def set_tile(self: Self, pos: TilePos, number: int) -> None:
        tile = Tiles.get_tile(number)
        Tile.update(tile, pos = (pos.x * (Tile.WIDTH + Board.SEP), pos.y * (Tile.HEIGHT + self.SEP)))
        self.__tiles[pos] = tile

    def remove_tile(self: Self, pos: TilePos):
        del self.__tiles[pos]

    def highlight(self: Self, pos: TilePos, state: TileState) -> None:
        if t := self.__tiles[pos]:
            t.highlight(state)

    def mark(self: Self, pos: TilePos, state: TileState) -> None: 
        if t := self.__tiles[pos]:
            t.mark(state)

    def get_tilerect(self: Self, pos: TilePos) -> pygame.Rect:
        if t := self.__tiles.get(pos):
            return t.get_rect() 
        else: 
            return None

    def __put_tiles_in_group(self: Self) -> None:
        self.empty()
        for t in self.__tiles.values():
            self.__add_tile_sprite(t)

    def __add_tile_sprite(self: Self, t: pygame.sprite) -> None:
        self.group.add(t)

    def draw(self: Self) -> None:
        self.__put_tiles_in_group()
        self.group.draw(self.screen)




