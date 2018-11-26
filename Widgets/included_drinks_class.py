from Widgets.my_widget_class import *
from Widgets.drink_tune_class import *



class included_drinks_class(my_widget):

    def __init__(self, stacked_widget, ui_gui, ui_layout, master_bar):
        super().__init__(stacked_widget, ui_gui, ui_layout, master_bar)

        self.live_drink = 0
        self.flag = 2

        std_height = self.layout.button_height
        std_width = self.layout.button_width
        std_y = self.layout.bottom_button_y

        drink_txt_width = self.layout.button_width * 1.8
        drink_txt_height = self.layout.button_width * 1.2
        drink_txt_x = self.layout.GUI_Width / 2 - drink_txt_width / 2
        drink_txt_y = self.layout.GUI_Height / 2 - drink_txt_height / 2

        self.drink_txt_label = QtWidgets.QLabel(self.widget)
        self.drink_txt_label.setGeometry(QtCore.QRect(drink_txt_x, drink_txt_y, drink_txt_width, drink_txt_height))
        self.drink_txt_label.setObjectName("Middle_Txt_Box")
        self.drink_txt_label.setText(self.bar.DrinkList[self.live_drink].getIngredientString())
        self.stdLabelSetUp(self.drink_txt_label)

        exit_button_x = (self.layout.GUI_Width / 2 - self.layout.button_width / 2)

        self.exit_button = QtWidgets.QPushButton(self.widget)
        self.exit_button.setGeometry(QtCore.QRect(exit_button_x, std_y, std_width, std_height))
        self.exit_button.setText("Exit")
        self.exit_button.clicked.connect(lambda: self.show_widget(self.ui_gui.main_container.widget, 1))

        next_button_size = self.layout.button_height * 1.5
        next_button_y = self.layout.GUI_Height / 2 - next_button_size / 2
        next_left_x = (self.layout.GUI_Width / 2 - drink_txt_width / 2) / 2 - next_button_size / 2
        next_right_x = self.layout.GUI_Width - next_left_x - next_button_size

        self.Next_left = QtWidgets.QPushButton(self.widget)
        self.Next_left.setGeometry(QtCore.QRect(next_left_x, next_button_y, next_button_size, next_button_size))
        self.Next_left.setObjectName("change_left")
        self.Next_left.setText("<-")
        self.Next_left.clicked.connect(lambda: self.change_live_drink(0))

        self.Next_right = QtWidgets.QPushButton(self.widget)
        self.Next_right.setGeometry(QtCore.QRect(next_right_x, next_button_y, next_button_size, next_button_size))
        self.Next_right.setObjectName("change_right")
        self.Next_right.setText("->")
        self.Next_right.clicked.connect(lambda: self.change_live_drink(1))

        new_drink_x = self.layout.bottom_button_getin
        delete_x = self.layout.GUI_Width - self.layout.bottom_button_getin - self.layout.button_width

        # delete - for navigation from widget to destination_Left

        delete_width = std_width / 2 - self.layout.button_space / 2

        self.delete = QtWidgets.QPushButton(self.widget)
        self.delete.setGeometry(QtCore.QRect(delete_x, std_y, delete_width, std_height))
        self.delete.setText("Delete")

        change_x = delete_x + delete_width + self.layout.button_space

        self.change = QtWidgets.QPushButton(self.widget)
        self.change.setGeometry(QtCore.QRect(change_x, std_y, delete_width, std_height))
        self.change.setText("Change")

        self.change.clicked.connect(lambda: self.tune_drink())

        self.delete.clicked.connect(lambda: self.delete_drink(self.live_drink))

        # NewDrink - for navigation from widget to NewDrink_page[0]

        self.newdrink_button = QtWidgets.QPushButton(self.widget)
        self.newdrink_button.setGeometry(QtCore.QRect(new_drink_x, std_y, std_width, std_height))
        self.newdrink_button.setText("Set up a new drink")

        self.newdrink_button.clicked.connect(lambda: self.show_widget(self.ui_gui.new_drink_container.NewDrink_pages[0].widget, 1))

        self.ui_gui.updateGUI_global.connect(lambda: self.updateWidget())


    def updateWidget(self):

        if(self.flag==1):self.live_drink = 0
        #self.flag = 1

        try:
            self.drink_txt_label.setText(self.bar.DrinkList[self.live_drink].getIngredientString())
        except:
            self.drink_txt_label.setText("No more drinks in the system...")

    def delete_drink(self,drink):
        try:
            self.bar.DrinkList.pop(drink)
            self.live_drink = self.live_drink - 1
            if self.live_drink < 0: self.live_drink = len(self.bar.DrinkList) - 1
            self.drink_txt_label.setText(self.bar.DrinkList[self.live_drink].getIngredientString())
        except:
            self.drink_txt_label.setText("No more drinks in the system...")

    def change_live_drink(self, direction):
        if direction == 1:
            self.live_drink = self.live_drink + 1
            if self.live_drink > len(self.bar.DrinkList) - 1: self.live_drink = 0
        if direction == 0:
            self.live_drink = self.live_drink - 1
            if self.live_drink < 0: self.live_drink = len(self.bar.DrinkList) - 1

        try:
            self.drink_txt_label.setText(self.bar.DrinkList[self.live_drink].getIngredientString())
        except:
            self.drink_txt_label.setText("No more drinks in the system...")

    def tune_drink(self):

        tuneWidget = drink_tune_class(self.stacked_widget, self.ui_gui, self.layout, self.bar, self.live_drink)

        self.show_widget(tuneWidget.help_pages[0].widget,1)



