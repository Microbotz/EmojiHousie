# EmojiHousie
A Simple Python project for Emoji Housie. The Source contains two different python script. TicketGenerator for generating tickets and GameBoardSimulator for playing the game.

# Requirements
Python 3.*
imgkit : https://pypi.org/project/imgkit/
Current version is tested on windows. 
Install any auto page refresh extension on your browser. This will be useful for automatically updating the board when ever its updated.

# Installation
No installation is required for this script. Make sure all the requirements are present.

# Uses

Ticket Generator
usage: TicketGenerator.py [-h] [-n N] [-i I] [-d D] [-o O] [-w W] [-c C]

```
optional arguments:
  -h, --help  show this help message and exit
  -n N        Number to Tickets. Default : 100
  -i I        Image Folder Path. This is where all the images used for housie ticker is stored. Could be any number.
  -d D        Output DataBase Path. This is where all the information about generated tickets will be stored and will be used by GameBoardSimulator.
  -o O        Output Ticket folder where all the generated tickets will be stored.
  -w W        wkhtmlToImage Path. This is used for rendering Tickets.
  -c C        Fix Corners in Ticket. If set to True, all the tickets will have images on corner. Default : False

GameBoardSimulator:
usage: GameBoardSimulator.py [-h] [-d D] [-b B]

optional arguments:
  -h, --help  show this help message and exit
  -d D        DataBase Path. Path of the data baase folder used while generating tickets.
  -b B        Board Path. This where the game board will be rendered as HTML.
  ```
 
 