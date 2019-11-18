from NasaCollageGUI.network.urltask import BaseUrlTask
from NasaCollageGUI.network.downloadimageurltask import DownloadImageUrlTask
from NasaCollageGUI.network.previewimageurltask import PreviewImageUrlTask
import json
import os
from threading import Thread
import threading
import time
from concurrent.futures import ThreadPoolExecutor


class PythonStatusJson(object):

    def __init__(self):
        """self.file = open("status_json.json", "r+")
        self.file.close()"""
        self.active_tasks: list[BaseUrlTask] = []
        self.executor = ThreadPoolExecutor()
        self.json_status = {
            "url_tasks_running": [

            ],
            "task_info": {
            },
            "finished_task_info": {
            }
        }
        self.load_original_status()
        Thread(target=self.update_on_50ms).start()

    def load_original_status(self):
        if os.path.isfile("status_json.json"):
            json_file = open("status_json.json", "r")
            loaded_json = json.load(json_file)
            self.json_status = loaded_json
            self.json_status['url_tasks_running'] = []
            self.json_status['task_info'] = {}
            print("original status json loaded")
        else:
            print("No original file to load")

    def update_on_50ms(self):
        while threading.main_thread().is_alive():
            #print("updating")
            self.update_json_file()
            time.sleep(.5)
        print("Exiting")

    def add_image_search(self, keyword=""):
        image_search = PreviewImageUrlTask(keyword)
        self.add_url_task(image_search)
        return image_search.id

    def add_image_download(self, from_keyword=None, to_dir="./"):
        thumbnail_list = []
        all_keywords = self.get_all_preview_completed()
        if from_keyword is None:
            if len(all_keywords) == 0:
                print("No completed preview fetches yet")
                return
            else:
                thumbnail_list = all_keywords[all_keywords.keys()[0]]
        else:
            thumbnail_list = all_keywords[from_keyword]

        image_download_task = DownloadImageUrlTask(thumbnail_list, to_dir, from_keyword=from_keyword)
        self.add_url_task(image_download_task)
        return image_download_task.id

    def get_all_preview_completed(self):
        completed_ids = {}
        for i in self.json_status['finished_task_info']:
            task_json = self.json_status['finished_task_info'][i]
            if task_json['type'] == PreviewImageUrlTask.TYPE:
                completed_ids[task_json['results']['keyword']] = task_json['results']['thumbnails']
        print(completed_ids)
        return completed_ids

    def add_url_task(self, url_task: BaseUrlTask):
        self.active_tasks.append(url_task)
        url_task.start()
        self.json_status['url_tasks_running'].append(url_task.id)

    def update_json_file(self):
        temp_file = open("status_file_temp.json", 'w')

        for i in self.active_tasks:
            if not i.is_alive():
                print("A task,", i.id, "has finished")
                self.active_tasks.remove(i)
                self.json_status['url_tasks_running'].remove(i.id)
                del self.json_status['task_info'][i.id]
                self.json_status['finished_task_info'][i.id] = i.serialize()
            else:
                try:
                    self.json_status['url_tasks_running'].index(i.id) # throws error if not found
                except ValueError:
                    self.json_status['url_tasks_running'].append(i.id)

                self.json_status['task_info'][i.id] = i.serialize()

        json.dump(self.json_status, temp_file, indent=4)
        # rename temp file to original file
        temp_file.close()
        os.rename(r"status_file_temp.json", r"status_json.json")
