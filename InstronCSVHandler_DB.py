#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Yinsong Li 
Date: 2023.09.28
"""

from PyQt5.QtWidgets import (QWidget, QApplication, QFileDialog, QMessageBox)
from PyQt5.QtCore import pyqtSignal, QCoreApplication, Qt
import sys, os

from InstronCSVHandler_UI import Ui_InstronCSVHandler
import pandas as pd

class MainWindow(QWidget, Ui_InstronCSVHandler):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.fullpath = ''

        self.setupUi(self)

    def handleSelectCSVFile(self):
        filepath = QFileDialog.getOpenFileName(self, "Select a CSV file", "./", "CSV files(*.csv)")
        if filepath[0]:
            self.fullpath = filepath[0]
            self.LB_CurrentFile.setText(self.fullpath)

    def handleApply(self):
        csv_fullpath = self.fullpath
        (filedir, filename) = os.path.split(csv_fullpath)
        filename_abs = filename[0:filename.rfind('_')]
        num_tests = 0

        with open(csv_fullpath, 'r', encoding='ANSI') as fp:
            res_list = []
            while True:
                l = fp.readline()
                if l=='\n':
                    break
                else:
                    res_list.append(l)

            num_tests = int(res_list[-1].split(',')[0].strip('"')) # 试件数量
            test_marks_list = []
            for i in range(num_tests):
                test_marks_list.append(res_list[i+3].split(',')[1].strip('"')) # 试件标识

            df = pd.read_csv(fp, encoding="ANSI", header=None, index_col=False)

            specimen_start_idxs = []
            for i in range(num_tests):
                specimen_start_idxs.append(df[df[0]==i+1].index)
            for i in range(num_tests):
                idxa = specimen_start_idxs[i][0]
                idxb = specimen_start_idxs[i+1][0] if i<num_tests-1 else -1
                df.iloc[idxa:idxb, 1:].to_csv(
                    os.path.join(
                        filedir ,"{}{:0>2d}_{}.csv".format(
                            filename_abs ,i+1, test_marks_list[i]
                            )
                        ), header=0, index=0
                    )
        with open(csv_fullpath, 'r', encoding='ANSI') as fp2:
            info = pd.read_csv(fp2, skiprows=1, nrows=num_tests+1)
            info.to_csv(os.path.join(
                filedir, "{}00_TestInfo.csv".format(filename_abs)), index=0
            )
        
        QMessageBox.information(self, 'Complete', 'This CSV file has been splited.', QMessageBox.Ok)
        return

if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())