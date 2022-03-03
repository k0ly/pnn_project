#!usr/bin/python
#-*- coding: utf-8 -*-

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import func
#import sys
import xlrd
import xlwt
import lgnd
import dint
import check
import random
import math as mth
import numpy as np
from  matplotlib import pyplot
from PyQt4 import QtGui, QtCore, uic, Qt


m = []


class main_window(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('main.ui', self)
        self.button_open.clicked.connect(self.button_open_click)
        self.button_x.clicked.connect(self.button_x_click)
        self.button_y.clicked.connect(self.button_y_click)
        self.button_trend.clicked.connect(self.button_trend_click)
        self.button_export.clicked.connect(self.button_export_click)

    def button_open_click(self):
        text = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
        self.textbox_file.setText(str(text))
        rb = xlrd.open_workbook(self.textbox_file.text(), formatting_info=False)
        sheet = rb.sheet_by_index(0)
        cols = 0
        for rownum in range(sheet.nrows):
            row = sheet.row_values(rownum)
            m.append(row)
            if rownum == 1:
                cols = len(row)
        model = QtGui.QStandardItemModel(sheet.nrows, cols)
        table = self.tableview
        for i in range(sheet.nrows):
            for j in range(cols):
                model.setData(model.index(i, j), m[i][j])
        table.setModel(model)
        table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        table.show()

    def button_x_click(self):
        n = 0
        for idx in self.tableview.selectedIndexes():
            n += 1
        model = QtGui.QStandardItemModel(1, n)
        table = self.table_x
        i = 0
        for idx in self.tableview.selectedIndexes():
            model.setData(model.index(0, i), m[idx.row()][idx.column()])
            i += 1
        table.setModel(model)
        table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        table.show()
        self.table_x.selectRow(0)

    def button_y_click(self):
        table = self.table_y
        num_row = []
        num_col = []
        for idx in self.tableview.selectedIndexes():
            if not(idx.row() in num_row):
                num_row.append(idx.row())
            if not (idx.column() in num_col):
                num_col.append(idx.column())
        model = QtGui.QStandardItemModel(len(num_row), len(num_col))

        edit_row = []
        for i in range(len(num_row)):
            if num_row[i] != i + 1:
                new_el = [i + 1, num_row[i]]
                edit_row.append(new_el)
        edit_col = []
        for i in range(len(num_col)):
            if num_col[i] != i + 1:
                new_el = [i + 1, num_col[i]]
                edit_col.append(new_el)
        for idx in self.tableview.selectedIndexes():
            a = -1
            for i in range(len(edit_row)):
                if idx.row() == edit_row[i][1]:
                    a = edit_row[i][0] - 1
            if a == -1:
                a = (idx.row() - 1)
            b = -1
            for i in range(len(edit_col)):
                if idx.column() == edit_col[i][1]:
                    b = edit_col[i][0] - 1
            if b == -1:
                b = (idx.column() - 1)
            model.setData(model.index(a, b), m[idx.row()][idx.column()])
        table.setModel(model)
        table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        table.show()
        self.table_y.selectRow(0)

    def button_trend_click(self):
        self.text_check.clear()
        x = []
        y = []
        for index in self.table_x.selectedIndexes():
            tmp = float(str(self.table_x.model().data(self.table_x.model().index(index.row(), index.column())).toString()))
            if tmp >= 2000:
                x.append(tmp - 2000 + 1)
            else:
                x.append(tmp)
        for index in self.table_y.selectedIndexes():
            y.append(float(str(self.table_y.model().data(self.table_y.model().index(index.row(), index.column())).toString())))

            print (x)
        # --------------------------------------------------------------------------------------------------------------
        self.textbox_x_new.setText(str(x[-1] + 1)) #прогнозное!!!
        n = 0
        for index in self.table_x.selectedIndexes():
            n += 1
        model = QtGui.QStandardItemModel(6, n + 6)  # количество строк для вывода нескольких моделей?
        table = self.table_res
        model.setData(model.index(0, 0), "x")
        model.setData(model.index(1, 0), "y")
        j = 0
        for index in self.table_x.selectedIndexes():
            model.setData(model.index(0, j + 1), self.table_x.model().data(self.table_x.model().index(index.row(), index.column())))
            j += 1
        j = 0
        for index in self.table_y.selectedIndexes():
            model.setData(model.index(1, j + 1), self.table_y.model().data(self.table_y.model().index(index.row(), index.column())))
            j += 1
        # --------------------------------------------------------------------------------------------------------------
        k = 1
        if len(x) == len(y):
            pyplot.plot(x, y, 'b.')

            # -------------------------------------------------a * (b ** x)---------------------------------------------
            if self.checkbox_1.checkState() == 2:
                k += 1
                xx, yy, c = func.function_c(x, y)
                l = str(lgnd.legend_c(c))
                x_new = float(self.textbox_x_new.text())
                y_new = func.func_c_one(x_new, c)
                pyplot.plot(np.hstack((list(xx), x_new)), np.hstack((yy, y_new)), 'b', label="y = " + l)
                yy = func.rg_log(y)
                dy = []
                for t in range(0, len(x)):
                    dy.append(c[1] + x[t] * c[0])

                # -------------------------------парная регрессия-------------------------------------------------------
                na1, na2, na3, na4 = dint.dint([x], yy, 0.05, dy, x_new, y_new, 1)
                na1 = np.hstack((na1, na3))
                na2 = np.hstack((na2, na4))
                pyplot.plot(np.hstack((x, x_new)), na1, 'm.', label="dint_a_2")
                pyplot.plot(np.hstack((x, x_new)), na2, 'm.', label="dint_b_2")

                nb1, nb2, nb3, nb4 = dint.dint_full([x], yy, 0.05, dy, x_new, y_new, 1)
                nb1 = np.hstack((nb1, nb3))
                nb2 = np.hstack((nb2, nb4))
                pyplot.plot(np.hstack((x, x_new)), nb1, 'r.', label="dint_a_1")
                pyplot.plot(np.hstack((x, x_new)), nb2, 'r.', label="dint_b_1")
                
                # -------------------------------множественная регрессия------------------------------------------------
                na1, na2, na3, na4, r2, f, ft = dint.mn_dint(x, yy, 0.05, func.func_c(x, c), 0, 1, 1, x_new, y_new)
                na1 = np.hstack((na1, na3))
                na2 = np.hstack((na2, na4))
                pyplot.plot(np.hstack((x, x_new)), na1, 'm--', label="dint_a_2_mn")
                pyplot.plot(np.hstack((x, x_new)), na2, 'm--', label="dint_b_2_mn")
                nb1, nb2, nb3, nb4, r2, f, ft = dint.mn_dint(x, yy, 0.05, func.func_c(x, c), 1, 1, 1, x_new, y_new)
                nb1 = np.hstack((nb1, nb3))
                nb2 = np.hstack((nb2, nb4))
                pyplot.plot(np.hstack((x, x_new)), nb1, 'r--', label="dint_a_1_mn")
                pyplot.plot(np.hstack((x, x_new)), nb2, 'r--', label="dint_b_1_mn")

                # -------------------------------------проверки---------------------------------------------------------
                self.text_check.append("y = " + l)
                e = y - np.array(func.func_c(x, c))
                ch_a, st_a, ch_b, st_b, ch_c, st_c, ch_d, st_d = check.print_check(e)
                self.text_check.append("check 1" + ": " + str(ch_a) + " " + str(ch_b) + " " + str(ch_c) + " " + str(ch_d))
                self.text_check.append(st_a)
                self.text_check.append(st_b)
                self.text_check.append(st_c)
                self.text_check.append(st_d)
                self.text_check.append("")
                self.text_check.append("R ** 2: " + str(r2))
                self.text_check.append("F: " + str(f))
                self.text_check.append("Ft:" + str(ft))

                # ------------------------------------вывод-------------------------------------------------------------
                model.setData(model.index(0, j + k - 2 + 1), str(x_new))
                model.setData(model.index(1, j + k - 2 + 1), str(y_new))
                model.setData(model.index(0, j + k - 1 + 1), "check")
                model.setData(model.index(1, j + k - 1 + 1), str(ch_a) + " " + str(ch_b) + " " + str(ch_c) + " " + str(ch_d))
                for t in range(0, len(x)):
                    model.setData(model.index(2, 0), "dint_a_1")
                    model.setData(model.index(2, t + 1), str(na1[t]))
                    model.setData(model.index(3, 0), "dint_b_1")
                    model.setData(model.index(3, t + 1), str(na2[t]))
                    model.setData(model.index(4, 0), "dint_a_2")
                    model.setData(model.index(4, t + 1), str(nb1[t]))
                    model.setData(model.index(5, 0), "dint_b_2")
                    model.setData(model.index(5, t + 1), str(nb2[t]))
                model.setData(model.index(2, t + 2), str(na3))
                model.setData(model.index(3, t + 2), str(na4))
                model.setData(model.index(4, t + 2), str(nb3))
                model.setData(model.index(5, t + 2), str(nb4))
                k += 1

            # -----------------------------------a * (b ** x) * (c ** (x ** 2))-----------------------------------------
            if self.checkbox_2.checkState() == 2:
                k += 1
                xx, yy, c = func.function_d(x, y)
                l = str(lgnd.legend_d(c))
                x_new = float(self.textbox_x_new.text())
                y_new = func.func_d_one(x_new, c)
                pyplot.plot(np.hstack((list(xx), x_new)), np.hstack((yy, y_new)), 'b', label="y = " + l)
                yyy = func.rg_log(y)

                # -------------------------------множественная регрессия------------------------------------------------
                na1, na2, na3, na4, r2, f, ft = dint.mn_dint(x, yyy, 0.05, func.func_d(x, c), 0, 2, 2, x_new, y_new)
                na1 = np.hstack((na1, na3))
                na2 = np.hstack((na2, na4))
                pyplot.plot(np.hstack((x, x_new)), na1, 'm--', label="dint_a_2")
                pyplot.plot(np.hstack((x, x_new)), na2, 'm--', label="dint_b_2")

                nb1, nb2, nb3, nb4, r2, f, ft = dint.mn_dint(x, yyy, 0.05, func.func_d(x, c), 1, 2, 2, x_new, y_new)
                nb1 = np.hstack((nb1, nb3))
                nb2 = np.hstack((nb2, nb4))
                pyplot.plot(np.hstack((x, x_new)), nb1, 'r--', label="dint_a_1")
                pyplot.plot(np.hstack((x, x_new)), nb2, 'r--', label="dint_b_1")

                # -------------------------------------проверки---------------------------------------------------------
                self.text_check.append("y = " + l)
                e = y - np.array(func.func_d(x, c))
                ch_a, st_a, ch_b, st_b, ch_c, st_c, ch_d, st_d = check.print_check(e)
                self.text_check.append("check 2" + ": " + str(ch_a) + " " + str(ch_b) + " " + str(ch_c) + " " + str(ch_d))
                self.text_check.append(st_a)
                self.text_check.append(st_b)
                self.text_check.append(st_c)
                self.text_check.append(st_d)
                self.text_check.append("")
                self.text_check.append("R ** 2: " + str(r2))
                self.text_check.append("F: " + str(f))
                self.text_check.append("Ft:" + str(ft))

                # ------------------------------------вывод-------------------------------------------------------------
                model.setData(model.index(0, j + k - 2 + 1), float(self.textbox_x_new.text()))
                model.setData(model.index(1, j + k - 2 + 1), str(func.func_d_one(float(self.textbox_x_new.text()), c)))
                model.setData(model.index(0, j + k - 1 + 1), "check")
                model.setData(model.index(1, j + k - 1 + 1), str(ch_a) + " " + str(ch_b) + " " + str(ch_c) + " " + str(ch_d))
                for t in range(0, len(x)):
                    model.setData(model.index(2, 0), "dint_a_1")
                    model.setData(model.index(2, t + 1), str(na1[t]))
                    model.setData(model.index(3, 0), "dint_b_1")
                    model.setData(model.index(3, t + 1), str(na2[t]))
                    model.setData(model.index(4, 0), "dint_a_2")
                    model.setData(model.index(4, t + 1), str(nb1[t]))
                    model.setData(model.index(5, 0), "dint_b_2")
                    model.setData(model.index(5, t + 1), str(nb2[t]))
                model.setData(model.index(2, t + 2), str(na3))
                model.setData(model.index(3, t + 2), str(na4))
                model.setData(model.index(4, t + 2), str(nb3))
                model.setData(model.index(5, t + 2), str(nb4))
                k += 1
            # -----------------------------------a0 * x ** n + a1 * x ** (n-1) + ...------------------------------------
            if self.checkbox_3.checkState() == 2:
                k += 1
                d = QtGui.QInputDialog()
                d.setTextValue('1')
                d.exec_()
                n = int(d.textValue())
                for i in range(n, n + 1):  # для перебора функций... пока одно значение
                    if i > 1:
                        k += 1
                    xx, yy, c = func.function_a(x, y, i)
                    l = str(lgnd.legend_a(c, i))
                    x_new = float(self.textbox_x_new.text())
                    y_new = func.func_a_one(x_new, c, i)
                    #pyplot.plot(np.hstack((list(xx), x_new)), np.hstack((yy, y_new)), 'b', label="y = " + l)
                    colr = 'ymcrgbk'
                    if i < 8:
                        if i > 1:
                            pyplot.plot(np.hstack((list(xx), x_new)), np.hstack((yy, y_new)), colr[i], label="y = " + l)
                    else:
                        pyplot.plot(np.hstack((list(xx), x_new)), np.hstack((yy, y_new)), colr[int(random.randrange(1, 7))], label="y = " + l)

                    if i == 1:
                        # -------------------------------множественная регрессия----------------------------------------
                        n1, n2, n3, n4, r2, f, ft = dint.mn_dint(x, y, 0.05, func.func_a(x, c, i), 0, i, 3, x_new, y_new)
                        n1 = np.hstack((n1, n3))
                        n2 = np.hstack((n2, n4))
                        pyplot.plot(np.hstack((x, x_new)), n1, 'm.', label="dint_a_2_mn")
                        pyplot.plot(np.hstack((x, x_new)), n2, 'm.', label="dint_b_2_mn")
                        n1, n2, n3, n4, r2, f, ft = dint.mn_dint(x, y, 0.05, func.func_a(x, c, i), 1, i, 3, x_new, y_new)
                        n1 = np.hstack((n1, n3))
                        n2 = np.hstack((n2, n4))
                        pyplot.plot(np.hstack((x, x_new)), n1, 'r.', label="dint_a_1_mn")
                        pyplot.plot(np.hstack((x, x_new)), n2, 'r.', label="dint_b_1_mn")

                        # -------------------------------парная регрессия-----------------------------------------------
                        na1, na2, na3, na4 = dint.dint([x], y, 0.05, func.func_a(x, c, i), x_new, y_new, 3)
                        na1 = np.hstack((na1, na3))
                        na2 = np.hstack((na2, na4))
                        pyplot.plot(np.hstack((x, x_new)), na1, 'm--', label="dint_a_2")
                        pyplot.plot(np.hstack((x, x_new)), na2, 'm--', label="dint_b_2")

                        nb1, nb2, nb3, nb4 = dint.dint_full([x], y, 0.05, func.func_a(x, c, i), x_new, y_new, 3)
                        nb1 = np.hstack((nb1, nb3))
                        nb2 = np.hstack((nb2, nb4))
                        pyplot.plot(np.hstack((x, x_new)), nb1, 'r--', label="dint_a_1")
                        pyplot.plot(np.hstack((x, x_new)), nb2, 'r--', label="dint_b_1")
                    else:
                        # -------------------------------множественная регрессия----------------------------------------
                        na1, na2, na3, na4, r2, f, ft = dint.mn_dint(x, y, 0.05, func.func_a(x, c, i), 0, i, 3, x_new, y_new)
                        na1 = np.hstack((na1, na3))
                        na2 = np.hstack((na2, na4))
                        nb1, nb2, nb3, nb4, r2, f, ft = dint.mn_dint(x, y, 0.05, func.func_a(x, c, i), 1, i, 3, x_new, y_new)
                        nb1 = np.hstack((nb1, nb3))
                        nb2 = np.hstack((nb2, nb4))
                        pyplot.plot(np.hstack((x, x_new)), na1, 'r--', label="dint_a_2")
                        pyplot.plot(np.hstack((x, x_new)), na2, 'r--', label="dint_b_2")
                        pyplot.plot(np.hstack((x, x_new)), nb1, 'm--', label="dint_a_1")
                        pyplot.plot(np.hstack((x, x_new)), nb2, 'm--', label="dint_b_1")

                    # -------------------------------------проверки-----------------------------------------------------
                    self.text_check.append("y = " + l)
                    print "y", np.array(func.func_a(x, c, i))
                    e = y - np.array(func.func_a(x, c, i))
                    ch_a, st_a, ch_b, st_b, ch_c, st_c, ch_d, st_d = check.print_check(e)
                    self.text_check.append("check 3" + ": " + str(ch_a) + " " + str(ch_b) + " " + str(ch_c) + " " + str(ch_d))
                    self.text_check.append(st_a)
                    self.text_check.append(st_b)
                    self.text_check.append(st_c)
                    self.text_check.append(st_d)
                    self.text_check.append("")
                    self.text_check.append("R ** 2: " + str(r2))
                    self.text_check.append("F: " + str(f))
                    self.text_check.append("Ft:" + str(ft))

                    # ------------------------------------вывод---------------------------------------------------------
                    model.setData(model.index(0, j + k - 2 + 1), float(self.textbox_x_new.text()))
                    model.setData(model.index(1, j + k - 2 + 1), str(func.func_a_one(float(self.textbox_x_new.text()), c, i)))
                    model.setData(model.index(0, j + k - 1 + 1), "check")
                    model.setData(model.index(1, j + k - 1 + 1), str(ch_a) + " " + str(ch_b) + " " + str(ch_c) + " " + str(ch_d))
                    for t in range(0, len(x)):
                        model.setData(model.index(2, 0), "dint_a_1")
                        model.setData(model.index(2, t + 1), str(na1[t]))
                        model.setData(model.index(3, 0), "dint_b_1")
                        model.setData(model.index(3, t + 1), str(na2[t]))
                        model.setData(model.index(4, 0), "dint_a_2")
                        model.setData(model.index(4, t + 1), str(nb1[t]))
                        model.setData(model.index(5, 0), "dint_b_2")
                        model.setData(model.index(5, t + 1), str(nb2[t]))
                    model.setData(model.index(2, t + 2), str(na3))
                    model.setData(model.index(3, t + 2), str(na4))
                    model.setData(model.index(4, t + 2), str(nb3))
                    model.setData(model.index(5, t + 2), str(nb4))

                    # --------------------------------------------------------------------------------------------------
                    #подобрать доверительный интервал, с использованием y предельного
                    result = True
                    yy = []
                    yy = func.func_a(x, c, i)
                    for ii in range(0, len(yy) - 1):
                        if yy[ii + 1] < yy[ii]:
                            result = False
                    if not result:
                        print "убывающая функция"
                    a = 1
                    b = 16
                    y_pr = 14.5
                    while mth.fabs(nb3 - y_pr) >= 0.0001:
                        x_pr = (a + b) / 2.0
                        nb = nb3
                        nb1, nb2, nb3, nb4, r2, f, ft = dint.mn_dint(x, y, 0.05, func.func_a(x, c, i), 1, i, 3, x_pr, func.func_a_one(x_pr, c, i))
                        if result:
                            a, b = (a, x_pr) if nb3 > y_pr else (x_pr, b)
                        else:
                            a, b = (a, x_pr) if nb3 < y_pr else (x_pr, b)
                        if nb - nb3 == 0:
                            break
                    print "!!! пересечение с нижней линией доверительного интервала", nb3, "x_pr = ", x_pr, "a,b = ", a,b

                    a = 1
                    b = 16
                    y_pr = 14.5
                    while mth.fabs(nb4 - y_pr) >= 0.0001:
                        x_pr = (a + b) / 2.0
                        nb = nb4
                        nb1, nb2, nb3, nb4, r2, f, ft = dint.mn_dint(x, y, 0.05, func.func_a(x, c, i), 1, i, 3, x_pr, func.func_a_one(x_pr, c, i))
                        if result:
                            a, b = (a, x_pr) if nb4 > y_pr else (x_pr, b)
                        else:
                            a, b = (a, x_pr) if nb4 < y_pr else (x_pr, b)
                        if nb - nb4 == 0:
                            break
                    print "!!! пересечение с верхней линией доверительного интервала", nb4, "x_pr = ", x_pr, "a,b = ", a,b
                    a = 1
                    b = 16
                    y_pr = 14.5
                    x_pr = a

                    y_p = func.func_a_one(x_pr, c, i)
                    while mth.fabs(y_p - y_pr) >= 0.0001:
                        x_pr = (a + b) / 2.0
                        nb = y_p
                        y_p = func.func_a_one(x_pr, c, i)
                        if result:
                            a, b = (a, x_pr) if y_p > y_pr else (x_pr, b)
                        else:
                            a, b = (a, x_pr) if y_p < y_pr else (x_pr, b)
                        if nb - y_p == 0:
                            break
                    print "!!! пересечение с  линией тренда", y_p, "x_pr = ", x_pr, "a,b = ", a,b



            k += 1

            # -------------------------------------a * (x ** b)---------------------------------------------------------
            if self.checkbox_4.checkState() == 2:
                k += 1
                xx, yy, c = func.function_b(x, y)
                l = str(lgnd.legend_b(c))
                pyplot.plot(list(xx), yy, 'r', label="y = " + l)

                xxx = func.rg_log(x)
                yyy = func.rg_log(y)
                dy = []
                for t in range(0, len(xxx)):
                    dy.append(c[1] + xxx[t] * c[0])


                #n1, n2 = dint.dint([xxx], yyy, 0.05, dy)
                #pyplot.plot(x, mth.exp(1.0) ** n1, 'r.', label="dint_a_ind_1")
                #pyplot.plot(x, mth.exp(1.0) ** n2, 'r.', label="dint_b_ind_2")

                self.text_check.append("y = " + l)
                e = y - np.array(func.func_b(x, c))
                ch_a, st_a, ch_b, st_b, ch_c, st_c, ch_d, st_d = check.print_check(e)
                self.text_check.append("check 4" + ": " + str(ch_a) + " " + str(ch_b) + " " + str(ch_c) + " " + str(ch_d))
                self.text_check.append(st_a)
                self.text_check.append(st_b)
                self.text_check.append(st_c)
                self.text_check.append(st_d)
                self.text_check.append("")
                model.setData(model.index(0, j + k - 2), float(self.textbox_x_new.text()))
                model.setData(model.index(1, j + k - 2), str(func.func_b_one(float(self.textbox_x_new.text()), c)))
                model.setData(model.index(0, j + k - 1), "check")
                model.setData(model.index(1, j + k - 1), str(ch_a) + " " + str(ch_b) + " " + str(ch_c) + " " + str(ch_d))
                k += 1

            #------------------------------------------a * (e ** (b * x))-----------------------------------------------
            if self.checkbox_5.checkState() == 2:
                k += 1
                xx, yy, c = func.function_e(x, y)
                l = str(lgnd.legend_e(c))
                pyplot.plot(list(xx), yy, 'g', label="y = " + l)


                yyy = func.rg_log(y)
                dy = []
                for t in range(0, len(x)):
                    dy.append(c[1] + x[t] * c[0])
                #n1, n2 = dint.dint([x], yyy, 0.05, dy)
                #pyplot.plot(x, mth.exp(1.0) ** n1, 'g.', label="dint_a_ind_1")
                #pyplot.plot(x, mth.exp(1.0) ** n2, 'g.', label="dint_b_ind_2")


                # print "y = ", l
                self.text_check.append("y = " + l)
                e = y - np.array(func.func_e(x, c))
                ch_a, st_a, ch_b, st_b, ch_c, st_c, ch_d, st_d = check.print_check(e)
                self.text_check.append("check 5" + ": " + str(ch_a) + " " + str(ch_b) + " " + str(ch_c) + " " + str(ch_d))
                self.text_check.append(st_a)
                self.text_check.append(st_b)
                self.text_check.append(st_c)
                self.text_check.append(st_d)
                self.text_check.append("")
                model.setData(model.index(0, j + k - 2), float(self.textbox_x_new.text()))
                model.setData(model.index(1, j + k - 2), str(func.func_e_one(float(self.textbox_x_new.text()), c)))
                model.setData(model.index(0, j + k - 1), "check")
                model.setData(model.index(1, j + k - 1), str(ch_a) + " " + str(ch_b) + " " + str(ch_c) + " " + str(ch_d))
                k += 1
            pyplot.legend(loc=0, prop={'size': 8})
            pyplot.show()
        # --------------------------------------------------------------------------------------------------------------
        table.setModel(model)
        table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        table.show()

    def button_export_click(self):
        text = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
        self.textbox_file_exp.setText(str(text))
        rb = xlrd.open_workbook(self.textbox_file.text(), formatting_info=False)
        wb = xlwt.Workbook()
        ws = wb.add_sheet('new')

        for i in range(0, 6):
            self.table_res.selectRow(i)
            j = 0
            for index in self.table_res.selectedIndexes():
                ws.write(i, j, str(self.table_res.model().data(self.table_res.model().index(index.row(), index.column())).toString()))
                j += 1
            wb.save(str(text))


def main():
    app = QtGui.QApplication(sys.argv)
    w = main_window()
    w.show()
    w.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()