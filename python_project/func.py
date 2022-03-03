#!usr/bin/python
#-*- coding: utf-8 -*-

import numpy as np
import math as mth


def function_a(x, y, n):  # a0 * x ** n + a1 * x ** (n-1) + ...
    c = np.polyfit(x, y, n)
    x_int = np.linspace(x[0], x[-1], 100)
    y_int = []
    for i in range(0, len(x_int)):
        f = 0
        for j in range(0, n + 1):
            f += c[j] * x_int[i] ** (n - j)
        y_int.append(f)
    return x_int, y_int, c


def rg_log(z):
    m = []
    for i in range(0, len(z)):
        if z[i] > 0:
            m.append(mth.log(z[i]))
    return m


def function_b(x, y):  # a * (x ** b)
    lx = rg_log(x)
    ly = rg_log(y)
    c = np.polyfit(lx, ly, 1)
    x_int = list(np.linspace(x[0], x[-1], 100))
    y_int = []
    for i in range(0, len(x_int)):
        y_int.append((mth.exp(1.0) ** c[1]) * x_int[i] ** c[0])
    return x_int, y_int, c


def function_c(x, y):  # a * (b ** x)
    ly = rg_log(y)
    c = np.polyfit(x, ly, 1)
    x_int = np.linspace(x[0], x[-1], 100)
    y_int = []
    for i in range(0, len(x_int)):
        y_int.append(mth.exp(1.0) ** (x_int[i] * c[0] + c[1]))
    return x_int, y_int, c


def function_d(x, y):  # a * (b ** x) * (c ** (x ** 2))
    ly = rg_log(y)
    c = np.polyfit(x, ly, 2)
    x_int = np.linspace(x[0], x[-1], 100)
    y_int = []
    for i in range(0, len(x_int)):
        y_int.append(mth.exp(1.0) ** (c[0] * (x_int[i] ** 2) + (c[1] * x_int[i]) + c[2]))
    print c
    return x_int, y_int, c


def function_e(x, y):  # a * (e ** (b * x))
    ly = rg_log(y)
    c = np.polyfit(x, ly, 1)
    x_int = np.linspace(x[0], x[-1], 100)
    y_int = []
    for i in range(0, len(x_int)):
        y_int.append(mth.exp(1.0) ** (x_int[i] * c[0]) * mth.exp(1.0) ** c[1])
    return x_int, y_int, c


def func_a(x, c, n):
    y = []
    for i in range(0, len(x)):
        f = 0
        for j in range(0, n + 1):
            f += c[j] * x[i] ** (n - j)
        y.append(f)
    return y


def func_b(x, c):
    y = []
    for i in range(0, len(x)):
        y.append((mth.exp(1.0) ** c[1]) * x[i] ** c[0])
    return y


def func_c(x, c):
    y = []
    for i in range(0, len(x)):
        y.append(mth.exp(1.0) ** (x[i] * c[0] + c[1]))
    return y


def func_d(x, c):
    y = []
    for i in range(0, len(x)):
        y.append(mth.exp(1.0) ** (c[0] * (x[i] ** 2) + (c[1] * x[i]) + c[2]))
    return y


def func_e(x, c):
    y = []
    for i in range(0, len(x)):
        y.append(mth.exp(1.0) ** (x[i] * c[0]) * mth.exp(1.0) ** c[1])
    return y


def func_a_one(x, c, n):
    f = 0
    for j in range(0, n + 1):
        f += c[j] * x ** (n - j)
    return f


def func_b_one(x, c):
    f = (mth.exp(1.0) ** c[1]) * x ** c[0]
    return f


def func_c_one(x, c):
    f = mth.exp(1.0) ** (x * c[0] + c[1])
    return f


def func_d_one(x, c):
    f = mth.exp(1.0) ** (c[0] * (x ** 2) + (c[1] * x) + c[2])
    return f


def func_e_one(x, c):
    f = (mth.exp(1.0) ** (x * c[0]) * mth.exp(1.0) ** c[1])
    return f