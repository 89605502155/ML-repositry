from sklearn.base import BaseEstimator
import numpy as np
class firstSellectionVariables (BaseEstimator):
    def __init__(self, var_excitation=0.01, var_emission=0.2):
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
        excitation_var=sorted(excitation, reverse=True)
        sortedExcitation=dict()
        k=0
        while(True):
            if (excitation_var[k] < self.var_excitation):
                break
            sortedExcitation[excitation_var[k]]=excitation[excitation_var[k]]
            k+=1
        wave1=list()
        wave1=sorted(sortedExcitation.values())
        x_meta=x[:,:,wave1]
        new_excitation=waveExcitation[wave1]
        
        emission=dict()
        for i in range(0, x.shape[1]):
            emission[max(self.dispersion[i,wave1])]=i
        emission_var=sorted(emission, reverse=True)
        #print(emission_var)
        wave2=list()
        k=0
        sortedEmission=dict()
        while(True):
            if (emission_var[k] < self.var_emission):
                break
            sortedEmission[emission_var[k]]=emission[emission_var[k]]
            k+=1
        wave2=sorted(sortedEmission.values())
        x_new_=x_meta[:,wave2,:]
        new_emission=waveEmission[wave2]
        self.x_new_=x_new_
        self.new_emission=new_emission
        self.new_excitation=new_excitation
        return self
