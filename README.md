# Image Tool for Inky Impression 4" and 5.7"

Button controls:
* 1 - random image
* 2 - next image
* 3 - previous image
* 4 - shutdown

# Warning

Note there is a custom dither algorithm that adjusts for the e-ink's poor dark blue output, 
as well as avoiding existing PIL dither bias towards a green representation of blue.

Unfortunately this algorithm is currently very slow, taking minutes on a device such as Pi Zero
to calculate, despite some caching of common colour data.

It is hoped performance will improve in subsequent versions.

# Setup
````bash
git clone https://github.com/KodeMunkie/Inky-Impression-Image-Tool.git
pip3 install -r requirements.txt
````

# Running
```bash
python3 /home/pi/Inky-Impression-Image-Tool/main.py /your/image/folder
```