import requests
import concurrent.futures
import math
import queue
from NasaImageProfiler.imagecollectionsearch import ImageCollection

class NasaMediaSearch(object):

    def __init__(self, keywords: []):
        self.base_url = "https://images-api.nasa.gov/search"
        self.found_collections = self.search(keywords)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=12)

    def search(self, search_keyword=[]):
        all_keyword_collections = []
        for i in search_keyword:
            all_keyword_collections += self.get_images_all_pages(i)
        return all_keyword_collections

    def get_images_all_pages(self, keyword):
        total_results, per_page_results = self.get_numresults(keyword)
        print(per_page_results, total_results)
        pages = math.ceil(total_results/per_page_results)
        print("{}: {} results spread over {} pages".format(keyword, total_results, pages))
        futures = []
        all_image_collections = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(pages):
                future = executor.submit(self.get_images_on_page, keyword, i)
                futures.append(future)

            for i, future in enumerate(futures):
                print("Collecting result from future", i)
                result = future.result()
                print("Received", len(result), "collections from future", i)
                all_image_collections += result
            
        return all_image_collections

    def get_numresults(self, search_keyword: str)-> (int, int):
        """
        get numresults: returns the total number of search results, as well as the results per page
        :param search_keyword: the keyword to be searched for
        :return: (int, int) where the first is number of results and seconds is results per page
        """
        api_response = requests.get(self.base_url+"?q="+search_keyword+"&media_type=image")
        api_response.raise_for_status()
        response_json = api_response.json()
        collection = response_json['collection']
        item_list = collection['items']
        return collection['metadata']['total_hits'], len(item_list)

    def get_images_on_page(self, keyword, page):
        api_response = requests.get(self.base_url+"?q="+keyword+"&media_type=image"+"&page="+str(page))
        api_response.raise_for_status()
        response_json = api_response.json()
        collection = response_json['collection']
        item_list = collection['items']
        returned_collections = []
        for i in item_list:
            returned_collections.append(i['href'])
            #self.collections_queue.put(i)
        return returned_collections

    """ def search_keyword(self, search_keyword: str, page=0) -> dict:
        image_url = self.base_url+'?q='+search_keyword+"&media_type=image"
        final_image_collection_urls = []
        gotten_res_num = 0
        while True:
            image_collections, nexturl = self.search_url(image_url, gotten_res_num)
            gotten_res_num += len(image_collections)
            final_image_collection_urls += image_collections
            if nexturl is not None:
                image_url = nexturl
            else:
                break
        return final_image_collection_urls

    def search_url(self, url, results_gotten=0) -> ([], str):
        api_response = requests.get(url)
        if api_response.status_code == 200:
            # all good carry on
            response_data = api_response.json()
            collection = response_data['collection']
            item_list = collection['items']
            total_hits = collection['metadata']['total_hits']
            print("Gotten {}/{} results".format(results_gotten, total_hits))
            all_image_collections = []
            for i in item_list:
                if 'image' in i['href']:
                    all_image_collections.append(i['href'])
            #print(len(all_image_collections))
            #print(collection['links'])
            nexturl = None
            for i in collection['links']:
                if i['rel'] == 'next':
                    return all_image_collections, i['href']
                    #all_image_collections += self.search_url(i['href'], results_gotten+len(all_image_collections))
            return all_image_collections, None
        else:
            raise(Exception("There was an error communicating with NASA API CODE:{}".format(api_response.status_code)))
    """

#searcher = NasaMediaSearch("https://images-api.nasa.gov/search")
#print(len(searcher.search_keyword("mars")))