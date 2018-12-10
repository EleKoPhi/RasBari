from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *
from functools import partial
from classes.class_myThread import *


class my_widget(QWidget, QObject):

    updateGUI = pyqtSignal()

    def __init__(self, stacked_widget, ui_gui, ui_layout, master_bar):
        super().__init__()

        self.stacked_widget = stacked_widget  # Main widget, where all othe widgets are stacked on
        self.ui_gui = ui_gui                  # The "running" program
        self.bar = master_bar                 # The whole bar
        self.layout = ui_layout               # All values for the layout (class lo())

        self.widget = QtWidgets.QWidget()  # The base for the new widget
        self.stacked_widget.addWidget(self.widget)  # Add the base widget to the stack of all widgets

        self.title = QtWidgets.QLabel(self.widget)
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
        self.title.setText("Rasbari V10")
        self.stdLabelSetUp(self.title)

    def stdLabelSetUp(self, label):
        label.setAlignment(Qt.AlignCenter)
        label.setFrameShape(6)
        label.setStyleSheet("background-color: white")

    def show_widget(self, widget, refresh):
        if refresh: self.ui_gui.updateGUI_global.emit()
        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(widget))

    def bottomNavigation(self, widget, destination_left, destination_right, destination_middle, button_txt):

        std_width = self.layout.button_width
        std_height = self.layout.button_height

        middle_x = self.layout.GUI_Width / 2 - self.layout.button_width / 2
        left_x = self.layout.bottom_button_getin
        right_x = self.layout.GUI_Width - self.layout.bottom_button_getin - self.layout.button_width
        std_y = self.layout.bottom_button_y

        self.middleButton = QtWidgets.QPushButton(widget)
        self.middleButton.setGeometry(QtCore.QRect(middle_x, std_y, std_width, std_height))
        self.middleButton.setText(button_txt[1])
        self.middleButton.clicked.connect(lambda: self.show_widget(destination_middle, 1))

        self.leftButton = QtWidgets.QPushButton(widget)
        self.leftButton.setGeometry(QtCore.QRect(left_x, std_y, std_width, std_height))
        self.leftButton.setText(button_txt[0])
        self.leftButton.clicked.connect(lambda: self.show_widget(destination_left, 1))

        self.rightButton = QtWidgets.QPushButton(widget)
        self.rightButton.setGeometry(QtCore.QRect(right_x, std_y, std_width, std_height))
        self.rightButton.setText(button_txt[2])
        self.rightButton.clicked.connect(lambda: self.show_widget(destination_right, 1))

    def side_navigation(self, widget, destination_left, destination_right):

        possible_space = self.layout.button_width * 1.8

        Next_button_size = self.layout.button_height * 1.5
        Next_button_y = self.layout.GUI_Height / 2 - Next_button_size / 2
        Next_left_x = (self.layout.GUI_Width / 2 - possible_space / 2) / 2 - Next_button_size / 2
        Next_right_x = self.layout.GUI_Width - Next_left_x - Next_button_size

        self.Next_left = QtWidgets.QPushButton(widget)
        self.Next_left.setGeometry(QtCore.QRect(Next_left_x, Next_button_y, Next_button_size, Next_button_size))
        self.Next_left.setObjectName("change_left")
        self.Next_left.setText("<-")
        self.Next_left.clicked.connect(lambda: self.show_widget(destination_left, 0))

        self.Next_right = QtWidgets.QPushButton(widget)
        self.Next_right.setGeometry(QtCore.QRect(Next_right_x, Next_button_y, Next_button_size, Next_button_size))
        self.Next_right.setObjectName("change_right")
        self.Next_right.setText("->")
        self.Next_right.clicked.connect(lambda: self.show_widget(destination_right, 0))

# finished 02.12.2018
