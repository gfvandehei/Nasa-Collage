from ImageUtils.squareconverter import *
from ImageUtils.imagestitch import *

import time
import os

ALL_IMAGE_DIRECTORY = input("Where are the images you want to use located: ")
print(ALL_IMAGE_DIRECTORY)
MAIN_IMAGE_PATH = input("Path to the main image: ")
print(MAIN_IMAGE_PATH)
MAIN_DOWNSCALING = int(input("Scale the original resolution by original (A value around 20 is good)/:"))
print(MAIN_DOWNSCALING)
INSERT_IMAGE_RESOLUTION = int(input("""each inserted picture should have a squared resolution
of smaller is less detailed, but much more memory effiecient (try 50) : """))
print(INSERT_IMAGE_RESOLUTION)
COLLAGE_NAME = input("What should the name of the outputted collage be?:")
print(COLLAGE_NAME)

print("FINISHED DOWNLOADING IMAGES")
# list directory where images were downloaded just to be sure
dirlist = os.listdir(ALL_IMAGE_DIRECTORY)

print("STARTING COLLAGE CREATION")
toConvert = []
for i in dirlist:
    if ".jpg" in i:
        toConvert.append(ALL_IMAGE_DIRECTORY+"/"+i)
print("Getting color map of", len(toConvert), "images")
color_map = convert_all_images(toConvert)
print("Starting collage")
run_image_stitch(color_map, MAIN_IMAGE_PATH, MAIN_DOWNSCALING,
                 INSERT_IMAGE_RESOLUTION, COLLAGE_NAME)