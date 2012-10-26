# -*- coding: utf-8 -*-

#Guihandler!
#standard library imports
import logging
import sys

#related third party imports
from PyQt4 import QtGui, QtCore
import numpy as np

#local application/library specific imports
import Fittergui
import rnio
import proghandler
import Plotterui
import Config

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
        self.config = Config.Config()
        self.get_settings()
        
        
    """
    def openWidgetWindow(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        wui = Fitterwidget.Ui_FitterWidget()
        wui.setupUi(self)
        self.show()
    """
    
    def get_settings(self):
        """ Get settings from settings.ini file and sets them
        
        """
        self.sdict = self.config.getConfigOptions('Specfit')
        #set spectrum
        _flag = False
        try:
            _filepath = self.sdict['spectrum']
            arr = self.myIo.read_prf_nparray(_filepath)
            self.ph.set_spectrum(arr)
        except (KeyError, IOError, TypeError):
            self.open_spectrum()
            _flag = True
        #set peaklist
        try:
            _filepath = self.sdict['peaklist']
            arr = self.myIo.read_originPeaklist_nparray(_filepath)
            self.ph.set_peaklist(arr)
        except (KeyError, IOError, TypeError):
            self.open_peaklist()
            _flag = True
        #set workspace
        try:
            _filepath = self.sdict['workspace']
            self.ph.set_workspace(_filepath)
        except (KeyError, TypeError):
            self.set_workspace()
            _flag = True
        #write settings if neccessary
        if _flag == True:
            self.write_settings()
        
    def write_settings(self):
        """ writes settings dictionary to settings.ini file
        
        """
        self.config.writeConfigOptions('Specfit', self.sdict)
        

        
    def open_spectrum(self):
        """ Open a spectrum file
        
        """
        #get file dialog
        _msg = 'Select a spectrum file to open'
        try:
            _prepath = self.sdict['spectrum']
        except (KeyError):
            _prepath = 'C:/'
        _Imagetypes = 'Spectrums (*.prf *.txt)'
        filepath = QtGui.QFileDialog.getOpenFileName(self, 
                                                      _msg,
                                                      _prepath, 
                                                      _Imagetypes)
        filepath = str(filepath)
        self.sdict['spectrum'] = filepath
        self.write_settings()
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
        
    
    def open_peaklist(self):
        """ Open a peaklist file
        
        """
        #get file dialog
        _msg = 'Select a peaklist to open'
        try:
            _prepath = self.sdict['peaklist']
        except (KeyError):
            _prepath = 'C:/'
        _Imagetypes = 'Peaklist (*.dat *.txt)'
        filepath = QtGui.QFileDialog.getOpenFileName(self, 
                                                      _msg,
                                                      _prepath, 
                                                      _Imagetypes)
        filepath = str(filepath)
        self.sdict['peaklist'] = filepath
        self.write_settings()
        #print filepath
        
        #open peaklist
        arr = self.myIo.read_originPeaklist_nparray(filepath)
        
        #set peaklist for program
        self.ph.set_peaklist(arr)
        self.populate_peaklistTable()
        
    def set_workspace(self):
        """ Set the workspace folder
        
        """
        #get directory dialog
        _msg = 'Select a working directory'
        try:
            _prepath = self.sdict['workspace']
        except (KeyError):
            _prepath = 'C:/'
        filepath = QtGui.QFileDialog.getExistingDirectory(self, _msg, _prepath)
        filepath += '/'
        self.sdict['workspace'] = filepath
        self.ph.set_workspace(filepath)
        self.write_settings()
        
        
    def populate_peaklistTable(self):
        """ Populate the peaklist table with peaks
        
        """
        _pl = self.ph.peaklist
        _tw = self.ui.Peaklist_Table
        
        _tw.setRowCount(len(_pl))
        _tw.horizontalHeader().setStretchLastSection(False)
        for i in xrange(len(_pl)):
            #fit checkbox
            _cb = QtGui.QCheckBox()
            _cb.setCheckState(0)
            _tw.setCellWidget(i, 0, _cb)
            
            #Wavelength entry
            _val = float(_pl[i, 0]) #ädata to be displayed
            _val = QtCore.QVariant(_val) #convert to QVariant
            item = QtGui.QTableWidgetItem(0) #ka wofür die 0 ist
            item.setData(0, _val) #0=data #set Vairant data to tableitem
            _tw.setItem(i,1,item) #place item in table
            
            #Intensity entry
            _val = float(_pl[i, 1]) #ädata to be displayed
            _val = QtCore.QVariant(_val) #convert to QVariant
            item = QtGui.QTableWidgetItem(0) #ka wofür die 0 ist
            item.setData(0, _val) #0=data #set Vairant data to tableitem
            _tw.setItem(i,2,item) #place item in table
            
            
            #_tw.setCellWidget(i, 1, _wl)
            #_tw.setCellWidget(i, 2, _int)
            #_tmp = _tw.item(i, 1)
            #print _tmp
            #_tmp2 = _tmp.data(0)
            #print _tmp2
            #_tmp3 = _tmp2.toFloat()[0]
            #print _tmp3
        _tw.resizeColumnsToContents()
        
    def get_peaks_forfit(self):
        """ Get the peaks for fitting
        
        """
        _tw = self.ui.Peaklist_Table
        _n_entrys = _tw.rowCount()
        _pl = []
        for i in xrange(_n_entrys):
            if _tw.cellWidget(i, 0).checkState() == 2:
                _wl = _tw.item(i,1).data(0).toFloat()[0]
                _int = _tw.item(i,2).data(0).toFloat()[0]
                try:
                    _pxg = _tw.item(i,3).data(0).toFloat()[0]
                except AttributeError:
                    _pxg = 0.0
                _pl.append([_wl, _int, _pxg])
        return _pl
        
        
            
    def fit_peaks_manual(self):
        """ Fit peaks to the spectrum
        
        """
        self.ph.peaklist = self.get_peaks_forfit()
        """
        self.sdict = {}
        _tmp = self.ui.Start_nm_doubleSpinBox.value()
        self.sdict['Start_nm'] = _tmp
        _tmp = self.ui.End_nm_doubleSpinBox.value()
        self.sdict['End_nm'] = _tmp
        """
        self.ph.calibrate_wavelength()
        
    def fit_peaks_automatic(self):
        """ Fit peaks and detect peaks automatically
        
        """
        self.ph.peaklist = self.get_peaks_forfit()
        self.ph.calibrate_wavelength_auto()
        
        
        
        
        
        
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
        elif self.pui.check_spectrumlog.checkState() ==2:
            self.plot_spectrumlog()
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
        
    def plot_spectrumlog(self):
        """ Plot the spectrum with logarytmic y- axis
        
        """
        try:
            _arr = self.ph.spectrum
        except NameError:
            logging.error('Spectrum file nicht gesetzt')
        
        _x = _arr[:,0]
        _y = _arr[:,1]
        _y = np.log10(_y)
        self.updatePlot(_x,_y)
        
        
    def plot_peaklist(self):
        """ Plot peaklist
        
        """
        try:
            _arr = self.ph.peaklist
        except NameError:
            logging.error('Spectrum file nicht gesetzt')
        _arr  = np.array(_arr)
        print _arr
        print _arr.shape
        
        _x = _arr[:,0]
        _y = _arr[:,1]
        self.updatePlot(_x,_y)

if __name__ == "__main__":
    app2 = QtGui.QApplication(sys.argv)
    myspecfit = specfit()
    sys.exit(app2.exec_())
