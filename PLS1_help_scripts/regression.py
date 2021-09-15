from sklearn.base import BaseEstimator
from sklearn.base import RegressorMixin
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np
from PLS1_help_scripts.variable_wave import firstSellectionVariables

class new_PLS1_regression(RegressorMixin,BaseEstimator):
    def __init__(self, var_excitation=0.01, var_emission=0.2, n_components=2):
        self.var_excitation=var_excitation
        self.var_emission=var_emission
        self.n_components=n_components
        
    def regression(self, x, y, x_excit, x_emiss, type_matter, test_size_):
        """"
        type_matter is a number column of y data. 
        Introducing
        Firstly, I make a selection of variables. I use the variance of our X-data.
        Data with small variance of data is not useful. 
        Secondly, I make a selection of number of components in PLS1 regression. 
        I find not only the number of components. I find the best variance, because
        I dont know how many useful cell in the spectra of fluorescent.
        """
        model1=firstSellectionVariables(var_excitation=self.var_excitation,
                                       var_emission=self.var_emission)
        model1.variance(x.copy())
        result1=model1.selectionWave(x.copy(),x_excit.copy(),x_emiss.copy())
        x_new=result1.x_new_
        new_excit_wave=result1.new_excitation
        new_emiss_wave=result1.new_emission
        
        x_new.shape = (x_new.shape[0], x_new.shape[1] * x_new.shape[2])
        X_train, X_test, y_train, y_test = train_test_split(
            x_new, y.iloc[:,type_matter], test_size=test_size_)
        pls1 = PLSRegression()
        parametrsNames={
            'copy': [True], 
            'max_iter': [10000], 
            'n_components': range(1,self.n_components+1), 
            'scale': [False], 
            'tol': [1e-06]
        }
        
        gridCought=GridSearchCV(pls1, parametrsNames, cv=5,return_train_score=True)
        gridCought.fit(X_train,y_train)
        self.r2_p=gridCought.score(X_test, y_test)
        self.r2_cv=gridCought.cv_results_[ "mean_test_score" ]
        self.r2_c=gridCought.cv_results_[ "mean_train_score" ]
        self.best=gridCought.best_params_
        self.predictors=gridCought.predict(X_test)
        self.y_test=y_test
        
        return self
