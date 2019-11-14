import sys
import queue
from NasaImageProfiler.imagecollectionsearch import ImageCollection
import concurrent.futures
collection_cache_file_name = sys.argv[1]

# read all collections
collection_urls = []
not_executed_url_queue = queue.Queue()

with open(collection_cache_file_name, 'r') as file:
    lines = file.readlines()
    for i in lines:
        collection_urls.append(i.rstrip("\n"))
        not_executed_url_queue.put(i.rstrip('\n'))
print(collection_urls)

completed_collection_log_file = open("collections_completed.txt", "w")
found_thumbnail_file = open("found_thumbnail_urls.txt", "w")

for i, value in enumerate(collection_urls):
    collection = ImageCollection(value)
    print("Got {}/{} collection Thumbnails".format(i,len(collection_urls)))
    found_thumbnail_file.write(collection.thumb+"\n")

"""futures = []
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
    for collection_url in nm.found_collections:
        print("Submitting collection")
        future = executor.submit(create_imagecollect, collection_url)
        futures.append(future)

    imageCollections = []
    print("collecting results from image collections, collection:", len(futures))

    for i, future in enumerate(futures):
        result = future.result()
        print("Collected result {}/{}".format(i, len(futures)))
        imageCollections.append(result)"""

print(len(imageCollections))