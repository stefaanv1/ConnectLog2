pyinstaller --noconfirm --log-level=WARN ^
	--onefile --window ^
	--add-data="README.txt;." ^
	--add-data="images/Tile1-small.png;images" ^
	--icon images/Tile1.ico ^
	ConnectLog2.py