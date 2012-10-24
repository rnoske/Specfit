# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Fittergui.ui'
#
# Created: Wed Oct 24 16:30:05 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Specfit(object):
    def setupUi(self, Specfit):
        Specfit.setObjectName(_fromUtf8("Specfit"))
        Specfit.resize(800, 600)
        self.centralwidget = QtGui.QWidget(Specfit)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.OpenSpectrum_pushButton = QtGui.QPushButton(self.centralwidget)
        self.OpenSpectrum_pushButton.setGeometry(QtCore.QRect(20, 40, 111, 21))
        self.OpenSpectrum_pushButton.setObjectName(_fromUtf8("OpenSpectrum_pushButton"))
        self.Spectrum_label = QtGui.QLabel(self.centralwidget)
        self.Spectrum_label.setGeometry(QtCore.QRect(170, 30, 551, 31))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Spectrum_label.sizePolicy().hasHeightForWidth())
        self.Spectrum_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        self.Spectrum_label.setFont(font)
        self.Spectrum_label.setObjectName(_fromUtf8("Spectrum_label"))
        self.OpenPeaklist_pushButton = QtGui.QPushButton(self.centralwidget)
        self.OpenPeaklist_pushButton.setGeometry(QtCore.QRect(20, 10, 111, 21))
        self.OpenPeaklist_pushButton.setObjectName(_fromUtf8("OpenPeaklist_pushButton"))
        self.Plotter_pushButton = QtGui.QPushButton(self.centralwidget)
        self.Plotter_pushButton.setGeometry(QtCore.QRect(30, 500, 111, 21))
        self.Plotter_pushButton.setObjectName(_fromUtf8("Plotter_pushButton"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 160, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 190, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 220, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.Start_nm_doubleSpinBox = QtGui.QDoubleSpinBox(self.centralwidget)
        self.Start_nm_doubleSpinBox.setGeometry(QtCore.QRect(110, 190, 91, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Start_nm_doubleSpinBox.setFont(font)
        self.Start_nm_doubleSpinBox.setDecimals(4)
        self.Start_nm_doubleSpinBox.setMaximum(10000.0)
        self.Start_nm_doubleSpinBox.setProperty("value", 380.0)
        self.Start_nm_doubleSpinBox.setObjectName(_fromUtf8("Start_nm_doubleSpinBox"))
        self.End_nm_doubleSpinBox = QtGui.QDoubleSpinBox(self.centralwidget)
        self.End_nm_doubleSpinBox.setGeometry(QtCore.QRect(110, 220, 91, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.End_nm_doubleSpinBox.setFont(font)
        self.End_nm_doubleSpinBox.setDecimals(4)
        self.End_nm_doubleSpinBox.setMaximum(10000.0)
        self.End_nm_doubleSpinBox.setProperty("value", 620.0)
        self.End_nm_doubleSpinBox.setObjectName(_fromUtf8("End_nm_doubleSpinBox"))
        self.FitPeaks_pushButton = QtGui.QPushButton(self.centralwidget)
        self.FitPeaks_pushButton.setGeometry(QtCore.QRect(40, 290, 75, 23))
        self.FitPeaks_pushButton.setObjectName(_fromUtf8("FitPeaks_pushButton"))
        Specfit.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Specfit)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        Specfit.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Specfit)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Specfit.setStatusBar(self.statusbar)

        self.retranslateUi(Specfit)
        QtCore.QObject.connect(self.OpenPeaklist_pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Specfit.open_peaklist)
        QtCore.QObject.connect(self.OpenSpectrum_pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Specfit.open_spectrum)
        QtCore.QObject.connect(self.Plotter_pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Specfit.plot_things)
        QtCore.QObject.connect(self.FitPeaks_pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Specfit.fit_peaks)
        QtCore.QMetaObject.connectSlotsByName(Specfit)

    def retranslateUi(self, Specfit):
        Specfit.setWindowTitle(QtGui.QApplication.translate("Specfit", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.OpenSpectrum_pushButton.setText(QtGui.QApplication.translate("Specfit", "Open Spectrum", None, QtGui.QApplication.UnicodeUTF8))
        self.Spectrum_label.setText(QtGui.QApplication.translate("Specfit", "Spektrum", None, QtGui.QApplication.UnicodeUTF8))
        self.OpenPeaklist_pushButton.setText(QtGui.QApplication.translate("Specfit", "Open Peaklist", None, QtGui.QApplication.UnicodeUTF8))
        self.Plotter_pushButton.setText(QtGui.QApplication.translate("Specfit", "Plot things", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Specfit", "Guess Spectrum boundaries:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Specfit", "Start nm", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Specfit", "End nm", None, QtGui.QApplication.UnicodeUTF8))
        self.FitPeaks_pushButton.setText(QtGui.QApplication.translate("Specfit", "Fit Peaks", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Specfit = QtGui.QMainWindow()
    ui = Ui_Specfit()
    ui.setupUi(Specfit)
    Specfit.show()
    sys.exit(app.exec_())

