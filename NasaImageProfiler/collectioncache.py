import os

class CollectionCache(object):

    def __init__(self, file_path):
        self.file = open(file_path, "a+")
        self.cached_collections = set()

    def exists_in_cache(self, collection_url) -> bool:
        return collection_url in self.cached_collections.keys()

    def add_to_cache(self, collection_url) -> None:
        if self.exists_in_cache(collection_url):
            return
        else:
            self.cached_collections.add(collection_url)
            self.file.write(collection_url+'\n')
            return

class CollectionCacheExisting(CollectionCache):

    def __init__(self, keyword, timestamp, path):

