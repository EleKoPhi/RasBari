from Widgets.my_widget_class import *

class included_drinks_class(my_widget):

    def __init__(self, main_widget, program, GUI_layout,main_bar):
        super().__init__(main_widget, program, GUI_layout,main_bar)

        """std_height = self.button_height
        std_width = self.button_width
        std_y = self.bottom_button_y

        # Build of new widget

        self.included_Drinks_widget.setObjectName("Drinks")
        stacked_widget.addWidget(self.included_Drinks_widget)

        # Headline - Contains Software title

        self.header(self.included_Drinks_widget)

        drink_txt_width = self.button_width * 1.8
        drink_txt_height = self.button_width * 1.2
        drink_txt_x = self.GUI_Width / 2 - drink_txt_width / 2
        drink_txt_y = self.GUI_Height / 2 - drink_txt_height / 2

        self.drink_txt_label = QtWidgets.QLabel(self.included_Drinks_widget)
        self.drink_txt_label.setGeometry(QtCore.QRect(drink_txt_x, drink_txt_y, drink_txt_width, drink_txt_height))
        self.drink_txt_label.setObjectName("Middle_Txt_Box")
        self.drink_txt_label.setText(self.RasBari.DrinkList[self.live_drink].getIngredientString())
        self.stdLabelSetUp(self.drink_txt_label)

        exit_button_x = (self.GUI_Width / 2 - self.button_width / 2)

        self.exit_button = QtWidgets.QPushButton(self.included_Drinks_widget)
        self.exit_button.setGeometry(QtCore.QRect(exit_button_x, std_y, std_width, std_height))
        self.exit_button.setText("Exit")
        self.exit_button.clicked.connect(lambda: self.show_widget(self.main_widget, 1))

        next_button_size = self.button_height * 1.5
        next_button_y = self.GUI_Height / 2 - next_button_size / 2
        next_left_x = (self.GUI_Width / 2 - drink_txt_width / 2) / 2 - next_button_size / 2
        next_right_x = self.GUI_Width - next_left_x - next_button_size

        self.Next_left = QtWidgets.QPushButton(self.included_Drinks_widget)
        self.Next_left.setGeometry(QtCore.QRect(next_left_x, next_button_y, next_button_size, next_button_size))
        self.Next_left.setObjectName("change_left")
        self.Next_left.setText("<-")
        self.Next_left.clicked.connect(lambda: self.change_live_drink(0))

        self.Next_right = QtWidgets.QPushButton(self.included_Drinks_widget)
        self.Next_right.setGeometry(QtCore.QRect(next_right_x, next_button_y, next_button_size, next_button_size))
        self.Next_right.setObjectName("change_right")
        self.Next_right.setText("->")
        self.Next_right.clicked.connect(lambda: self.change_live_drink(1))

        new_drink_x = self.bottom_button_getin
        delete_x = self.GUI_Width - self.bottom_button_getin - self.button_width

        # delete - for navigation from widget to destination_Left

        delete_width = std_width / 2 - self.button_space / 2

        self.delete = QtWidgets.QPushButton(self.included_Drinks_widget)
        self.delete.setGeometry(QtCore.QRect(delete_x, std_y, delete_width, std_height))
        self.delete.setText("Delete")

        change_x = delete_x + delete_width + self.button_space

        self.change = QtWidgets.QPushButton(self.included_Drinks_widget)
        self.change.setGeometry(QtCore.QRect(change_x, std_y, delete_width, std_height))
        self.change.setText("Change")

        self.change.clicked.connect(lambda: self.tuneDrink(stacked_widget, self.live_drink))

        self.delete.clicked.connect(lambda: delete_drink(self.live_drink))

        # NewDrink - for navigation from widget to NewDrink_page[0]

        self.newdrink_button = QtWidgets.QPushButton(self.included_Drinks_widget)
        self.newdrink_button.setGeometry(QtCore.QRect(new_drink_x, std_y, std_width, std_height))
        self.newdrink_button.setText("Set up a new drink")

        self.newdrink_button.clicked.connect(lambda: self.show_widget(self.NewDrink_pages[0], 1))

        self.updateGUI.connect(lambda: updateWidget())




    def updateWidget():
        if (len(self.RasBari.DrinkList) != 0 & self.flag == 1): self.live_drink = 0

        self.flag == 1

        try:
            self.drink_txt_label.setText(self.RasBari.DrinkList[self.live_drink].getIngredientString())
        except:
            self.drink_txt_label.setText("No more drinks in the system...")

    def delete_drink(drink):
        try:
            self.RasBari.DrinkList.pop(drink)
            self.live_drink = self.live_drink - 1
            if self.live_drink < 0: self.live_drink = len(self.RasBari.DrinkList) - 1
            self.drink_txt_label.setText(self.RasBari.DrinkList[self.live_drink].getIngredientString())
        except:
            self.drink_txt_label.setText("No more drinks in the system...")"""

