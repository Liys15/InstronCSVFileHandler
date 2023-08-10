# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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
    
    num_specimens = int(res_list[-1].split(',')[0].strip('"'))

    df = pd.read_csv(fp, encoding="ANSI", header=None, index_col=False)

    specimen_start_idxs = []
    for i in range(num_specimens):
        specimen_start_idxs.append(df[df[0]==i+1].index)
    for i in range(num_specimens):
        idxa = specimen_start_idxs[i][0]
        idxb = specimen_start_idxs[i+1][0] if i<num_specimens-1 else -1
        df.iloc[idxa:idxb, 1:].to_csv("./specimen{:0>2d}.csv".format(i+1), header=0, index=0)
    