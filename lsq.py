from math import sin, cos, pi, sqrt
from random import random
import numpy as np
from collections import namedtuple
from scipy.optimize import fmin_bfgs as bgfs

#Error = sigma_i ((x_i-x_c)^2 + (y_i-y_c)^2 - r^2)^2

def LSQ(XY, initialGuess = None):
	
	Circle = namedtuple("Circle",["x","y","r","error"])
	
	if initialGuess == None:	
		V = np.matrix([random(), random(), random()])
	elif len(initialGuess) == 3:
		V = np.matrix([initialGuess[0], initialGuess[1], initialGuess[2]])
	else:
		raise Exception()
	
	def LSE_wrapper(XY):
		def LSE(V): # Creating a Python closure to wrap data into target function for optimizer
			if len(V.shape) > 1: #Jugaad for stupid Scipy bug that randomly calls with array and matrix
				T = np.array([0,0,0])
			 	T[0] = V[0,0]
			 	T[1] = V[0,1]
			 	T[2] = V[0,2]
			 	V = T
			a = np.sum(np.power(XY-V[:2],2),axis=1)
			return np.sum(np.power(a - V[2]**2,2),axis=0)
		return LSE
	
	circ_msr = LSE_wrapper(XY)
	result =  bgfs(circ_msr,V)
	return Circle(result[0], result[1], result[2], sqrt(sqrt(circ_msr(result))/5))