from PyQt5 import QtWidgets
from functools import partial
from classes.class_Bar import *
from classes.class_eMailGuard import *

from drink_menue import *
from main_menue import *
from bottle_display import *
from ingredients_display import *
from new_drink_menue import *


class UiGui(QWidget, QObject):

    NewDrink_pages = []
    help_pages = []
    Bottle_pages = []
    updateGUI = pyqtSignal()
    clear = pyqtSignal()

    live_drink = 0
    flag = 0

    def __init__(self, width, height, global_widget):
        QObject.__init__(self)
        self.RasBari = Bar()
        self.EmailOrder = eMailGuard()
        self.threadpool = QThreadPool()

        self.GW = global_widget
        self.MailTimer = QtCore.QTimer()

        self.GUI_layout = self.calculateGUI(width, height)

        self.drink_menue = drink_menue(self.GW, self, self.GUI_layout,self.RasBari)
        self.main_menue = main_widget(self.GW, self, self.GUI_layout, self.RasBari)
        self.bottle_display = bottle_display(self.GW, self, self.GUI_layout, self.RasBari)
        self.missing_Ingred = ingredients_display(self.GW, self, self.GUI_layout,self.RasBari)
        self.new_drink_page = new_drink_menue(self.GW, self, self.GUI_layout,self.RasBari)

        self.setupUi(self.GW)

    def setupUi(self, stacked_widget):

        stacked_widget.setObjectName("stacked_widget")

        ################################### ---> START GUI SETUP <--- #################################################

        stacked_widget.setObjectName("GUI")
        stacked_widget.resize(self.GUI_layout.GUI_Width, self.GUI_layout.GUI_Height)
        stacked_widget.setMaximumSize(QtCore.QSize(self.GUI_layout.GUI_Width, self.GUI_layout.GUI_Height))
        stacked_widget.setMinimumSize(QtCore.QSize(self.GUI_layout.GUI_Width, self.GUI_layout.GUI_Height))

        QtCore.QMetaObject.connectSlotsByName(stacked_widget)

        ############################### ---> START CONNECTION [CodeSignals]<--- #######################################

        #self.RasBari.missingIngred.connect(lambda: self.show_widget(self.ingredWidg, 1))
       # self.RasBari.drinkunknown.connect(lambda: self.showmsgbox)
       # self.RasBari.changedAmountSig.connect(self.update_glass_txt)
       # self.RasBari.changedStatus.connect(self.update_status_txt)

        #self.EmailOrder.CheckMail.connect(self.exeOrder)

        ################################### ---> START TIMER <--- #####################################################

        self.MailTimer.setSingleShot(False)
        if getFlag("Mailorder") & self.EmailOrder.status: self.MailTimer.start(3000)
        self.MailTimer.timeout.connect(lambda: self.check4order())

        ################################### ---> END TIMER <--- #######################################################

        self.show_widget(self.new_drink_page.NewDrink_pages[0].widget,1)
        QtCore.QMetaObject.connectSlotsByName(stacked_widget)

        ################################### ---> END setUp_Ui <--- ####################################################

    def show_widget(self, widget, refresh):
        if refresh: self.updateGUI.emit()
        self.GW.setCurrentIndex(self.GW.indexOf(widget))

    """def included_Drinks_widget1(self, stacked_widget):

        def delete_drink(drink):
            try:
                self.RasBari.DrinkList.pop(drink)
                self.live_drink = self.live_drink - 1
                if self.live_drink < 0: self.live_drink = len(self.RasBari.DrinkList) - 1
                self.drink_txt_label.setText(self.RasBari.DrinkList[self.live_drink].getIngredientString())
            except:
                self.drink_txt_label.setText("No more drinks in the system...")

        std_height = self.button_height
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

        def updateWidget():
            if (len(self.RasBari.DrinkList) != 0 & self.flag == 1): self.live_drink = 0

            self.flag == 1

            try:
                self.drink_txt_label.setText(self.RasBari.DrinkList[self.live_drink].getIngredientString())
            except:
                self.drink_txt_label.setText("No more drinks in the system...")

        self.updateGUI.connect(lambda: updateWidget())

    def tuneDrink(self, stacked_widget, drink_nr):

        def change_value(calling_slider):

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

        std_height = self.button_height
        std_width = self.button_width
        std_y = self.bottom_button_y

        space_width = self.button_width * 1.8
        space_x = self.GUI_Width / 2 - space_width / 2
        topspace = self.GUI_Height * 0.16

        slider_width = std_width * 0.83
        amount_width = std_height
        name_width = slider_width - amount_width

        space_bt_elements = (space_width - slider_width - name_width - amount_width) / 2
        slider_x = (self.GUI_Width / 2) - (slider_width + name_width + amount_width + 2 * space_bt_elements) / 2
        name_x = slider_x + space_bt_elements + slider_width
        amount_x = name_x + space_bt_elements + name_width

        exit_button_x = self.GUI_Width / 2 - self.button_width / 2
        change_left_x = self.bottom_button_getin
        change_right_x = self.GUI_Width - self.bottom_button_getin - self.button_width

        slider = []
        name = []
        amount = []
        name_list = []


        j = 1
        page = 0
        nr_ingredients = 0

        for i in range(1, len(self.RasBari.DrinkList[drink_nr].Ingredients)):
            if self.RasBari.DrinkList[drink_nr].Ingredients[i][1] != "0":
                nr_ingredients = nr_ingredients + 1

        nr_widgets = int(len(self.RasBari.DrinkList) / 4)

        if nr_ingredients < 4: nr_widgets = nr_widgets - 1
        if nr_ingredients > 4: nr_widgets = nr_widgets + 1

        for i in range(nr_widgets):
            self.helpWig = QtWidgets.QWidget()
            self.helpWig.setObjectName("helpWig" + str(i))
            self.help_pages.extend([self.helpWig])

            self.header(self.helpWig)

            self.Name = QtWidgets.QLabel(self.helpWig)
            self.Name.setGeometry(QtCore.QRect(space_x, topspace, space_width, std_height))
            self.Name.setObjectName("Drink_Name")
            self.Name.setText(self.RasBari.DrinkList[drink_nr].Ingredients[0][1])
            self.stdLabelSetUp(self.Name)
            stacked_widget.addWidget(self.helpWig)

        for l in range(1, len(self.RasBari.DrinkList[drink_nr].Ingredients)):
            if self.RasBari.DrinkList[drink_nr].Ingredients[l][1] != "0":
                name_list.extend([self.RasBari.DrinkList[drink_nr].Ingredients[l]])


        for i in range(nr_ingredients):

            if (0 == i % 4) & (i != 0):
                page = page + 1
                j = 1

            line_y = topspace + j * (std_height + self.top_space * 1.7)

            self.help_slider = QtWidgets.QSlider(Qt.Horizontal, self.help_pages[page])
            slider.extend([self.help_slider])
            slider[i].setMaximum(100)
            slider[i].setMinimum(1)
            slider[i].setSliderPosition(int(name_list[i][1]))
            slider[i].setGeometry(QtCore.QRect(slider_x, line_y, slider_width, std_height))

            self.help_name = QtWidgets.QLabel(self.help_pages[page])
            name.extend([self.help_name])
            name[i].setText(name_list[i][0])
            name[i].setGeometry(QtCore.QRect(name_x, line_y, name_width, std_height))
            self.stdLabelSetUp(name[i])

            self.help_amount = QtWidgets.QLabel(self.help_pages[page])
            amount.extend([self.help_amount])
            amount[i].setText(name_list[i][1])
            amount[i].setGeometry(QtCore.QRect(amount_x, line_y, amount_width, std_height))
            self.stdLabelSetUp(amount[i])

            self.exit_button = QtWidgets.QPushButton(self.help_pages[page])
            self.exit_button.setGeometry(QtCore.QRect(exit_button_x, std_y, std_width, std_height))
            self.exit_button.setText("Exit")
            self.exit_button.clicked.connect(lambda: self.show_widget(self.main_widget, 1))

            self.Back = QtWidgets.QPushButton(self.help_pages[page])
            self.Back.setGeometry(QtCore.QRect(change_left_x, std_y, std_width, std_height))
            self.Back.setText("Back")
            self.Back.clicked.connect(lambda: self.show_widget(self.included_Drinks_widget, 1))

            self.Apply = QtWidgets.QPushButton(self.help_pages[page])
            self.Apply.setGeometry(QtCore.QRect(change_right_x, std_y, std_width, std_height))
            self.Apply.setText("Apply changes")
            self.Apply.clicked.connect(lambda: self.apply_drink_tune(drink_nr, slider, name))

            slider[i].sliderReleased.connect(partial(new_maximum, i))
            slider[i].valueChanged.connect(partial(change_value, i))

            j = j + 1

        if nr_ingredients > 4:

            for i in range(len(self.help_pages)):
                try:
                    self.side_navigation(self.help_pages[i], self.help_pages[i - 1], self.help_pages[i + 1])

                except:
                    self.side_navigation(self.help_pages[i], self.help_pages[i - 1], self.help_pages[0])

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
        self.show_widget(self.included_Drinks_widget, 1)

    def change_live_drink(self, direction):
        if direction == 1:
            self.live_drink = self.live_drink + 1
            if self.live_drink > len(self.RasBari.DrinkList) - 1: self.live_drink = 0
        if direction == 0:
            self.live_drink = self.live_drink - 1
            if self.live_drink < 0: self.live_drink = len(self.RasBari.DrinkList) - 1

        try:
            self.drink_txt_label.setText(self.RasBari.DrinkList[self.live_drink].getIngredientString())
        except:
            self.drink_txt_label.setText("No more drinks in the system...")


    def check4order(self):

        c4o_thread = myThread(lambda: self.EmailOrder.gotNewOrder())
        self.threadpool.start(c4o_thread)

    def exeOrder(self):

        find = 99
        order = self.EmailOrder.getLastMessageTitel()

        print("Check whats ordered..." + order)

        if ((order != None) & (self.RasBari.getProductionFlag() == False)):

            for i in range(len(self.RasBari.DrinkList)):
                if self.RasBari.DrinkList[i]:
                    if self.RasBari.DrinkList[i].getName().upper() in order.upper():
                        find = i
                        break

        if find != 99:

            reply = self.EmailOrder.orderexecuted + "\n\nYour order: " + self.RasBari.DrinkList[find].getName()

            thread_mail = myThread(lambda: self.EmailOrder.send_mail_to(self.EmailOrder.lastSenderAdress, reply,
                                                                        "Automatic reply from RasBari"))
            self.threadpool.start(thread_mail)

            self.production_thread_handler(find)

        else:
            print("order received but cant offer - Sorry")

            if self.RasBari.getProductionFlag():
                thread_mail = myThread(lambda: self.EmailOrder.send_mail_to(self.EmailOrder.lastSenderAdress,
                                                                            self.EmailOrder.orderallreadrunning,
                                                                            "Automatic reply from RasBari"))
                self.threadpool.start(thread_mail)

            else:
                thread_mail = myThread(
                    lambda: self.EmailOrder.send_mail_to(self.EmailOrder.lastSenderAdress, self.EmailOrder.unknownorder,
                                                         "Automatic reply from RasBari"))
                self.threadpool.start(thread_mail)

            print(self.EmailOrder.lastSenderAdress)
            print("Mail sent")"""

    def calculateGUI(self, width, height):

        class lo():
            def __init__(self):
                self.GUI_Width = width * 1.048 * 0.58  # TODO CHANGE THIS !!!
                self.GUI_Height = height * 0.5479

                self.button_space = self.GUI_Height / 100
                self.top_space = self.GUI_Height / 50
                self.bottom_button_getin = self.GUI_Width * 0.05

                self.button_width = self.GUI_Width / 4
                self.button_height = self.GUI_Height * 0.1
                self.txt_height = self.GUI_Height * 0.06

                self.bottom_button_y = self.GUI_Height * 0.84
                self.bottom_txt_y = self.GUI_Height * 0.83 - self.txt_height

        Gui_layout = lo()

        return Gui_layout
