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
                 rounding_long=2, ms=30, lw=3):
        self.marker_color=marker_color
        self.line_color=line_color
        self.form_marker=form_marker
        self.form_line=form_line
        self.language_axis=language_axis
        self.save_fig=save_fig
        self.rounding_long=rounding_long
        self.ms=ms
        self.lw=lw

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

    def optimal_num(self,a):
        #This function calculate the optimal number of marks on the grid
        
    def axs_marker(self,fr):
        numm=int((fr[1]-fr[0])*math.pow(10,self.rounding_long))
        self.optimal_num(numm)
        a=-1
        for i in range(2,11):
            if num%i==0:
                a=i
        if a==-1:
            
        print(np.linspace(fr[0], fr[1], num = numm+1))
        
    def main(self, tru_dat_inp, pred_dat_inp):
        self.round_ex() #It is a function which make string example of
        #rounding for decimal
        tru_dat=self.go_to_numpy(tru_dat_inp)
        pred_dat=self.go_to_numpy(pred_dat_inp)
        a1=self.set_data_fig(tru_dat) #make a frame for grid of axis
        a2=self.set_data_fig(pred_dat_inp) #make a frame for grid of axis

        self.axs_marker(a1)
        self.axs_marker(a2)

a=PR_plts()
t=a.main([1.009,1.1,2,2.111],[1.001,2,2])
