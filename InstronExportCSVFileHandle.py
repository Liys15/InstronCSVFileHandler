# -*- coding: utf-8 -*-
"""
Author: Liys15
Date: 2023-08-11
Description: This is a script file dealing CSV.
"""

import pandas as pd
import os

cwd = os.getcwd()
subfolder = 'testdata'
filedir = os.path.join(cwd, subfolder)
filename_inp = '环氧树脂拉伸_1.csv'
file_inp = os.path.join(filedir, filename_inp)

filename_abs = filename_inp[0:filename_inp.rfind('_')]

num_tests = 0

with open(file_inp, 'r', encoding='ANSI') as fp:
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
        df.iloc[idxa:idxb, 1:].to_csv(os.path.join(filedir ,"{}{:0>2d}_{}.csv".format(filename_abs ,i+1, test_marks_list[i])), header=0, index=0)

with open(file_inp, 'r', encoding='ANSI') as fp2:
    info = pd.read_csv(fp2, skiprows=1, nrows=num_tests+1)
    info.to_csv(os.path.join(filedir ,"{}00_TestInfo.csv".format(filename_abs)), index=0)
