# Slither.io bot using openCV

!["Working" GIF](currentprogress.gif)

## Requirements

`opencv`, `python3-dev` and `python-tk` via package manager. `pillow`, `numpy`, `imutils`, `pyautogui` via pip.

Using openCV version 4.5, python 3.8

## Usage
_IMPORTANT_ slither.io must be in low quality mode (top right of the screen), due to changes in the contrast, brightness and colour values.

### Automatically find capture windows

Run `python3 slither.py -c` to define the capture area based on mouse positions. Move the mouse to top left by the end of the first countdown and bottom right by the end of the second countdown. Values are saved to `capture_size.conf`. When `python slither.py` it reads from `capture_size.conf`.

### Manually find capture windows

Edit the `capture_size.conf` file to set the bounds of the slither.io window.

For example `19, 91, 970, 1015`, where `19, 91` is the upper left value and `970, 1015` is the bottom right value. Performance can be improved by reducing the area, but at the cost of enemy snake avoidance. Ensure that the yellow center marker is in the middle of the player snake head, else the contour detection will detect the player snake as an enemy.

Options for finding these values on windows: [Stackoverflow](https://superuser.com/questions/85822/utilities-for-finding-x-y-screen-coordinates) or [Point Position](https://www.snapfiles.com/get/pointpos.html) or trial and error...

On linux with xdotool, for example `xdotool getmouselocation --shell` from a terminal emulator with the mouse positioned at the corners of the slither.io window.

### Running

`python3 slither.py` from within `pySlither/slither/`. `python3 slither.py -c` to create the config file.

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
