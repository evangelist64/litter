#coding=utf8
import pandas as pd
import matplotlib as mpl
mpl.use('TkAgg')
import os,sys
import matplotlib.pyplot as plt
import numpy as np
import time
import tushare as ts
import struct
import datetime

#df = ts.get_money_supply()
#df.to_csv('xx.csv')
df = pd.read_csv('xx.csv')
df = df.sort(columns='month')
print df
df.plot(x='month',y='m2',style='o')
plt.show()
