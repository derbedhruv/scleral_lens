from math import sin, cos, pi, sqrt
from random import random
import numpy as np
from collections import namedtuple
from scipy.optimize import fmin_bfgs as bgfs

#Error = sigma_i ((x_i-x_c)^2 + (y_i-y_c)^2 - r^2)^2
#d(Error)/d(x_c) = -2*sigma_i {(x_i-x_c)^2 + (y_i-y_c)^2 - r^2}{2*(x_i-x_c)}
#d(Error)/d(y_c) = -2*sigma_i {(x_i-x_c)^2 + (y_i-y_c)^2 - r^2}{2*(y_i-y_c)}
#d(Error)/d(r) = -2*sigma_i {(x_i-x_c)^2 + (y_i-y_c)^2 - r^2}{2*r}
		
def LSqFitCircle(XY,initialGuess = None):
	
	Circle = namedtuple("Circle",["x","y","r","error"])
	
	def LSE(pos,r,XY):
# 		print np.power(XY-pos,2)
# 		raw_input()
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
	alpha = 0.00001
	newpos = np.matrix([0.0,0.0])
	while(LSE(c,r,XY) > 0.00001 and iter<10000):
		iter += 1
		newpos = c - alpha*np.concatenate([grad_x(c,r,XY),grad_y(c,r,XY)],axis=1)
		r			= r      - alpha*grad_r(c,r,XY)
		c = newpos
	return Circle(c[0,0],c[0,1],r[0,0],sqrt(sqrt(LSE(c,r,XY)[0,0]/XY.shape[0])))

def LSQ(XY, initialGuess = None):
	
	Circle = namedtuple("Circle",["x","y","r"])
	
	if initialGuess == None:	
		V = np.array([random(), random(), random()])
	elif len(initialGuess) == 3:
		V = np.array([initialGuess[0], initialGuess[1], initialGuess[2]])
	else:
		raise Exception()
	
	def LSE_wrapper(XY):
		def LSE(V):
			a = np.sum(np.power(XY-V[:2],2),axis=1)
			return np.sum(np.power(a - V[2]**2,2),axis=0)
		return LSE
	
	circ_msr = LSE_wrapper(XY)
	result =  bgfs(circ_msr,V)
	return Circle(result[0], result[1], result[2])

if __name__ == "__main__":
	print LSQ(np.matrix([[2,0],[-2,0],[0,2]]),(0,0,1))