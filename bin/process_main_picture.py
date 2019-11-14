import sys
import cv2
import os
import numpy as np
import math
import json

def blockshaped(arr, res):
    """
    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.
    """
    h, w = arr.shape
    assert h % res == 0, "{} rows is not evenly divisble by {}".format(h, res)
    assert w % res == 0, "{} cols is not evenly divisble by {}".format(w, res)
    return (arr.reshape(h//res, res, -1, res)
               .swapaxes(1,2)
               .reshape(-1, res, res))




main_picture_dir = sys.argv[1]
resolution = int(sys.argv[2])

picture = cv2.imread(main_picture_dir, 0) #read as greyscale
(origh, origw,) = picture.shape
rows = int(origh/resolution)
cols = int(origw/resolution)
print(len(picture)*640/64)
chunked = blockshaped(picture, resolution)
print(chunked.dtype)
new_res_picture = np.zeros((rows, cols), dtype=np.uint8)
print(new_res_picture.shape)
print()
for i in range(rows):
    for u in range(cols):
        #print(math.ceil(np.mean(chunked[i*cols+u])))
        new_res_picture[i][u] = math.ceil(np.mean(chunked[i*cols+u]))

print(new_res_picture.shape)

cv2.imwrite("descaled_img.jpg", new_res_picture)

'''cv2.imshow("changed_img", new_res_picture)
cv2.waitKey(0)
cv2.destroyAllWindows()'''
'''cv2.imshow("image", picture)
cv2.waitKey(0)
cv2.destroyAllWindows()'''