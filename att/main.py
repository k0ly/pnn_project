import pnn_lib
import numpy as np
from numpy.lib import stride_tricks
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from matplotlib import pyplot as plt
#import probflow as pf
#import tensorflow as tf
#import neupy.algorithms.rbfn.utils as utl
from sklearn.ensemble import GradientBoostingRegressor as gg
import cufflinks as cf

data = np.genfromtxt('data.csv', delimiter=',')

#df = pd.DataFrame(np.log(data))
#print(df.describe())


def rolling(a, window, st):
    shape = (a.size - window + st, window)
    strides = (a.itemsize, a.itemsize)
    return stride_tricks.as_strided(a, shape=shape, strides=strides)


def get_stats(p, percentiles):
    # Get the standard deviation and percentile estimates for each point in the feature grid
    stdevs = np.expand_dims(np.std(p, axis=1), axis=1)
    bottom = np.expand_dims(np.percentile(p, q=percentiles[0], axis=1), axis=1)
    top = np.expand_dims(np.percentile(p, q=percentiles[1], axis=1), axis=1)
    return stdevs, bottom, top


def get_intervals(preds, confidence_percentiles=(5.0, 95.0),
                  prediction_percentiles=(5.0, 95.0)):

    intervals = {'prediction': {}, 'confidence': {}}

    ps = np.concatenate(preds['main'], axis=1)
    _, boot_bottom, boot_top = get_stats(ps, percentiles=confidence_percentiles)
    intervals['confidence'] = {'top': boot_top, 'bottom': boot_bottom}

    pred_ints = []
    for p in prediction_percentiles:
        quant = np.round(p / 100, 2)
        ps = np.concatenate(preds[quant], axis=1)
        pred_ints.append(np.expand_dims(np.percentile(ps, q=p, axis=1), axis=1))

    intervals['prediction']['bottom'] = pred_ints[0]
    intervals['prediction']['top'] = pred_ints[1]

    return intervals

x1 = rolling(data, 4, 1)

x2 = np.empty((0,4),float)
for i in range(0,len(x1)):
    x2=np.vstack((x2,np.flip(x1[i], 0)))

x3 = np.empty((0,4),float)
for i in range(0,len(x1)):
    x3 = np.append(x3,np.array([np.hstack([data[:3], np.max(x1)])]), axis=0)

x = np.vstack((x1,x2))
x = np.vstack((x,x3))
nx = preprocessing.normalize(x)
sx = preprocessing.scale(x)
print (len(x))
y = list(range(0,len(x)))
for i in range(0,len(x)):
    if i<=2*len(x1):
        y[i]=0
    else:
        y[i]=1

x_train, x_test, y_train, y_test = train_test_split(nx, np.array(y), test_size=0.3)
pnn = pnn_lib.PNN(std=10, verbose=False)
pnn.train(x_train, y_train)
y_predicted = pnn.predict(x_test)
metrics.accuracy_score(y_test, y_predicted)

data_predict = np.genfromtxt('data_predict_223_7_more.csv', delimiter=',')

newxx = np.empty((0,4),float)
for i in range(0,len(data_predict)):
  newx=[np.hstack([data[-3:], data_predict[i]])]
  newxx = np.append(newxx,np.array(newx), axis=0)


newxx=preprocessing.normalize(newxx)
print('newxx=',newxx)

y_predicted_new = pnn.predict(newxx)

y_predicted_pp = (pnn.predict_proba(newxx))

for i in range(0,len(y_predicted_new)):
        print(i, '___', data_predict[i], '____', y_predicted_new[i], y_predicted_pp [i], '------',newxx[i])

ind =  (np.where(y_predicted_pp==np.max(y_predicted_pp[:,0]))[0].astype(int))
print(ind,'___',data_predict[ind],'p=',np.max(y_predicted_pp[:,0]))


#===============================================================
# Instantiate the class
model = gg.GradientBoostingPredictionIntervals(
    lower_alpha=0.1, upper_alpha=0.9
)
# Fit and make predictions
_ = model.fit(x_train, y_train)
predictions = model.predict(x_test, y_test)
fig = model.plot_intervals(mid=True, start='2017-05-26',
                           stop='2017-06-01')
plt.plot(fig)
