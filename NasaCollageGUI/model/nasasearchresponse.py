class NASASearchResponse(object):

    def __init__(self, nasa_api_response: dict):
        collection = nasa_api_response['collection']
        self.metadata = collection['metadata']
        self.search_items = []
        items_list = collection['items']
        for i in items_list:
            self.search_items.append(NASASearchItem(i))


class NASASearchItem(object):

    def __init__(self, item_dict: dict):
        self.media_type = item_dict['data'][0]['media_type']
        self.nasa_id = item_dict['data'][0]['nasa_id']
        self.collection_url =  item_dict['href']
        self.thumbnail_image = None
        links = item_dict['links']
        for i in links:
            if i['rel'] == "preview":
                self.thumbnail_image = i['href']
