# -*- coding: utf-8 -*-

#Guihandler!

import Fittergui
import Fitterwidget
import sys
from PyQt4 import QtCore, QtGui

class specfit(QtGui.QMainWindow):
    """ Guihandler for all of the specfit program
    
    """
    def __init__(self, parent = None):
        """ Initialisation methond
        
        """

        
        QtGui.QWidget.__init__(self, parent)

        ui = Fittergui.Ui_Fittergui()
        ui.setupUi(self)
        self.show()
        
        #self.openWidgetWindow()
    
        
        
        

    def openWidgetWindow(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        wui = Fitterwidget.Ui_FitterWidget()
        wui.setupUi(self)
        self.show()
        
    def raysfunc(self):
        print 'blub'
        self.openWidgetWindow()
        
    def raysfunc2(self):
        print 'bla'

if __name__ == "__main__":
    app2 = QtGui.QApplication(sys.argv)
    myspecfit = specfit()
    #myspecfit.show()
    sys.exit(app2.exec_())
    
    #app = QtGui.QApplication(sys.argv)
    
       
    
    
    
    
    
    
    #sys.exit(app.exec_())
     