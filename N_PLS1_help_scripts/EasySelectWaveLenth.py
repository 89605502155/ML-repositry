#from sklearn.base import BaseEstimator
import numpy as np
"""
This class calculates the variances of cells. For example,
we can take 240 waves of excitation and 500 waves of emission
and all 35 samples and make from this a vector. This vector
has a length of 35. And then, we calculate the variance in this
vector. The meaning of variance we put on the matrix of
variance. Similarly, we chose other meanings. Then we sorted
our matrix on the axis excitation wavelength. We delete columns
from the matrix with a small meaning of variance. Then we sort
this matrix on the axis of emission wavelength. Then we remove from
our data wavelength with the small meaning of variance. residuals of
data we put on the regression class.
"""

class firstSellectionVariables():
    def __init__(self, var_excitation=3, var_emission=7):
        self.var_excitation=var_excitation
        self.var_emission=var_emission
        
    def variance(self, x):
        dispersion=np.zeros([x.shape[1],x.shape[2]])
        for i in range(0, x.shape[1]):
            for j in range(0, x.shape[2]):
                dispersion[i,j]=(1/x.shape[0])*(sum((x[:,i,j]-x[:,i,j].mean())**2))
        self.dispersion=dispersion
        
    def selectionWave(self,x,waveExcitation, waveEmission):
        excitation=dict()
        for i in range(0,x.shape[2]):
            excitation[max(self.dispersion[:,i])]=i
        #print(excitation)
        excitation_var=sorted(excitation, reverse=True)
        #print(excitation_var)
        
        sortedExcitation=dict()
        
        for i in range(self.var_excitation):
            sortedExcitation[excitation_var[i]]=excitation[excitation_var[i]]
        #print(sortedExcitation)
        wave1=list()
        wave1=sorted(sortedExcitation.values())
        x_meta=x[:,:,wave1]
        new_excitation=waveExcitation[wave1]
        
        emission=dict()
        for i in range(0, x.shape[1]):
            emission[max(self.dispersion[i,wave1])]=i
        #print(emission)
        emission_var=sorted(emission, reverse=True)
        #print(emission_var)
        #print(emission_var)
        wave2=list()

        sortedEmission=dict()

        
        for i in range(self.var_emission):
            sortedEmission[emission_var[i]]=emission[emission_var[i]]

        wave2=sorted(sortedEmission.values())
        x_new_=x_meta[:,wave2,:]
        
        new_emission=waveEmission[wave2]
        self.x_new_=x_new_
        self.new_emission=new_emission
        self.new_excitation=new_excitation
        return self
        
        
