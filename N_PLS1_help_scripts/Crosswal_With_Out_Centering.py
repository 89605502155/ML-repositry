from sklearn.base import BaseEstimator
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

class crossval(BaseEstimator):
    """"Этот класс производит центрирование, а потом из центрированных
        данных переходит обратно"""
    def  __init__(self, testSize=0.1428, column_y=0):
        self.testSize = testSize
        self.column_y=column_y

    def crosswal(self,xx,yy):
        x=xx.copy()
        y=yy.copy()
        x_centrir=np.array(x)
        y_centrir=y.iloc[:,self.column_y].to_numpy()
        X_train, X_test, y_train, y_test = train_test_split(
                x_centrir, y_centrir, test_size=self.testSize 
                )
        self.X_train=X_train
        self.X_test=X_test
        self.y_train=y_train
        self.y_test=y_test
        return self
