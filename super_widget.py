from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from functools import partial
from classes.class_myThread import *


class my_widget(QWidget, QObject):
    updateGUI = pyqtSignal()

    def __init__(self, main_widget, program, GUI_layout):
        super().__init__()

        self.stacked_widget = main_widget  # Main widget, where all othe widgets are stacked on
        self.program = program  # The "running" program
        self.layout = GUI_layout  # All values for the layout (class lo())

        self.widget = QtWidgets.QWidget()  # The base for the new widget
        self.stacked_widget.addWidget(self.widget)  # Add the base widget to the stack of all widgets
        self.title = QtWidgets.QLabel(self.widget)  # Add a title to the new widget

        self.setup_gui_elements()  # layout the new added gui elements

    def setup_gui_elements(self):
        self.header()

    def header(self):
        title_font = QtGui.QFont()
        title_font.setPointSize(26)
        title_font.setBold(True)
        title_font.setItalic(False)
        title_font.setWeight(75)

        title_x = 0
        title_y = self.layout.top_space
        title_width = self.layout.GUI_Width
        title_height = self.layout.GUI_Height * 0.1

        self.title.setGeometry(QtCore.QRect(title_x, title_y, title_width, title_height))
        self.title.setFont(title_font)
        self.title.setText("Rasbari V7")
        self.stdLabelSetUp(self.title)

    def stdLabelSetUp(self, label):
        label.setAlignment(Qt.AlignCenter)
        label.setFrameShape(6)
        label.setStyleSheet("background-color: white")

    def show_widget(self, widget, refresh):
        if refresh: self.updateGUI.emit()
        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(widget))
