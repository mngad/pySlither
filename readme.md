# Slither.io bot using openCV

!["Working" GIF](currBest.gif)

## Requirements

`opencv`, `python3-dev` and `python-tk` via package manager. `pillow`, `numpy`, `imutils`, `pyautogui` via pip. 

Using openCV version 4.5, python 3.8

## Usage

Change the screen grab area in `getScr()` function. I used xdotool (`xdotool getmouselocation --shell`), to "draw" out the shape of the capture window for the slither.io window.

Not sure if it works on windows...
