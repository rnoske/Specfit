# -*- coding: utf-8 -*-

#Programm Handler!
#standard library imports
import logging

#related third party imports
import numpy as np
from lmfit import Parameters, Parameter

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
        self.data = {}
        
    def set_spectrum(self, nparray):
        """ Sets a spectrum file on which work is done
        
        nparray: 2D numpy array with first column = index, 
                second = intensity
                
        """
        #self.spectrum = nparray
        self.data['spectrum'] = nparray
        #add spectrum with logarithmic scale
        _arr = nparray
        _x = _arr[:,0]
        _y = _arr[:,1]
        _y = np.log10(_y)
        _spectrum_logy = np.column_stack((_x,_y))
        self.data['spectrum_logy'] = _spectrum_logy
        
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
        
    
    def calibrate_wavelength(self, peakguess = 1):
        """ Calibrate the wavelength of the spectrum
        
        peakguess (int): 0 = manual, 1 = automatic
        
        """
        _pl = self.peaklist
        _spectrum = self.data['spectrum']
        y = _spectrum[:, 1]
        x = _spectrum[:, 0]
        
        if peakguess == 0:
            _peaks = []
            for i in xrange(len(_pl)):
                _peaks_px = _pl[i][2]
                _peaks_int = y[_peaks_px]
                _peaks.append([_peaks_px, _peaks_int])
        elif peakguess ==1:
            _peaks = self.detect_peaks(len(_pl))
            if len(_pl) != len(_peaks):
                logging.error('peaklist longer than detected peaks!')
        _peaks = np.array(_peaks)
                
        # set fit parameters:
        n = len(_peaks)
        b = 0.
        m = _peaks[:,0]
        a = _peaks[:,1]
        s = [float(self.fdict['inital_s'])]*n
        #fit:
        b, a, m, s, data = self.fitter.multi_gauss_fit(x, y, n, b, a, m, s,
                                                       plotflag = False)
        #save results
        _x = data[:,0]
        _y = np.log10(data[:,1])
        _y2 = np.log10(data[:,2])
        data_log = np.column_stack((_x, _y, _y2))
        if peakguess == 0:
            self.data['manual_gauss_fit'] = data
            filepath = self.workspace + 'manual_multi_gauss_fit.txt'
            self.myIo.write_nparray_txt(filepath, data)
            self.data['manual_gauss_fit_log'] = data_log
        elif peakguess == 1:
            self.data['auto_gauss_fit'] = data
            filepath = self.workspace + 'auto_multi_gauss_fit.txt'
            self.myIo.write_nparray_txt(filepath, data)
            self.data['auto_gauss_fit_log'] = data_log
            
        #set fit parameters for polynom fit
        n = 3 #polynom order + 1 (for constant)
        p = [1] * n
        _wl = []
        for i in xrange(len(_pl)):
            _wl.append(_pl[i][0])
        #fit:
        param, data = self.fitter.polynom(m, _wl, n, p, plotflag = True)
        #save results:
        if peakguess == 0:
            filepath = self.workspace + 'manual_polynom_fit.txt'
            self.myIo.write_nparray_txt(filepath, data)
        elif peakguess == 1:
            filepath = self.workspace + 'auto_polynom_fit.txt'
            self.myIo.write_nparray_txt(filepath, data)
        #print linear equation:
        print str(param[0]) + ' + ' +str(param[1]) + '*x' + ' + ' + str(param[2])+'x^2'
        #calculate new wavelength axis:
        _newx = param[0]
        for i in xrange(1,n):
            _newx += param[i] * np.power(x, i)
        #save wavelength axis
        if peakguess == 0:
            _tofile = np.column_stack((x, _newx))
            filepath = self.workspace + 'manual_calibrated_wavelength.txt'
            self.myIo.write_nparray_txt(filepath, _tofile)
        elif peakguess == 1:
            _tofile = np.column_stack((x, _newx))
            filepath = self.workspace + 'auto_calibrated_wavelength.txt'
            self.myIo.write_nparray_txt(filepath, _tofile)
            
    def calibrate_wavelength_bounds(self, peakguess=1):
        """ Calibrate the wavelength of the spectrum
        
        peakguess (int): 0 = manual, 1 = automatic
        
        """
        _pl = self.peaklist
        _spectrum = self.data['spectrum']
        y = _spectrum[:, 1]
        x = _spectrum[:, 0]
        
        if peakguess == 0:
            _peaks = []
            for i in xrange(len(_pl)):
                _peaks_px = _pl[i][2]
                _peaks_int = y[_peaks_px]
                _peaks.append([_peaks_px, _peaks_int])
        elif peakguess ==1:
            _peaks = self.detect_peaks(len(_pl))
            if len(_pl) != len(_peaks):
                logging.error('peaklist longer than detected peaks!')
        _peaks = np.array(_peaks)
                
        # set fit parameters:
        n = len(_peaks)
        params = Parameters()
        #background
        params.add('b_0')
        params['b_0'].value = float(self.fdict['b_0_value'])
        _vary =(self.fdict['b_0_vary'])
        if _vary == 'True':
            params['b_0'].vary = True
        else:
            params['b_0'].vary = False
        # m, a, s
        m = _peaks[:,0]
        a = _peaks[:,1]
        s = [float(self.fdict['inital_s'])]*n
        for i in xrange(n):
            params.add('m_'+str(i))
            params['m_'+str(i)].value = m[i]
            params['m_'+str(i)].min = m[i] - float(self.fdict['m_pm'])
            params['m_'+str(i)].max = m[i] + float(self.fdict['m_pm'])
            params.add('a_'+str(i))
            params['a_'+str(i)].value = a[i]
            params['a_'+str(i)].min = float(self.fdict['a_min'])
            params.add('s_'+str(i))
            params['s_'+str(i)].value= s[i]
            params['s_'+str(i)].min = s[i] - float(self.fdict['s_pm'])
            params['s_'+str(i)].max = s[i] + float(self.fdict['s_pm'])
        #print params
        #fit
        params, fit = self.fitter.multi_gauss_fit_bounds(x, y, n, params,
                                                              plotflag = False)
        #print params
        #save results
        data = np.column_stack((x, y, fit))
        data_log = np.column_stack((x, np.log10(y), np.log10(fit)))
        _header = [['Pixel', 'Original Data', 'fitted Data']]
        if peakguess == 0:   
            self.data['manual_gauss_fit'] = data
            filepath = self.workspace + 'manual_multi_gauss_fit.txt'
            self.myIo.write_nparray_txt(filepath, data, _header)
            self.data['manual_gauss_fit_log'] = data_log
        elif peakguess == 1:
            self.data['auto_gauss_fit'] = data
            filepath = self.workspace + 'auto_multi_gauss_fit.txt'
            self.myIo.write_nparray_txt(filepath, data, _header)
            self.data['auto_gauss_fit_log'] = data_log
            
        #set fit parameters for polynom fit
        n = 3 #polynom order + 1 (for constant)
        p = [1] * n
        _wl = []
        for i in xrange(len(_pl)):
            _wl.append(_pl[i][0])
        pos = []
        for i in xrange(len(_pl)):
            pos.append(params['m_'+str(i)].value)
        #fit:
        param, data = self.fitter.polynom(pos, _wl, n, p, plotflag = False)
        #save results:
        if peakguess == 0:
            filepath = self.workspace + 'manual_polynom_fit.txt'
            self.myIo.write_nparray_txt(filepath, data)
        elif peakguess == 1:
            filepath = self.workspace + 'auto_polynom_fit.txt'
            self.myIo.write_nparray_txt(filepath, data)
        #print linear equation:
        print str(param[0]) + ' + ' +str(param[1]) + '*x' + ' + ' + str(param[2])+'x^2'
        #calculate new wavelength axis:
        _newx = param[0]
        for i in xrange(1,n):
            _newx += param[i] * np.power(x, i)
        #save wavelength axis
        _tofile = np.column_stack((x, _newx))
        _header = [['Pixel', 'Wavelength']]
        if peakguess == 0:
            filepath = self.workspace + 'manual_calibrated_wavelength.txt'
            self.myIo.write_nparray_txt(filepath, _tofile, _header)
        elif peakguess == 1:
            filepath = self.workspace + 'auto_calibrated_wavelength.txt'
            self.myIo.write_nparray_txt(filepath, _tofile, _header)

        
    def detect_peaks(self, max_n_peaks = 6):
        """ Detect maxima in given data
        
        max_n_peaks (int): maximum number of peaks that shuld be returned
        
        """
        _spectrum = self.data['spectrum']
        y = _spectrum[:, 1]
        x = _spectrum[:, 0]
        
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
        

        