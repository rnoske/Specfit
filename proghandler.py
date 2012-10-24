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
        
        
    def calibrate_wavelength(self, sdict):
        """ Calibrate the wavelength of the spectrum
        
        sdict: dictionary of some values
        
        """
        self.sdict = sdict
        
        
        _g_px, _g_int, _g_wl = self.guess_inital_fitparams()
        n = len(_g_px) #number of gauss functions to fit
        y = self.spectrum[:, 1]
        x = self.spectrum[:, 0]
        b = 0. #background
        #a = _g_int * (max(y)/max(_g_int)) #intensities are bullshit!
        
        m = _g_px
        s = [1]*n
        
        
        m = [96, 111, 233, 712, 847, 856]
        a = []
        for i in xrange(len(m)):
            a.append(y[m[i]])
        param = self.fitter.multi_gauss_fit(x, y, n, b, a, m, s, plotflag = True)
        #print param
        
        
        
    def guess_inital_fitparams(self):
        """ Guess the inital position fit parameters
        
        """
        _peaklist = self.calc_peaklist()
        #_n_gauss = len(_peaklist) #number of gauss functions to fit
        
        start_nm = self.sdict['Start_nm']
        end_nm = self.sdict['End_nm']
         #guess of delta wavelength
        _delta_w = (end_nm - start_nm)/len(self.spectrum)
        
        #peaklist wavelength into pixel
        for entry in _peaklist:
            wl = entry[0]
            px = (wl - start_nm)/_delta_w #guessed pixel position
            entry.append(px)
        #print _peaklist
        _peaklist = np.array(_peaklist)
        _g_px = _peaklist[:, 2]
        _g_wl = _peaklist[:, 0]
        _g_int = _peaklist[:, 1]
        #print _g_px, _g_int, _g_wl
        return (_g_px, _g_int, _g_wl)
        
        
    def calc_peaklist(self):
        """ Calculate the appropiate peaklist
        
        """
        start_nm = self.sdict['Start_nm']
        end_nm = self.sdict['End_nm']
        _pl = [] #temporary peak list, holding all peaks for spectrum fit
        for entry in self.peaklist:
            wavelength = entry[0]
            intensity = entry[1]
            if wavelength >= start_nm and wavelength <= end_nm and intensity > 100:
                _pl.append([wavelength, intensity])
        return _pl
        