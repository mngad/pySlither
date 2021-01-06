# Slither.io bot using openCV

!["Working" GIF](currentprogress.gif)

## Requirements

`opencv`, `python3-dev` and `python-tk` via package manager. `pillow`, `numpy`, `imutils`, `pyautogui` via pip. 

Using openCV version 4.5, python 3.8

## Usage

Edit the `capture_size.conf` file to set the bounds of the slither.io window.
The lower boundary should avoid inclusing the minimap in the bottom right.

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
