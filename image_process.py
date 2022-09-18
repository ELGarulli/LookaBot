import numpy as np

from const import (lms2lmsd, lms2lmsp, lms2lmst, lms2rgb, err2mod, rgb2lms)


def space_conversion(origin, matrix):
    destination = np.zeros_like(origin)
    for i in range(origin.shape[0]):
        for j in range(origin.shape[1]):
            origin_px = origin[i, j, :3]
            destination[i, j, :3] = np.dot(matrix, origin_px)
    return destination


def sim_defect(lms, defect):
    if defect == 'd':
        lms_defect = space_conversion(lms, lms2lmsd)
    elif defect == 'p':
        lms_defect = space_conversion(lms, lms2lmsp)
    elif defect == 't':
        lms_defect = space_conversion(lms, lms2lmst)
    return lms_defect


def compare(true, defect):
    error = (true - defect)
    return error


def daltonize(rgb, rgb_defect, matrix):
    error = compare(rgb, rgb_defect)
    delta = space_conversion(error, matrix)
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


def lookap(rgb, defect):
    lms = space_conversion(rgb, rgb2lms)
    lms_defect = sim_defect(lms, defect)
    rgb_defect = space_conversion(lms_defect, lms2rgb)
    corrected = daltonize(rgb, rgb_defect, err2mod)
    return corrected
