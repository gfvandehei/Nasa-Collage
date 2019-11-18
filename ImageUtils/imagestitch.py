import sys
import cv2
import os
import numpy as np
import math
import json
import random
from PIL import Image
import psutil
from threading import Thread
import time
from concurrent.futures import ThreadPoolExecutor


def getSubImageAndCopy(pixelValue, pixel_img_map, i, u, copy_to, target_res) -> None:
    # print("Started")
    images_for_pixel = pixel_img_map[pixelValue]
    #print(images_for_pixel)
    cur_image_pixel = None

    if len(images_for_pixel) == 0:
        cur_image_pixel = Image.new("RGB", (target_res, target_res), (pixelValue, pixelValue, pixelValue)).convert("L")
    else:
        image_index = random.randint(0, len(images_for_pixel) - 1)
        image_loaded = Image.open(images_for_pixel[image_index]).convert('L')
        image_resized = image_loaded.resize((target_res, target_res))
        cur_image_pixel = image_resized

    copy_to.paste(cur_image_pixel, (u * target_res, i * target_res))


"""json_filemap = sys.argv[1]
pic_dir = sys.argv[2]
processed_pic = sys.argv[3]

# load image map json
json_file = open(json_filemap, 'r')
img_val_map = json.load(json_file)"""


def run_image_stitch(color_map, to_stitch_pic, to_stitch_target_res, insert_pic_target_res, collage_name):
    # load origin image
    img_val_map = color_map
    processed_pic = to_stitch_pic
    ref_image = cv2.imread(processed_pic, 0)
    (h, w,) = ref_image.shape
    print(h, w)
    ref_image = cv2.resize(ref_image, (math.floor(w/to_stitch_target_res), math.floor(h/to_stitch_target_res)))
    (h, w,) = ref_image.shape
    print(h, w)
    new_img_shape = (h * insert_pic_target_res, w * insert_pic_target_res)
    print(new_img_shape)

    row = []
    pic = []
    print("Here")
    final_image = Image.new("RGB", new_img_shape).convert("L")
    print("Here")
    futures = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        try:
            main_pid = os.getpid()
            process = psutil.Process(main_pid)
            ram_usage = 0
            for i, rowi in enumerate(ref_image):
                for u, pixel in enumerate(rowi):
                    ram_usage = process.memory_info().rss / 1e9
                    if ram_usage > 3:
                        print("Awaiting ram clearing")
                        for i in futures:
                            i.result()
                        futures = []
                    future = executor.submit(getSubImageAndCopy, pixel, img_val_map, i, u,
                                             final_image, insert_pic_target_res)
                    futures.append(future)
                print("Ram Used:", ram_usage)

                print("Executed {}/{} rows".format(i, len(ref_image)))
        except Exception as err:
            print(err)
        except KeyboardInterrupt:
            print("Program ended due to ram usage")
            exit(1)

        print("Ex")
        # make sure all futures finish
        for i, future in enumerate(futures):
            #print("Awaiting future {}/{}".format(i, len(futures)))
            future.result()
            #print("Got future {}/{}".format(i, len(futures)))

    print(pic)
    final_image.save(collage_name)

