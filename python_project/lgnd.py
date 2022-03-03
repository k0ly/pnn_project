#!usr/bin/python
#-*- coding: utf-8 -*-


import math as mth


def legend_a(c, n):
    l = ""
    for j in range(0, n + 1):
        if j != n + 1:
            if c[n - j] >= 0:
                if j > 0:
                    l += " + "
            l += str(round(c[n - j], 2))
            if j > 0:
                l += " * x"
            if j > 1:
                l += " ^ " + str(j)
        elif j == n + 1:
            l += str(round(c[n - j], 2)) + " + "
    print "koef", c
    return l


def legend_b(c):
    if c[0] > 0:
        l = str(round(mth.exp(1.0) ** c[1], 2)) + " * x ^ " + str(round(c[0], 2))
    else:
        l = str(round(mth.exp(1.0) ** c[1], 2)) + " * x ^ (" + str(round(c[0], 2)) + ")"
    return l


def legend_c(c):
    l = str(round(mth.exp(1.0) ** c[1], 2)) + " * "
    if c[0] > 0:
        l = l + str(round(mth.exp(1.0) ** c[0], 2)) + " ^ x"
    else:
        l = l + "(" + str(round(mth.exp(1.0) ** c[0], 2)) + ") ^ x"
    print "koef", mth.exp(1.0) ** c[1], " ", mth.exp(1.0) ** c[0]
    return l


def legend_d(c):
    l = ""
    l = l + str(round(mth.exp(1.0) ** c[2], 2)) + " * ("
    if c[1] > 0:
        l = l + str(round(mth.exp(1.0) ** c[1], 2)) + " ^ x) * ("
    else:
        l = l + "(" + str(round(mth.exp(1.0) ** c[1], 2)) + ") ^ x) * ("
    if c[0] > 0:
        l = l + str(round(mth.exp(1.0) ** c[0], 2)) + " ^ (x ^ 2))"
    else:
        l = l + "(" + str(round(mth.exp(1.0) ** c[0], 2)) + ") ^ (x ^ 2))"
    return  l


def legend_e(c):
    l = str(round(mth.exp(1.0) ** c[1], 2)) + " * e ^ ( " + str(round(c[0], 2)) + " * x)"
    return l