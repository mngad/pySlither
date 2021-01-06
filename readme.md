# Slither.io bot using openCV

!["Working" GIF](currentprogress.gif)

## Requirements

`opencv`, `python3-dev` and `python-tk` via package manager. `pillow`, `numpy`, `imutils`, `pyautogui` via pip. 

Using openCV version 4.5, python 3.8

## Usage

Edit the `capture_size.conf` file to set the bounds of the slither.io window.
The lower boundary should avoid inclusing the minimap in the bottom right.

For example `19, 91, 970, 900`, where `19, 91` is the upper left value and `970, 900` is the bottom right value.

Options for finding these values on windows: ![Stackoverflow](https://superuser.com/questions/85822/utilities-for-finding-x-y-screen-coordinates), or easily on linux with xdotool, for example `xdotool getmouselocation --shell` from a terminal emulator with the mouse positioned at the corners of the slither.io window.

Not sure if it works on windows...

`python3 slither.py` to run

## How it works

Use `blob.png` for target matching to the food items. A heavily filtered,
colour and morphological, image is used for the contour detection of enemys.

## Visuals

- Green rectangle = food
- Pink cross = current target food
- Yellow cross = center / neutral point
- Red cross = enemy midpoint
- Orange = escape direction

Viewport 1: General Vision









Viewport 2: Contour based enemy detection
