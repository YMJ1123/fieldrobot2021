import cv2
import numpy as np
from utilities import *
import matplotlib.pyplot as plt
import ipdb 

img_path = 'testdata/avocado1.jpg'
image  = cv2.imread(img_path)
find_range(image)