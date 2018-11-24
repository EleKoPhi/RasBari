from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class drink_menue(QWidget, QObject):
    def __init__(self, main_widget, GUI_layout):
        super().__init__()

        self.main_widget = main_widget
        self.layout = GUI_layout

        print("widget build")
