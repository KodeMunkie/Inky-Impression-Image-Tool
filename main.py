#!/usr/bin/env python3
import os
import glob
from random import randrange
import signal

import RPi.GPIO as GPIO
import textwrap

from inky.auto import auto

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("""This script requires PIL/Pillow, try:
sudo apt install python3-pil
""")

print("""
inky_frame.py - Display a image files on the E-Ink.
""")

# Gpio pins for each button (from top to bottom)
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, C and D respectively
LABELS = ['A', 'B', 'C', 'D']

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

inky = auto(ask_user=True, verbose=True)


def draw_multiple_line_text(image, text, font, text_color, text_start_height):
    """
    From ubuntu on [python PIL draw multiline text on image](https://stackoverflow.com/a/7698300/395857)
    """
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=40)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text),
                  line, font=font, fill=text_color)
        y_text += line_height


class ImageFrame:
    displayWidth = 600
    displayHeight = 448
    images = []
    images_albums = []
    images_artwork = []
    images_comics = []
    images_postcards = []
    images_default = []
    image = None
    image_file = None
    current_image_list = "default"
    image_file_extension = None
    current_image_index = 0

    def __init__(self, real_path, saturation=0.5, display_width=600, display_height=448):
        self.current_image_index = None
        self.image_file = None
        self.displayWidth = display_width
        self.displayHeight = display_height
        self.realpath = real_path
        self.saturation = saturation

        self.init_files()

    def init_files(self):

        print(self.realpath)

        extensions = ('*.png', '*.jpg')  # extensions to load
        for extension in extensions:
            self.images_albums.extend(glob.glob("%s/albums/**/%s" % (realpath, extension), recursive=True))
        print(self.images_albums)
        
        for extension in extensions:
            self.images_artwork.extend(glob.glob("%s/artwork/**/%s" % (realpath, extension), recursive=True))
        print(self.images_artwork)
        
        for extension in extensions:
            self.images_comics.extend(glob.glob("%s/comics/**/%s" % (realpath, extension), recursive=True))
        print(self.images_comics)
        
        for extension in extensions:
            self.images_postcards.extend(glob.glob("%s/postcards/**/%s" % (realpath, extension), recursive=True))
        print(self.images_postcards)
        
        for extension in extensions:
            self.images_default.extend(glob.glob("%s/default/**/%s" % (realpath, extension), recursive=True))

        print(self.images_default)

        self.images = self.images_default

    def switch_file_list(self):
        if self.current_image_list == "default":
            self.images = self.images_albums
            self.current_image_list = "albums"
        elif self.current_image_list == "albums":
            self.images = self.images_artwork
            self.current_image_list = "artwork"
        elif self.current_image_list == "artwork":
            self.images = self.images_comics
            self.current_image_list = "comics"
        elif self.current_image_list == "comics":
            self.images = self.images_postcards
            self.current_image_list = "postcards"
        else:
            self.images = self.images_default
            self.current_image_list = "default"
            
            

        if len(self.images) == 0:
            error_message = "Error: folder \"%s\" contains no images" % self.current_image_list
            print(error_message)

            error_image = self.render_error_message(error_message)
            inky.set_image(error_image, saturation=self.saturation)
            inky.show()
            exit(1)

        self.image_file = self.images[0]

    def display_next_image(self):
        print("display_next_sprite")
        next_sprite = self.current_image_index + 1

        if next_sprite >= len(self.images):
            next_sprite = 0

        self.display_image_by_index(next_sprite)

    def display_previous_image(self):
        print("display_previous_sprite")
        next_image_index = self.current_image_index - 1

        if next_image_index < 0:
            next_image_index = len(self.images) - 1

        self.display_image_by_index(next_image_index)

    def render_error_message(self, error_text, text_color=(0, 0, 0), text_start_height=0):
        image_message = Image.new("RGB", (self.displayWidth, self.displayHeight), color=(200, 0, 0))
        font = ImageFont.load_default()
        draw_multiple_line_text(image_message, error_text, font, text_color, text_start_height)
        return image_message

    def display_image_by_index(self, number):
        print("display_sprite_by_number: %s" % number)
        self.current_image_index = number
        self.image_file = self.images[number]

        print('Loading image: {}...'.format(self.image_file))
        try:
            image = Image.open(self.image_file)

            # upscale
            if image.width < self.displayWidth or image.height < self.displayWidth:
                image = image.resize((self.displayWidth, self.displayHeight))

            # Resize the image
            image_file_extension = self.image_file.lower().split(".")[-1]
            if image_file_extension != "gif":
                image = image.resize((self.displayWidth, self.displayHeight))

        except BaseException as err:
            error_text = f"Unexpected {err=}, {type(err)=}"
            print(error_text)
            image = self.render_error_message(error_text)

        print('Draw image')

        try:
            inky.set_image(image, saturation=self.saturation)
            inky.show()
        except BaseException as err:
            error_text = f"Unexpected {err=}, {type(err)=}"
            print(error_text)

    def display_random_image(self):
        """
        random choose one of two lists and choose show one random image
        :return:
        """
        print("display_random_image")
        # choose between two lists
        image_list_index = randrange(2)

        if image_list_index == 0:
            self.images = self.images_artwork
            self.current_image_list = "artwork"
        else:
            self.images = self.images_default
            self.current_image_list = "default"

        image_index_to_show = randrange(len(self.images))
        self.display_image_by_index(image_index_to_show)


realpath = os.path.dirname(os.path.realpath(__file__))

imageFrame = ImageFrame(realpath,
                        saturation=0.5,
                        display_width=600,
                        display_height=448
                        )

imageFrame.display_image_by_index(0)


# "handle_button" will be called every time a button is pressed
# It receives one argument: the associated input pin.
def handle_button(pin):
    last_button = LABELS[BUTTONS.index(pin)]
    print("Button press detected on pin: {} label: {}".format(pin, last_button))

    if last_button == "A":
        print("random image")
        imageFrame.display_random_image()
    elif last_button == "B":
        print("next image")
        imageFrame.display_next_image()
    elif last_button == "C":
        print("switch list")
        imageFrame.switch_file_list()
        imageFrame.display_image_by_index(0)
    elif last_button == "D":
        print("Shutting down")
        subprocess.run("sudo shutdown --poweroff now", shell=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Loop through out buttons and attach the "handle_button" function to each
    # We're watching the "FALLING" edge (transition from 3.3V to Ground) and
    # picking a generous bouncetime of 250ms to smooth out button presses.
    for pin in BUTTONS:
        GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=5000)

    # Finally, since button handlers don't require a "while True" loop,
    # we pause the script to prevent it exiting immediately.
    signal.pause()
