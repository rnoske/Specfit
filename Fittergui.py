# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Fittergui.ui'
#
# Created: Thu Oct 25 14:19:19 2012
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
        self.FitPeaks_pushButton = QtGui.QPushButton(self.centralwidget)
        self.FitPeaks_pushButton.setGeometry(QtCore.QRect(40, 290, 75, 23))
        self.FitPeaks_pushButton.setObjectName(_fromUtf8("FitPeaks_pushButton"))
        self.Peaklist_Table = QtGui.QTableWidget(self.centralwidget)
        self.Peaklist_Table.setGeometry(QtCore.QRect(350, 30, 391, 521))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Peaklist_Table.sizePolicy().hasHeightForWidth())
        self.Peaklist_Table.setSizePolicy(sizePolicy)
        self.Peaklist_Table.setObjectName(_fromUtf8("Peaklist_Table"))
        self.Peaklist_Table.setColumnCount(4)
        self.Peaklist_Table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.Peaklist_Table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.Peaklist_Table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.Peaklist_Table.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.Peaklist_Table.setHorizontalHeaderItem(3, item)
        self.Peaklist_Table.horizontalHeader().setCascadingSectionResizes(False)
        self.Peaklist_Table.horizontalHeader().setHighlightSections(False)
        self.Peaklist_Table.horizontalHeader().setMinimumSectionSize(19)
        self.Peaklist_Table.horizontalHeader().setSortIndicatorShown(False)
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
        self.FitPeaks_pushButton.setText(QtGui.QApplication.translate("Specfit", "Fit Peaks", None, QtGui.QApplication.UnicodeUTF8))
        item = self.Peaklist_Table.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("Specfit", "Fit?", None, QtGui.QApplication.UnicodeUTF8))
        item = self.Peaklist_Table.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("Specfit", "Wellenlaenge", None, QtGui.QApplication.UnicodeUTF8))
        item = self.Peaklist_Table.horizontalHeaderItem(2)
        item.setText(QtGui.QApplication.translate("Specfit", "Intensitaet", None, QtGui.QApplication.UnicodeUTF8))
        item = self.Peaklist_Table.horizontalHeaderItem(3)
        item.setText(QtGui.QApplication.translate("Specfit", "Pixel guess", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Specfit = QtGui.QMainWindow()
    ui = Ui_Specfit()
    ui.setupUi(Specfit)
    Specfit.show()
    sys.exit(app.exec_())

