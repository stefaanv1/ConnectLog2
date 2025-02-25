The aim is to make the Tile with the largest number.<br>
The game ends if no connections can be made anymore.

Connections are made first by connecting two tiles with the same number. After that extra tiles with the same number or doubles can be connected and so on.<br>
All tiles are removed except the last that is replaced with the sum of the connected tiles rounded to the next power over two (all tiles are powers over two).<br>
The game is called ConnectLog2 because you don't see the actual numbers but log2 of the numbers. This works because all tile numbers are powers over 2 and the tiles show the exponent.<br>
This way the numbers don't increase too much, but connecting two tiles will make a new tile with the next number.<br>
The status shows the highest tile in actual number and log2 and the score which is the sum of the actual numbers of all times with a rounded down log2.<br>

a-s-d-w and arrow keys work to navigate, space selects the tiles that connect and enter makes the new tile. Esc resets the selection.<br>
mouse single click and drag selects (and deselects) the tiles and double click makes the new tile. Right mouse button resets the selection.<br>
\<Ctrl-N\> makes a new game and \<Ctrl-Q\> quits the game, both with confirmation.<br>
On quit, the game can be saved for later.<br>

