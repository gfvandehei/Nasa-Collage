from NasaCollageGUI.model.downloadimageurltask import DownloadImageUrlTask
from NasaCollageGUI.model.previewimageurltask import PreviewImageUrlTask
from NasaCollageGUI.model.pythonstatusjson import PythonStatusJson
from ImageUtils.squareconverter import *
from ImageUtils.imagestitch import *

import time
import os

FROMDIR = "./downloaded_images"
KEYWORD = "mars rover"
PICTURE_DOWNSCALING = 20
INSERT_IMAGE_RESOLUTION = 50
FROM_IMAGE = "/home/gfvandehei/Downloads/20191108_163113.jpg"

print("FINISHED DOWNLOADING IMAGES")
# list directory where images were downloaded just to be sure
dirlist = os.listdir(FROMDIR)

print("STARTING COLLAGE CREATION")
toConvert = []
for i in dirlist:
    filenamesplit = i.split("_")
    if KEYWORD in filenamesplit[0]:
        toConvert.append(FROMDIR+"/"+i)
print(toConvert)
color_map = convert_all_images(toConvert, 0)
print(color_map)
print("Starting collage")
run_image_stitch(color_map, FROM_IMAGE, PICTURE_DOWNSCALING,
                 INSERT_IMAGE_RESOLUTION, "gabecollage.jpg")