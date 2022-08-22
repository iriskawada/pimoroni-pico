import math
import time
import badger2040
import badger_os

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

IMAGE_WIDTH = 104

NAME_HEIGHT = 60
DETAILS_HEIGHT = 30
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1

DETAIL1_TEXT_SIZE = 0.8
DETAIL2_TEXT_SIZE = 

LEFT_PADDING = 5
NAME_PADDING = 20
DETAIL_SPACING = 10

DEFAULT_TEXT = """BRATHADAIR
OSWP | DSOC
blog.brathadarean.com"""

BADGE_IMAGE = bytearray(int(IMAGE_WIDTH * HEIGHT / 8))

try:
    open("badge-image.bin", "rb").readinto(BADGE_IMAGE)
except OSError:
    try:
        import badge_image
        BADGE_IMAGE = bytearray(badge_image.data())
        del badge_image
    except ImportError:
        pass


# ------------------------------
#      Utility functions
# ------------------------------

# Reduce the size of a string until it fits within a given width
def truncatestring(text, text_size, width):
    while True:
        length = display.measure_text(text, text_size)
        if length > 0 and length > width:
            text = text[:-1]
        else:
            text += ""
            return text


# ------------------------------
#      Drawing functions
# ------------------------------

# Draw the badge, including user text
def draw_badge():
    display.pen(0)
    display.clear()

    # Draw badge image
    display.image(BADGE_IMAGE, IMAGE_WIDTH, HEIGHT, 0, 0)

    # Draw a border around the image
    display.pen(0)
    display.thickness(1)
    display.line(0, 0, IMAGE_WIDTH - 1, 0)
    display.line(IMAGE_WIDTH - 1, 0, IMAGE_WIDTH - 1, HEIGHT - 1)
    display.line(IMAGE_WIDTH - 1, HEIGHT - 1, 0, HEIGHT - 1)
    display.line(0, HEIGHT - 1, 0, 0)

    # Draw a black background behind the name
    display.pen(0)
    display.thickness(1)
    display.rectangle(IMAGE_WIDTH, 1, TEXT_WIDTH, NAME_HEIGHT)

    # Draw the name, scaling it based on the available width
    display.pen(15)
    display.font("sans")
    display.thickness(4)
    name_size = 2.0  # A sensible starting scale
    while True:
        name_length = display.measure_text(name, name_size)
        if name_length >= (TEXT_WIDTH - NAME_PADDING) and name_size >= 0.1:
            name_size -= 0.01
        else:
            display.text(name, ((TEXT_WIDTH - name_length) // 2) + IMAGE_WIDTH, (NAME_HEIGHT // 2) + 1, name_size)
            break

    # Draw a white backgrounds behind the details
    display.pen(15)
    display.thickness(1)
    display.rectangle(1, NAME_HEIGHT, TEXT_WIDTH, DETAILS_HEIGHT * 2)

    # Draw the first detail's title and text
    display.pen(0)
    display.font("sans")
    display.thickness(3)
    detail_size = 2.0  # A sensible starting scale
    while True:
        detail_length = display.measure_text(name, detail_size)
        if detail_length >= (TEXT_WIDTH - NAME_PADDING) and name_size >= 0.1:
            detail_size -= 0.01
        else:
            display.text(name, ((TEXT_WIDTH - detail_length) // 2) + IMAGE_WIDTH, (DETAILS_HEIGHT // 2) + 1, detail_size)
            break

    # Draw the second detail's title and text
    display.thickness(3)
    detail_size = 2.0  # A sensible starting scale
    while True:
        detail_length = display.measure_text(name, detail_size)
        if detail_length >= (TEXT_WIDTH - NAME_PADDING) and name_size >= 0.1:
            detail_size -= 0.01
        else:
            display.text(name, ((TEXT_WIDTH - detail_length) // 2) + IMAGE_WIDTH, (DETAILS_HEIGHT // 2) + 1, detail_size)
            break

# ------------------------------
#        Program setup
# ------------------------------

# Create a new Badger and set it to update NORMAL
display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_NORMAL)

# Open the badge file
try:
    badge = open("badge.txt", "r")
except OSError:
    with open("badge.txt", "w") as f:
        f.write(DEFAULT_TEXT)
        f.flush()
    badge = open("badge.txt", "r")

# Read in the next 6 lines
name = badge.readline()            # "BRATHADAIR"
detail1 = badge.readline()         # "OSWP | DSOC"
detail2 = badge.readline()         # "blog.brathadarean.com"


# ------------------------------
#       Main program
# ------------------------------

draw_badge()

while True:
    if display.pressed(badger2040.BUTTON_A) or display.pressed(badger2040.BUTTON_B) or display.pressed(badger2040.BUTTON_C) or display.pressed(badger2040.BUTTON_UP) or display.pressed(badger2040.BUTTON_DOWN):
        badger_os.warning(display, "To change the text, connect Badger2040 to a PC, load up Thonny, and modify badge.txt")
        time.sleep(4)

        draw_badge()

    display.update()

    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()
