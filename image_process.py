import numpy as np
from math import ceil


def color_blind_it(img, color):
    colors_dict = {"R": 0, "G": 1, "B": 2}
    mask = np.zeros(img.shape[:-1])
    cb_img = np.copy(img)
    cb_img[:, :, colors_dict[color]] = mask
    return cb_img


def chromashift(img):
    # first matrix implementation adapted from https://github.com/reidjason/ChromaShift/blob/master/chromashift.py
    width = img.shape[0]
    height = img.shape[1]
    corrected_img = np.copy(img)
    for x in range(width):
        for y in range(height):
            oldValue = img[x, y]

            oldRed = oldValue[0]
            oldGreen = oldValue[1]
            oldBlue = oldValue[2]

            longValue = (17.8824 * oldRed) + (43.5161 * oldGreen) + (4.11935 * oldBlue)
            medValue = (3.45565 * oldRed) + (27.1554 * oldGreen) + (3.86714 * oldBlue)
            shortValue = (0.0299566 * oldRed) + (0.184309 * oldGreen) + (1.46709 * oldBlue)

            longValue = (1 * longValue) + (0 * medValue) + (0 * shortValue)
            medValue = (0.494207 * longValue) + (0 * medValue) + (1.24827 * shortValue)
            shortValue = (0 * longValue) + (0 * medValue) + (1 * shortValue)

            newRed = (0.0809444479 * longValue) + (-0.130504409 * medValue) + (0.116721066 * shortValue)
            newGreen = (-0.0102485335 * longValue) + (0.0540193266 * medValue) + (-0.113614708 * shortValue)
            newBlue = (-0.000365296938 * longValue) + (-0.00412161469 * medValue) + (0.693511405 * shortValue)

            newRed = oldRed - newRed
            newGreen = oldGreen - newGreen
            newBlue = oldBlue - newBlue

            newRed = (1.0 * newRed) + (0.7 * newGreen) + (0.0 * newBlue)
            newGreen = (0.0 * newRed) + (0.0 * newGreen) + (0.0 * newBlue)
            newBlue = (0.0 * newRed) + (0.7 * newGreen) + (1.0 * newBlue)

            newRed = int(ceil(newRed + oldRed))
            newGreen = int(ceil(newGreen + oldGreen))
            newBlue = int(ceil(newBlue + oldBlue))

            corrected_img[x, y] = (newRed, newGreen, newBlue)

    return corrected_img
