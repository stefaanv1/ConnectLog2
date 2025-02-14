# start and end of the program 
#
# This game is based on the "Offline Games - No WIFI Games" android collections of games app game called "Number Connect". I haven't seen it elsewhere.
# Connect 2 neighbouring tiles with same value and extent with same value or 1 up to make a new value on the last connected tile.
# The aim is to make the biggest number possible and the game ends when no tiles can be connected anymore.
# The numbers are the exponents of the power over 2 and can be found by the log2 function (hence the name).
# The new value is the log2 of the sum of all the real values rounded up.
# This may seem a bit weird, but the numbers become too large to represent rather quickly and thy are powers of 2 anyway.
# The biggest number is 60 (2^60 = 1,152,921,504,606,846,976 = 1 quintillion) and I doubt that this will ever be reached, but it can be extended.
# When the largest number becomes larger, the smallest sometimes disappears so it is easier to continue. (Not implemented yet)

# Bugs:
# None?

# remark: dataclasses may be used instead of tuples.

# Implemented:
# V implement status field under the board (should be enhanced by following implementations, like score)
# V check and announce end of the game. Maybe extra loop to restart. (Check is implemented but probably still has a bug, reset is added: Ctrl-r with confirmation, also quit: Ctrl-q with confirmation)
# V smallest numbers disappear (from 4096 (2^12) on every 2 largest numbers, so it still becomes more difficult). Remark: a bug may be introduced.
# V score (sum of all numbers on board) and status under the board
# V separate model (game_play, grid) and view (board, tiles)
# V mouse control, click to mark
# V mouse control double-click to make move (with timer)
# V mouse control by dragging (only marking, no unmarking or making move, which can be done by clicking and double clicking or keys)
# V extra information (real number of highest tile, calculation of marked tiles)
# To implement (somewhat prioritized):
# V local hiscore (top 10 with date) per user with nicer end if hiscore is beaten and handling largest number (decrease largest number to check)
#    V save to file (json) in users datapath
#    V read from file
#    V check for new hiscore (or insert in top 10)
#    V display at the end (by reuse screen, now also printed to console is done)
#    V handle possible errors with the hiscore-file, can maybe be improved, but users shouldn't mess with the file anyway.
# V logo icon
# ***** first showable version ******* V1.0
# V look for installer. (pyinstaller, win advanced installer)
# - put in github
# - make browser game (pygbag, replit.com?)
# - lines connecting marked tiles, which makes it easier to unmark (see original game)
# - help window (like test above, but more elaborated)
# - animation on changes in board
# - settings: difficulty, level of animation, colors
# - hiscore (local and via service, but then users are needed?), make a separate Data module to save the hiscore
# - nicer graphics, also the status pane or hiscore


PYGAME_HIDE_SUPPORT_PROMPT = 1

import pygame
from game_play import Gameplay
from about_help import Version
import os 

def main() :
    print("Starting the python application")
    
    pygame.init()
    pygame.display.set_caption(f"Connect Log2 V{Version.PROGRAM_VERSION}")

    dir_path = os.path.dirname(os.path.realpath(__file__))
    programIcon = pygame.image.load(os.path.join(dir_path, 'images', 'Tile1-small.png'))
    pygame.display.set_icon(programIcon)

    gameplay: Gameplay = Gameplay()
    gameplay.play()

    print("Closing the application")
    pygame.quit()

if __name__ == "__main__":
    main()
