# -*- coding: utf-8 -*-
"""
Author: Liys15
Date: 2023-08-11
Description: This is a script file dealing CSV.
"""

import pandas as pd

filepath = "./环氧树脂拉伸_1.csv"

specimen_df_list = []

with open(filepath, 'r', encoding='ANSI') as fp:
    res_list = []
    while True:
        l = fp.readline()
        if l=='\n':
            break
        else:
            res_list.append(l)
    
    num_tests = int(res_list[-1].split(',')[0].strip('"'))
    test_marks_list = []
    for i in range(num_tests):
        test_marks_list.append(res_list[i+3].split(',')[1].strip('"'))

    df = pd.read_csv(fp, encoding="ANSI", header=None, index_col=False)

    specimen_start_idxs = []
    for i in range(num_tests):
        specimen_start_idxs.append(df[df[0]==i+1].index)
    for i in range(num_tests):
        idxa = specimen_start_idxs[i][0]
        idxb = specimen_start_idxs[i+1][0] if i<num_tests-1 else -1
        df.iloc[idxa:idxb, 1:].to_csv("./Test{:0>2d}_{}.csv".format(i+1, test_marks_list[i]), header=0, index=0)
    