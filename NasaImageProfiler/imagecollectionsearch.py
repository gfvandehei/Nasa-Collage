import requests

class ImageCollection(object):

    def __init__(self, collection_url):
        self.thumb = None
        self.small = None
        self.medium = None
        self.large = None
        self.orig = None
        self.metadata = None
        self.others = []
        self.collection_url = collection_url
        assets = self.get_asset_list()
        self.parse_asset_list(assets)


    def get_asset_list(self):
        api_response = requests.get(self.collection_url)
        api_response.raise_for_status()

        asset_list = api_response.json()
        return asset_list

    def parse_asset_list(self, asset_list):
        for i in asset_list:
            if '~orig' in i:
                self.orig = i
            elif 'metadata' in i:
                self.metadata = i
            elif '~large' in i:
                self.large = i
            elif '~medium' in i:
                self.medium = i
            elif '~small' in i:
                self.small = i
            elif '~thumb' in i:
                self.thumb = i
            else:
                self.others.append(i)

    """def getAllThumbnails(self, collection_url_list):
        for i in collection_url_list:
            print("Processed {}/{} thumbnails".format(len(self.thumbnail_urls), len(collection_url_list)))
            thumb, meta = self.getThumbnail(i)
            self.thumbnail_urls[thumb] = meta
        return self.thumbnail_urls

    def getThumbnail(self, collection_url):
        response = requests.get(collection_url)
        response.raise_for_status()
        asset_list = response.json()
        thumb_url = ""
        meta_url = ""
        for i in asset_list:
            if 'thumb' in i:
                thumb_url = i # then i is the thumpnail
            elif 'metadata' in i:
                meta_url = i

        return thumb_url, meta_url"""