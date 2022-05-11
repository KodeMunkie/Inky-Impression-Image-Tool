#!/usr/bin/env python3
import os
import glob
import sys
import ImageProcessor
from random import randrange

import signal

import RPi.GPIO as GPIO
import textwrap

from inky.auto import auto
#from inky.mock import InkyMockImpression as Inky # Simulator

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("""This script requires PIL/Pillow, try:
sudo apt install python3-pil
""")

print("""
inky_frame.py - Display a image files on the E-Ink.
""")

# extensions to load
EXTENSIONS = ('*.png', '*.jpg')

# Gpio pins for each button (from top to bottom)
BUTTONS = [5, 6, 16, 24]

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)


inky = auto(ask_user=True, verbose=True)
# inky = Inky();

class ImageFrame:
    images = []
    current_image_index = 0
    path_to_images = ''
    imPro = None

    def __init__(self, path_to_images):
        self.imPro =  ImageProcessor.ImageProcessor()
        self.path_to_images = path_to_images
        self.init_files() 
        self.add_buttons()
  
    def init_files(self):
        for extension in EXTENSIONS:
            self.images.extend(glob.glob("%s/**/%s" % (self.path_to_images, extension), recursive=True))
    
        if len(self.images) == 0:
            error_message = "Error: folder \"%s\" contains no images" % self.images
            self.display_error_message(error_message)
            exit(1)

    def display_next_image(self):
        next_image_index = self.current_image_index + 1

        if next_image_index >= len(self.images):
            next_image_index = 0

        self.display_image_by_index(next_image_index)

    def display_previous_image(self):
        prev_image_index = self.current_image_index - 1

        if prev_image_index < 0:
            prev_image_index = len(self.images) - 1

        self.display_image_by_index(prev_image_index)

    def display_error_message(self, error_text, text_color=(0, 0, 0), text_start_height=0):
        image_message = Image.new("RGB", inky.resolution, color=(200, 0, 0))
        font = ImageFont.load_default()
        self.draw_multiple_line_text(image_message, error_text, font, text_color, text_start_height)
        try:
            inky.set_image(image_message, 1)
            inky.show()
        except BaseException as err:
            error_text = f"Unexpected {err=}, {type(err)=}"
            print(error_text)

    def display_image_by_index(self, number):
        try:
            print('Opening image ', self.images[number])
            image = Image.open(self.images[number])
            resizedimage = image.resize(inky.resolution)
            self.imPro.diffuse_image(resizedimage)
            inky.set_image(resizedimage, 1)
            inky.show()
        except BaseException as err:
            error_text = f"Unexpected {err=}, {type(err)=}"
            self.display_error_message(error_text)

    def display_random_image(self):
        image_index_to_show = randrange(len(self.images))
        self.display_image_by_index(image_index_to_show)

    def draw_multiple_line_text(image, text, font, text_color, text_start_height):
        draw = ImageDraw.Draw(image)
        image_width, image_height = image.size
        y_text = text_start_height
        lines = textwrap.wrap(text, width=40)
        for line in lines:
            line_width, line_height = font.getsize(line)
            draw.text(((image_width - line_width) / 2, y_text),
                    line, font=font, fill=text_color)
            y_text += line_height
     
    def add_buttons(self):
        print('Adding button hooks')
        for pin in BUTTONS:
            GPIO.add_event_detect(pin, GPIO.FALLING, self.handle_button, bouncetime=5000)

    def handle_button(self, pin):
        last_button = BUTTONS.index(pin)
        if last_button == 0:
            imageFrame.display_random_image()
        elif last_button == 1:
            imageFrame.display_next_image()
        elif last_button == 2:
            imageFrame.display_previous_image()
        elif last_button == 3:
            subprocess.run("sudo shutdown --poweroff now", shell=True)

imageFrame = ImageFrame(sys.argv[1])
imageFrame.display_image_by_index(0)
signal.pause()