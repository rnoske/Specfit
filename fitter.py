# -*- coding: utf-8 -*-

#Fitting class!
import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
#from multiprocessing import Pool, Process
from lmfit import minimize, Parameters, Parameter, report_errors

class Fitter():
    """ Class for fitting data
    
    """
    
    def create_testdata(self):
        """ creates two gaussion functions as testdata
        
        Returns:
            np.array testdata
        
        """
        # Setting up test data
        def norm(x, mean, sd):
          norm = []
          for i in range(x.size):
              norm += [1.0/(sd*np.sqrt(2*np.pi))*np.exp(-(x[i] - mean)**2/(2*sd**2))]
          return np.array(norm)
        
        mean1, mean2 = 0, -2
        std1, std2 = 0.5, 1 
        
        x = np.linspace(-20, 20, 500)
        y_real = norm(x, mean1, std1) + norm(x, mean2, std2)
        return x, y_real
        
    def beispiel(self):
        """ Testbeispiel. Muss mit creat_testdata zusammen funktionieren!
        
        """
        def norm(x, mean, sd):
            norm = []
            for i in range(x.size):
                norm += [1.0/(sd*np.sqrt(2*np.pi))*np.exp(-(x[i] - mean)**2/(2*sd**2))]
            return np.array(norm)
        x, y_real = self.create_testdata()
        # Solving
        m, dm, sd1, sd2 = [5, 10, 1, 1]
        p = [m, dm, sd1, sd2] # Initial guesses for leastsq
        y_init = norm(x, m, sd1) + norm(x, m + dm, sd2) # For final comparison plot
        
        def res(p, y, x):
            m, dm, sd1, sd2 = p
            m1 = m
            m2 = m1 + dm
            y_fit = norm(x, m1, sd1) + norm(x, m2, sd2)
            err = y - y_fit
            return err
        
        plsq = leastsq(res, p, args = (y_real, x))        
        y_est = norm(x, plsq[0][0], plsq[0][2]) + norm(x, plsq[0][1], plsq[0][3])
        
        plt.plot(x, y_real, label='Real Data')
        plt.plot(x, y_init, 'r.', label='Starting Guess')
        plt.plot(x, y_est, 'g.', label='Fitted')
        plt.legend()
        plt.show()
        
        return plsq
        
    def gauss_norm(self, x, mean, sd):
        norm = []
        for i in range(x.size):
            norm += [1.0/(sd*np.sqrt(2*np.pi))*np.exp(-(x[i] - mean)**2/(2*sd**2))]
        return np.array(norm)
        
    def multi_gauss_fit_norm(self, x, y, n, m, s, plotflag = False):
        """ Fit n Gauss functions do data
        
        x (np.array): numpy array with x-axis
        y (np.array): numpy array with data
        n (int): number of Gauss functions to fit
        m (np.array): m[0]= initial mean value for first gauss
                    m[n]= differenzes to mean before    
        s (np.array): array of standard deviations
        plotflag (bool): if true an graph is plottet
        
        Example:
            n = 2
            m = [5., 5.]
            s = [1, 1]
            x, y_real = myfitter.create_testdata()
            multiGaussFit(x, y_real, n, m, s)
            
        """    
        # Initial fit
        y_init = self.gauss_norm(x, m[0], s[0])
        for i in xrange(1, n):
            y_init += self.gauss_norm(x, m[i]+m[i-1], s[i])
                
        def res(p, y, x):
            #initialisation of paramters
            m = []
            s = []
            for i in xrange(n):
                m.append(p[i])
                s.append(p[i+n])
            absm = []
            for i in xrange(n):
                if i == 0:
                    absm.append(m[i])
                elif i >= 1:
                    absm.append(m[i] + m[i-1])
            #generation fit function
            y_fit = self.gauss_norm(x, absm[0], s[0])
            for i in xrange(1,n):
                y_fit += self.gauss_norm(x, absm[i], s[i]) 
            err = y - y_fit
            return err
        #parameter magic, notwendig um paramter für leastsq zu bekommen
        p = []
        for item in m:
            p.append(item)
        for item in s:
            p.append(item)
        p = np.array(p)
        param, success = leastsq(res, p, args = (y, x))
        #print param
        
        
        
        #plotting
        if plotflag == True:
            #result function
            y_est = self.gauss_norm(x, param[0], param[n])
            for i in xrange(1, n):
                y_est += self.gauss_norm(x, param[i+0], param[i+2])
            
            plt.plot(x, y, label='Real Data')
            plt.plot(x, y_init, 'r.', label='Starting Guess')
            plt.plot(x, y_est, 'g.', label='Fitted')
            plt.legend()
            plt.show()
        
        return param
        
        
    def gauss(self, x, b, a, m, s):
        """
        gauss = []
        for i in range(x.size):
            gauss.append(b+a*np.exp(-((x[i]-m)/s)**2))
        return np.array(gauss)
        """
        return b+a*np.exp(-((x-m)/s)**2)
        
      
    def multi_gauss_fit(self, x, y, n, b, a, m, s, plotflag = True):
        """ Fit n Gauss functions do data
        
        x (np.array): numpy array with x-axis
        y (np.array): numpy array with data
        n (int): number of Gauss functions to fit
        b (int): offset of gauss functions
        a (np.array): preexponential factors
        m (np.array): m[0]= initial mean value for first gauss
                    m[n]= initial guess for mean value, diffrent from norm 
                    gauss fit
        s (np.array): array of standard deviations
        plotflag (bool): if true an graph is plottet
        filepath (str): complete filepath to save the figure if plotflag = True
        
        Example:
            n = 2
            m = [5., 5.]
            s = [1, 1]
            x, y_real = myfitter.create_testdata()
            multiGaussFit(x, y_real, n, m, s)
            
        Returns:
            param, data (numpy.ndarrays)
            
        """    
        """
        _a = np.arange(n)
        _m = np.arange(n)
        _s = np.arange(n)
        """
        def res(p, y, x):
            #initialisation of paramters
            b = p[0]
            a = []
            m = []
            s = []
            for i in xrange(n):
                a.append(p[i+1]) #+1 because 0 is offset b
                m.append(p[i+1+n]) #3 because 3 params
                s.append(p[i+1+(2*n)])
                #print a, m, s
              
            #generation fit function
            y_fit = self.gauss(x, b, a[0], m[0], s[0])
            for i in xrange(1,n):
                y_fit += self.gauss(x, b, a[i], m[i], s[i])
            err = y - y_fit
            return err
        #parameter magic, notwendig um paramter für leastsq zu bekommen
        p = []
        p.append(b)
        for item in a:
            p.append(item)
        for item in m:
            p.append(item)
        for item in s:
            p.append(item)
        p = np.array(p)
        param, success = leastsq(res, p, args = (y, x))
        #print param
        
        #result function
        b = param[0]
        a = []
        m = []
        s = []
        for i in xrange(n):
            a.append(param[i+1]) #+1 because 0 is offset b
            m.append(param[i+1+n]) #3 because 3 params
            s.append(param[i+1+(2*n)])
            #print a, m, s     
        
        #generation fit function
        y_est = self.gauss(x, b, a[0], m[0], s[0])
        for i in xrange(1,n):
            y_est += self.gauss(x, b, a[i], m[i], s[i])
        #plotting
        if plotflag == True:
            plt.clf()
            plt.plot(x, y, label='Real Data')
            plt.plot(x, y_est, 'g.', label='Fitted')
            plt.legend()
            plt.show()
            #plt.show()
        
        _tup = (x, y, y_est)
        data = np.column_stack(_tup)
        return b, a, m, s, data
        
    def polynom(self, x, y, n, p, plotflag = True):
        """ Fit a polynom to the given data
        
        x (np.array): numpy array with x-axis
        y (np.array): numpy array with data
        n (int): order of polynom to fit
        p (np.array): numpy array of initial parameter values (len(p) = n)
        plotflag (bool): if true an graph is plottet
        filepath (str): complete filepath to save the figure if plotflag = True
        
        """
        def res(p, y ,x):
            model = p[0]
            for i in xrange(1, n):
                model += p[i] * np.power(x, i)
            err = y - model
            return err
            
        param, success = leastsq(res, p, args = (y, x))
        #print param
        
        
        #generation fit function
        y_est = param[0]
        for i in xrange(1,n):
            y_est += param[i] * np.power(x, i)
        #plotting
        if plotflag == True:
            plt.clf()
            plt.plot(x, y, label='Real Data')
            plt.plot(x, y_est, 'g.', label='Fitted')
            plt.legend()
            plt.show()
            #plt.show()
            
        _tup = (x, y, y_est)
        data = np.column_stack(_tup)
        return param, data

    def multi_gauss_fit_bounds(self, x, y, n, params, plotflag = True):
        """ Multiple gauss fit using possibilities of lmfit
          
        x (numpy.ndarray): x-axis
        y (numpy.ndarray): y-axis
        n (int): number of gauss functions to fit
        params (lmfit.Parameters): paramter object (value must not be min or 
                                    max bound)
        
        """
        def res(params, x, y):
            b = params['b_0'].value
            a = []
            m = []
            s = []
            for i in xrange(n):
                a.append(params['a_'+str(i)].value)
                m.append(params['m_'+str(i)].value)
                s.append(params['s_'+str(i)].value)      
            #print b, a, m, s
            #generation fit function
            model = self.gauss(x, b, a[0], m[0], s[0])
            for i in xrange(1,n):
                model += self.gauss(x, b, a[i], m[i], s[i])
            err = y - model
            
            return err
            
        #do fit
        result = minimize(res, params, args=(x, y))
        # calculate final result
        b = params['b_0'].value
        a = []
        m = []
        s = []
        for i in xrange(n):
            a.append(params['a_'+str(i)].value)
            m.append(params['m_'+str(i)].value)
            s.append(params['s_'+str(i)].value)      
        #print b, a, m, s
        #generation fit function
        fit = self.gauss(x, b, a[0], m[0], s[0])
        for i in xrange(1,n):
            fit += self.gauss(x, b, a[i], m[i], s[i])
        """
        print result.nfev
        print result.success
        print result.message
        print result.ier
        print result.lmdif_message
        print result.nvarys
        print result.ndata
        print result.nfree
        print result.params
        
        # write error report
        report_errors(params)
        """
        if plotflag == True:
            # try to plot results
            try:
                import pylab
                pylab.plot(x, y, 'k+')
                pylab.plot(x, fit, 'r')
                pylab.show()
            except:
                pass
        
        return result.params, fit
        
if __name__ == "__main__":
    myfitter = Fitter()
    
    # create a set of Parameters
    params = Parameters()
    params.add('b_0', value= 0.01, min=0)
    params.add('a_0', value = 1)
    params.add('a_1', value = 1)
    params.add('m_0', value = -5)
    params.add('m_1', value = 2)
    params.add('s_0', value = 4)
    params.add('s_1', value = 4)
    
    #fit params
    n = 2
    x, y = myfitter.create_testdata()
    params, residual = myfitter.multi_gauss_fit_bounds(x, y, n, params)
    print params

    """
    n = 2
    b = 0.
    a = [1., 1.]
    m = [-5., 1.]
    s = [1., 1.]
    x, y = myfitter.create_testdata()
    b, a, m, s, data = myfitter.multi_gauss_fit(x, y, n, b, a, m, s, plotflag = True)
    print b, a, m, s
    """
    

    
    