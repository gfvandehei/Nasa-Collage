from NasaImageProfiler.imagecollectionsearch import ImageCollection
from NasaImageProfiler.keywordsearch import NasaMediaSearch
import concurrent.futures
import time


def create_imagecollect(url):
    return ImageCollection(url)


nm = NasaMediaSearch(['saturn'])
print(len(nm.found_collections))

# write this

futures = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    for collection_url in nm.found_collections:
        print("Submitting collection")
        future = executor.submit(create_imagecollect, collection_url)
        futures.append(future)

    imageCollections = []
    print("collecting results from image collections, collection:", len(futures))

    for i, future in enumerate(futures):
        result = future.result()
        print("Collected result {}/{}".format(i, len(futures)))
        imageCollections.append(result)

print(len(imageCollections))
"""imc = ImageCollectionSearch()
thumbdict = imc.getAllThumbnails(collections)
print(thumbdict)"""