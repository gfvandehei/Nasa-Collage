import concurrent.futures
import sys
from NasaCollageGUI.collage.collagecreatortask import CollageCreatorTask
import time


def done_callback(f):
    if f.exception():
        raise(f.exception())
    else:
        print("Finished successfully")


main_picture_path, sub_pic_dir, main_scale, sub_wb, final_name, ram_limit = sys.argv[1:]

th = concurrent.futures.ThreadPoolExecutor()
task = CollageCreatorTask(main_picture_path, sub_pic_dir, main_scale, sub_wb, final_name, ram_limit)
future = th.submit(task.run)
future.add_done_callback(done_callback)

while task.running:
    print("{}: {}/{}".format(task.status_mon.time_elapsed, task.status_mon.done_tasks, task.status_mon.total_tasks))
    time.sleep(2)