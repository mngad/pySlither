# Slither.io bot using openCV

!["Working" GIF](currBest.gif)

## Requirements

using conda
conda create -n pySlither python=3.8
pip install -r requirements.txt

## Usage for Linux/Unix

Change the screen grab area in `getScr()` function. I used xdotool (`xdotool getmouselocation --shell`), to "draw" out the shape of the capture window for the slither.io window.

Not sure if it works on windows...

`python3 slither.py` to run
