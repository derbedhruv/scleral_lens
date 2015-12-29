'''
  SCLERAL RADIAL CONVERSION MEASUREMENT SOFTWARE
  
  Authors: Darpan Sanghavi, Sujeath Pareddy, Dhruv Joshi
  
  HOW TO USE:
  1. User chooses folder containing TIFF reports from the Visante AS-OCT Instrument (Nasal, temporal, superior, inferior and cornea per eye - the scans should have edge detection enabled (where red implies the outer surface))
  2. The software displays a cropped portion of this report containing the actual OCT image
  3. The user selects the point around which the radius of curvature is desired
  4. The program displays the Radii of curvature at these points.
'''

import scipy.misc as sp
import matplotlib.pyplot as plt