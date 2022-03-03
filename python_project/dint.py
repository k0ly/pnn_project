#!usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import division
import numpy as np
from scipy.stats import f
import scipy.stats as sc
import math as mth

def dint(x, y, alpha, y_tr, x_new, y_new, ch_box):
    n = len(y)
    t_tabl = sc.t.ppf(1 - alpha / 2, n - 2)  # t-критерий стьюдента при уровне значимости alpha и числом степеней свободы n-2
    dost = y - np.array(y_tr)
    dstd = sc.stats.nanstd(dost, 0, False)
    dmean = np.mean(x[0], axis=0)
    dvar = np.var(x[0], axis=0, ddof=1)

    #f_obr = f.isf(alpha, 2, len(y) - 2) # СТЬЮДРАСПОБР
    #n1 = y_tr - (2 * f_obr * std * ((1 / len(x[0]) + ((x[0] - np.mean(x[0])) ** 2) / (len(x[0]) - 1) / np.var(x[0], axis=0, ddof=1)) ** 0.5))
    #n2 = y_tr + (2 * f_obr * std * ((1 / len(x[0]) + ((x[0] - np.mean(x[0])) ** 2) / (len(x[0]) - 1) / np.var(x[0], axis=0, ddof=1)) ** 0.5))

    n1 = y_tr - t_tabl * dstd * ((1 / n) + (((x[0] - dmean) ** 2) / ((n - 1) * dvar))) ** 0.5
    n2 = y_tr + t_tabl * dstd * ((1 / n) + (((x[0] - dmean) ** 2) / ((n - 1) * dvar))) ** 0.5



    if ch_box != 3:
        n3 = mth.log(y_new) - t_tabl * dstd * ((1 / n) + (((x_new - dmean) ** 2) / ((n - 1) * dvar))) ** 0.5
        n4 = mth.log(y_new) + t_tabl * dstd * ((1 / n) + (((x_new - dmean) ** 2) / ((n - 1) * dvar))) ** 0.5
        n1 = mth.exp(1.0) ** n1
        n2 = mth.exp(1.0) ** n2
        n3 = mth.exp(1.0) ** n3
        n4 = mth.exp(1.0) ** n4
    else:
        n3 = y_new - t_tabl * dstd * ((1 / n) + (((x_new - dmean) ** 2) / ((n - 1) * dvar))) ** 0.5
        n4 = y_new + t_tabl * dstd * ((1 / n) + (((x_new - dmean) ** 2) / ((n - 1) * dvar))) ** 0.5

    print "n1", n1
    print "n2", n2
    print "n3", n3
    print "n4", n4

    return  n1, n2, n3, n4


def dint_full(x, y, alpha, y_tr, x_new, y_new, ch_box):
    n = len(y)
    t_tabl = sc.t.ppf(1 - alpha / 2, n - 2)  # t-критерий стьюдента при уровне значимости alpha и числом степеней свободы n-2
    dost = y - np.array(y_tr)
    dstd = sc.stats.nanstd(dost, 0, False)
    dmean = np.mean(x[0], axis=0)
    dvar = np.var(x[0], axis=0, ddof=1)

    n1 = y_tr - t_tabl * dstd * (1 + (1 / n) + (((x[0] - dmean) ** 2) / ((n - 1) * dvar))) ** 0.5
    n2 = y_tr + t_tabl * dstd * (1 + (1 / n) + (((x[0] - dmean) ** 2) / ((n - 1) * dvar))) ** 0.5

    if ch_box != 3:
        n3 = mth.log(y_new) - t_tabl * dstd * (1 + (1 / n) + (((x_new - dmean) ** 2) / ((n - 1) * dvar))) ** 0.5
        n4 = mth.log(y_new) + t_tabl * dstd * (1 + (1 / n) + (((x_new - dmean) ** 2) / ((n - 1) * dvar))) ** 0.5
        n1 = mth.exp(1.0) ** n1
        n2 = mth.exp(1.0) ** n2
        n3 = mth.exp(1.0) ** n3
        n4 = mth.exp(1.0) ** n4
    else:
        n3 = y_new - t_tabl * dstd * (1 + (1 / n) + (((x_new - dmean) ** 2) / ((n - 1) * dvar))) ** 0.5
        n4 = y_new + t_tabl * dstd * (1 + (1 / n) + (((x_new - dmean) ** 2) / ((n - 1) * dvar))) ** 0.5

    print "n1", n1
    print "n2", n2
    print "n3", n3
    print "n4", n4

    return  n1, n2, n3, n4


