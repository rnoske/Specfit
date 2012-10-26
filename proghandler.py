# -*- coding: utf-8 -*-

#Programm Handler!
#standard library imports
import logging

#related third party imports
import numpy as np

#local application/library specific imports
import rnio
import fitter
import peakdetect
import Config


class ProgHandler():
    """ Program class for fitting a spectrum
    
    """
    def __init__(self):
        """ Initializes program
        
        """
        self.myIo = rnio.RnIo()
        self.fitter = fitter.Fitter()
        self.config = Config.Config()
        self.fdict = self.config.getConfigOptions('fit')
        
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
        
    def set_workspace(self, workspace):
        """ Set the workspace
        
        workspace (str): workspace filepath
        
        """
        self.workspace = workspace
        
        
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
        s = [float(self.fdict['inital_s'])]*n
        
        #only for testing!
        #m = [96, 111, 233, 712, 847, 856]
        
        a = []
        for i in xrange(len(m)):
            a.append(y[m[i]])
        _sp = self.workspace + 'manual_multi_gauss_fit.jpg'
        param = self.fitter.multi_gauss_fit(x, y, n, b, a, m, s, 
                                            plotflag = True, filepath = _sp)
        b,a,m,s = param
        #print b, a, m, s
        n = 3
        p = [1] * n
        _sp = self.workspace + 'manual_fit_polynom.jpg'
        param = self.fitter.polynom(m, _wl, n, p, plotflag = True, filepath = _sp)
        #print param
        print str(param[0]) + ' + ' +str(param[1]) + '*x' + ' + ' + str(param[2])+'x^2'
        _newx = param[0]
        for i in xrange(1,n):
            _newx += param[i] * np.power(x, i)
        #print x, _newx
        #save things
        _tofile = np.column_stack((x, _newx))
        filepath = self.workspace + 'manual_calibrated_wavelength.txt'
        self.myIo.write_nparray_txt(filepath, _tofile)
        
    def calibrate_wavelength_auto(self):
        """ Calibrate Wavelength with automatic peak detection
        
        """
        _pl = self.peaklist
        _peaks = self.detect_peaks(len(_pl))
        if len(_pl) != len(_peaks):
            logging.error('peaklist longer than detected peaks!')
        #fitting
        _peaks = np.array(_peaks)
        b = 0.
        m = _peaks[:,0]
        a = _peaks[:,1]
        s = [2] * len(_pl)
        n = len(_pl) #number of gauss functions to fit
        y = self.spectrum[:, 1]
        x = self.spectrum[:, 0]
        
        _sp = self.workspace + 'auto_multi_gauss_fit.jpg'
        param = self.fitter.multi_gauss_fit(x, y, n, b, a, m, s, 
                                            plotflag = True, filepath = _sp)
        b,a,m,s = param
        #print b, a, m, s
        n = 3
        p = [1] * n
        _wl = []
        for i in xrange(len(_pl)):
            _wl.append(_pl[i][0])
        _sp = self.workspace + 'auto_fit_polynom.jpg'
        param = self.fitter.polynom(m, _wl, n, p, plotflag = True, filepath = _sp)
        #print param
        print str(param[0]) + ' + ' +str(param[1]) + '*x' + ' + ' + str(param[2])+'x^2'
        _newx = param[0]
        for i in xrange(1,n):
            _newx += param[i] * np.power(x, i)
        #print x, _newx
        _tofile = np.column_stack((x, _newx))
        #print _tofile
        filepath = self.workspace + 'auto_calibrated_wavelength.txt'
        self.myIo.write_nparray_txt(filepath, _tofile)
        
        
        
        
    def detect_peaks(self, max_n_peaks = 6):
        """ Detect maxima in given data
        
        max_n_peaks (int): maximum number of peaks that shuld be returned
        
        """
        y = self.spectrum[:, 1]
        x = self.spectrum[:, 0]
        
        #look for maxima
        max_peaks, min_peaks = peakdetect.peakdetect(y, x, lookahead= 5, delta = 0)
        peaks = []
        threshold = 1000
        for peak in max_peaks:
            if peak[1] > threshold:
                peaks.append(peak)
        
        while len(peaks) > max_n_peaks:
            threshold += 1
            peaks = []
            for peak in max_peaks:
                if peak[1] > threshold:
                    peaks.append(peak)
            
            
        return peaks
        

        