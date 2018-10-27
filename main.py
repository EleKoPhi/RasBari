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
from PyQt5 import QtWidgets

if __name__ == "__main__":

    import sys

    app = QtWidgets.QApplication(sys.argv)
    StackedWidget = QtWidgets.QStackedWidget()

    screen = app.primaryScreen()
    rect = screen.availableGeometry()

    ui = Ui_GUI(rect.width(),rect.height())
    ui.setupUi(StackedWidget)

    #StackedWidget.showFullScreen() #Comment line 28 or 29 in for full or part screen
    StackedWidget.show()

    sys.exit(app.exec_())