def mn_dint(x0, y, alpha, y_tr, type_dint, k, ch_box, x_new, y_new):  # n-k-1
    n = len(x0)
    for t in range(0, n):
        x_n = []
        x_n.append(1)
        x_n.append(x0[t])
        for j in range(2, k + 1):
            d = x0[t] ** j
            x_n.append(d)
        x_n = np.matrix(x_n)
        if t == 0:
            x = x_n
        else:
            x = np.vstack((x, x_n))
        if (ch_box == 2) or (ch_box == 1):
            y_tr[t] = mth.log(y_tr[t])
    y_tr = np.matrix(y_tr).T
    xt = x.T
    xtx = np.dot(xt, x)
    xtxi = np.matrix(xtx).I

    #print "xtxi"
    #print xtxi

    t_tabl = sc.t.ppf(1 - alpha / 2, n - k - 1)

    y = np.matrix(y).T
    ost = y - y_tr
    tor = y - np.mean(y)
    dstd = 0
    tor2 = 0
    for i in range(0, n):
        dstd += ost[i][0] ** 2
        tor2 += tor[i][0] ** 2
    e2 = np.sum(dstd)
    tor2 = np.sum(tor2)
    dstd = (e2 / (n - k - 1)) ** 0.5

    # критерии!
    r2 = 1 - (e2 / tor2)
    fcr = (r2 / k) / ((1 - r2) / (n - k - 1))
    ft = f.isf(alpha, 2, n - k - 1)

    nx = []
    for i in range(0, len(x)):
        xx = np.dot(x[i], xtxi)
        xx = np.dot(xx, x[i].T)
        if type_dint == 0:
            nx.append(xx.sum() ** 0.5 * dstd * t_tabl)
        else:
            nx.append((1 + xx.sum()) ** 0.5 * dstd * t_tabl)
    nx = np.matrix(nx).T
    n1 = np.array(np.matrix(y_tr) - np.matrix(nx))
    n2 = np.array(np.matrix(y_tr) + np.matrix(nx))
    n1.shape = -1
    n2.shape = -1


    if (ch_box == 2) or (ch_box == 1):
        n1 = mth.exp(1.0) ** n1
        n2 = mth.exp(1.0) ** n2


    # для прогноза
    x = []
    x.append(1)
    x.append(x_new)
    for j in range(2, k + 1):
        d = x_new ** j
        x.append(d)
    x = np.matrix(x)
    if (ch_box == 2) or (ch_box == 1):
        y_new = mth.log(y_new)
    xx = np.dot(x, xtxi)
    xx = np.dot(xx, x.T)
    if type_dint == 0:
        n3 = y_new - xx.sum() ** 0.5 * dstd * t_tabl
        n4 = y_new + xx.sum() ** 0.5 * dstd * t_tabl
    else:
        n3 = y_new - (((1 + xx.sum()) ** 0.5) * dstd * t_tabl)
        #print y_new, " u ", ((1 + xx.sum()) ** 0.5) * dstd * t_tabl
        #print "n3", n3
        n4 = y_new + (((1 + xx.sum()) ** 0.5) * dstd * t_tabl)
        #print "n4", n4
    if (ch_box == 2) or (ch_box == 1):
        n3 = mth.exp(1.0) ** n3
        n4 = mth.exp(1.0) ** n4

    return  n1, n2, n3, n4, r2, fcr, ft



