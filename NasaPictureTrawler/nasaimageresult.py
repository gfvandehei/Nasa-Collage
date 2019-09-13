from pprint import pprint
from NasaPictureTrawler.nasaimage import NasaImage

class NasaImageQueryResult(object):
    """
    Stores received data and navigational data from a NASA images
    API Query
    """
    def __init__(self, collection_json):
        self.next_link = None
        self.prev_link = None
        self.asset_list = []

        # get different components of the json
        metadata = collection_json['collection'].get('metadata')
        items = collection_json['collection'].get('items')
        href = collection_json['collection'].get('href') # original search string
        links = collection_json['collection'].get('links') # list of pages?
        # set the navigational links

        for link in links:
            if link['rel'] == "next":
                self.next_link = link['href']
            elif link['rel'] == "prev":
                self.prev_link = link['href']
        
        # set the data storage object
        for data_object in items:
            for data in data_object['data']:
                self.asset_list.append(NasaImage(data['nasa_id']))
        
        print("Generated result object with {} assets".format(
                len(self.asset_list)
            )
        )

    def get_assets(self):
        return self.asset_list



        


