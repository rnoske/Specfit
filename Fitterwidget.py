# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Fitterwidget.ui'
#
# Created: Thu Oct 25 19:06:33 2012
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FitterWidget(object):
    def setupUi(self, FitterWidget):
        FitterWidget.setObjectName(_fromUtf8("FitterWidget"))
        FitterWidget.resize(800, 600)
        self.centralwidget = QtGui.QWidget(FitterWidget)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 140, 241, 51))
        self.label.setObjectName(_fromUtf8("label"))
        FitterWidget.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(FitterWidget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuMenu = QtGui.QMenu(self.menubar)
        self.menuMenu.setObjectName(_fromUtf8("menuMenu"))
        FitterWidget.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(FitterWidget)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        FitterWidget.setStatusBar(self.statusbar)
        self.actionLoad = QtGui.QAction(FitterWidget)
        self.actionLoad.setObjectName(_fromUtf8("actionLoad"))
        self.menuMenu.addAction(self.actionLoad)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(FitterWidget)
        QtCore.QObject.connect(self.actionLoad, QtCore.SIGNAL(_fromUtf8("triggered()")), FitterWidget.raysfunc2)
        QtCore.QMetaObject.connectSlotsByName(FitterWidget)

    def retranslateUi(self, FitterWidget):
        FitterWidget.setWindowTitle(QtGui.QApplication.translate("FitterWidget", "Fitterwidget", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FitterWidget", "langer text", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMenu.setTitle(QtGui.QApplication.translate("FitterWidget", "Menu", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad.setText(QtGui.QApplication.translate("FitterWidget", "Load", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FitterWidget = QtGui.QMainWindow()
    ui = Ui_FitterWidget()
    ui.setupUi(FitterWidget)
    FitterWidget.show()
    sys.exit(app.exec_())

