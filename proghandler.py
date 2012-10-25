# -*- coding: utf-8 -*-

#Programm Handler!
#standard library imports


#related third party imports
import numpy as np

#local application/library specific imports
import rnio
import fitter


class ProgHandler():
    """ Program class for fitting a spectrum
    
    """
    def __init__(self):
        """ Initializes program
        
        """
        self.myIo = rnio.RnIo()
        self.fitter = fitter.Fitter()
        
    def set_spectrum(self, nparray):
        """ Sets a spectrum file on which work is done
        
        nparray: 2D numpy array with first column = index, 
                second = intensity
                
        """
        self.spectrum = nparray
        
    def set_peaklist(self, nparray):
        """ Sets a peaklist file
        
        nparray: 2D numpy array
        
        """
        self.peaklist = nparray
        
        
    def calibrate_wavelength(self):
        """ Calibrate the wavelength of the spectrum
        
        sdict: dictionary of some values
        
        """
        _pl = self.peaklist
        
        _gpx =[]
        _wl = []
        for i in xrange(len(_pl)):
            _gpx.append(_pl[i][2])
            _wl.append(_pl[i][0])
        
        n = len(_gpx) #number of gauss functions to fit
        y = self.spectrum[:, 1]
        x = self.spectrum[:, 0]
        b = 0. #background
        #a = _g_int * (max(y)/max(_g_int)) #intensities are bullshit!
        
        m = _gpx
        #print m
        s = [2]*n
        
        #only for testing!
        m = [96, 111, 233, 712, 847, 856]
        
        a = []
        for i in xrange(len(m)):
            a.append(y[m[i]])
        param = self.fitter.multi_gauss_fit(x, y, n, b, a, m, s, plotflag = False)
        b,a,m,s = param
        #print b, a, m, s
        n = 3
        p = [1] * n
        param = self.fitter.polynom(m, _wl, n, p, plotflag = False)
        #print param
        print str(param[0]) + ' + ' +str(param[1]) + '*x' + ' + ' + str(param[2])+'x^2'
        _newx = param[0]
        for i in xrange(1,n):
            _newx += param[i] * np.power(x, i)
        #print x, _newx
        _tofile = np.column_stack((x, _newx))
        #print _tofile
        filepath = 'D:/Raimund Buero/Python/SpyDev/Specfit/testdata/testaxis.txt'
        self.myIo.write_nparray_txt(filepath, _tofile)
        
        

        