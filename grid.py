# positions of tiles in the game, used by the game play

from dataclasses import dataclass
import pygame
from typing import Dict, Self
import random
from functools import reduce
import json
import os


from board import Board
from tiles import TilePos, Tiles
from config import Config


#to do: use Grid_Tile here and let board handle tile.Tile to separate model (gameplay, grid) from view (board, tiles, status_pane)
@dataclass
class GridTile:
    number: int = 0

class PositionedTiles(Dict):
    pos: TilePos
    tile: GridTile


class Grid(object):
    NBR_ROWS = 6
    NBR_COLUMNS = 5
    MIN_X = MIN_Y = 0
    MAX_X = NBR_COLUMNS - 1
    MAX_Y = NBR_ROWS - 1
    TOTAL_TILES = (MAX_X + 1) * (MAX_Y + 1)


    def __init__(self, board: Board):
        self.board: Board = board
        self.board.set_number_rows(Grid.NBR_ROWS)
        self.board.set_number_columns(Grid.NBR_COLUMNS)
        self.__tiles: PositionedTiles = PositionedTiles()
        
        for i, pos in enumerate(self.__iterate_tiles_pos()):
            self.__tiles[pos] = None # random: actually playing

    def to_json(self: Self):
        return { 'tile-numbers': [ t.number for t in self ] }

    def from_json(self: Self, js) -> None:
        if len(js['tile-numbers']) == self.TOTAL_TILES:
            for i, pos in enumerate(self.__iterate_tiles_pos()):
                self.set_tile(pos, js['tile-numbers'][i])


    def refill(self: Self, in_min: int, in_max: int, delay_ms: int) -> None:
        # first drop all tiles in the grid
        for y in range(self.MAX_Y,self.MIN_Y, -1):
            for x in range(self.MIN_X, self.MAX_X + 1):
                p = TilePos(x, y)
                if not self.get_tile(p):
                    self.drop_tile(p)

        self.animation_wait(delay_ms)

        # then fill up the empty spaces
        for y in range(self.MAX_Y,self. MIN_Y - 1, -1):
            for x in range(self.MIN_X, self.MAX_X + 1):
                p = TilePos(x, y)
                if not self.get_tile(p):
                    self.set_tile(p, random.randrange(in_min, in_max)) # actual game: random
                    # self.set_tile(p, 1 + y*self.MAX_Y + x) # test fill all numbers sequentially, no moves possible

    def check_connections_possible_for_pos(self: Self, pos: TilePos) -> bool:
        for n in self.__iterate_neighbour_tiles(pos):
            tile_n = self.get_tile(n)
            tile_pos = self.get_tile(pos)
            if tile_n and tile_pos:
                if tile_n.number == tile_pos.number:
                    return True
        return False


    def check_connections_possible(self: Self) -> bool:
        for p in self.__iterate_tiles_pos():
            if self.check_connections_possible_for_pos(p):
                return True
        return False

    def get_highest_number(self: Self) -> int:
        return reduce(lambda x, y: max(x, y), (t.number for t in self if t), 1)

    def get_tile(self: Self, pos: TilePos) -> GridTile:
    # def get_tile(self, pos):
        return self.__tiles[pos] if self.is_tilepos_in_grid(pos) else None

    def set_tile(self: Self, pos: TilePos, number: int) -> None:
    # def set_tile(self, new_pos, new_tile: Tile) -> None:
        self.__tiles[pos] = GridTile(number)
        self.board.set_tile(pos, number)

    def remove_tile(self: Self, pos: TilePos) -> None:
        self.__tiles[pos] = None;
        self.board.remove_tile(pos)

    # drop a higher tile to the given position
    def drop_tile(self: Self, pos: TilePos) -> bool: # return whether tile could be dropped
        for y in range(pos.y - 1, self.MIN_Y - 1, -1):
            pos_up = TilePos(pos.x, y)
            if t := self.get_tile(pos_up):
                self.set_tile(pos, t.number)
                self.remove_tile(pos_up)
                return True
        return False

    # remove all tiles with number lower than the given number
    def remove_low_tiles(self: Self, low: int) -> None:
        for p in self.__iterate_tiles_pos():
            if self.get_tile(p).number < low:
                self.remove_tile(p)

    def display_grid(self: Self) -> None:
        self.board.draw()

    def animation_wait(self: Self, delay_ms: int):
        self.display_grid()
        pygame.display.flip()
        pygame.time.delay(delay_ms)

    def __iterate_tiles_pos(self: Self):
        for i in range(self.TOTAL_TILES):
            yield TilePos(i % (self.MAX_X + 1), i // (self.MAX_X + 1))

    def __iterate_neighbour_tiles(self: Self, pos: TilePos):
        for x in range(pos.x - 1, pos.x + 2):
            for y in range(pos.y - 1, pos.y + 2):
                n = TilePos(x, y)
                if n != pos and self.is_tilepos_in_grid(n):
                    yield n

    def is_tilepos_in_grid(self: Self, pos: TilePos) -> bool:
        return (self.MIN_X <= pos.x <= self.MAX_X and
                self.MIN_Y <= pos.y <= self.MAX_Y)

    def __iter__(self):
        self.it = iter(self.__tiles)
        return self

    def __next__(self) -> GridTile:
        return self.__tiles[next(self.it)]

    @staticmethod
    def __get_filename() -> str:
        Config.make_user_datapath()
        return os.path.join(Config.get_user_datapath(), 'grid.json')

    def read(self: Self) -> None:
        p = self.__get_filename()
        try:
            with open(p, 'r') as f:
                js = json.load(f)
                self.from_json(js)
        except (KeyError, ValueError):
            self.__init__(self.board)
            os.remove(p)
        except FileNotFoundError:
            pass # no file found, no board should be read in.


    def write(self: Self) -> None:
        p = self.__get_filename()
        try:
            with open(p, 'w') as f:
                json.dump(self.to_json(), f)
        except Exception as e:
            print(e)

    def remove_file(self: Self) -> None:
        try:
            os.remove(self.__get_filename())
        except Exception:
            pass # no real problem if file can't be removed. Probably already removed.

    @staticmethod
    def is_file_present() -> bool:
        return os.path.isfile(Grid.__get_filename())
