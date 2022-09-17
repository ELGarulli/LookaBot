import numpy as np

# Transformation matrix for Deuteranope (a form of red/green color deficit)
lms2lmsd = np.array([[1, 0, 0], [0.494207, 0, 1.24827], [0, 0, 1]])
# Transformation matrix for Protanope (another form of red/green color deficit)
lms2lmsp = np.array([[0, 2.02344, -2.52581], [0, 1, 0], [0, 0, 1]])
# Transformation matrix for Tritanope (a blue/yellow deficit - very rare)
lms2lmst = np.array([[1, 0, 0], [0, 1, 0], [-0.395913, 0.801109, 0]])
# Colorspace transformation matrices
rgb2lms = np.array([[17.8824, 43.5161, 4.11935], [3.45565, 27.1554, 3.86714], [0.0299566, 0.184309, 1.46709]])
# Daltonize image correction matrix
err2mod = np.array([[0, 0, 0], [0.7, 1, 0], [0.7, 0, 1]])

lms2rgb = np.linalg.inv(rgb2lms)

color_blindness = {"p": "Protanopia", "d": "Deuteranopia", "t": "Tritanopia"}
