from NasaCollageGUI.model.downloadimageurltask import DownloadImageUrlTask
from NasaCollageGUI.model.previewimageurltask import PreviewImageUrlTask
from NasaCollageGUI.model.pythonstatusjson import PythonStatusJson
from ImageUtils.squareconverter import *
from ImageUtils.imagestitch import *

import time
import os

KEYWORD = input("Type a keyword to get images for: ")
print(KEYWORD)
TODIR = input("Type a directory to save all images to: ")
print(TODIR)

pstat = PythonStatusJson()
print("STARTING DOWNLOAD OF INDEXES")
new_active_task = PreviewImageUrlTask(KEYWORD)
pstat.add_url_task(new_active_task)
while new_active_task.is_alive():
    progress = new_active_task.progress
    print(progress.todo_done, "/", progress.todo_total, "Time left",
          progress.timeleft)
    time.sleep(.1)

print("STARTING DOWNLOAD OF IMAGES")
# start download of images
images_to_download = new_active_task.results['thumbnails']
new_active_task = DownloadImageUrlTask(images_to_download, TODIR, KEYWORD)
pstat.add_url_task(new_active_task)

while new_active_task.is_alive():
    progress = new_active_task.progress
    print(progress.todo_done, "/", progress.todo_total, "Time left",
          progress.timeleft)
    time.sleep(1)

print("FINISHED DOWNLOADING IMAGES")
# list directory where images were downloaded just to be sure
dirlist = os.listdir(TODIR)
print(len(dirlist), "images were downloaded")