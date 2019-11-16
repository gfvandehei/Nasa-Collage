from NasaCollageGUI.model.urltask import BaseUrlTask
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import requests
import random
import time
import os

class DownloadImageUrlTask(BaseUrlTask):

    def __init__(self, images_to_download, base_directory: str, from_keyword="na"):
        super().__init__()
        self.running = True
        self.base_directory = base_directory

        self.from_keyword = from_keyword
        self.todo_urls = images_to_download
        self.progress.add_total(len(images_to_download))
        self.executor = ThreadPoolExecutor()
        self.type = "image_download"
        self.results = {
            "saved_to": base_directory,
            "unable_to_get": []
        }
        if not os.path.isdir(self.base_directory):
            os.makedirs(self.base_directory)

    def run(self):
        futures_to_url = {}
        for i in self.todo_urls:
            future = self.executor.submit(self.request_image, i, 5)
            futures_to_url[future] = i
        todo_url_len = len(futures_to_url)
        url_counter = 0
        for future in concurrent.futures.as_completed(futures_to_url):
            url = futures_to_url[future]
            data = future.result()
            self.progress.increment()
            if data is not True:
                print("Failed:", url)
            url_counter += 1
            #print(todo_url_len-url_counter, "Images left to download")

        self.running = False

    def request_image(self, url, retry_attempts):
        url_split = url.split("/")
        file_name = url_split[-1]

        for i in range(retry_attempts):
            try:
                request = requests.get(url, timeout=5, stream=True)
                request.raise_for_status()
                with open(self.base_directory + "/" + self.from_keyword+"_" + file_name, 'wb') as imgfile:
                    for chunk in request:
                        imgfile.write(chunk)
                self.todo_urls.remove(url)
                self.done_urls.append(url)
                return True

            except Exception as err:
                print("request_img ERROR:", err)
                sleep_secs = random.randint(3, 15)
                time.sleep(sleep_secs)
                continue

        self.results['unable_to_get'].append(url)
        self.todo_urls.remove(url)
        return False
