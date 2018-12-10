from Widgets.my_widget_class import *


class drink_tune_class(my_widget):

    def __init__(self, stacked_widget, ui_gui, ui_layout, master_bar, drink_nr):
        super().__init__(stacked_widget, ui_gui, ui_layout, master_bar)

        self.drink_nr = drink_nr

        std_height = self.layout.button_height
        std_width = self.layout.button_width
        std_y = self.layout.bottom_button_y

        space_width = self.layout.button_width * 1.8
        space_x = self.layout.GUI_Width / 2 - space_width / 2
        topspace = self.layout.GUI_Height * 0.16

        slider_width = std_width * 0.83
        amount_width = std_height
        name_width = slider_width - amount_width

        # space_bt_elements - Space between slider name and amount
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
        self.help_pages = []
        self.help_pages.extend([self])

        self.Name = QtWidgets.QLabel(self.widget)
        self.Name.setGeometry(QtCore.QRect(space_x, topspace, space_width, std_height))
        self.Name.setObjectName("Drink_Name")
        self.Name.setText(self.bar.DrinkList[drink_nr].Ingredients[0][1])
        self.stdLabelSetUp(self.Name)

        self.j = 1
        self.page = 0
        self.nr_ingredients = 0

        for i in range(1, len(self.bar.DrinkList[drink_nr].Ingredients)):
            if self.bar.DrinkList[drink_nr].Ingredients[i][1] != "0":
                self.nr_ingredients = self.nr_ingredients + 1

        nr_widgets = int(self.nr_ingredients/4)

        for i in range(nr_widgets):
            self.helpWig = my_widget(stacked_widget, ui_gui, ui_layout, master_bar)
            self.helpWig.setObjectName("helpWig" + str(i))
            self.help_pages.extend([self.helpWig])

            self.Name = QtWidgets.QLabel(self.helpWig.widget)
            self.Name.setGeometry(QtCore.QRect(space_x, topspace, space_width, std_height))
            self.Name.setObjectName("Drink_Name")
            self.Name.setText(self.bar.DrinkList[drink_nr].Ingredients[0][1])
            self.stdLabelSetUp(self.Name)

            stacked_widget.addWidget(self.helpWig.widget)

        for l in range(1, len(self.bar.DrinkList[drink_nr].Ingredients)):
            if self.bar.DrinkList[drink_nr].Ingredients[l][1] != "0":
                self.name_list.extend([self.bar.DrinkList[drink_nr].Ingredients[l]])

        for i in range(self.nr_ingredients):

            if (0 == i % 4) & (i != 0):
                self.page = self.page + 1
                self.j = 1

            line_y = topspace + self.j * (std_height + self.layout.top_space * 1.7)

            print(len(self.help_pages))

            self.help_slider = QtWidgets.QSlider(Qt.Horizontal, self.help_pages[self.page].widget)
            self.slider.extend([self.help_slider])
            self.slider[i].setMaximum(100)
            self.slider[i].setMinimum(1)
            self.slider[i].setSliderPosition(int(self.name_list[i][1]))
            self.slider[i].setGeometry(QtCore.QRect(slider_x, line_y, slider_width, std_height))

            self.help_name = QtWidgets.QLabel(self.help_pages[self.page].widget)
            self.name.extend([self.help_name])
            self.name[i].setText(self.name_list[i][0])
            self.name[i].setGeometry(QtCore.QRect(name_x, line_y, name_width, std_height))
            self.stdLabelSetUp(self.name[i])

            self.help_amount = QtWidgets.QLabel(self.help_pages[self.page].widget)
            self.amount.extend([self.help_amount])
            self.amount[i].setText(self.name_list[i][1])
            self.amount[i].setGeometry(QtCore.QRect(amount_x, line_y, amount_width, std_height))
            self.stdLabelSetUp(self.amount[i])

            self.exit_button = QtWidgets.QPushButton(self.help_pages[self.page].widget)
            self.exit_button.setGeometry(QtCore.QRect(exit_button_x, std_y, std_width, std_height))
            self.exit_button.setText("Exit")
            self.exit_button.clicked.connect(lambda: self.show_widget(self.ui_gui.main_container.widget, 1))

            self.Back = QtWidgets.QPushButton(self.help_pages[self.page].widget)
            self.Back.setGeometry(QtCore.QRect(change_left_x, std_y, std_width, std_height))
            self.Back.setText("Back")
            self.Back.clicked.connect(lambda: self.show_widget(self.ui_gui.included_drinks_container.widget, 0))

            self.Apply = QtWidgets.QPushButton(self.help_pages[self.page].widget)
            self.Apply.setGeometry(QtCore.QRect(change_right_x, std_y, std_width, std_height))
            self.Apply.setText("Apply changes")
            self.Apply.clicked.connect(lambda: self.apply_drink_tune(self.slider, self.name))

            self.slider[i].sliderReleased.connect(partial(self.new_maximum, i))
            self.slider[i].valueChanged.connect(partial(self.change_value, i))

            self.j = self.j + 1

        if self.nr_ingredients > 4:

            for i in range(len(self.help_pages)):
                try:
                    self.side_navigation(self.help_pages[i].widget, self.help_pages[i - 1].widget,
                                         self.help_pages[i + 1].widget)

                except:
                    self.side_navigation(self.help_pages[i].widget, self.help_pages[i - 1].widget,
                                         self.help_pages[0].widget)

    def change_value(self, calling_slider):

        # change_value is called from the calling_slider every time the value changed
        # it limits the slider value and updated the amount label

        if self.slider[calling_slider].value() > (100 - len(self.slider) + 1):
            self.slider[calling_slider].setSliderPosition(100 - len(self.slider) + 1)

        self.amount[calling_slider].setText(str(self.slider[calling_slider].value()))

    def new_maximum(self, calling_slider):

        # new_maximum is called when a slider from the drink_tune_container is released
        # calculates the sum of all new values and separates the difference to all remaining sliders

        ingred_sum = 0  # variable where the slider sum is saved
        start_slider = calling_slider  # the slider, witch is calling (released)

        for loop_iteration in range(len(self.slider)):  # calculate the slider sum
            ingred_sum = ingred_sum + self.slider[loop_iteration].value()

        ingred_sum = ingred_sum - 100  # The amount of set ingredients that is to much

        if ingred_sum > 0:  # If the set amount is more than 100%
            while True:
                if (start_slider != calling_slider) and (self.slider[start_slider].value() != 1):
                    self.slider[start_slider].setSliderPosition(self.slider[start_slider].value() - 1)
                    ingred_sum = ingred_sum - 1
                    start_slider = start_slider + 1
                else:
                    start_slider = start_slider + 1

                if start_slider > (len(self.slider) - 1): start_slider = 0

                if ingred_sum == 0: break  # nothing left

        if ingred_sum < 0:  # If the set amount is less than 100%
            while True:
                if start_slider != calling_slider:
                    self.slider[start_slider].setSliderPosition(self.slider[start_slider].value() + 1)
                    ingred_sum = ingred_sum + 1
                    start_slider = start_slider + 1
                else:
                    start_slider = start_slider + 1

                if start_slider > (len(self.slider) - 1): start_slider = 0

                if ingred_sum == 0: break  # nothing left

    def apply_drink_tune(self, slider, name):

        # appy_drink_tune is called from the tune button and applies the current slider setting to the current
        # shown drink. After that is shows the included_drinks_contrainer with the new applied settings.

        new_ingredients = []  # A empty list, where all the slider and names are saved

        for i in range(len(slider)):  # build the new_ingredients list
            new_ingredients.extend([[name[i].text(), str(slider[i].value())]])

        self.bar.DrinkList[self.drink_nr].put_new_ingredients(new_ingredients)

        # update the current text box in the included_drink_container that the applied changes are shown

        live_drink_dummy = self.ui_gui.included_drinks_container.live_drink
        txt_box = self.ui_gui.included_drinks_container.widget.findChild(QtWidgets.QWidget, "Middle_Txt_Box")
        txt_box.setText(self.bar.DrinkList[live_drink_dummy].get_ingredient_string())

        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.ui_gui.included_drinks_container.widget))

# finished 30.11.2018
