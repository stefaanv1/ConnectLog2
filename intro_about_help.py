# about and help info
# also version for internal use (?)
from typing import Self
import pygame
from tiles import Tiles, Tile, TileState
from enum import Enum

from grid import Grid
class Version:
    PROGRAM_VERSION = 1.1

class IntroPage:
    class Return(Enum):
        NEW = 1
        LOAD = 2
        HELP = 3
        QUIT = 4

    def __init__(self: Self, image: pygame.Surface):
        self.image = image
        self.bg_color = "grey"

    def show(self: Self) -> bool:
        self.__display()
        return self.__handle_input()

    # remark: temporary code
    def __display(self: Self) -> None:
        self.image.fill(pygame.Color("paleturquoise"))

        font = pygame.font.Font(None, 30)
        text: pygame.Surface = font.render(f"Connect Log2 V{Version.PROGRAM_VERSION}", True, "darkblue")
        text_rect: pygame.Rect = text.get_rect()
        text_rect.centery = 70
        text_rect.centerx = self.image.get_rect().center[0]
        self.image.blit(text, text_rect)

        height = self.image.get_rect().center[1] - 40
        centerx = self.image.get_rect().center[0] - 40
        bg_height = 100
        background = pygame.Surface((self.image.get_rect().width, self.image.get_rect().height))
        bg_rect = background.get_rect()
        background.fill(pygame.Color(self.bg_color))
        background.set_colorkey(self.bg_color)

        tile1 = Tiles.get_tile(1)
        Tile.update(tile1, pos = (centerx - 85, height - 40))
        tile2 = Tiles.get_tile(1)
        Tile.update(tile2, pos = (centerx, height - 40))
        tile3 = Tiles.get_tile(2)
        Tile.update(tile3, pos = (centerx + 85, height - 40))
        group = pygame.sprite.Group()
        group.add(tile1)
        group.add(tile2)
        group.add(tile3)
        group.draw(background)
        self.image.blit(background, background.get_rect())

        font = pygame.font.Font(None, 24)
        option_text: str = "New game, Load saved game, Help <N/L/H>" if Grid.is_file_present() else "New game, Help <N/H>"
        text: pygame.Surface = font.render(option_text, True, "darkblue")
        text_rect: pygame.Rect = text.get_rect()
        text_rect.centery = self.image.get_rect().height - 70
        text_rect.centerx = self.image.get_rect().center[0]
        self.image.blit(text, text_rect)

        font = pygame.font.Font(None, 18)
        option_text: str = "Made by Stefaan Verstraeten"
        text: pygame.Surface = font.render(option_text, True, "grey56")
        text_rect: pygame.Rect = text.get_rect()
        text_rect.centery = self.image.get_rect().height - 30
        text_rect.centerx = self.image.get_rect().center[0]
        self.image.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(300)

        tile1.mark(TileState.ON)
        group.draw(background)
        self.image.blit(background, background.get_rect())
        pygame.display.update(pygame.Rect(0, height - 50, self.image.get_rect().width, height + 50))
        pygame.display.flip()
        pygame.time.delay(300)

        tile2.mark(TileState.ON)
        pygame.draw.line(background, pygame.Color("black"), (centerx - 55, height), (centerx + 30, height), 7)
        group.draw(background)
        self.image.blit(background, background.get_rect())
        pygame.display.update(pygame.Rect(0, height - 50, self.image.get_rect().width, height + 50))
        #pygame.display.update()
        pygame.time.delay(300)

        tile3.mark(TileState.ON)
        pygame.draw.line(background, pygame.Color("black"), (centerx + 30, height), (centerx + 115, height), 7)
        group.draw(background)
        self.image.blit(background, background.get_rect())
        pygame.display.update(pygame.Rect(0, height - 50, self.image.get_rect().width, height + 50))

    # remark: temporary code
    def __handle_input(self: Self) -> bool:
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.Return.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        return self.Return.NEW
                    elif event.key == pygame.K_l:
                        return self.Return.LOAD
                    elif event.key == pygame.K_h:
                        return self.Return.HELP
                    return True


class HelpPage:
    def show(self: Self):
        pass


