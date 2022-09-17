import numpy as np

def color_blind_it(img, color):
    colors_dict = {"R":0, "G":1, "B":2}
    mask = np.zeros(img.shape[:-1])
    cb_img = np.copy(img)
    cb_img[:,:,colors_dict[color]] = mask
    return cb_img