from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from functools import partial
from classes.class_myThread import *

class BottleLine(QWidget, QObject):
    def __init__(self, ui_gui, widget, Bottle, total_x, total_y,layout,main_bar):
        super().__init__()
        self.wg = widget
        self.Bottle_in = Bottle
        self.rev_x = total_x + 10
        self.rev_y = total_y
        self.ui_gui = ui_gui
        self.layout = layout
        self.bar = main_bar

        self.build_line()

    def build_line(self):

        self.BottleNameDsp = QtWidgets.QLabel(self.wg)
        self.BottleNameDsp.setGeometry(
            QtCore.QRect(self.rev_x, self.rev_y, self.layout.GUI_Width * 0.145, self.layout.button_height))
        self.BottleNameDsp.setObjectName("Bottle Name")
        self.BottleNameDsp.setText(self.Bottle_in.get_name())
        self.stdLabelSetUp(self.BottleNameDsp)

        xLevel = self.rev_x + self.layout.GUI_Width * 0.145 + self.layout.top_space

        self.level = QtWidgets.QProgressBar(self.wg)
        self.level.setGeometry(
            QtCore.QRect(xLevel, self.rev_y, self.layout.GUI_Width * 0.3, self.layout.button_height))
        self.level.setProperty("value",
                               (int(self.Bottle_in.get_remaining_content()) / (int(self.Bottle_in.get_bottle_size()))) * 100)

        xClear = xLevel + self.layout.top_space + self.layout.GUI_Width * 0.3

        self.ClearButton = QtWidgets.QPushButton(self.wg)
        self.ClearButton.setGeometry(
            QtCore.QRect(xClear, self.rev_y, self.layout.button_width, self.layout.button_height))
        self.ClearButton.setText("Output")

        xResetbutton = xClear + self.layout.top_space + self.layout.button_width

        self.Resetbutton = QtWidgets.QPushButton(self.wg)
        self.Resetbutton.setGeometry(
            QtCore.QRect(xResetbutton, self.rev_y, self.layout.button_width, self.layout.button_height))
        self.Resetbutton.setText("RESET")

        self.Resetbutton.clicked.connect(lambda: self.placeNewBottle())
        self.ClearButton.clicked.connect(lambda: self.emptyBottle())

    def placeNewBottle(self):

        print("Reset Bottle")

        for i in range(len(self.ui_gui.bar.Bottles)):

            if self.Bottle_in.get_name() == self.ui_gui.bar.Bottles[i].get_name():
                self.ui_gui.bar.Bottles[i].put_amount(self.ui_gui.bar.Bottles[i].get_bottle_size())
                print(self.ui_gui.bar.Bottles[i].get_level())
                self.Bottle_in = self.ui_gui.bar.Bottles[i]
                break

        self.level.setProperty("value",
                               (int(self.Bottle_in.get_level()) / (int(self.Bottle_in.get_bottle_size()))) * 100)

    def emptyBottle(self):

        print("empty Bottle")

        self.Bottle_in.put_level_zero()
        self.level.setProperty("value",
                               (int(self.Bottle_in.get_level()) / (int(self.Bottle_in.get_bottle_size()))) * 100)

    def updateStatusBar(self):

        for i in range(len(self.bar.Bottles)):
            if self.Bottle_in.get_name() == self.bar.Bottles[i].get_name():

                self.Bottle_in = self.bar.Bottles[i]
                value = int((int(self.bar.Bottles[i].get_level()) / int(self.Bottle_in.get_bottle_size())) * 100)
                if value < 0: value = 0
                self.level.setProperty("value", value)
                break

    def stdLabelSetUp(self, Label):
        Label.setAlignment(Qt.AlignCenter)
        Label.setFrameShape(6)
        Label.setStyleSheet("background-color: white")
