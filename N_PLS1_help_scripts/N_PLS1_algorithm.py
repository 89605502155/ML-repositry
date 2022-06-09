import numpy as np
from sklearn.base import BaseEstimator
from sklearn.base import RegressorMixin
from sklearn.metrics import mean_squared_error
from numba import jit

class Tri_PLS1_grid(RegressorMixin,BaseEstimator):
    def  __init__(self, n_components=2,a=3):
        self.n_components = n_components
        self.a=a
        
    @jit        
    def fit(self, xx, yy):
        """Fits the model to the data (X, y)

        Parameters
        ----------
        X : ndarray
        y : 1D-array of shape (n_samples, )
            labels associated with each sample"""
        x=xx.copy()
        y=yy.copy()        
        Tt=np.zeros([x.shape[0],self.n_components])
        mass=np.zeros([y.shape[0]])
        y_copy=yy.copy()
        """"
        При различных способах разрезания исходных данных, массивы w_k и w_i имеют похожие значения и именно их я планирую 
        использовать для функции predict данного класса. """
        w_k_mass=np.zeros([self.n_components,x.shape[1],1])
        w_i_mass=np.zeros([self.n_components,x.shape[2],1])
        bf_array=[]
        
        mmas=np.zeros([x.shape[0],x.shape[1],x.shape[2]])
        z_pz=np.eye(x.shape[1])
        z_z=z_pz[:,:x.shape[2]]
        
        for f in range(0,self.n_components):
            z=np.zeros([x.shape[1],x.shape[2]])
            x_product=np.zeros([x.shape[0],x.shape[1],x.shape[2]])
            
            for i in range(0,x.shape[0]):
                x_product[i,:,:]=y[i]*x[i,:,:]
            z=x_product.sum(axis=0)
            
            # Блок регуляризации z
            #z_po=LA.pinv(z)
            #z=np.dot((np.dot(z,z_po)+(self.a*np.eye(z.shape[0]))),z)
            
            
            Wk, S, WI = np.linalg.svd(z)
            #plt.imshow(Wk, aspect='auto')
            #plt.imshow(WI, aspect='auto')
            #plt.imshow(S, aspect='auto')
            #plt.show();
            w_k=np.array(Wk[:,0]).reshape(x.shape[1],1)
            w_i=np.array(WI[0,:]).reshape(x.shape[2],1)
            w_k_mass[f,:,:]=w_k
            w_i_mass[f,:,:]=w_i
            
            for h in range(0,x.shape[0]):
                 Tt[h,f]=np.dot(np.dot(w_i.transpose(),x[h,:,:].transpose()),w_k)
            T=np.array(Tt[:,0:f+1]).reshape(x.shape[0],f+1)        
            #print(T)
            #print((np.dot(np.linalg.inv(np.dot(T,T.transpose())+(self.a*np.eye(x.shape[0]))),T)).shape)
            
            
            
            bf=np.dot((np.dot(np.linalg.inv(np.dot(T,T.transpose())-(((self.a/(f+1)))*np.eye(x.shape[0]))),T)).transpose(),
                          y.reshape([x.shape[0],1]))
            #print(bf.shape) (self.a/(f+1)
            #print((np.dot(T,bf)).shape).reshape(x.shape[1],x.shape[2])
            bf_array+=[bf]
            #plt.plot(bf)
            #plt.show();
            
            WW=np.kron(w_k,w_i).reshape(x.shape[1],x.shape[2])
            for g in range(0,x.shape[0]):
                mmas[g,:,:]=Tt[g,f]*WW
            #mmas=np.kron(Tt[:,f],WW).reshape(x.shape[0],x.shape[1],x.shape[2])
            x=np.array(x-(mmas)) 
            #plt.imshow(mmas[5,:,:], aspect='auto')
            #plt.show();
            #for g in range(0,x.shape[0]):
            
            #plt.imshow(np.kron(w_k,w_i).reshape(x.shape[1],x.shape[2]), aspect='auto')
            #plt.show();
            
            Y_m=(np.dot(T,bf)).reshape(x.shape[0])
            #plt.plot(Y_m, color="red")
            #plt.plot(y_copy, color="blue")
            
            y=(y-(np.dot(T,bf)).reshape(x.shape[0]))
            
            #plt.plot(y, color="green")
    
            #print(y)
            mass+=(np.dot(T,bf)).reshape(x.shape[0]).reshape(x.shape[0])
            #plt.plot(mass, color="yellow")
            #plt.show();
            bf=0
            
        self.bf_array=bf_array
        #self.train_error=mean_squared_error(mass,y_copy)
        self.train_error=(np.square(mass - y_copy)).mean(axis=None)
        self.w_k=w_k_mass
        self.w_i=w_i_mass
        
        return self
    
    #def fit_transform(self,x.copy()):
        """"
        Даже для 20 компонент функция fit работает быстро, а вот функция predict нет.
        Кроме того, некоторые вычислительные операции требуют колоссальных 
        объёмов памяти, поэтому, сначала нужно провести анализ нагрузок и 
        трансформацию данных в форму поменьше.
        
        Отбор длин волн я решил делать при помощи поглощающих жадных алгоритмов поиска. SBS алгоритм.
        """
    @jit
    def predict(self, xx):
        x=xx.copy()
        Tt=np.zeros([x.shape[0],self.n_components])
        #y=np.random.normal(loc=0,scale=10,size=x.shape[0])
        y=np.zeros([x.shape[0]])
        mmas=np.zeros([x.shape[0],x.shape[1],x.shape[2]])
        for f in range(0,self.n_components):
            w_k=self.w_k[f,:,:]
            w_i=self.w_i[f,:,:]
            for h in range(0,x.shape[0]):
                 Tt[h,f]=np.dot(np.dot(w_i.transpose(),x[h,:,:].transpose()),w_k)
            
            T=np.array(Tt[:,0:f+1]).reshape(x.shape[0],f+1)
            #bf=np.dot((np.dot(np.linalg.inv(np.dot(T,T.transpose())),T)).transpose(),
            #              y.reshape([x.shape[0],1]))
            WW=np.kron(w_k,w_i).reshape(x.shape[1],x.shape[2])
            #plt.imshow(WW, aspect='auto')
            #plt.show();
            for g in range(0,x.shape[0]):
                #mmas[g,:,:]=Tt[g,f]*WW
                mmas[g,:,:]=Tt[g,f]*WW
            x=np.array(x-(mmas))
            #print(len(np.kron(Tt[:,f],np.kron(w_i,w_k).reshape(x.shape[1],x.shape[2]))))
            #print()
            #plt.plot(self.bf_array[f])
            #plt.show();
            
            #bf=np.dot((np.dot(np.linalg.inv(np.dot(T,T.transpose())-(self.a*np.eye(x.shape[0]))),T)).transpose(),
             #             y.reshape([x.shape[0],1]))
            
            y=(y+(np.dot(T,self.bf_array[f])).reshape(x.shape[0]))
            #y=(y+(np.dot(T,bf)).reshape(x.shape[0]))
        
        return y
            
            
    
