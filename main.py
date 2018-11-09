#
#
# GUI and logical software for the RasBari
#
# Name: Philipp Mochti
#
# V1.0
#
#

from PyQt5 import QtWidgets

from StyleFunctions import ApplyStyleSheets
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

    #StackedWidget.showFullScreen() #Comment line 28 or 29 in for full or part screen
    StackedWidget.show()

    sys.exit(app.exec_())
