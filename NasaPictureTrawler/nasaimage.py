import requests
import threading
import time
from NasaPictureTrawler.requesthandler import RequestHandler
"""
A Datastructure to represent a single image received from the
Nasa images API
"""
NASA_ASSET_URL = "https://images-api.nasa.gov/asset/"

class NasaImage(object):

    def __init__(self, asset_name, file_storage_path="./"):
        self.asset_name = asset_name
        self.asset_url = NASA_ASSET_URL+asset_name
        self.failed = True
        self.file_storage_path = file_storage_path
        self.asset_storage = {
            "href": {
                "orig": None,
                "medium": None,
                "small": None,
                "thumb": None,
            },
            "local": {
                "orig": None,
                "medium": None,
                "small": None,
                "thumb": None,
            }
        }

        threading.Thread(target=self.assure_image_component_fetch).start()

    def assure_image_component_fetch(self):
        while self.failed == True:
            try:
                if not self.fetch_asset_information():
                    break
            except Exception as err:
                print("ERROR1",err)
            time.sleep(1)

    def fetch_asset_information(self):
        response = RequestHandler.make_new_request(self.asset_url)

        if response.status_code != 200:
            self.failed = True
            return False
        
        json_data = response.json()
        size_keys = self.asset_storage['href'].keys()
        for i in json_data['collection']['items']:
            for key in size_keys:
                if key in i['href']:
                    self.asset_storage['href'][key] = i['href']
        
        self.failed = False
        return True

    def download_real_image(self, size):
        local_path = self.file_storage_path+"/"+self.asset_name+"_"+size+".jpg"
        if self.asset_storage['href'][size] is not None:
            try:
                web_file = requests.get(self.asset_storage['href'][size])
                if web_file.status_code != 200:
                    print("Could not find file", self.asset_storage['href'][size])
                    return False

                with open(local_path, 'wb') as f:
                    f.write(web_file.content)

                self.asset_storage['local'][size] = local_path
                return True
            except Exception as err:
                print("ERROR2", err)
                return False
        else:
            return False


    

        

