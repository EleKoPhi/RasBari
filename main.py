#
#
# GUI and logical software for the RasBari
#
# Name: Philipp Mochti
#
# V1.0
#
#

from classes.class_GUI import Ui_GUI
from PyQt5 import QtCore, QtGui, QtWidgets

if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    GUI = QtWidgets.QMainWindow()
    ui = Ui_GUI()
    ui.setupUi(GUI)
    GUI.show()
    sys.exit(app.exec_())

