from super_widget import *

class new_drink_menue(my_widget):

    def __init__(self, main_widget, program, GUI_layout,main_bar):
        super().__init__(main_widget, program, GUI_layout,main_bar)

        self.NewDrink_pages = []
        self.slider = []
        self.name = []
        self.amount = []
        self.stats = []

        std_Hight = self.layout.button_height
        std_Width = self.layout.button_width
        std_Y = self.layout.bottom_button_y
        Topspace = self.layout.GUI_Height * 0.16
        possible_spcae = self.layout.button_width * 1.8

        slider_width = std_Width * 0.83
        amount_width = std_Hight
        name_width = slider_width - amount_width

        self.page = 0
        self.j = 0

        totalNr_Widgets = int(len(self.bar.DrinkList) / 5)

        space_bt_elements = (possible_spcae - slider_width - name_width - amount_width) / 2
        slider_x = (self.layout.GUI_Width / 2) - (slider_width + name_width + amount_width + 2 * space_bt_elements) / 2
        name_x = slider_x + space_bt_elements + slider_width
        amount_x = name_x + space_bt_elements + name_width
        Stat_x = self.layout.GUI_Width - self.layout.bottom_button_getin - self.layout.button_width

        if len(self.bar.DrinkList) % 5 != 0:
            totalNr_Widgets += 1

        for i in range(totalNr_Widgets):
            self.NewDrink_pages.extend([my_widget(main_widget, program, GUI_layout,main_bar)])
            self.NewDrink_pages[i].setObjectName("NewDrink_page" + str(i))
            main_widget.addWidget(self.NewDrink_pages[i])
            self.newdrink_bottom_navigation(self.slider, self.NewDrink_pages[i].widget)

        for i in range(len(self.NewDrink_pages)-1):
            try:
                self.side_navigation(self.NewDrink_pages[i], self.NewDrink_pages[i - 1], self.NewDrink_pages[i + 1])

            except:
                self.side_navigation(self.NewDrink_pages[i], self.NewDrink_pages[i - 1], self.NewDrink_pages[0])

            self.help_slider = QtWidgets.QLabel(self.NewDrink_pages[i].widget)
            self.help_slider.setGeometry(QtCore.QRect(Stat_x, std_Y, std_Width, std_Hight))
            self.help_slider.setText("Make your drink!")
            self.stdLabelSetUp(self.help_slider)
            self.stats.extend([self.help_slider])

        #self.help_slider.extend([self])

        for i in range(len(self.bar.Bottles)):

            if ((i % 5 == 0) & (i != 0)):
                self.page = self.page + 1
                self.j = 0

            line_y = Topspace + self.j * (std_Hight + self.layout.top_space * 1.7)

            self.help_slider = QtWidgets.QSlider(Qt.Horizontal, self.NewDrink_pages[self.page].widget)
            self.slider.extend([self.help_slider])
            self.slider[i].setMaximum(100)
            self.slider[i].setMinimum(0)
            self.slider[i].setGeometry(QtCore.QRect(slider_x, line_y, slider_width, std_Hight))

            self.help_name = QtWidgets.QLabel(self.NewDrink_pages[self.page].widget)
            self.name.extend([self.help_name])
            self.name[i].setText(self.bar.Bottles[i].getname())
            self.name[i].setGeometry(QtCore.QRect(name_x, line_y, name_width, std_Hight))
            self.stdLabelSetUp(self.name[i])

            self.help_amount = QtWidgets.QLabel(self.NewDrink_pages[self.page])
            self.amount.extend([self.help_amount])
            self.amount[i].setText("0")
            self.amount[i].setGeometry(QtCore.QRect(amount_x, line_y, amount_width, std_Hight))
            self.stdLabelSetUp(self.amount[i])

            self.slider[i].valueChanged.connect(partial(self.Amount_Slider, i))
            self.slider[i].valueChanged.connect(partial(self.newMaxima, i))

            #self.updateGUI.connect(lambda: self.reset_slider_list(slider))

            self.j = self.j + 1

        ############################ END of newDrink_Widget(self, StackedWidget) #######################################

    def saveNewDrink(self, slider_list, bottles):

        amount_sum = 0

        for i in range(len(slider_list)):
            amount_sum = amount_sum + slider_list[i].value()

        if amount_sum == 100:

            self.Ingredients = []

            new_drink_name = ""

            for i in range(len(slider_list)):
                if slider_list[i].value() != 0:
                    name = bottles[i].getname()
                    name = name[:3]
                    name = name + str(slider_list[i].value())
                    new_drink_name = new_drink_name + name

            self.Ingredients.extend([("name", new_drink_name)])

            for i in range(len(slider_list)):
                Ingred = [bottles[i].getname(), str(slider_list[i].value())]
                self.Ingredients.extend([Ingred])

            new_drink = Drink(self.Ingredients)

            self.RasBari.DrinkList.extend([new_drink])
            self.reset_slider_list(slider_list)
            self.show_widget(self.main_widget, 1)

        else:
            print("Drink not completed")  # TODO change the reset button to an textbrowser that indictes status

    def reset_slider_list(self, slider_list):
        for i in range(len(slider_list)):
            slider_list[i].setSliderPosition(0)

    def Amount_Slider(self,i):
        self.amount[i].setText(str(self.slider[i].value()))

        sum = 0

        for i in range(len(self.slider)):
            sum = sum + self.slider[i].value()

        message = "amount: %d/100" % sum
        add = ""

        if sum < 100:
            add = "\nplease add %d%% more" % (100 - sum)
        if sum == 100:
            add = "\nPress save to add your drink!"
        if sum == 0:
            message = ""
            add = "Make your drink!"

        for i in range(len(self.stats)):
            self.stats[i].setText(message + add)

    def newMaxima(self,callingSlider):
        sum = 0

        for i in range(len(self.slider)):
            sum = sum + self.slider[i].value()

        if sum >= 100:
            self.slider[callingSlider].setSliderPosition(self.slider[callingSlider].value() - (sum - 100))

    def newdrink_bottom_navigation(self, slider, widget):

        std_height = self.layout.button_height
        std_width = self.layout.button_width
        std_y = self.layout.bottom_button_y

        # ExitButton - Button to navigate from the first drink widget back to the main widget

        exit_button_x = (self.layout.GUI_Width / 2 - self.layout.button_width / 2)

        self.exit_button = QtWidgets.QPushButton(widget)
        self.exit_button.setGeometry(QtCore.QRect(exit_button_x, std_y, std_width, std_height))
        self.exit_button.setText("Exit")
        #self.exit_button.clicked.connect(lambda: self.show_widget(self.main_widget, 1))

        # Save - Button to Save the current drink setup as a new drink

        self.Save = QtWidgets.QPushButton(widget)
        self.Save.setGeometry(QtCore.QRect(self.layout.bottom_button_getin, std_y, std_width, std_height))
        self.Save.setText("Save Drink")
        #self.Save.clicked.connect(lambda: self.saveNewDrink(slider, self.RasBari.Bottles))

    def saveNewDrink(self, slider_list, bottles):

        amount_sum = 0

        for i in range(len(slider_list)):
            amount_sum = amount_sum + slider_list[i].value()

        if amount_sum == 100:

            self.Ingredients = []

            new_drink_name = ""

            for i in range(len(slider_list)):
                if slider_list[i].value() != 0:
                    name = bottles[i].getname()
                    name = name[:3]
                    name = name + str(slider_list[i].value())
                    new_drink_name = new_drink_name + name

            self.Ingredients.extend([("name", new_drink_name)])

            for i in range(len(slider_list)):
                Ingred = [bottles[i].getname(), str(slider_list[i].value())]
                self.Ingredients.extend([Ingred])

            new_drink = Drink(self.Ingredients)

            self.RasBari.DrinkList.extend([new_drink])
            self.reset_slider_list(slider_list)
            self.show_widget(self.main_widget, 1)

        else:
            print("Drink not completed")

    def reset_slider_list(self, slider_list):
        for i in range(len(slider_list)):
            slider_list[i].setSliderPosition(0)

    def update_glass_txt(self):

        self.amount_LCD.display(self.RasBari.getAmount())
        glas_string = "Glass volume: " + str(self.RasBari.getAmount()) + " ml"
        self.DigitText.setText(glas_string)

    def update_status_txt(self):

        if not self.RasBari.getProductionFlag():
            self.StatTxt.setText("Status: Wait for input...")
        else:
            self.StatTxt.setText("Status: Busy")
