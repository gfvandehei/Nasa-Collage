import requests
import json
import inspect
import pprint
import threading
from NasaPictureTrawler.nasaimageresult import NasaImageQueryResult
from NasaPictureTrawler.requesthandler import RequestHandler
root_nasa_images_url = "https://images-api.nasa.gov"

class NasaImageAPI(object):

    @staticmethod
    def search(q=None, center=None, description=None, description_508=None,
               keywords=None, location=None, media_type=None, nasa_id=None,
               page=None, photographer=None, secondary_creator=None, title=None,
               year_start=None, year_end=None, url=None):
        # assemble url from passed parameters
        if url == None:
            search_url = root_nasa_images_url+"/search?"
            frame = inspect.currentframe()
            args, _, _, values = inspect.getargvalues(frame)
            for i in args:
                if values[i] != None:
                    search_url += "&"+i+"="+str(values[i])
        else:
            search_url = url

        print("Searching images with url {}".format(search_url))
        # make request to api
        web_response = RequestHandler.make_new_request(search_url)
        response_json = web_response.json()
        # ensure request did not have an error
        if web_response.status_code != 200:
            print("Recieved status code {}, ERROR: {}".format(
                web_response.status_code,
                response_json['reason']
            ))
            return None

        return NasaImageQueryResult(response_json)
