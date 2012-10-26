# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Plotterui.ui'
#
# Created: Fri Oct 26 10:17:29 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Plotterui(object):
    def setupUi(self, Plotterui):
        Plotterui.setObjectName(_fromUtf8("Plotterui"))
        Plotterui.setEnabled(True)
        Plotterui.resize(803, 586)
        self.MPLArea = MplWidget(Plotterui)
        self.MPLArea.setGeometry(QtCore.QRect(150, 10, 651, 561))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MPLArea.sizePolicy().hasHeightForWidth())
        self.MPLArea.setSizePolicy(sizePolicy)
        self.MPLArea.setFocusPolicy(QtCore.Qt.NoFocus)
        self.MPLArea.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.MPLArea.setObjectName(_fromUtf8("MPLArea"))
        self.PLOT_Button = QtGui.QPushButton(Plotterui)
        self.PLOT_Button.setGeometry(QtCore.QRect(20, 180, 75, 23))
        self.PLOT_Button.setObjectName(_fromUtf8("PLOT_Button"))
        self.check_rawData = QtGui.QCheckBox(Plotterui)
        self.check_rawData.setEnabled(True)
        self.check_rawData.setGeometry(QtCore.QRect(11, 101, 71, 17))
        self.check_rawData.setMouseTracking(False)
        self.check_rawData.setChecked(True)
        self.check_rawData.setAutoExclusive(True)
        self.check_rawData.setObjectName(_fromUtf8("check_rawData"))
        self.check_spectrumlog = QtGui.QCheckBox(Plotterui)
        self.check_spectrumlog.setEnabled(True)
        self.check_spectrumlog.setGeometry(QtCore.QRect(10, 130, 91, 17))
        self.check_spectrumlog.setMouseTracking(False)
        self.check_spectrumlog.setChecked(False)
        self.check_spectrumlog.setAutoExclusive(True)
        self.check_spectrumlog.setObjectName(_fromUtf8("check_spectrumlog"))

        self.retranslateUi(Plotterui)
        QtCore.QObject.connect(self.PLOT_Button, QtCore.SIGNAL(_fromUtf8("clicked()")), Plotterui.myPlot)
        QtCore.QMetaObject.connectSlotsByName(Plotterui)

    def retranslateUi(self, Plotterui):
        Plotterui.setWindowTitle(QtGui.QApplication.translate("Plotterui", "Plotter", None, QtGui.QApplication.UnicodeUTF8))
        self.PLOT_Button.setText(QtGui.QApplication.translate("Plotterui", "PLOT!", None, QtGui.QApplication.UnicodeUTF8))
        self.check_rawData.setText(QtGui.QApplication.translate("Plotterui", "Spectrum", None, QtGui.QApplication.UnicodeUTF8))
        self.check_spectrumlog.setText(QtGui.QApplication.translate("Plotterui", "Spectrum log", None, QtGui.QApplication.UnicodeUTF8))

from mplwidget import MplWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Plotterui = QtGui.QWidget()
    ui = Ui_Plotterui()
    ui.setupUi(Plotterui)
    Plotterui.show()
    sys.exit(app.exec_())

