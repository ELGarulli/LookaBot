import numpy
import skimage.io
from image_process import test_pipeline
from PIL import Image

rgb2lms = numpy.array([[17.8824, 43.5161, 4.11935], [3.45565, 27.1554, 3.86714], [0.0299566, 0.184309, 1.46709]])

im = Image.open("./fall_trees.jpg")
im = im.copy()
im = im.convert('RGB')
rgb = numpy.asarray(im, dtype=float)

corrected = test_pipeline(rgb)

im_converted = Image.fromarray(corrected, mode='RGB')
im_converted.save("./corrected.jpg")


