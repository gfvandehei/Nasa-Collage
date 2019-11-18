from NasaCollageGUI.model.task import Task
import os
import concurrent.futures
import cv2
from PIL import Image
import math
import numpy as np
import psutil
import random


class CollageCreatorTask(Task):

    def __init__(self, main_picture_path, sub_picture_dir, main_scale, sub_wh, final_name, ram_limit=5.0):
        super().__init__()
        self.main_picture_path = main_picture_path
        self.sub_picture_dir = sub_picture_dir
        self.main_scale = int(main_scale)
        self.sub_width_height = int(sub_wh)
        self.final_result_name = final_name
        self.ram_limit = float(ram_limit)
        self.verify_parameters()

        self.thread_pool_executor = concurrent.futures.ThreadPoolExecutor()

    def verify_parameters(self):
        if not os.path.isfile(self.main_picture_path):
            raise(AssertionError("Main picture file does not exist"))

        if not os.path.isdir(self.sub_picture_dir):
            raise(AssertionError("Sub picture directory does not exist"))

    def _run(self):
        color_map = self.run_colormap()
        self.status_mon.clear()
        print("Completed profiling available images")
        final_image = self.run_collage_creation(color_map)
        final_image.save(self.final_result_name)

    def run_colormap(self):
        # generate picture color map
        all_files_in_subdir = os.listdir(self.sub_picture_dir)
        self.status_mon.set_total_tasks(len(all_files_in_subdir))
        image_future_map = {}
        # only use jpg files
        for image in all_files_in_subdir:
            if ".jpg" in image:
                future = self.thread_pool_executor.submit(self.get_color_profile, self.sub_picture_dir+"/"+image)
                image_future_map[future] = image
            else:
                self.status_mon.do_task()

        color_map = self.generate_greyscale_map()
        for future in concurrent.futures.as_completed(image_future_map):
            image_path = image_future_map[future]
            color_profile = future.result()
            color_map[color_profile].append(image_path)
            self.status_mon.do_task()

        return color_map

    def run_collage_creation(self, color_map):
        #print(self.main_picture_path)
        load_main_image = cv2.imread(self.main_picture_path, 0)

        height, width, = load_main_image.shape

        #new_height = math.ceil(height/self.main_scale)
        #new_width = math.ceil(width/self.main_scale)
        print("Original image has height", height, "and width", width)
        resized_image = cv2.resize(load_main_image, None, fx=1/float(self.main_scale), fy=1/float(self.main_scale))
        height, width, = resized_image.shape
        print("Resized image has height", height, "and width", width)

        target_image_shape = (width * self.sub_width_height, height * self.sub_width_height)
        target_image = Image.new("RGB", target_image_shape).convert("L")  # Make a greyscale image of the correct size
        print(target_image_shape)
        main_pid = os.getpid()
        process = psutil.Process(main_pid)
        todo = height * width
        self.status_mon.set_total_tasks(todo)
        futures = {}
        b_flag = False

        for i, row in enumerate(resized_image):
            for u, pixel in enumerate(row):
                ram_usage = process.memory_info().rss / 1e9
                if ram_usage > self.ram_limit:
                    print("Ram usage is higher than limit {}, shutting down. RAM: {}".format(self.ram_limit, ram_usage))
                    b_flag = True
                    break
                possible_images = color_map[pixel]
                future = self.thread_pool_executor.submit(self.add_sub_image, pixel, possible_images,
                                                          i, u, target_image, self.sub_width_height)
                futures[future] = ""
                self.status_mon.do_task()
            if b_flag:
                break
        print("collecting")
        for i in concurrent.futures.as_completed(futures):
            #print(i.exception(), "ASDASD")
            if i.exception():
                raise(i.exception())
            i.result()
            self.status_mon.do_task()

        return target_image

    @staticmethod
    def generate_greyscale_map() -> dict:
        gmap = {}
        for i in range(256):
            gmap[i] = []
        return gmap

    @staticmethod
    def get_color_profile(image_path):
        image_as_grey = cv2.imread(image_path, 0)
        flattened = image_as_grey.flatten()
        average_grey = math.ceil(np.mean(flattened))
        return average_grey

    def add_sub_image(self, pixel_value, possible_img_arr, i, u, target_image, target_res) -> None:

        if len(possible_img_arr) == 0:
            cur_image_pixel = Image.new("RGB", (target_res, target_res),
                                        (pixel_value, pixel_value, pixel_value)).convert("L")
        else:
            image_index = random.randint(0, len(possible_img_arr) - 1)
            image_loaded = Image.open(self.sub_picture_dir+"/"+possible_img_arr[image_index]).convert('L')
            image_resized = image_loaded.resize((target_res, target_res))
            cur_image_pixel = image_resized

        target_image.paste(cur_image_pixel, (u * target_res, i * target_res))