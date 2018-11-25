from Widgets.my_widget_class import *


class drink_tune_class(my_widget):

    def __init__(self, stacked_widget, ui_gui, ui_layout, master_bar, drink_nr):
        super().__init__(stacked_widget, ui_gui, ui_layout, master_bar)

        std_height = self.layout.button_height
        std_width = self.layout.button_width
        std_y = self.layout.bottom_button_y

        space_width = self.layout.button_width * 1.8
        space_x = self.laoyut.GUI_Width / 2 - space_width / 2
        topspace = self.layout.GUI_Height * 0.16

        slider_width = std_width * 0.83
        amount_width = std_height
        name_width = slider_width - amount_width

        space_bt_elements = (space_width - slider_width - name_width - amount_width) / 2
        slider_x = (self.layout.GUI_Width / 2) - (slider_width + name_width + amount_width + 2 * space_bt_elements) / 2
        name_x = slider_x + space_bt_elements + slider_width
        amount_x = name_x + space_bt_elements + name_width

        exit_button_x = self.layout.GUI_Width / 2 - self.layout.button_width / 2
        change_left_x = self.layout.bottom_button_getin
        change_right_x = self.layout.GUI_Width - self.layout.bottom_button_getin - self.layout.button_width

        self.slider = []
        self.name = []
        self.amount = []
        self.name_list = []
        self.helpWig = []

        self.j = 1
        self.page = 0
        self.nr_ingredients = 0

        for i in range(1, len(self.bar.DrinkList[drink_nr].Ingredients)):
            if self.bar.DrinkList[drink_nr].Ingredients[i][1] != "0":
                self.nr_ingredients = self.nr_ingredients + 1

        nr_widgets = int(len(self.bar.DrinkList) / 4)

        if self.nr_ingredients < 4: nr_widgets = nr_widgets - 1
        if self.nr_ingredients > 4: nr_widgets = nr_widgets + 1

        for i in range(nr_widgets):
            self.helpWig = QtWidgets.QWidget()
            self.helpWig.setObjectName("helpWig" + str(i))
            self.help_pages.extend([self.helpWig])


            self.Name = QtWidgets.QLabel(self.helpWig)
            self.Name.setGeometry(QtCore.QRect(space_x, topspace, space_width, std_height))
            self.Name.setObjectName("Drink_Name")
            self.Name.setText(self.RasBari.DrinkList[drink_nr].Ingredients[0][1])
            self.stdLabelSetUp(self.Name)

            stacked_widget.addWidget(self.helpWig)

        for l in range(1, len(self.bar.DrinkList[drink_nr].Ingredients)):
            if self.bar.DrinkList[drink_nr].Ingredients[l][1] != "0":
                self.name_list.extend([self.bar.DrinkList[drink_nr].Ingredients[l]])

        for i in range(self.nr_ingredients):

            if (0 == i % 4) & (i != 0):
                self.page = self.page + 1
                self.j = 1

            line_y = topspace + j * (std_height + self.layout.top_space * 1.7)

            self.help_slider = QtWidgets.QSlider(Qt.Horizontal, self.help_pages[self.page])
            self.slider.extend([self.help_slider])
            self.slider[i].setMaximum(100)
            self.slider[i].setMinimum(1)
            self.slider[i].setSliderPosition(int(self.name_list[i][1]))
            self.slider[i].setGeometry(QtCore.QRect(slider_x, line_y, slider_width, std_height))

            self.help_name = QtWidgets.QLabel(self.help_pages[self.page])
            self.name.extend([self.help_name])
            self.name[i].setText(self.name_list[i][0])
            self.name[i].setGeometry(QtCore.QRect(name_x, line_y, name_width, std_height))
            self.stdLabelSetUp(self.name[i])

            self.help_amount = QtWidgets.QLabel(self.help_pages[self.page])
            self.amount.extend([self.help_amount])
            self.amount[i].setText(self.name_list[i][1])
            self.amount[i].setGeometry(QtCore.QRect(amount_x, line_y, amount_width, std_height))
            self.stdLabelSetUp(self.amount[i])

            self.exit_button = QtWidgets.QPushButton(self.help_pages[self.page])
            self.exit_button.setGeometry(QtCore.QRect(exit_button_x, std_y, std_width, std_height))
            self.exit_button.setText("Exit")
            #self.exit_button.clicked.connect(lambda: self.show_widget(self.ui_gui, 1))

            self.Back = QtWidgets.QPushButton(self.help_pages[self.page])
            self.Back.setGeometry(QtCore.QRect(change_left_x, std_y, std_width, std_height))
            self.Back.setText("Back")
            #self.Back.clicked.connect(lambda: self.show_widget(self.included_Drinks_widget, 1))

            self.Apply = QtWidgets.QPushButton(self.help_pages[self.page])
            self.Apply.setGeometry(QtCore.QRect(change_right_x, std_y, std_width, std_height))
            self.Apply.setText("Apply changes")
            #self.Apply.clicked.connect(lambda: self.apply_drink_tune(drink_nr, slider, name))

            #self.slider[i].sliderReleased.connect(partial(new_maximum, i))
            #self.slider[i].valueChanged.connect(partial(change_value, i))

            self.j = self.j + 1

        if self.nr_ingredients > 4:

            for i in range(len(self.help_pages)):
                try:
                    self.side_navigation(self.help_pages[self.i], self.help_pages[self.i - 1], self.help_pages[self.i + 1])

                except:
                    self.side_navigation(self.help_pages[self.i], self.help_pages[self.i - 1], self.help_pages[0])

    """def change_value(calling_slider):

        if slider[calling_slider].value() > (100 - len(slider) + 1):
            slider[calling_slider].setSliderPosition(100 - len(slider) + 1)

        if slider[calling_slider].value() < 1:
            slider[calling_slider].setSliderPosition(1)
        amount[calling_slider].setText(str(slider[calling_slider].value()))

    def new_maximum(calling_slider):
        ingred_sum = 0
        start_slider = calling_slider

        for loop_iteration in range(len(slider)):
            ingred_sum = ingred_sum + slider[loop_iteration].value()

        ingred_sum = ingred_sum - 100

        if ingred_sum > 0:
            while True:
                if (start_slider != calling_slider) and (slider[start_slider].value() != 1):
                    slider[start_slider].setSliderPosition(slider[start_slider].value() - 1)
                    ingred_sum = ingred_sum - 1
                    start_slider = start_slider + 1
                else:
                    start_slider = start_slider + 1

                if start_slider > (len(slider) - 1): start_slider = 0

                if ingred_sum == 0: break

        if ingred_sum < 0:
            while True:
                if start_slider != calling_slider:
                    slider[start_slider].setSliderPosition(slider[start_slider].value() + 1)
                    ingred_sum = ingred_sum + 1
                    start_slider = start_slider + 1
                else:
                    start_slider = start_slider + 1

                if start_slider > (len(slider) - 1): start_slider = 0

                if ingred_sum == 0: break

    def updateWidget():
        self.help_pages.clear()
        self.updateGUI.connect(lambda: updateWidget())
        self.show_widget(self.help_pages[0], 0)

    def apply_drink_tune(self, drink_nr, slider, name):

        new_ingredients = []

        for i in range(len(slider)):
            new_ingredients.extend([[name[i].text(), str(slider[i].value())]])

        self.RasBari.DrinkList[drink_nr].setNewIngredients(new_ingredients)

        self.flag = 0
        self.show_widget(self.included_Drinks_widget, 1)"""