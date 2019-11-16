from NasaCollageGUI.model.urltask import BaseUrlTask
from NasaCollageGUI.model.nasasearchresponse import NASASearchResponse
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import requests
import math
import time
import sys

NASAAPIURL = "https://images-api.nasa.gov/search"


class PreviewImageUrlTask(BaseUrlTask):

    TYPE = "get_previews"

    def __init__(self, keyword: str=""):
        super().__init__()
        self.keyword = keyword
        self.running = True
        self.type = PreviewImageUrlTask.TYPE
        self.thread_executor = ThreadPoolExecutor()
        self.results = {
            "keyword": self.keyword,
            "thumbnails": []
        }

    def run(self):
        try:
            page_results, all_results = self.make_initial_request_for_metadata()
            total_pages = math.ceil(all_results/page_results)
            self.initialize_todo_pages(total_pages)
        except Exception as err:
            tb = sys.exc_info()[2]
            print(err.with_traceback(tb))
            self.failed = True
            self.running = False
            return

        self.make_all_requests(0, 5)
        print("HERE")
        self.running = False

    def make_initial_request_for_metadata(self):
        initial_request = requests.get(NASAAPIURL+"?q="+self.keyword+"&media_type=image")
        initial_request.raise_for_status()
        response = NASASearchResponse(initial_request.json())

        per_request = len(response.search_items)
        per_all = int(response.metadata['total_hits'])

        return per_request, per_all

    def initialize_todo_pages(self, total_pages):
        if total_pages > 100:
            # nasa image search wont serve over 100 pages
            print("The keyword you have searched is too vague has over 10000 related images, terminating")
            raise(Exception("To many images to execute"))
        self.progress.add_total(total_pages)
        for i in range(total_pages):
            self.todo_urls.append("{}?q={}&media_type=image&page={}".format(NASAAPIURL, self.keyword, i))

    def make_all_requests(self, current_retry, max_reties):
        future_to_url = {self.thread_executor.submit(self.make_request, url): url for url in self.todo_urls}
        todo_url_len = len(self.todo_urls)
        url_counter = 0
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                #print(data)
                if data is True:
                    url_counter += 1
                    self.progress.increment()
                else:
                    print("A URL Failed")
            except Exception as err:
                tb = sys.exc_info()[2]
                print(err.with_traceback(tb))
            """else:
                #print("Completed url:", url, "more to go:", len(self.todo_urls))"""

        if url_counter < todo_url_len and current_retry < max_reties and self.running is True:
            print("{} requests did not complete, retrying in 10 seconds".format(len(self.todo_urls)))
            for i in range(10):
                print(10-i)
                time.sleep(1)
            print("Retrying")
            self.make_all_requests(current_retry+1, max_reties)

    def make_request(self, request_url):
        try:
            request = requests.get(request_url, timeout=5)
            response = NASASearchResponse(request.json())
            for i in response.search_items:
                self.results['thumbnails'].append(i.thumbnail_image)
            self.todo_urls.remove(request_url)
            self.done_urls.append(request_url)
            return True
        except Exception as err:
            tb = sys.exc_info()[2]
            print(err.with_traceback(tb))
            return False


"""task = PreviewImageUrlTask("Mars rover")
task.start()
while task.is_alive():
    time.sleep(1)
print("TODOS:",task.todo_urls)
print("Completed:", task.done_urls)
print("RESULTS:", len(task.results['thumbnails']))"""