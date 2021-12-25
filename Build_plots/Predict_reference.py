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
                 number_y_mark=10,
                 font_family='Times New Roman',
                 name_plot='N-pls1 for Humic',
                 end_name_for_file='picture_1'):
        self.marker_color=marker_color
        self.line_color=line_color
        self.form_marker=form_marker
        self.form_line=form_line
        self.language_axis=language_axis
        self.save_fig=save_fig
        self.rounding_long=rounding_long
        self.ms=ms
        self.lw=lw
        self.font_family=font_family
        self.number_x_mark=number_x_mark
        self.number_y_mark=number_y_mark
        self.name_plot=name_plot
        self.end_name_for_file=end_name_for_file

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
        #print(numm,fr)
        a=-1
        for i in range(4,ax+1):
            if numm%i==0:
                a=i
        if a==-1:
            return (self.er_num(fr,ax,numm))
        else:
            return (np.linspace(fr[0], fr[1], num = a+1))
        
    def to_decimal(self):
        list_x=list()
        for i in self.x_mark_num:
            list_x.append(Decimal(str(i)).
                                  quantize(Decimal(self.
                                                   float_decimal_ex)))
        self.x_mark_decim=list_x
        del(list_x)
        list_y=list()
        for i in self.y_mark_num:
            list_y.append(Decimal(str(i)).
                                  quantize(Decimal(self.
                                                   float_decimal_ex)))
        self.y_mark_decim=list_y
        del(list_y)

    def lang_axis(self):
        if self.language_axis=='ru':
            return ["Предсказанные значения","Истинные значения",
                    "График введено-найдено"]
        if self.language_axis=='en':
            return ["Predict","Reference",
                    "Predict-reference"]
            
    def plot_fig(self, t, p):
        mpl.rc('font',family=self.font_family)
        fig, axs = plt.subplots(figsize=(12, 7))
        axs.plot(t,p,".",color=self.marker_color,ms=self.ms)
        axs.plot(t,t,color=self.line_color,lw=self.lw)
        axs.set_xticks(self.x_mark_num)
        axs.set_yticks(self.y_mark_num)
        axs.grid(color="black",linewidth=0.7)
        axs.tick_params(which='major', length=10, width=2)
        axs.get_xaxis().set_tick_params(direction='in')
        axs.get_yaxis().set_tick_params(direction='in')
        loc_name_axs=self.lang_axis()
        axs.set_ylabel(loc_name_axs[0] , fontsize=25,labelpad=8)
        axs.set_xlabel(loc_name_axs[1],  fontsize=25,labelpad=15)
        axs.set_title(loc_name_axs[2]+' '+self.name_plot,
                      fontsize=28,loc="center" ,
                      pad=15)
        axs.set_xticklabels(self.x_mark_decim, fontsize=20)
        axs.set_yticklabels(self.y_mark_decim, fontsize=20)
        axs.tick_params(which='major', length=10, width=2)
        if self.save_fig==True:
            plt.savefig(self.end_name_for_file+'.png',
                        format='png', dpi=300)
            plt.savefig(self.end_name_for_file+".svg",
                        format="svg")
        plt.show();

    def main(self, tru_dat_inp, pred_dat_inp):
        self.round_ex() #It is a function which make string example of
        #rounding for decimal
        tru_dat=self.go_to_numpy(tru_dat_inp)
        pred_dat=self.go_to_numpy(pred_dat_inp)
        a1=self.set_data_fig(tru_dat) #make a frame for grid of axis
        a2=self.set_data_fig(pred_dat_inp) #make a frame for grid of axis

        self.x_mark_num=self.axs_marker(a1,self.number_x_mark)
        a3=[min(a1[0],a2[0]),max(a1[1],a2[1])]
        self.y_mark_num=self.axs_marker(a3,self.number_y_mark)
        #predict data will be on the y-axsis
        #print(self.x_mark_num)
        #print(self.y_mark_num)
        self.to_decimal()
        #print(self.x_mark_decim)
        #print(self.y_mark_decim)
        #print(tru_dat)
        #print(pred_dat)
        self.plot_fig(tru_dat,pred_dat)

#a=PR_plts(save_fig=True, language_axis='en')
#t=a.main([1.009,1.1,2,2.111],[2,2,2,6.06])
