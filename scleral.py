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
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.widgets import Cursor, Button
from PIL import Image
from ransac import RANSAC_circle

# defaultCursorOnMoveHandler = Cursor.onmove #Total jugaad
# 
# class scleralViewer(object):
# 	def __init__(self,img):
# 		self.img = img
# 		self.fig = plt.figure()
# 		self.main_img = plt.subplot2grid((6,4),(0,0),rowspan = 5,colspan = 4)
# 		self.main_img.imshow(img)
# 		self.button1 = plt.subplot2grid((6,4),(5,0),rowspan = 1,colspan = 1)
# 		
# 		self.ptx = None
# 		self.pty = None
# 		Cursor.onmove = self.recordAndPassToDefaultHandler #Total jugaad
# 		pointChooser = Cursor(self.main_img,useblit=False)
# 		
# 		evaluateCurvature = Button(self.button1,'Find Curvature')
# 		evaluateCurvature.on_clicked(self.doRANSAC)
# 		
# 		self._widgets = []
# 		self._widgets.append(pointChooser)
# 		self._widgets.append(evaluateCurvature)
# 	
# 	def recordAndPassToDefaultHandler(self,event): #Total jugaad
# 		self.ptx = event.x
# 		self.pty = event.y
# 		defaultCursorOnMoveHandler(self._widgets[0],event)
# 		
# 	def doRANSAC(self, event):
# 		print("Doing the dew")
# 		
# if __name__ == "__main__":
# 	img = Image.open('images/Tiff/cropped.tiff')
# 	s = scleralViewer(img)
# 	plt.show()

class scleralViewer(object):
	
	def __init__(self,img,frame_width = 30,frame_height = 30):
		self.frame_width = frame_width
		self.frame_height = frame_height
		channels = img.split()#Get all channels in a tuple
		self.img = np.array(channels[0] * (1-channels[1]) * (1-channels[2])) # Max Rs
		self.fig = plt.figure()
		self.main_img = plt.subplot2grid((6,4),(0,0),rowspan = 5,colspan = 4)
		self.main_img.imshow(self.img)
		self.button1 = plt.subplot2grid((6,4),(5,0),rowspan = 1,colspan = 1)
		
		pointChooser = Cursor(self.main_img,useblit=False)
		self.cursor = pointChooser
		
		evaluateCurvature = Button(self.button1,'Find Curvature')
		evaluateCurvature.on_clicked(self.doRANSAC)
		
		self.fig.canvas.mpl_connect('button_press_event',self.onClick)
		
		self._widgets = []
		self._widgets.append(pointChooser)
		self._widgets.append(evaluateCurvature)
		
	def doRANSAC(self, event):
		x = event.x
		y = event.y
		# Get list of coordinates of all black points in a window of size 20x20 around the clicked point
		subimg = self.img[x-self.frame_height:x+self.frame_height,y-self.frame_width:y+self.frame_width]
		#TODO: Insert out of image guards ^
		px,py = np.nonzero(subimg)
		points = np.matrix([px,py]).transpose() + np.matrix([x+self.frame_height,y+self.frame_width])
		c = RANSAC_circle(points)
		print (c.x,c.y,c.r)
		
	def onClick(self, event):
		self.cursor.clear(event)
		self.cursor.onmove(event)
		
if __name__ == "__main__":
	img = Image.open('images/Tiff/cropped_borders.tiff')
	s = scleralViewer(img)
	plt.show()
