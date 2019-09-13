from queue import Queue
import uuid
import time
import requests
from threading import Thread

class RequestHandler(object):
    
    request_queue = Queue()
    finished_requests = {}
    request_threads = {}
    exit_flag = False
    max_concurrent_requests = 10

    @staticmethod
    def make_new_request(url):

        request_id = str(uuid.uuid1())
        RequestHandler.request_queue.put((request_id, url))

        while RequestHandler.finished_requests.get(request_id) is None:
            time.sleep(1)
        
        result = RequestHandler.finished_requests.get(request_id)
        del RequestHandler.finished_requests[request_id]
        return result

    @staticmethod
    def _run_requests():
        while not RequestHandler.exit_flag:
            if len(RequestHandler.request_threads) >= RequestHandler.max_concurrent_requests:
                time.sleep(1)
            else:
                try:
                    uuid,url = RequestHandler.request_queue.get(timeout=1)
                    print("Request", uuid, "started")
                    new_req_thread = Thread(target=RequestHandler.request_thread, 
                                            args=(url, uuid,))
                    RequestHandler.request_threads[uuid] = new_req_thread
                    new_req_thread.start()
                except:
                    continue
    
    @staticmethod
    def request_thread(url, uuid):
        r = requests.get(url)
        RequestHandler.finished_requests[uuid] = r
        del RequestHandler.request_threads[uuid]
        print("request", uuid, "finished")

Thread(target=RequestHandler._run_requests).start()