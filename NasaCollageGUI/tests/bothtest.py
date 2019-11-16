from NasaCollageGUI.model.downloadimageurltask import DownloadImageUrlTask
from NasaCollageGUI.model.previewimageurltask import PreviewImageUrlTask
from NasaCollageGUI.model.pythonstatusjson import PythonStatusJson
from ImageUtils.squareconverter import *
from ImageUtils.imagestitch import *

import time
import os

KEYWORD = "mars rover"
TODIR = "./downloaded_images"
ORIGINAL_SCALING = 50
SUBIMAGESRES = 50
COLLAGE_NAME = "gabe_collage.jpg"
ORIGINAL_FILE = "/home/gfvandehei/Downloads/20191108_163113.jpg"


pstat = PythonStatusJson()
print("STARTING DOWNLOAD OF INDEXES")
new_active_task = PreviewImageUrlTask("mars rover")
pstat.add_url_task(new_active_task)
while(new_active_task.is_alive()):
    progress = new_active_task.progress
    print(progress.todo_done, "/", progress.todo_total, "Time left",
          progress.timeleft)
    time.sleep(.1)

print("STARTING DOWNLOAD OF IMAGES")
# start download of images
images_to_download = new_active_task.results['thumbnails']
new_active_task = DownloadImageUrlTask(images_to_download, TODIR, KEYWORD)
pstat.add_url_task(new_active_task)

while(new_active_task.is_alive()):
    progress = new_active_task.progress
    print(progress.todo_done, "/", progress.todo_total, "Time left",
          progress.timeleft)
    time.sleep(1)

print("FINISHED DOWNLOADING IMAGES")
# list directory where images were downloaded just to be sure
dirlist = os.listdir(TODIR)

print("STARTING COLLAGE CREATION")
toConvert = []
for i in dirlist:
    if ".jpg" in i:
        toConvert.append(TODIR+"/"+i)

color_map = convert_all_images(toConvert, 0)
print("Starting collage")
run_image_stitch(color_map, ORIGINAL_FILE, ORIGINAL_SCALING,
                 SUBIMAGESRES, COLLAGE_NAME)


"""prev_task = PreviewImageUrlTask("Mars Rover")
all_thumb_urls = prev_task.results['thumbnails']
download_task = DownloadImageUrlTask(all_thumb_urls, "./downloaded_images", "Mars Rover")
print(download_task.results)"""