# Slither.io bot using openCV

!["Working" GIF](currentprogress.gif)

## Requirements

`opencv`, `python3-dev` and `python-tk` via package manager. `pillow`, `numpy`, `imutils`, `pyautogui` via pip. 

Using openCV version 4.5, python 3.8

## Usage

Edit the `capture_size.conf` file to set the bounds of the slither.io window.

For example `19, 91, 970, 1015`, where `19, 91` is the upper left value and `970, 900` is the bottom right value.

Options for finding these values on windows: [Stackoverflow](https://superuser.com/questions/85822/utilities-for-finding-x-y-screen-coordinates) or [Point Position](https://www.snapfiles.com/get/pointpos.html) or trial and error...

On linux with xdotool, for example `xdotool getmouselocation --shell` from a terminal emulator with the mouse positioned at the corners of the slither.io window.

`python3 slither.py` to run.

Press `q` to exit the mouse control.

## How it works

Screengrabs the area with slither.io playing in. Uses [openCV](https://opencv.org/) for image tracking and contour detection and [pyautogui](https://pyautogui.readthedocs.io/en/latest/) for the required mouse input.
Uses `blob.png` for target matching to the food items. A heavily filtered,
colour and morphological, image is used for the contour detection of enemys.

## Visuals

- Green rectangle = food
- Pink cross = current target food
- Yellow cross = center / neutral point
- Red cross = enemy midpoint
- Orange = escape direction

Viewport 1: General Vision

Viewport 2: Contour based enemy detection
