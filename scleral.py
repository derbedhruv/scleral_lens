'''
  SCLERAL RADIAL CONVERSION MEASUREMENT SOFTWARE
  
  Authors: Darpan Sanghavi, Sujeath Pareddy, Dhruv Joshi
  
  HOW TO USE:
  1. User chooses folder containing TIFF reports from the Visante AS-OCT Instrument (Nasal, temporal, superior, inferior and cornea per eye - the scans should have edge detection enabled (where red implies the outer surface))
  2. The software displays a cropped portion of this report containing the actual OCT image
  3. The user selects the point around which the radius of curvature is desired
  4. The program displays the Radii of curvature at these points.
'''

import scipy as sc
import scipy.misc
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Button
from lsq import LSQ
import math

class scleralViewer(object):
	
	def __init__(self,img,frame_width = 30,frame_height = 30):
		self.frame_width = frame_width
		self.frame_height = frame_height
		self.fig = plt.figure()
		self.img = img
		self.main_img = plt.subplot2grid((6,5),(0,0),rowspan = 6,colspan = 5)
		self.main_img.imshow(self.img,cmap = plt.cm.gray)
		
		self.cursor = Cursor(self.main_img,useblit=False)
		
		self.fig.canvas.mpl_connect('button_press_event',self.onClick)
		
		self.lastclick_x = None
		self.lastclick_y = None
		
		self.clickStack = []
		
	def onClick(self, event):
		# Event has coordinate system with origin in the bottom left, y up and x right
		# bbox.bounds = (lower left x,lower left y, width, height) of image
		# image coordinate system has origin in upper right, x down, y to the right
		if event.inaxes == self.main_img:
			click_in_window_coords_x = event.x - self.main_img.bbox.bounds[0]
			click_in_window_coords_y = event.y - self.main_img.bbox.bounds[1]
			y = (click_in_window_coords_x)/self.main_img.bbox.bounds[2]*self.img.shape[1]
			x = (self.main_img.bbox.bounds[3] - click_in_window_coords_y)/self.main_img.bbox.bounds[3]*self.img.shape[0]
			self.clickStack.append([x,y])
			print [x,y]
			if len(self.clickStack) == 5:
				# Wait for 5 points are accumulated
				circle = LSQ(np.matrix(self.clickStack),(0,0,1))
				print circle
				self.clickStack = []
		
if __name__ == "__main__":
	img = scipy.misc.imread('images/Tiff/test.tif')
	s = scleralViewer(img,20,20)
	plt.show()
