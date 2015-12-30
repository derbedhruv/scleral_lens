import numpy as np
import random
from math import sqrt, sin, cos, pi

def RANSAC_circle(XY, iters = None):
	
	class Circle:
		
		def __init__(self,pt1,pt2,pt3):
			#From http://math.stackexchange.com/questions/213658/get-the-equation-of-a-circle-when-given-3-points
			x1 = pt1[0,0]
			y1 = pt1[0,1]
			x2 = pt2[0,0]
			y2 = pt2[0,1]
			x3 = pt3[0,0]
			y3 = pt3[0,1]
			self.x = -0.5*(- (x1**2)*y2 + (x1**2)*y3 + (x2**2)*y1 - (x2**2)*y3 - (x3**2)*y1 + (x3**2)*y2 - (y1**2)*y2 + (y1**2)*y3 + y1*(y2**2) - y1*(y3**2) - (y2**2)*y3 + y2*(y3**2))/(x1*y2 - x2*y1 - x1*y3 + x3*y1 + x2*y3 - x3*y2)
			self.y = -0.5*((x1**2)*x2 - (x1**2)*x3 - x1*(x2**2) + x1*(x3**2) - x1*(y2**2) + x1*(y3**2) + (x2**2)*x3 - x2*(x3**2) + x2*(y1**2) - x2*(y3**2) - x3*(y1**2) + x3*(y2**2))/(x1*y2 - x2*y1 - x1*y3 + x3*y1 + x2*y3 - x3*y2)
			self.r = sqrt( (self.x-x1)**2 + (self.y-y1)**2)
			self.pos = np.matrix([self.x,self.y])
	
		def distanceToCircle(self,XY):
			"""
				Pass an Nx2 matrix of points (XY)
			"""
			return np.abs(np.sum(np.sum(np.power((XY-self.pos),2),axis=1)[0,0] - self.r**2))
	
	N = XY.shape[0]
	
	if iters == None:
		if N > 1000:
			iters = XY.shape[0]/10
		else:
			iters = 200
	
	bestErrorSoFar = float('inf')
	bestCircleSoFar = None
	for i in xrange(iters):
		# Pick three points randomly
		pts = random.sample(xrange(1,N),3)
		# Find the circle which passes through the above 3 points
		circle = Circle(XY[pts[0],:],XY[pts[1],:],XY[pts[2],:])
		# Find error with respect to all the point
		thisError = circle.distanceToCircle(XY)
		
		if thisError < bestErrorSoFar:
			bestErrorSoFar = thisError
			bestCircleSoFar = circle
		print bestErrorSoFar
	return bestCircleSoFar
		
if __name__ == "__main__":
	pts = []
	for i in range(1,100):
		theta = pi*i/100.0;
		pts.append([cos(theta) + random.uniform(0,0.1),sin(theta) + random.uniform(0,0.1)])
	pts = np.matrix(pts)
	c = RANSAC_circle(pts)
		
		