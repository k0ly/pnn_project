import numpy as np
from numpy.lib import stride_tricks
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

def rolling(a, window, st):
    shape = (a.size - window + st, window)
    strides = (a.itemsize, a.itemsize)
    return stride_tricks.as_strided(a, shape=shape, strides=strides)


def input():
	data = np.genfromtxt('data.csv', delimiter=',')

	x = rolling(np.log(data), 4, 1)
	nx = preprocessing.normalize(x)
	sx = preprocessing.scale(x)

	y = rolling(np.log(data), 1, 4)
	y = y[1:len(x)+1]
	for i in range(0,len(y)):
		y[i]=int(y[i]>=np.mean(x[i]))+1

	x_train, x_test, y_train, y_test = train_test_split(nx, np.array(y), test_size=0.3)#, random_state = 0)



	data = {'x_train': x_train,
		'x_test': x_test,
		'y_train': y_train,
		'y_test': y_test}

	return data
