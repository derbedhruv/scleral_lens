from math import sin, cos, pi
from random import random
import numpy as np
from collections import namedtuple

#Error = sigma_i ((x_i-x_c)^2 + (y_i-y_c)^2 - r^2)^2
#d(Error)/d(x_c) = -2*sigma_i {(x_i-x_c)^2 + (y_i-y_c)^2 - r^2}{2*(x_i-x_c)}
#d(Error)/d(y_c) = -2*sigma_i {(x_i-x_c)^2 + (y_i-y_c)^2 - r^2}{2*(y_i-y_c)}
#d(Error)/d(r) = -2*sigma_i {(x_i-x_c)^2 + (y_i-y_c)^2 - r^2}{2*r}
		
def LSqFitCircle(XY,initialGuess = None):
	
	Circle = namedtuple("Circle",["x","y","r","error"])
	
	def LSE(pos,r,XY):
		return np.sum(np.power(np.sum(np.power(XY-pos,2),axis=1) - r**2,2),axis=0)
	
	def grad_x(pos,r,XY):
		return -4*np.sum(np.multiply(np.sum(np.power(XY-pos,2),axis=1) - r**2,XY[:,0]-pos[0,0]),axis=0)
		
	def grad_y(pos,r,XY):
		return -4*np.sum(np.multiply(np.sum(np.power(XY-pos,2),axis=1) - r**2,XY[:,1]-pos[0,1]),axis=0)
		
	def grad_r(pos,r,XY):
		return -4*np.sum((np.sum(np.power(XY-pos,2),axis=1) - r**2)*r,axis=0)

	if initialGuess == None:	
		c = np.matrix([random(), random()])
		r = random()
	elif len(initialGuess) == 3:
		c = np.matrix([initialGuess[0], initialGuess[1]])
		r = initialGuess[2]
	else:
		raise Exception()
		
	iter = 0
	alpha = 0.01
	newpos = np.matrix([0.0,0.0])
	while(LSE(c,r,XY) > 0.00001 and iter<10000):
		iter += 1
		newpos = c - alpha*np.concatenate([grad_x(c,r,XY),grad_y(c,r,XY)],axis=1)
		r			= r      - alpha*grad_r(c,r,XY)
		c = newpos
	return Circle(c[0,0],c[0,1],r[0,0],LSE(c,r,XY)[0,0])

if __name__ == "__main__":
	print LSqFitCircle(np.matrix([[1,0],[0,1],[0,0]]))	