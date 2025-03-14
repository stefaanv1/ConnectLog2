# the actual handling of the game.

from dataclasses import dataclass
from itertools import filterfalse
from turtle import width
from typing import Self, Tuple
from enum import Enum
from copy import deepcopy
import math
import time
from functools import reduce

import pygame
from tiles import TileState, TilePos, Tile
from grid import Grid, GridTile
from statuspane import StatusPane
from board import Board
from mouse import MouseEventChecker
from hiscore import HiScore
from config import Config

# range of numbers from which the new tile number can be chosen
@dataclass
class TileRange:
    low: int = 0
    high: int = 0

class Gameplay:
    NEW_TILE_RANGE_SIZE = 8
    class Start(Enum):
        NEW = 1
        LOAD = 2


    def __init__(self, screen: pygame.Surface):
        # the actual game window
        self.screen = screen
        self.__animation_delay_ms = 500

        # flag to end the game
        self.running = True
        # status need for confirmation
        self.quit = False
        self.reset = False
        self.no_moves = False
        # graphics to display the board of tiles
        self.board: Board = Board(self.screen)
        
        self.tile_range: TileRange = self.get_tile_range(1)
        self.grid = Grid(self.board)
        self.active_tile_pos = TilePos(0, 0)
        self.marked_tiles = []

        # put status under the board, filling up the space
        self.board_height = self.board.get_height()
        self.board_width = self.board.get_width()
        self.status = StatusPane((0, self.board_height), (screen.get_width(), screen.get_height() - self.board_height))

        self.clock = pygame.time.Clock()
        self.mouse_checker: MouseEventChecker = MouseEventChecker(self.status)

    # the actual game loop
    def play(self: Self, start):

        hiscore: HiScore = HiScore(Config.get_user(), self.screen)

        save_game : bool = False
        if start == Gameplay.Start.LOAD:
            self.grid.read()
        else:
            self.grid.remove_file()

        self.grid.refill(self.tile_range.low, self.tile_range.high, 0)
        self.score = self.calculate_score()
        self.handle_highest_number()
        self.status.set_score(self.calculate_score())

        while self.running:

            if not self.grid.check_connections_possible():
                self.status.set_message("No more moves, quit or next game? <q/n>")
                self.no_moves = True
            if self.active_tile_pos and self.grid.get_tile(self.active_tile_pos):
                self.board.highlight(self.active_tile_pos, TileState.ON)
        
            self.grid.display_grid()
            self.status.draw(self.screen)
        
            # flip() the display to put your work on screen
            pygame.display.flip()
        
            if self.active_tile_pos and self.grid.get_tile(self.active_tile_pos):
                self.board.highlight(self.active_tile_pos, TileState.OFF)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.status.set_message("quit, safe for later, continue? <q/s/c>")
                    self.quit = True
                    break

                if event.type == pygame.KEYUP:
                    # quit the game, todo: ask confirmation in status
                    if event.key == pygame.K_q and event.mod & pygame.KMOD_CTRL != 0:
                        self.status.set_message("quit, safe for later, continue? <q/s/c>")
                        self.quit = True
                        break
                    # restart the game, todo: ask confirmation in status
                    elif event.key == pygame.K_n and event.mod & pygame.KMOD_CTRL != 0:
                        self.status.set_message("new game? <y/n>")
                        self.reset = True;
                        break
                    elif event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL != 0:
                        self.quit = hiscore.display()
                        break

                    # navigation keys (a-s-d-w, useful on qwerty and arrows, useful on full keyboards)
                    elif (event.key == pygame.K_w or event.key == pygame.K_UP) and self.active_tile_pos.y > self.grid.MIN_Y:
                        self.active_tile_pos.y -= 1
                        break
                    elif ((event.key == pygame.K_s and not self.quit) or event.key == pygame.K_DOWN) and self.active_tile_pos.y < self.grid.MAX_Y:
                        self.active_tile_pos.y += 1
                        break
                    elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and self.active_tile_pos.x > self.grid.MIN_X:
                        self.active_tile_pos.x -= 1
                        break
                    elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and self.active_tile_pos.x < self.grid.MAX_X:
                        self.active_tile_pos.x += 1
                        break

                    #TODO: put marking and make_move in functions instead of delaying it.
                    # <Space>mark the highlighted tile, making a string of tiles
                    elif event.key == pygame.K_SPACE:
                        self.mark_highlighted_tile()
                        break
                    # <Enter> handle the marked tiles
                    elif event.key == pygame.K_RETURN:
                        self.make_move()
                        break
                    # <Esc>: reset the marked tiles
                    elif event.key == pygame.K_ESCAPE:
                        self.reset_marked_tiles()
                        break

                    elif (event.key == pygame.K_y and self.reset) or (event.key == pygame.K_n and self.no_moves):
                        self.reset = self.no_moves = False
                        hiscore.add_score(self.calculate_score(), self.grid.get_highest_number())
                        self.__init__()
                        self.grid.refill(self.tile_range.low, self.tile_range.high, 0)
                        self.score = self.calculate_score()
                        self.handle_highest_number()
                        self.status.set_score(self.calculate_score())
                        break
                    elif event.key == pygame.K_q:
                        if self.quit:
                            self.quit = False
                            self.running = False
                            save_game = False
                            break
                    elif event.key == pygame.K_s:
                        if self.quit:
                            self.quit = False
                            self.running = False
                            save_game = True
                            break
                    elif event.key == pygame.K_q:
                        if self.no_moves:
                            save_game = False
                            self.running = False
                            break
                    elif (event.key == pygame.K_n and self.reset) or (event.key == pygame.K_c and self.quit):
                        self.status.set_message("")
                        self.reset = self.quit = False
                        break

                else:
                    click: MouseEventChecker.Click = self.mouse_checker.check(event)
                    if click == MouseEventChecker.Click.SINGLE:
                        self.active_tile_pos = self.board_position_to_grid_pos(self.mouse_checker.get_clicked_pos())
                        if self.active_tile_pos:
                            self.mark_highlighted_tile()
                        break
                    elif click == MouseEventChecker.Click.DOUBLE:
                        # take clicked tile into account but don't unmark it
                        self.active_tile_pos = self.board_position_to_grid_pos(self.mouse_checker.get_clicked_pos())
                        if self.active_tile_pos:
                            self.mark_highlighted_tile_last_on()
                        self.make_move()
                        break
                    elif click == MouseEventChecker.Click.DRAG_START:
                        self.active_tile_pos = self.board_position_to_grid_pos(self.mouse_checker.get_clicked_pos())
                        if self.active_tile_pos:
                            self.mark_highlighted_tile_first_on()
                            break
                    elif click == MouseEventChecker.Click.DRAG:
                        previous_active = self.active_tile_pos
                        board_pos = self.mouse_checker.get_clicked_pos()
                        if board_pos:
                            self.active_tile_pos = self.board_position_to_grid_pos_circle(board_pos)
                            if self.active_tile_pos != previous_active:
                                if self.active_tile_pos:
                                    self.mark_highlighted_tile_drag()
                                    break
                                else:
                                    self.active_tile_pos = previous_active
                    elif click == MouseEventChecker.Click.DRAG_STOP:
                        pass
                    elif click == MouseEventChecker.Click.RIGHT_BUTTON:
                        self.reset_marked_tiles()
                        break

            self.clock.tick(60)

        if save_game:
            self.grid.write()
        else:
            hiscore.add_score(self.calculate_score(), self.grid.get_highest_number())
            self.grid.remove_file()


    def __actually_mark_when_possible(self: Self, t: GridTile) -> None:
            last_pos = self.marked_tiles[-1]
            if self.active_tile_pos.is_neighbour(last_pos):
                last_t = self.grid.get_tile(last_pos)
                if t.number == last_t.number or (len(self.marked_tiles) > 1 and t.number == last_t.number + 1):
                    self.marked_tiles.append(deepcopy(self.active_tile_pos))
                    self.board.set_marked_tiles(self.marked_tiles)
                    self.__show_sum()

    # <Space>: mark the tile, making a string of marked tiles to handle in the next move
    def mark_highlighted_tile(self: Self) -> None:
        if t := self.grid.get_tile(self.active_tile_pos):
            # no marked tiles: mark highlighted if connections are possible (neighbour with same number)
            if not self.marked_tiles:
                if self.grid.check_connections_possible_for_pos(self.active_tile_pos):
                    self.marked_tiles.append(deepcopy(self.active_tile_pos))
                    self.board.set_marked_tiles(self.marked_tiles)
                    self.__show_sum()
                return
            # some tiles are marked
            # last marked tile: undo marking
            if self.active_tile_pos == self.marked_tiles[-1]:
                self.marked_tiles.pop()
                self.board.set_marked_tiles(self.marked_tiles)
                self.__show_sum()
                return
            # don't mark twice the same tile
            if self.active_tile_pos in self.marked_tiles:
                return
            # following tile must be neighbour and same or first higher number
            self.__actually_mark_when_possible(t)

    # specific for drag start no unmarking but mark if no tiles are marked yet
    def mark_highlighted_tile_first_on(self: Self) -> None:
        if t := self.grid.get_tile(self.active_tile_pos):
            # no marked tiles: mark highlighted if connections are possible (neighbour with same number)
            if not self.marked_tiles:
                if self.grid.check_connections_possible_for_pos(self.active_tile_pos):
                    self.marked_tiles.append(deepcopy(self.active_tile_pos))
                    self.board.set_marked_tiles(self.marked_tiles)
                    self.__show_sum()
                return
            # don't mark twice the same tile
            if self.active_tile_pos in self.marked_tiles:
                return
            # following tile must be neighbour and same or first higher number
            self.__actually_mark_when_possible(t)


    # specific for marking when double clicking to avoid user forgetting to single click before double clicking
    def mark_highlighted_tile_last_on(self: Self) -> None:
        if t := self.grid.get_tile(self.active_tile_pos):
            # no marked tiles: no marking needed
            if not self.marked_tiles:
                return
            # don't mark twice the same tile
            if self.active_tile_pos in self.marked_tiles:
                return
            # following tile must be neighbour and same or first higher number
            self.__actually_mark_when_possible(t)

    def mark_highlighted_tile_drag(self: Self) -> None:
        if t := self.grid.get_tile(self.active_tile_pos):
            # no marked tiles: no marking needed
            if not self.marked_tiles:
                return
            # unmark last when returning to previous marked tile
            if len(self.marked_tiles) > 1 and self.active_tile_pos == self.marked_tiles[-2]:
                self.marked_tiles.pop()
                self.board.set_marked_tiles(self.marked_tiles)
                self.__show_sum()
                return
            # don't mark twice the same tile
            if self.active_tile_pos in self.marked_tiles:
                return
            # following tile must be neighbour and same or first higher number
            self.__actually_mark_when_possible(t)

    # <Enter> or double click left mouse button: make the move: handle the marked tiles to make a new tile on the position of the last marked tile
    def make_move(self: Self) -> None:
        if not self.marked_tiles:
            return
        sum = 0
        # remove all the marked tiles and calculate new tile
        # round up to next log2 by adding 1 if the 2 ** log2(sum) != sum
        for pos in self.marked_tiles:
            t = self.grid.get_tile(pos)
            self.grid.remove_tile(pos)
            sum += 2 ** t.number
        nbr = int(math.log2(sum))
        if 2 ** nbr != sum:
            nbr += 1
        # put new number on the position of the last marked number
        pos = self.marked_tiles[-1]
        self.marked_tiles.clear()
        self.grid.set_tile(pos, nbr)
        self.grid.animation_wait(self.__animation_delay_ms)

        # let the grid refill the board by dropping tiles and adding new ones.
        self.grid.refill(self.tile_range.low, self.tile_range.high, self.__animation_delay_ms)
        self.grid.animation_wait(self.__animation_delay_ms)
        self.handle_highest_number()

        self.status.set_score(self.calculate_score())
        self.status.set_message("")

    # <Esc>: reset, let the user start a new string of marked tiles
    def reset_marked_tiles(self: Self) -> None:
        self.marked_tiles.clear()
        self.board.set_marked_tiles(self.marked_tiles)
        self.status.set_message("")

    def handle_highest_number(self: Self) -> None:
        high = self.grid.get_highest_number()
        self.status.set_highest_tile(high)
        new_tile_range: TileRange = self.get_new_tiles_range_based_on_highest_number(high)
        if new_tile_range == self.tile_range: # no change: no action needed.
            return
        self.tile_range = new_tile_range
        self.grid.remove_low_tiles(self.tile_range.low)
        self.grid.animation_wait(self.__animation_delay_ms)
        self.grid.refill(self.tile_range.low, self.tile_range.high, self.__animation_delay_ms)

    @staticmethod
    def get_tile_range(low: int) -> TileRange:
        return TileRange(low, low + Gameplay.NEW_TILE_RANGE_SIZE)

    def get_new_tiles_range_based_on_highest_number(self: Self, number: int) -> TileRange:
        low = max(1, (number - 8) // 2)
        return self.get_tile_range(low)

    def calculate_score(self: Self) -> int:
        # the score is the sum of 2 to the power of the tile-number
        return reduce(lambda tot, n: tot + 2**n, (t.number for t in self.grid if t), 0)

    def board_position_to_grid_pos(self: Self, b_pos: Tuple[int, int]) -> TilePos | None: # None: not positioned on a tile
        # remark: the position could also have been found by iterating the tiles. This should be a bit faster and I felt like trying this, but it is less flexible to use in other games
        if b_pos[0] >= self.board_width or b_pos[0] >= self.board_height:
            return None
        x1 = b_pos[0] % (Tile.WIDTH + Board.SEP)
        y1 = b_pos[1] % (Tile.HEIGHT + Board.SEP)
        if x1 > Tile.WIDTH or y1 > Tile.HEIGHT:
            return None # in between tiles
        return TilePos(b_pos[0] // (Tile.WIDTH + Board.SEP), b_pos[1] // (Tile.HEIGHT + Board.SEP))

    # avoid adding unwanted tiles while dragging by only selecting a tile via a circle
    def board_position_to_grid_pos_circle(self: Self, board_pos: Tuple[int, int]) -> TilePos | None: # None: not positioned on a tile
        grid_pos: TilePos = self.board_position_to_grid_pos(board_pos)
        if not grid_pos:
            return None
        rect: pygame.Rect = self.board.get_tile_rect(grid_pos)
        if not rect:
            return None
        radius_sq: int = (min(rect.width, rect.height) / 2) ** 2
        from_center: int = (board_pos[0] - rect.center[0]) ** 2 + (board_pos[1] - rect.center[1]) ** 2
        return grid_pos if from_center <= radius_sq else None

    def __show_sum(self: Self) -> None:
        texts = []
        sum = 0
        for pos in self.marked_tiles:
            t : GridTile = self.grid.get_tile(pos)
            texts.append(f"{2**t.number}") 
            sum += 2**t.number
        
        text = f"{sum} (2^{math.log2(sum):.2f}) = " + " + ".join(texts) if texts else ""
        self.status.set_message(text)







