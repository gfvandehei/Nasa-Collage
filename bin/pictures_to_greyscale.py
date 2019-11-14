import sys
import cv2
import os
import numpy as np
import math
import json

img_in_dir = sys.argv[1]
img_out_dir = sys.argv[2]

img_files = [f for f in os.listdir(img_in_dir) if os.path.isfile(os.path.join(img_in_dir, f))]

# create color map:
color_map = {}
for i in range(256):
    color_map[i] = []

for i, file in enumerate(img_files):
    #print("starting {}/{} ".format(i, len(img_files)))
    grey_img = cv2.imread("{}/{}".format(img_in_dir, file), 0) # read as a greyscale image
    resized_img = cv2.resize(grey_img, dsize=(640, 640), interpolation=cv2.INTER_CUBIC)
    # write file to out_dir
    cv2.imwrite("{}/{}".format(img_out_dir, file), resized_img)

    # cv2.imshow("Greyscale", resized_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    flattened = grey_img.flatten()
    avg_grey = math.ceil(np.mean(flattened))
    color_map[avg_grey].append("{}/{}".format(img_out_dir,file))
    #print(math.ceil(np.mean(flattened)))

    #print(flattened)
color_file = open("color_map.json", "w")
json.dump(color_map, color_file)


#print(img_files)
