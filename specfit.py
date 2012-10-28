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
            self.populate_peaklistTable()
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
            _val = float(_pl[i, 0]) #data to be displayed
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
        
    def add_peak(self):
        """ Add an peak to the peaklist table
        
        """
        _tw = self.ui.Peaklist_Table
        _cRows = _tw.rowCount() #current number of rows
        _tw.setRowCount(_cRows + 1) # add row
        #populate new row
        #checkbox
        _cb = QtGui.QCheckBox()
        _cb.setCheckState(0)
        _tw.setCellWidget(_cRows, 0, _cb)
        #Wavelength entry
        _val = self.ui.addWavelength_doubleSpinBox.value() #data to be displayed
        _val = QtCore.QVariant(_val) #convert to QVariant
        item = QtGui.QTableWidgetItem(0) #ka wofür die 0 ist
        item.setData(0, _val) #0=data #set Vairant data to tableitem
        _tw.setItem(_cRows,1,item) #place item in table
        #Intensity entry
        _val = 0.0 #ädata to be displayed
        _val = QtCore.QVariant(_val) #convert to QVariant
        item = QtGui.QTableWidgetItem(0) #ka wofür die 0 ist
        item.setData(0, _val) #0=data #set Vairant data to tableitem
        _tw.setItem(_cRows,2,item) #place item in table
        
        #resize columns
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
        #set peaklist to perform fit on
        self.ph.peaklist = self.get_peaks_forfit()
        #start the wavelength calibration
        self.ph.calibrate_wavelength(peakguess = 0)
        
    def fit_peaks_automatic(self):
        """ Fit peaks and detect peaks automatically
        
        """
        #set peaklist to perform fit on
        self.ph.peaklist = self.get_peaks_forfit()
        #start the wavelength calibration
        self.ph.calibrate_wavelength(peakguess = 1)
       
    def plot_things(self):
        """ Responds to open Plotter call from Plotter.ui
        
        """
        QtGui.QWidget.__init__(self, parent = None)
        self.pui = Plotterui.Ui_Plotterui()
        self.pui.setupUi(self)
        self.show()
        
        #call myPlot to display something
        self.myPlot()
        
    def myPlot(self):
        """ Responds to event from Plot_button from Plotter.ui
        
        """
        #add possible data to plot
        _pD = self.ph.data
        #shortcut to comboBox
        _cB = self.pui.Plot_comboBox
        
        _seen = []
        for i in range(_cB.count()):
            _cB_c = _cB.itemData(i, 0).toString()
            _cB_c = str(_cB_c) #convert pyqt string to normal string
            if _cB_c not in _seen:
                _seen.append(_cB_c)

        for key in _pD.keys():
            if key not in _seen:
                _val = QtCore.QVariant(key) #convert to QVariant
                #_cB.setItemData(i, _val, 0)
                _cB.addItem(key, _val)
        
        #current item index
        _cB_index = _cB.currentIndex() 
        #get Variant Object as pyqt string object
        _cB_c = _cB.itemData(_cB_index, 0).toString()
        _cB_c = str(_cB_c) #convert pyqt string to normal string
        
        data = _pD[_cB_c]
        if data.shape[1] == 2:
            _x = data[:, 0]
            _y = data[:, 1]
            self.pui.MPLArea.qmc.updatePlot(_x,_y)
        elif data.shape[1] == 3:
            _x = data[:, 0]
            _y = data[:, 1]
            _y2 = data[:, 2]
            self.pui.MPLArea.qmc.updatePlot_2y(_x,_y, _y2)
            
    
if __name__ == "__main__":
    app2 = QtGui.QApplication(sys.argv)
    myspecfit = specfit()
    sys.exit(app2.exec_())
