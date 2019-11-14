import sys
import requests
import shutil

thumbnail_img_filenames = sys.argv[1]
img_save_dir = sys.argv[2]

lines = []
with open(thumbnail_img_filenames, 'r') as thumbnail_file:
    lines = thumbnail_file.readlines()
    for i, line in enumerate(lines):
        lines[i] = line.rstrip('\n')
    #print(lines)

total_images = len(lines)
for indx, i in enumerate(lines):
    url_split = i.split("/")
    filename = url_split[-1]
    print("Writing request for image {} {}/{}".format(filename, indx, total_images))
    image_request = requests.get(i, stream=True, timeout=5)
    if image_request.status_code == 200:
        with open("{}/{}".format(img_save_dir,filename), 'wb') as f:
            image_request.raw.decode_content = True
            shutil.copyfileobj(image_request.raw, f)
        print("Finished receiving image {} to {}".format(filename, img_save_dir))
    else:
        print("Failed to retrieve image from remote")

print("Finished")