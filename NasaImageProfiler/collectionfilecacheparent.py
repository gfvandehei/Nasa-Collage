import os
import sys
import time

class collectionfilecacheparent(object):

    def __init__(self, collection_cache_dir='./collectioncache'):
        if not os.path.exists(collection_cache_dir):
            os.makedirs(collection_cache_dir)

        self.cache_directory = collection_cache_dir
        self.cached_words = dict()

    def _update_existing_cached_collection_keywords(self):
        cache_files = os.listdir(self.cache_directory)
        for i in cache_files:
            if "cache" not in i:
                raise(Exception("Non cache file found in directory, please remove {}".format(i)))
            else:
                (found_cache_keyword, timestamp) = self.parse_cache_filename(i)
                self.cached_words[found_cache_keyword] = timestamp
        print(self.cached_words)

    def check_cache_information(self, keyword) -> (bool, int):
        """
        check_cache_information: checks if the cache exists and retrieves the last time it was updated
        :param keyword: the keyword for the cache
        :return: (False, 0) if cache does not exist, (True, timestamp) if cache exists
        """
        if keyword in self.cached_words.keys():
            return True, self.cached_words[keyword]
        else:
            return False, 0

    def create_new_cache(self, keyword, overwrite=False):


    @staticmethod
    def parse_cache_filename(cache_filename: str) -> (str, int):
        # <keyword>_timestamp_cache.txt
        (keyword,timestamp,) = cache_filename.split("_")
        return keyword, int(timestamp)

    @staticmethod
    def create_cache_filename(keyword: str, timestamp: int):
        filename = "{}_{}_cache.txt".format(keyword, timestamp)
        return filename
