# Description
	Entry for the PyWeek 33 Game Jam, the theme is 'My Evil Twin'.
	{**Pyweek link}
	This is a puzzle game, the levels are easy (8 in total), but if you got stuck you can watch the game play video.
	The goal is to find the 'portals' to get out of all the levels. The problem is that you need to get out together with your twin and what is worse, you twin is evil so he will move in your opposite direction. Will you be able to find the way out and escape with your evil twin?
	
# Game Play
{**Youtube Link}

# How to run:
	Command line to run the game: python run_game.py
	You can change the resolution in the run_game.py

# Requirements:
	Python 3.9.1 (The game was only tested on this version)
	pygame 2.1.2

# How to Play
	At first you will see the title screen, press any key to continue.
	You will see the menu screen with the options (Use the mouse to press the buttons):
		-Play         : Start the game. Continue game if it has already started.
		-Reset Level : Start the current level from the beginning.
		-Level Select: You can choose the level that you want to play. (Only if you already unlock the level)
		-Make Level   : You can make your own level (More info below). This was for me, to easily make the levels.
		-Quit Game    : Quit the game. The game saves your progress.

	Play Mode:
		Your objective is to reach the goal (Red twin to the red circle, blue twin to the blue circle)
		Move controls: UP/DOWN/LEFT/RIGHT arrows or WASD
		ESC or QUIT (window button) : open menu screen if you are in the game, quit the game if you are in the menu screen.
		When reach the goal press SPACE or 'e' to continue.
		At the end of the level, you will see a title screen with some story/hints. Press any key to continue.

	Make Level Mode:
		Use the mouse to select the tile.
		Use the mouse wheel to select the object to add.
		Right click to add the selected object.
		Left click to remove the object in the selected tile.
		Press SPACE to save the level. (It will print the file name in the console)
		Press 'r' to load the last level.
		You can play in this mode, but you can't win the level, also there are some bugs playing in this mode. You need to add both twins, if not it crashes.
		Each time to enter this mode it resets.

# Assets
	All the assets are made by me.
	For the sprites/images were made in MS Paint.
	For the music and sounds were made in BeepBox (https://www.beepbox.co)
	(I have no idea what I was doing with for the music, is my first time trying to make music, sorry if your ears blew up)


# Thanks for Playing
