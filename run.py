from NasaPictureTrawler.nasaimageapi import NasaImageAPI
from threading import Thread

result = NasaImageAPI.search("planet", media_type="image")
counter = 1
asset_list = []
while result.next_link != None:
    print("page", counter)
    new_result = NasaImageAPI.search(url=result.next_link)
    asset_list.extend(new_result.get_assets())
    counter += 1
    result = new_result

print(len(asset_list))
#print(result.get_assets())
