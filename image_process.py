import numpy as np
from math import ceil
from const import (lms2lmsd, lms2lmsp, lms2lmst, lms2rgb, err2mod)


def color_blind_it(img, color):
    colors_dict = {"R": 0, "G": 1, "B": 2}
    mask = np.zeros(img.shape[:-1])
    cb_img = np.copy(img)
    cb_img[:, :, colors_dict[color]] = mask
    return cb_img

def srgb2lin(s):
    if s <= 0.0404482362771082:
        lin = s / 12.92
    else:
        lin = pow(((s + 0.055) / 1.055), 2.4)
    return lin


def lin2srgb(lin):
    if lin > 0.0031308:
        s = 1.055 * (pow(lin, (1.0 / 2.4))) - 0.055
    else:
        s = 12.92 * lin
    return s

def degammafy(origin):
    # adapted from https://stackoverflow.com/questions/34472375/linear-to-srgb-conversion
    destination = np.zeros_like(origin)
    for i in range(origin.shape[0]):
        for j in range(origin.shape[1]):
            for z in range(3):
                destination[i,j,z] = srgb2lin(origin[i,j,z])
    return destination


def gammafy(origin):
    destination = np.zeros_like(origin)
    for i in range(origin.shape[0]):
        for j in range(origin.shape[1]):
            for z in range(3):
                destination[i, j, z] = lin2srgb(origin[i, j, z])
    return destination


def space_conversion(origin, matrix):
    destination = np.zeros_like(origin)
    for i in range(origin.shape[0]):
        for j in range(origin.shape[1]):
            origin_px = origin[i, j, :3]
            destination[i, j, :3] = np.dot(matrix, origin_px)
    return destination


def sim_defect(rgb, defect):
    if defect == 'd':
        lms = space_conversion(rgb, lms2lmsd)
    elif defect == 'p':
        lms = space_conversion(rgb, lms2lmsp)
    elif defect == 't':
        lms = space_conversion(rgb, lms2lmst)
    return lms


def compare(true, defect):
    error = (true - defect)
    return error


def daltonize(rgb, rgb_defect, matrix):
    error = compare(rgb, rgb_defect)
    delta = np.zeros_like(rgb)
    for i in range(rgb.shape[0]):
        for j in range(rgb.shape[1]):
            err = error[i, j, :3]
            delta[i, j, :3] = np.dot(matrix, err)
    dtpn = delta + rgb

    for i in range(rgb.shape[0]):
        for j in range(rgb.shape[1]):
            dtpn[i, j, 0] = max(0, dtpn[i, j, 0])
            dtpn[i, j, 0] = min(255, dtpn[i, j, 0])
            dtpn[i, j, 1] = max(0, dtpn[i, j, 1])
            dtpn[i, j, 1] = min(255, dtpn[i, j, 1])
            dtpn[i, j, 2] = max(0, dtpn[i, j, 2])
            dtpn[i, j, 2] = min(255, dtpn[i, j, 2])

    return dtpn


def test_pipeline(rgb):
    lms_defect = sim_defect(rgb, "p")
    rgb_defect = space_conversion(lms_defect, lms2rgb)
    corrected = daltonize(rgb, rgb_defect, err2mod)
    return corrected
