# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Fittergui.ui'
#
# Created: Thu Oct 11 21:19:30 2012
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Fittergui(object):
    def setupUi(self, Fittergui):
        Fittergui.setObjectName(_fromUtf8("Fittergui"))
        Fittergui.resize(800, 600)
        self.centralwidget = QtGui.QWidget(Fittergui)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(130, 200, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 120, 311, 31))
        self.label.setObjectName(_fromUtf8("label"))
        Fittergui.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Fittergui)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuMenu = QtGui.QMenu(self.menubar)
        self.menuMenu.setObjectName(_fromUtf8("menuMenu"))
        Fittergui.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Fittergui)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Fittergui.setStatusBar(self.statusbar)
        self.actionLoad = QtGui.QAction(Fittergui)
        self.actionLoad.setObjectName(_fromUtf8("actionLoad"))
        self.menuMenu.addAction(self.actionLoad)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(Fittergui)
        QtCore.QObject.connect(self.actionLoad, QtCore.SIGNAL(_fromUtf8("triggered()")), self.label.clear)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Fittergui.raysfunc)
        QtCore.QMetaObject.connectSlotsByName(Fittergui)

    def retranslateUi(self, Fittergui):
        Fittergui.setWindowTitle(QtGui.QApplication.translate("Fittergui", "Fittergui", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Fittergui", "click me", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Fittergui", "Mein text der gecleared werden soll", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMenu.setTitle(QtGui.QApplication.translate("Fittergui", "Menu", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad.setText(QtGui.QApplication.translate("Fittergui", "Load", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Fittergui = QtGui.QMainWindow()
    ui = Ui_Fittergui()
    ui.setupUi(Fittergui)
    Fittergui.show()
    sys.exit(app.exec_())

