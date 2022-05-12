# Image Tool for Inky Impression 4" and 5.7"

Button controls:
* 1 - random image
* 2 - next image
* 3 - previous image
* 4 - shutdown

# Information

This project fork differs from the original implementation - it is uses a single image
folder to read your image files from and contains no example images.

The goal of this fork is to simplify and clean the code base (ongoing) whilst implementing 
a better algorithm for the rendering of photos on the 7 colour display.

It achieves this with a custom palette and an Atkinson dither algorithm that adjusts for the 
e-ink's dark blue output (which for example is useless for sky blue) as well as avoiding 
PIL's dither bias towards a green representation of blue, or other over saturated yellow/orange
colours.

Unfortunately this algorithm is currently very slow, taking minutes on a device such as Pi Zero
to calculate, despite some caching of common colour data, and currently has no indicator of
rendering progress until it's ready to show.

It is hoped performance will improve in subsequent versions.

# Setup
````bash
git clone https://github.com/KodeMunkie/Inky-Impression-Image-Tool.git
pip3 install -r requirements.txt
````

# Usage
```bash
python3 /home/pi/Inky-Impression-Image-Tool/main.py /your/image/folder
```