# -*- coding: utf-8 -*-

#Guihandler!
#standard library imports
import logging
import sys

#related third party imports
from PyQt4 import QtGui, QtCore

#local application/library specific imports
import Fittergui
import rnio
import proghandler
import Plotterui

class specfit(QtGui.QMainWindow):
    """ Guihandler for all of the specfit program
    
    """
    def __init__(self, parent = None):
        """ Initialisation methond
        
        """        
        QtGui.QWidget.__init__(self, parent)

        self.ui = Fittergui.Ui_Specfit()
        self.ui.setupUi(self)
        self.show()
        self.ph = proghandler.ProgHandler()
        self.myIo = rnio.RnIo()
        
        #just for testing purposes
        filepath = 'C:/Python/SpyDev/Specfit/testdata/spectrum1.prf'
        arr = self.myIo.read_prf_nparray(filepath)
        self.ph.set_spectrum(arr)
        #only for testing!!!
        filepath = 'C:/Python/SpyDev/Specfit/testdata/Peaklist.dat'
        arr = self.myIo.read_originPeaklist_nparray(filepath)
        self.ph.set_peaklist(arr)
        
    """
    def openWidgetWindow(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        wui = Fitterwidget.Ui_FitterWidget()
        wui.setupUi(self)
        self.show()
    """
        
    def open_spectrum(self):
        """ Open a spectrum file
        
        """
        #get file dialog
        _msg = 'Select a spectrum file to open'
        _prepath = 'D:/Raimund Buero/Python/SpyDev/Specfit/testdata/'
        _Imagetypes = 'Spectrums (*.prf *.txt)'
        filepath = QtGui.QFileDialog.getOpenFileName(self, 
                                                      _msg,
                                                      _prepath, 
                                                      _Imagetypes)
        filepath = str(filepath)
        #print filepath
        
        #finde dateiendung
        _end = filepath.split('.')
        _end = _end.pop()
        
        #entsprechend der endung öffne passend
        if _end == 'prf':
            arr = self.myIo.read_prf_nparray(filepath)
        elif _end == 'txt':
            arr = self.myIo.read_suaptxt_nparray(filepath)
        
        #print arr
        #set sepectrum for program
        self.ph.set_spectrum(arr)
        
        #show file on gui
        self.ui.Spectrum_label.setText(filepath)
    
    def open_peaklist(self):
        """ Open a peaklist file
        
        """
        #get file dialog
        _msg = 'Select a peaklist to open'
        _prepath = 'D:/Raimund Buero/Python/SpyDev/Specfit/testdata/'
        _Imagetypes = 'Peaklist (*.dat *.txt)'
        filepath = QtGui.QFileDialog.getOpenFileName(self, 
                                                      _msg,
                                                      _prepath, 
                                                      _Imagetypes)
        filepath = str(filepath)
        #print filepath
        
        #open peaklist
        arr = self.myIo.read_originPeaklist_nparray(filepath)
        
        #set peaklist for program
        self.ph.set_peaklist(arr)
    
    def fit_peaks(self):
        """ Fit peaks to the spectrum
        
        """
        self.sdict = {}
        _tmp = self.ui.Start_nm_doubleSpinBox.value()
        self.sdict['Start_nm'] = _tmp
        _tmp = self.ui.End_nm_doubleSpinBox.value()
        self.sdict['End_nm'] = _tmp
        
        self.ph.calibrate_wavelength(self.sdict)
        
        
        
        
        
        
    def plot_things(self):
        """ Responds to open Plotter call from Plotter.ui
        
        """
        QtGui.QWidget.__init__(self, parent = None)
        self.pui = Plotterui.Ui_Plotterui()
        self.pui.setupUi(self)
        self.show()
        
    def myPlot(self):
        # checked = 2 unchecked = 0
        if self.pui.check_rawData.checkState() == 2:
            self.plot_spectrum()
        elif self.pui.check_peaklist.checkState() == 2:
            self.plot_peaklist()
        else:
            self.test_plotter()
            
    def updatePlot(self, x, y):
        """ Updates plot window
        
        x (arr): x values
        y (arr): y values
        
        """
        self.pui.MPLArea.qmc.updatePlot(x,y)
        
    def test_plotter(self):
        """ my testplotter func"""
        _x = [0,1]
        _y = [0,0]
        self.updatePlot(_x,_y)
        
    def plot_spectrum(self):
        """ Plot spectrum file
        
        """
        try:
            _arr = self.ph.spectrum
        except NameError:
            logging.error('Spectrum file nicht gesetzt')
        
        _x = _arr[:,0]
        _y = _arr[:,1]
        self.updatePlot(_x,_y)
        
    def plot_peaklist(self):
        """ Plot peaklist
        
        """
        try:
            _arr = self.ph.peaklist
        except NameError:
            logging.error('Spectrum file nicht gesetzt')
        
        _x = _arr[:,0]
        _y = _arr[:,1]
        self.updatePlot(_x,_y)

if __name__ == "__main__":
    app2 = QtGui.QApplication(sys.argv)
    myspecfit = specfit()
    sys.exit(app2.exec_())
