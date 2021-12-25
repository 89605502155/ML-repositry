# This script will be build a predict-reference figures
# This class need a y_train, predictors, names on figure

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
from decimal import Decimal

class PR_plts():
    def __init__(self, marker_color="red",
                 line_color="blue", form_marker=".",
                 form_line="-", language_axis="ru",
                 save_fig=False,
                 rounding_long=2, ms=30, lw=3,
                 number_x_mark=10,
                 number_y_mark=10):
        self.marker_color=marker_color
        self.line_color=line_color
        self.form_marker=form_marker
        self.form_line=form_line
        self.language_axis=language_axis
        self.save_fig=save_fig
        self.rounding_long=rounding_long
        self.ms=ms
        self.lw=lw
        self.number_x_mark=number_x_mark
        self.number_y_mark=number_y_mark

    def go_to_numpy(self,a):
        if isinstance(a, pd.Series):
            return a.to_numpy()
        if isinstance(a, pd.DataFrame):
            return a.to_numpy()
        if isinstance(a, list):
            return np.array(a)
        if isinstance(a, np.ndarray):
            return a
        else:
            print("Переведите данные в numpy.ndarray, np.Series, list")

    def round_ex(self):
        #The decimal module need example string for rounding sone float
        a=9/math.pow(10,self.rounding_long)
        self.float_decimal_ex=str(a)
    
    def set_data_fig(self, tr):
        max_tr=np.max(tr)
        tr1=round(max_tr,self.rounding_long)
        if tr1<max_tr:
            tr1+=math.pow(0.1,self.rounding_long)
        del(max_tr)
        n1=round(tr1,self.rounding_long)
        del(tr1)
        
        min_tr=np.min(tr)
        tr1=round(min_tr,self.rounding_long)
        if tr1>min_tr:
            tr1-=math.pow(0.1,self.rounding_long)
        n2=round(tr1,self.rounding_long)
        del(tr1)
        return [n2,n1]

    def er_num(self,fr,ax,n):
        #This function calculate the optimal number of marks on the grid
        n1=n
        a=-1
        #print(n1)
        while True:
            for i in range(5,ax+1):
                if n1%i==0:
                    a=i
                    break
            if a!=-1:
                break
            n1+=1
        #print(n1)
        delta=n1-n
        lev=delta//2
        prav=delta-lev
        fr_0_loc=round(fr[0]-(lev*math.pow(0.1,self.rounding_long)),
                       self.rounding_long)
        fr_1_loc=round(fr[1]+(prav*math.pow(0.1,self.rounding_long)),
                       self.rounding_long)
        #print(fr_0_loc,fr_1_loc,a)
        return np.linspace(fr_0_loc,
                           fr_1_loc, num = a+1)
        
        
    def axs_marker(self,fr,ax):
        #ax - max number of marks on the grid
        numm=round((fr[1]-fr[0])*math.pow(10,self.rounding_long))
        print(numm,fr)
        a=-1
        for i in range(4,ax+1):
            if numm%i==0:
                a=i
        if a==-1:
            print(self.er_num(fr,ax,numm))
        else:
            print(np.linspace(fr[0], fr[1], num = a+1))
            print(a)
        
        
    def main(self, tru_dat_inp, pred_dat_inp):
        self.round_ex() #It is a function which make string example of
        #rounding for decimal
        tru_dat=self.go_to_numpy(tru_dat_inp)
        pred_dat=self.go_to_numpy(pred_dat_inp)
        a1=self.set_data_fig(tru_dat) #make a frame for grid of axis
        a2=self.set_data_fig(pred_dat_inp) #make a frame for grid of axis

        self.axs_marker(a1,self.number_x_mark)
        self.axs_marker(a2,self.number_x_mark)

a=PR_plts()
t=a.main([1.009,1.1,2,2.111],[1,2.06])
