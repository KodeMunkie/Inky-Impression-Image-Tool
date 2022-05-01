# Image Tool for Inky Impression 4" and 5.7"

Button controls:
* A - random image
* B - next image
* C - previous image
* D - switch between gif and logos folders

# Setup
````bash
git clone https://github.com/KodeMunkie/Inky-Impression-Image-Tool.git
pip3 install -r requirements.txt
````
* add images to folders:
  * `defaults` -  put `png` or `jpg` files which will be shown on boot.
  * `stills` - put `png` or `jpg` files here.

You can use sub folders.

* add script to autostart
````bash
sudo nano /etc/rc.local
sudo python3 /home/pi/Inky-Impression-Image-Tool/main.py
sudo reboot now
````
