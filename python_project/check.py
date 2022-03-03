#!usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import division
import math as mth
import main as mn

# проверка случайности колебаний уровней остаточной последовательности
# критерий пиков


def check_a(e):
    k = len(e)
    mx = 2 / 3 * (k - 2)
    dx = (16 * k - 29) / 90
    pp = mx - (1.96 * (dx ** 0.5))
    p = 0
    try:
        for i in range(2, k - 1):
            if ((e[i] > e[i - 1])) and ((e[i] > e[i + 1])):
                p += 1
            else:
                if (e[i] < e[i - 1]) and (e[i] < e[i + 1]):
                    p += 1
    except:
        print "ошибка -> 0"
        st_a = "ошибка -> 0"
        return 0, st_a
    else:
        if p > mth.modf(pp)[1]:
            print p, " > ", mth.modf(pp)[1], " -> 1"
            st_a = str(p) + " > " + str(mth.modf(pp)[1]) + " -> 1"
            return 1, st_a
        else:
            print p, " <= ", mth.modf(pp)[1], " -> 0"
            st_a = str(p) + " <= " + str(mth.modf(pp)[1]) + " -> 0"
            return 0, st_a


# проверка соответствия распределения случайной компоненты нормальному закону распределения
# показатели ассиметрии и эксцесса


def check_b(e):
    k = len(e)
    try:
        f1 = (1.0 / k) * sum(e ** 3) / (((1.0 / k) * sum(e ** 2)) ** (3 / 2))
        sf1 = ((6 * (k - 2)) / ((k + 1) * (k + 3))) ** 0.5
        f2 = ((1.0 / k) * sum(e ** 4) / ((1.0 / k) * sum(e ** 2) ** 2)) - 3
        sf2 = ((24 * k * (k - 2) * (k - 3)) / ((k + 1) ** 2 * (k + 3) * (k + 5))) ** 0.5
    except:
        print "ошибка -> 0"
        st_b = "ошибка -> 0"
        return 0, st_b
    else:
        if (mth.fabs(f1) < (1.5 * sf1)) and (mth.fabs(f2 + (6.0 / (k + 1)) < (1.5 * sf2))):
            print mth.fabs(f1), " < ", 1.5 * sf1, " and ", mth.fabs(f2 + (6.0 / (k + 1))), " < ", 1.5 * sf2, " -> 1"
            st_b = str(mth.fabs(f1)) + " < " + str(1.5 * sf1) + " and " + str(mth.fabs(f2 + (6.0 / (k + 1))))
            st_b += " < " + str(1.5 * sf2) + " -> 1"
            return 1, st_b
        else:
            if (mth.fabs(f1) >= (2 * sf1)) or ((mth.fabs(f2 + (6.0 / (k + 1))) >= (2 * sf2))):
                print mth.fabs(f1), " >= ", (2 * sf1), " or ", (mth.fabs(f2 + (6.0 / (k + 1)))), " >= ", 2 * sf2, " -> 0"
                st_b = str(mth.fabs(f1)) + " >= " + str(2 * sf1) + " or "
                st_b += str((mth.fabs(f2 + (6.0 / (k + 1))))) + " >= " + str(2 * sf2) + " -> 0"
                return 0, st_b
            else:
                rs = (max(e) - min(e)) / ((sum(e ** 2)) / ((k - 1)) ** 0.5)

                if (rs >= 2.67) and (rs <= 3.658):
                    print rs, " >= 2.67 and ", rs, " <= 3.658 -> 1"
                    st_b = str(rs) + " >= 2.67 and " + str(rs) + " <= 3.658 -> 1"
                    return 1, st_b
                else:
                    print "not(", rs, " >= 2.67 and ", rs, " <= 3.658) -> 0"
                    st_b = "not(" + str(rs) + " >= 2.67 and " + str(rs) + " <= 3.658) -> 0"
                    return 0, st_b


# проверка равенства математического ожидания случайной компоненты нулю


def check_c(e):
    k = len(e)
    try:
        tr = (sum(e) / k) / ((sum(e ** 2) / (k - 1)) ** 0.5) * (k ** 0.5)
        if tr < 2.57:
            print tr, " < 2.57 -> 1"
            st_c = str(tr) + " < 2.57 -> 1"
            return 1, st_c
        else:
            print tr, " >= 2.57 -> 0"
            st_c = str(tr) + " >= 2.57 -> 0"
            return 0, st_c
    except:
        print "ошибка -> 0"
        st_c = "ошибка -> 0"
        return 0, st_c


# проверка независимости значений уровней случайной компоненты


def check_d(e):
    k = len(e)
    e = e.T
    d = 0
    if k <= 15:
        d1 = 1.08
        d2 = 1.36
    else:
        if k <= 20:
            d1 = 1.2
            d2 = 1.41
        else:
            d1 = 1.35
            d2 = 1.49
    for i in range(2, k):
        d += (e[i] - e[i - 1]) ** 2
    try:
        d /= sum(e ** 2)
        if (d <= 4) and (d >= 2):
            d = 4 - d
        if d > d2:
            st_d = str(d) + " > " + str(d2) + " -> 1"
            print d, " > ", d2, " -> 1"
            return 1, st_d
        else:
            if d < d1:
                st_d = str(d) + " < " + str(d1) + " -> 0"
                print d, " < ", d1, " -> 0"
                return 0, st_d
            else:
                r = 0
                for i in range(2, k):
                    r += e[i] * e[i - 1]
                r /= sum(e ** 2)
                if mth.fabs(r) < mth.fabs(1 - d2):
                    st_d = str(mth.fabs(r)) + " > " + str(mth.fabs(1 - d2)) + " -> 1"
                    print mth.fabs(r), " > ", mth.fabs(1 - d2), " -> 1"
                    return 1, st_d
                else:
                    st_d = str(mth.fabs(r)) + " <= " + str(mth.fabs(1 - d2)) + " -> 0"
                    print mth.fabs(r), " <= ", mth.fabs(1 - d2), " -> 0"
                    return 0, st_d
    except:
        st_d = "ошибка -> 0"
        print "ошибка -> 0"
        return 0, st_d


def print_check(e):
    ch_a, st_a = check_a(e)
    ch_b, st_b = check_b(e)
    ch_c, st_c = check_c(e)
    ch_d, st_d = check_d(e)
    print "проверка: ", str(ch_a), " ", str(ch_b), " ", str(ch_c), " ", str(ch_d)
    return ch_a, st_a,  ch_b, st_b, ch_c, st_c, ch_d, st_d