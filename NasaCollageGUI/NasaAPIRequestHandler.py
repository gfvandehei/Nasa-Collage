from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import math
import requests

NASAIMAGEURL = "https://images-api.nasa.gov/search"

class NasaAPIRequestHandler(object):

    def __init__(self, active_collection_cache, status_monitor):
        self.request_queue = Queue()
        self.close_f = None
        self.active_collection_cache = active_collection_cache
        self.url_executor = ThreadPoolExecutor()
        self.status_monitor = status_monitor

    def run_requests(self):
        while not self.close_f:
            try:
                funct, args = self.request_queue.get(timeout=1)
                funct(*args)
            except Exception as e:
                print(e)

    def find_collection_for_keyword(self, keyword):
        self.request_queue.put((self._find_collection_for_keyword, (keyword, )))

    def _find_collection_for_keyword(self, keyword):
        self.status_monitor.set_status_function("find keyword "+keyword)
        total_results, per_page_results = self.get_numresults(keyword)
        print(per_page_results, total_results)
        pages = math.ceil(total_results / per_page_results)
        self.status_monitor.set_status_progress(0, pages)
        print("{}: {} results spread over {} pages".format(keyword, total_results, pages))
        futures = []
        all_image_collections = []
        executor = self.url_executor
        for i in range(pages):
            future = executor.submit(self.get_images_on_page, keyword, i)
            futures.append(future)

        for i, future in enumerate(futures):
            print("Collecting result from future", i)
            result = future.result()
            print("Received", len(result), "collections from future", i)
            all_image_collections += result

        self.active_collection_cache
        return all_image_collections

    def get_numresults(self, search_keyword: str)-> (int, int):
        """
        get numresults: returns the total number of search results, as well as the results per page
        :param search_keyword: the keyword to be searched for
        :return: (int, int) where the first is number of results and seconds is results per page
        """
        api_response = requests.get(NASAIMAGEURL+"?q="+search_keyword+"&media_type=image")
        api_response.raise_for_status()
        response_json = api_response.json()
        collection = response_json['collection']
        item_list = collection['items']
        return collection['metadata']['total_hits'], len(item_list)

    def get_images_on_page(self, keyword, page):
        api_response = requests.get(NASAIMAGEURL+"?q="+keyword+"&media_type=image"+"&page="+str(page))
        api_response.raise_for_status()
        response_json = api_response.json()
        collection = response_json['collection']
        item_list = collection['items']
        returned_collections = []
        for i in item_list:
            returned_collections.append(i['href'])
            #self.collections_queue.put(i)
        return returned_collections