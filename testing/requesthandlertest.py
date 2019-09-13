from NasaPictureTrawler.requesthandler import RequestHandler
from threading import Thread
def make_req():
    print(RequestHandler.make_new_request("http://google.com"))

for i in range(20):
    Thread(target=make_req).start()