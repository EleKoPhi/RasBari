from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from classes.class_myThread import *


def stdLabelSetUp(label):
    label.setAlignment(Qt.AlignCenter)
    label.setFrameShape(6)
    label.setStyleSheet("background-color: white")


class bottle_line(QObject):
    def __init__(self, ui_gui, widget, bottle, total_x, total_y, layout, main_bar):

        super().__init__()
        self.live_widget = widget
        self.Bottle_in = bottle
        self.rev_x = total_x + 10
        self.rev_y = total_y
        self.ui_gui = ui_gui
        self.layout = layout
        self.bar = main_bar

        self.reset_button = QtWidgets.QPushButton(self.live_widget)
        self.clear_button = QtWidgets.QPushButton(self.live_widget)
        self.amount_progressbar = QtWidgets.QProgressBar(self.live_widget)
        self.bottle_name_label = QtWidgets.QLabel(self.live_widget)

        self.format_line()

    def format_line(self):

        label_width = self.layout.GUI_Width * 0.145
        self.bottle_name_label.setObjectName("Bottle Name")
        self.bottle_name_label.setGeometry(self.rev_x, self.rev_y, label_width, self.layout.button_height)
        self.bottle_name_label.setText(self.Bottle_in.get_name())
        stdLabelSetUp(self.bottle_name_label)

        progressbar_x = self.rev_x + self.layout.GUI_Width * 0.145 + self.layout.top_space
        progressbar_width = self.layout.GUI_Width * 0.3
        progressbar_value = (int(self.Bottle_in.get_remaining_content()) / (
            int(self.Bottle_in.get_bottle_size()))) * 100
        self.amount_progressbar.setGeometry(progressbar_x, self.rev_y, progressbar_width, self.layout.button_height)
        self.amount_progressbar.setProperty("value", progressbar_value)

        clear_button_x = progressbar_x + self.layout.top_space + self.layout.GUI_Width * 0.3
        self.clear_button.setGeometry(clear_button_x, self.rev_y, self.layout.button_width, self.layout.button_height)
        self.clear_button.setText("Output")
        self.clear_button.clicked.connect(lambda: self.emptyBottle())

        reset_button_x = clear_button_x + self.layout.top_space + self.layout.button_width
        self.reset_button.setGeometry(reset_button_x, self.rev_y, self.layout.button_width, self.layout.button_height)
        self.reset_button.setText("RESET")
        self.reset_button.clicked.connect(lambda: self.placeNewBottle())

    def placeNewBottle(self):

        print("reset bottle")

        for i in range(len(self.ui_gui.bar.Bottles)):

            if self.Bottle_in.get_name() == self.ui_gui.bar.Bottles[i].get_name():
                self.ui_gui.bar.Bottles[i].put_amount(self.ui_gui.bar.Bottles[i].get_bottle_size())
                print(self.ui_gui.bar.Bottles[i].get_level())
                self.Bottle_in = self.ui_gui.bar.Bottles[i]
                break

        self.amount_progressbar.setProperty("value", 100)

    def emptyBottle(self):

        print("empty bottle")
        self.Bottle_in.put_level_zero()
        self.amount_progressbar.setProperty("value", 0)

    def updateStatusBar(self):

        for i in range(len(self.bar.Bottles)):
            if self.Bottle_in.get_name() == self.bar.Bottles[i].get_name():

                self.Bottle_in = self.bar.Bottles[i]
                value = int((int(self.bar.Bottles[i].get_level()) / int(self.Bottle_in.get_bottle_size())) * 100)
                if value < 0: value = 0
                self.amount_progressbar.setProperty("value", value)
                break
