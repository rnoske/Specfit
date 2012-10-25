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
        filepath = 'D:/Raimund Buero/Python/SpyDev/Specfit/testdata/spectrum1.prf'
        arr = self.myIo.read_prf_nparray(filepath)
        self.ph.set_spectrum(arr)
        #only for testing!!!
        filepath = 'D:/Raimund Buero/Python/SpyDev/Specfit/testdata/Peaklist.dat'
        arr = self.myIo.read_originPeaklist_nparray(filepath)
        self.ph.set_peaklist(arr)
        
        #resize column width
        self.ui.Peaklist_Table.resizeColumnsToContents()
        
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
        self.populate_peaklistTable()
        
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
            _tmp = _tw.item(i, 1)
            #print _tmp
            _tmp2 = _tmp.data(0)
            #print _tmp2
            _tmp3 = _tmp2.toFloat()[0]
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
        
        
            
    def fit_peaks(self):
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
