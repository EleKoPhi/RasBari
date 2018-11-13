#
#
# GUI and logical software for the RasBari
#
# Name: Philipp Mochti
#
# V4.0
#
#

from PyQt5 import QtWidgets

from StyleFunctions import ApplyStyleSheets
from TxTMethoden import getFlag
from classes.class_GUI import UiGui

if __name__ == "__main__":

    import sys

    app = QtWidgets.QApplication(sys.argv)
    ApplyStyleSheets(app)
    StackedWidget = QtWidgets.QStackedWidget()

    screen = app.primaryScreen()
    rect = screen.availableGeometry()

    ui = UiGui(rect.width(), rect.height(), StackedWidget)
    ui.setupUi(StackedWidget)

    if (getFlag("Fullscreen")):
        StackedWidget.showFullScreen()
    else:
        StackedWidget.show()

    sys.exit(app.exec_())