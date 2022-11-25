import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops, label
from skimage.morphology import erosion 

def count_lakes_and_bays(region):
    symbol= ~region.image
    lb = label(symbol)
    lakes=0
    bays=0
    for reg in regionprops(lb):
        is_lake = True
        for y, x in reg.coords:
            if y==0 or x == 0 or y == region.image.shape[0]-1 or x == region.image.shape[1]-1:
                is_lake = False
                break
        lakes += is_lake
        bays += not is_lake
    return lakes, bays

def has_vline(image):
    return 1 in erosion(np.mean(image, 0), [1, 1, 1])

def has_hline(image):
    return 1 in np.mean(image, 1)

def recognize(im_region):
    lakes, bays = count_lakes_and_bays(im_region)
    if lakes == 2:
        if has_vline(im_region.image):
            return 'B'
        else:
            return '8'
    elif lakes == 1:
        if bays == 4:
            return '0'
        elif bays == 3:
            return 'A'
        else:
            if im_region.eccentricity > 0.65:
                return 'P'
            else:
                return 'D'
    elif lakes == 0:
        if np.mean(im_region.image) == 1.0:
            return '-'
        elif has_vline(im_region.image):
            return '1'
        elif bays == 2:
            return '/'
        elif has_hline(im_region.image):
            return '*'
        elif bays == 4:
            return 'X'
        else:
            return 'W'

im = plt.imread('/Users/svetaparilova/Downloads/symbols.png')
im = np.mean(im, 2)
im[im > 0] = 1 

lb = label(im)
print(f"Objects = {np.max(lb)}")

regions=regionprops(lb)
result = {}
for reg in regions:
    symbol = recognize(reg)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1

print(result)

plt.imshow(im)

plt.show()