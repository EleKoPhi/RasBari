from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets

from classes.class_Bar import *
from classes.class_eMailGuard import *
from classes.class_myThread import *


class UiGui(QWidget, QObject):
    RasBari = Bar()
    EmailOrder = eMailGuard()

    Bottle_pages = []
    NewDrink_pages = []
    grid_button_list = []
    help_pages = []

    updateGUI = pyqtSignal()
    clear = pyqtSignal()

    live_drink = 0
    flag = 0

    def __init__(self, width, height, global_widget):
        QObject.__init__(self)
        self.MailTimer = QtCore.QTimer()
        self.calculateGUI(width, height)
        self.threadpool = QThreadPool()
        self.GW = global_widget

    def setupUi(self, stacked_widget):

        stacked_widget.setObjectName("stacked_widget")

        ################################### ---> START GUI SETUP <--- #################################################

        stacked_widget.setObjectName("GUI")
        stacked_widget.resize(self.GUI_Width, self.GUI_Height)
        stacked_widget.setMaximumSize(QtCore.QSize(self.GUI_Width, self.GUI_Height))
        stacked_widget.setMinimumSize(QtCore.QSize(self.GUI_Width, self.GUI_Height))

        ################################### ---> BUILD WIDGETS HER <--- ###############################################

        self.main_widget(stacked_widget)
        self.bottle_Widget(stacked_widget)
        self.ingredient_Widget(stacked_widget)
        self.newdrink_widget(stacked_widget)
        self.drinks_menue_widget(stacked_widget)
        self.included_Drinks_widget(stacked_widget)

        ################################### ---> END GUI OBJECTS <--- #################################################

        QtCore.QMetaObject.connectSlotsByName(stacked_widget)

        ############################### ---> START CONNECTION [CodeSignals]<--- #######################################

        self.RasBari.missingIngred.connect(lambda: self.show_widget(self.ingredWidg, 1))
        self.RasBari.drinkunknown.connect(lambda: self.showmsgbox)
        self.RasBari.changedValSig.connect(self.update_progressbar)
        self.RasBari.changedAmountSig.connect(self.update_glass_txt)
        self.RasBari.changedStatus.connect(self.update_status_txt)

        self.EmailOrder.CheckMail.connect(self.exeOrder)

        ################################### ---> START TIMER <--- #####################################################

        self.MailTimer.setSingleShot(False)
        if getFlag("Mailorder") & self.EmailOrder.status: self.MailTimer.start(3000)
        self.MailTimer.timeout.connect(lambda: self.check4order())

        ################################### ---> END TIMER <--- #######################################################

        main_widget_index = stacked_widget.indexOf(self.main_widget)
        stacked_widget.setCurrentIndex(main_widget_index)
        QtCore.QMetaObject.connectSlotsByName(stacked_widget)

        ################################### ---> END setUp_Ui <--- ####################################################

    def main_widget(self, stacked_widget):

        # Build of new widget

        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setObjectName("Mainwig")
        stacked_widget.addWidget(self.main_widget)

        # std. values

        std_y = self.bottom_button_y
        std_txt_y = self.bottom_txt_y
        std_hight = self.button_height
        std_hight_txt = self.txt_height
        std_width = self.button_width

        # Headline - Contains Software title

        self.header(self.main_widget)

        self.button_grid()

        # Progessbar that shows the progress of the mixture

        Progress_x = self.bottom_button_getin
        Progress_y = self.bottom_txt_y * 0.87
        Progress_width = self.GUI_Width - 2 * self.bottom_button_getin
        Progress_hight = self.GUI_Height * 0.08

        self.Progress = QtWidgets.QProgressBar(self.main_widget)
        self.Progress.setGeometry(QtCore.QRect(Progress_x, Progress_y, Progress_width, Progress_hight))
        self.Progress.setProperty("value", 0)
        self.Progress.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.Progress.setObjectName("Progress")

        # AddAmount & SubtactAmount - Pushbutton to change the drink size

        AddAmount_x = self.bottom_button_getin + self.button_width - self.button_height
        SubtracAmount_x = self.bottom_button_getin

        self.AddAmount = QtWidgets.QPushButton(self.main_widget)
        self.AddAmount.setGeometry(QtCore.QRect(AddAmount_x, std_y, std_hight, std_hight))
        self.AddAmount.setText("+")

        self.AddAmount.clicked.connect(lambda: self.RasBari.change_volume(+10))

        self.SubtractAmount = QtWidgets.QPushButton(self.main_widget)
        self.SubtractAmount.setGeometry(QtCore.QRect(SubtracAmount_x, std_y, std_hight, std_hight))
        self.SubtractAmount.setText("-")

        self.SubtractAmount.clicked.connect(lambda: self.RasBari.change_volume(-10))

        # LCD Display that shows the drink size

        amount_LCD_Width = std_width - 2 * std_hight - 2 * self.button_space
        amount_LCD_x = self.bottom_button_getin + (std_width / 2) - (amount_LCD_Width / 2)

        self.amount_LCD = QtWidgets.QLCDNumber(self.main_widget)
        self.amount_LCD.setGeometry(QtCore.QRect(amount_LCD_x, std_y, amount_LCD_Width, std_hight))
        self.amount_LCD.setAutoFillBackground(False)
        self.amount_LCD.setFrameShape(QtWidgets.QFrame.Panel)
        self.amount_LCD.setFrameShadow(QtWidgets.QFrame.Raised)
        self.amount_LCD.setLineWidth(2)
        self.amount_LCD.setMidLineWidth(1)
        self.amount_LCD.setSmallDecimalPoint(True)
        self.amount_LCD.setDigitCount(3)
        self.amount_LCD.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.amount_LCD.setProperty("intValue", self.RasBari.getAmount())
        self.amount_LCD.setObjectName("amount_LCD")

        # Exit - Pushbutton to stop the production thread

        Exit_x = self.GUI_Width - self.bottom_button_getin - self.button_width

        stopFont = QtGui.QFont()
        stopFont.setPointSize(26)
        stopFont.setBold(True)
        stopFont.setItalic(False)
        stopFont.setWeight(75)

        self.Exit = QtWidgets.QPushButton(self.main_widget)
        self.Exit.setGeometry(QtCore.QRect(Exit_x, std_y, std_width, std_hight))
        self.Exit.setObjectName("Exit")
        self.Exit.setFont(stopFont)
        self.Exit.setText("STOP")
        self.Exit.setStyleSheet("background-color: red")

        self.Exit.clicked.connect(lambda: self.RasBari.errorFunction())

        # DigitText - Textbox that shows the dink size

        DigitText_x = self.bottom_button_getin

        self.DigitText = QtWidgets.QLabel(self.main_widget)
        self.DigitText.setGeometry(QtCore.QRect(DigitText_x, std_txt_y, std_width, std_hight_txt))
        self.DigitText.setObjectName("Glasvolume")
        self.stdLabelSetUp(self.DigitText)

        GlasString = "Glass volume: " + str(self.RasBari.getAmount()) + " ml"

        self.DigitText.setText(GlasString)

        # StatTxt - Textbox in the bottom right corner - shows system status

        StatTxt_x = self.GUI_Width - self.bottom_button_getin - self.button_width

        self.StatTxt = QtWidgets.QLabel(self.main_widget)
        self.StatTxt.setGeometry(QtCore.QRect(StatTxt_x, std_txt_y, std_width, std_hight_txt))
        self.StatTxt.setObjectName("Status-text-box")
        self.StatTxt.setText("Status: Wait for input...")
        self.stdLabelSetUp(self.StatTxt)

        # TxtBox_middle - Textbox in the center bottom of the main GUI

        TxtBox_middle_x = self.GUI_Width / 2 - self.button_width / 2

        self.TxtBox_middle = QtWidgets.QLabel(self.main_widget)
        self.TxtBox_middle.setGeometry(QtCore.QRect(TxtBox_middle_x, std_txt_y, std_width, std_hight_txt))
        self.TxtBox_middle.setObjectName("Middle_Txt_Box")
        self.TxtBox_middle.setText("Welcome")
        self.stdLabelSetUp(self.TxtBox_middle)

        # Bottles - Button for navigation from main widget to bottles widgt

        Bottles_x = (self.GUI_Width / 2 - self.button_width / 2)
        Bottles_width = self.button_width / 2 - self.button_space / 2

        self.Bottles = QtWidgets.QPushButton(self.main_widget)
        self.Bottles.setGeometry(QtCore.QRect(Bottles_x, std_y, Bottles_width, std_hight))
        self.Bottles.setText("Bottles")

        self.Bottles.clicked.connect(lambda: self.show_widget(self.Bottle_pages[0], 1))

        # Drinks - Button for navigation from main widget to driks widget

        Drinks_x = (self.GUI_Width / 2 - self.button_width / 2) + Bottles_width + self.button_space
        Drinks_width = Bottles_width

        self.Drinks = QtWidgets.QPushButton(self.main_widget)
        self.Drinks.setGeometry(QtCore.QRect(Drinks_x, std_y, Drinks_width, std_hight))
        self.Drinks.setText("Drinks")

        self.Drinks.clicked.connect(lambda: self.show_widget(self.drinks_menue_widget, 1))

        def updateWidget():

            self.GridLayout = self.main_widget.findChild(QtWidgets.QWidget, "gridLayoutWidget")
            self.ButtonGrid = self.main_widget.findChild(QtWidgets.QGridLayout, "AuswahlGrid")

            try:
                self.GridLayout.deleteLater()
                self.ButtonGrid.deleteLater()

                for i in range(len(self.grid_button_list)):
                    Button = self.main_widget.findChild(QtWidgets.QPushButton, "Button_" + str(i))
                    Button.disconect()
                    Button.deleteLater()

                self.button_grid()

            except:
                self.button_grid()

        self.updateGUI.connect(lambda: updateWidget())

        ################################### END of main_Widget(self, stacked_widget) ####################################

    def bottle_Widget(self, stacked_widget):

        # Function to update bottle_Widget (progressbar)

        def updateWidget():
            for i in range(0, len(lines)):
                lines[i].updateStatusBar()

        # std. values

        lines = []
        top_space = self.GUI_Height * 0.16
        button_txt = ["<- Change left", "Exit", "Change right ->"]

        # Signals for showing the fist bottle widget & updating all statusbar's

        self.updateGUI.connect(updateWidget)

        # Calculate the necessary number of bottle_Widgets

        nr_widgets = int(len(self.RasBari.Bottles) / 5)

        if len(self.RasBari.Bottles) % 5 != 0:
            nr_widgets += 1

        # Build all necessary widgets, to show all bottles included in Rasbari

        for i in range(nr_widgets):
            self.Bottle_pages.extend([QtWidgets.QWidget()])
            self.Bottle_pages[i].setObjectName("Bottlepage" + str(i))
            stacked_widget.addWidget(self.Bottle_pages[i])
            self.header(self.Bottle_pages[i])

        # Build the bottomNavigation for every bottle_Widget

        for i in range(len(self.Bottle_pages)):

            page_left = self.Bottle_pages[i - 1]

            try:
                page_right = self.Bottle_pages[i + 1]
            except:
                page_right = self.Bottle_pages[0]

            self.bottomNavigation(self.Bottle_pages[i], page_left, page_right, self.main_widget, button_txt)

        # Build for every bottle one line that's shows - NAME - LEVEL + REST_Button + CLEAR_Button

        page = -1
        j = 0

        for i in range(len(self.RasBari.Bottles)):

            if i % 5 == 0:
                page += 1
                j = 0

            line_y = top_space + j * (self.button_height + self.top_space * 1.7)

            lines.extend([self.BottleLine(self, self.Bottle_pages[page], self.RasBari.Bottles[i], 0, line_y)])

            j += 1

        ############################ END of bottle_Widget(self, widgetA, widgetB, StackedWidget) #######################

    def ingredient_Widget(self, stacked_widget):

        # Build of new widget

        self.ingredWidg = QtWidgets.QWidget()
        self.ingredWidg.setObjectName("Missing_Ingred")
        stacked_widget.addWidget(self.ingredWidg)

        # Std. values

        std_width = self.button_width
        std_hight = self.button_height

        # Headline - Contains Software title

        self.header(self.ingredWidg)

        # YESBut - Button for navigation to the bottle widget

        YESBut_x = self.bottom_button_getin
        YESBut_y = self.GUI_Height / 2 - std_hight / 2
        FstBottleWidgetIndex = stacked_widget.indexOf(self.Bottle_pages[0])

        self.YESBut = QtWidgets.QPushButton(self.ingredWidg)
        self.YESBut.setGeometry(QtCore.QRect(YESBut_x, YESBut_y, std_width, std_hight))
        self.YESBut.setText("Yes")

        self.YESBut.clicked.connect(lambda: self.GW.setCurrentIndex(FstBottleWidgetIndex))

        # NOBut - Button for navigation to the main widget

        NOBut_x = self.GUI_Width - self.bottom_button_getin - self.button_width
        NOBut_y = YESBut_y

        self.NOBut = QtWidgets.QPushButton(self.ingredWidg)
        self.NOBut.setGeometry(QtCore.QRect(NOBut_x, NOBut_y, std_width, std_hight))
        self.NOBut.setText("No")

        self.NOBut.clicked.connect(lambda: self.show_widget(self.main_widget, 1))

        # Message - Textbrowser that shows the message for missing ingredients

        Message_x = self.GUI_Width / 2 - std_width / 2
        Message_y = self.GUI_Height / 2 - std_hight
        Message_hight = std_hight * 2
        Message_content = "You have missing ingredients\n\nDo you want to reset them?\nPlease make a desision"

        self.Message = QtWidgets.QTextBrowser(self.ingredWidg)
        self.Message.setGeometry(QtCore.QRect(Message_x, Message_y, std_width, Message_hight))
        self.Message.setText(Message_content)

        ############################ END of ingredient_Widget(self, widget, stacked_widget) #############################

    #### Function for the newdrink_widget start ####

    def newdrink_widget(self, stacked_widget):

        def Amount_Slider(i):
            amount[i].setText(str(slider[i].value()))

            sum = 0

            for i in range(len(slider)):
                sum = sum + slider[i].value()

            message = "amount: %d/100" % sum
            add = ""

            if sum < 100:
                add = "\nplease add %d%% more" % (100 - sum)
            if sum == 100:
                add = "\nPress save to add your drink!"
            if sum == 0:
                message = ""
                add = "Make your drink!"

            for i in range(len(stats)):
                stats[i].setText(message + add)

        def newMaxima(callingSlider):
            sum = 0

            for i in range(len(slider)):
                sum = sum + slider[i].value()

            if sum >= 100:
                slider[callingSlider].setSliderPosition(slider[callingSlider].value() - (sum - 100))

        slider = []
        name = []
        amount = []
        stats = []

        std_Hight = self.button_height
        std_Width = self.button_width
        std_Y = self.bottom_button_y
        Topspace = self.GUI_Height * 0.16
        possible_spcae = self.button_width * 1.8

        slider_width = std_Width * 0.83
        amount_width = std_Hight
        name_width = slider_width - amount_width

        page = 0
        j = 0

        totalNr_Widgets = int(len(self.RasBari.DrinkList) / 5)

        space_bt_elements = (possible_spcae - slider_width - name_width - amount_width) / 2
        slider_x = (self.GUI_Width / 2) - (slider_width + name_width + amount_width + 2 * space_bt_elements) / 2
        name_x = slider_x + space_bt_elements + slider_width
        amount_x = name_x + space_bt_elements + name_width
        Stat_x = self.GUI_Width - self.bottom_button_getin - self.button_width

        if len(self.RasBari.DrinkList) % 5 != 0:
            totalNr_Widgets += 1

        for i in range(totalNr_Widgets):
            self.NewDrink_pages.extend([QtWidgets.QWidget()])
            self.NewDrink_pages[i].setObjectName("NewDrink_page" + str(i))
            stacked_widget.addWidget(self.NewDrink_pages[i])
            self.header(self.NewDrink_pages[i])
            self.newdrink_bottom_navigation(slider, self.NewDrink_pages[i])

        for i in range(len(self.NewDrink_pages)):
            try:
                self.side_navigation(self.NewDrink_pages[i], self.NewDrink_pages[i - 1], self.NewDrink_pages[i + 1])

            except:
                self.side_navigation(self.NewDrink_pages[i], self.NewDrink_pages[i - 1], self.NewDrink_pages[0])

            self.help_slider = QtWidgets.QLabel(self.NewDrink_pages[i])
            self.help_slider.setGeometry(QtCore.QRect(Stat_x, std_Y, std_Width, std_Hight))
            self.help_slider.setText("Make your drink!")
            self.stdLabelSetUp(self.help_slider)
            stats.extend([self.help_slider])

        for i in range(len(self.RasBari.Bottles)):

            if ((i % 5 == 0) & (i != 0)):
                page = page + 1
                j = 0

            line_y = Topspace + j * (std_Hight + self.top_space * 1.7)

            self.help_slider = QtWidgets.QSlider(Qt.Horizontal, self.NewDrink_pages[page])
            slider.extend([self.help_slider])
            slider[i].setMaximum(100)
            slider[i].setMinimum(0)
            slider[i].setGeometry(QtCore.QRect(slider_x, line_y, slider_width, std_Hight))

            self.help_name = QtWidgets.QLabel(self.NewDrink_pages[page])
            name.extend([self.help_name])
            name[i].setText(self.RasBari.Bottles[i].getname())
            name[i].setGeometry(QtCore.QRect(name_x, line_y, name_width, std_Hight))
            self.stdLabelSetUp(name[i])

            self.help_amount = QtWidgets.QLabel(self.NewDrink_pages[page])
            amount.extend([self.help_amount])
            amount[i].setText("0")
            amount[i].setGeometry(QtCore.QRect(amount_x, line_y, amount_width, std_Hight))
            self.stdLabelSetUp(amount[i])

            slider[i].valueChanged.connect(partial(Amount_Slider, i))
            slider[i].valueChanged.connect(partial(newMaxima, i))

            self.updateGUI.connect(lambda: self.reset_slider_list(slider))

            j = j + 1

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

    #### Function for the newdrink_widget end ####

    def drinks_menue_widget(self, stacked_widget):

        # Build of new widget

        self.drinks_menue_widget = QtWidgets.QWidget()
        self.drinks_menue_widget.setObjectName("Drink_menue")
        stacked_widget.addWidget(self.drinks_menue_widget)

        # Std. values

        std_height = self.button_height
        std_width = self.button_width
        std_width_menue = self.GUI_Width / 2 - self.bottom_button_getin * 1.5
        std_y_menue = self.GUI_Height / 2 - std_height / 2
        std_y = self.bottom_button_y

        # Headline - Contains Software title

        self.header(self.drinks_menue_widget)

        # NewDrink pushbutton to navigate to the newdrink widget

        self.newdrink_button = QtWidgets.QPushButton(self.drinks_menue_widget)
        self.newdrink_button.setGeometry(
            QtCore.QRect(self.bottom_button_getin, std_y_menue, std_width_menue, std_height))
        self.newdrink_button.setText("Let me make a new drink!")

        self.newdrink_button.clicked.connect(lambda: self.show_widget(self.NewDrink_pages[0], 1))

        # ShowDrink pushbutton to naviate to the widget that shows all included drinks

        show_drink_x = self.GUI_Width - self.bottom_button_getin - std_width_menue

        self.showdrink_button = QtWidgets.QPushButton(self.drinks_menue_widget)
        self.showdrink_button.setGeometry(QtCore.QRect(show_drink_x, std_y_menue, std_width_menue, std_height))
        self.showdrink_button.setText("Show included drinks!")

        self.showdrink_button.clicked.connect(lambda: self.show_widget(self.included_Drinks_widget, 1))

        # ExitButton - Button to navigate back to the main widget

        exit_button_x = (self.GUI_Width / 2 - self.button_width / 2)

        self.exit_button = QtWidgets.QPushButton(self.drinks_menue_widget)
        self.exit_button.setGeometry(QtCore.QRect(exit_button_x, std_y, std_width, std_height))
        self.exit_button.setText("Exit")

        self.exit_button.clicked.connect(lambda: self.show_widget(self.main_widget, 1))

    def included_Drinks_widget(self, stacked_widget):

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

        self.included_Drinks_widget = QtWidgets.QWidget()
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
            if (len(self.RasBari.DrinkList) != 0): self.live_drink = 0

            try:
                self.drink_txt_label.setText(self.RasBari.DrinkList[self.live_drink].getIngredientString())
            except:
                self.drink_txt_label.setText("No more drinks in the system...")

        self.updateGUI.connect(lambda: updateWidget())

    def tuneDrink(self, stacked_widget, drink_nr):

        def change_value(calling_slider):
            amount[calling_slider].setText(str(slider[calling_slider].value()))

        def new_maximum(calling_slider):
            ingred_sum = 0
            start_slider = calling_slider

            for loop_iteration in range(len(slider)):
                ingred_sum = ingred_sum + slider[loop_iteration].value()

            ingred_sum = ingred_sum - 100

            if ingred_sum > 0:
                while True:
                    if (start_slider != calling_slider) and (slider[start_slider].value() != 0):
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
            slider[i].setMinimum(0)
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
            self.Apply.clicked.connect(lambda: print("settings"))  # TODO include the apply function her

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

        self.show_widget(self.help_pages[0], 1)

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

    def production_thread_handler(self, drink_nr):

        self.RasBari.changeErrorFlag(False)

        if not self.RasBari.getProductionFlag():

            if self.RasBari.DrinkList[drink_nr]:

                thread = myThread(lambda: self.RasBari.mixIt(drink_nr))
                progressbar = myThread(self.update_progressbar)
                self.threadpool.start(thread)
                self.threadpool.start(progressbar)
            else:

                print("Drink unknown")
                self.RasBari.changeProductionFlag(False)

        else:
            print("Production already running")

    def exit_thread_handler(self):
        exit_thread = myThread(self.RasBari.errorFunction)
        self.threadpool.start(exit_thread)

    def show_widget(self, widget, refresh):
        if refresh: self.updateGUI.emit()
        self.GW.setCurrentIndex(self.GW.indexOf(widget))

    #### Functions for updating the GUI start ####

    def update_progressbar(self):
        self.Progress.setValue(self.RasBari.getProgress())

    def update_glass_txt(self):

        self.amount_LCD.display(self.RasBari.getAmount())
        glas_string = "Glass volume: " + str(self.RasBari.getAmount()) + " ml"
        self.DigitText.setText(glas_string)

    def update_status_txt(self):

        if not self.RasBari.getProductionFlag():
            self.StatTxt.setText("Status: Wait for input...")
        else:
            self.StatTxt.setText("Status: Busy")

    #### Functions for updating the GUI end ####

    #### Functions for the email guard start ####

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
            print("Mail sent")

    #### Functions for the email guard end ####

    #### Functions for simplified GUI build start ####

    def calculateGUI(self, width, height):

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

    def header(self, widget):

        title_font = QtGui.QFont()
        title_font.setPointSize(26)
        title_font.setBold(True)
        title_font.setItalic(False)
        title_font.setWeight(75)

        self.title = QtWidgets.QLabel(widget)
        self.title.setGeometry(QtCore.QRect(0, self.top_space, self.GUI_Width, self.GUI_Height * 0.1))
        self.title.setFont(title_font)
        self.title.setText("Rasbari V5")
        self.stdLabelSetUp(self.title)

    def bottomNavigation(self, widget, destination_left, destination_right, destination_middle, button_txt):

        std_width = self.button_width
        std_height = self.button_height

        middle_x = self.GUI_Width / 2 - self.button_width / 2
        left_x = self.bottom_button_getin
        right_x = self.GUI_Width - self.bottom_button_getin - self.button_width
        std_y = self.bottom_button_y

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

        possible_spcae = self.button_width * 1.8

        Next_button_size = self.button_height * 1.5
        Next_button_y = self.GUI_Height / 2 - Next_button_size / 2
        Next_left_x = (self.GUI_Width / 2 - possible_spcae / 2) / 2 - Next_button_size / 2
        Next_right_x = self.GUI_Width - Next_left_x - Next_button_size

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

    def newdrink_bottom_navigation(self, slider, widget):

        std_height = self.button_height
        std_width = self.button_width
        std_y = self.bottom_button_y

        # ExitButton - Button to navigate from the first drink widget back to the main widget

        exit_button_x = (self.GUI_Width / 2 - self.button_width / 2)

        self.exit_button = QtWidgets.QPushButton(widget)
        self.exit_button.setGeometry(QtCore.QRect(exit_button_x, std_y, std_width, std_height))
        self.exit_button.setText("Exit")
        self.exit_button.clicked.connect(lambda: self.show_widget(self.main_widget, 1))

        # Save - Button to Save the current drink setup as a new drink

        self.Save = QtWidgets.QPushButton(widget)
        self.Save.setGeometry(QtCore.QRect(self.bottom_button_getin, std_y, std_width, std_height))
        self.Save.setText("Save Drink")
        self.Save.clicked.connect(lambda: self.saveNewDrink(slider, self.RasBari.Bottles))

    def button_grid(self):

        # gridWidget contains all buttons, that start a mixture

        if 0 != len(self.RasBari.DrinkList):

            grid_widget_x = 0
            grid_widget_y = self.button_height + self.top_space
            grid_width = self.GUI_Width
            grid_height = self.GUI_Height * 0.55

            self.grid_layout_widget = QtWidgets.QWidget(self.main_widget)
            self.grid_layout_widget.setGeometry(QtCore.QRect(grid_widget_x, grid_widget_y, grid_width, grid_height))
            self.grid_layout_widget.setObjectName("gridLayoutWidget")

            self.ButtonGrid = QtWidgets.QGridLayout(self.grid_layout_widget)
            self.ButtonGrid.setObjectName("buttongrid")

            number_of_rows = -(-len(self.RasBari.DrinkList) // 4)
            grid_button_height = grid_height / number_of_rows * 0.9
            grid_button_width = grid_width / 4 * 0.8

            column = 0
            line = 0

            # include the buttons in the ButtonGrid

            self.grid_button_list.clear()

            for i in range(len(self.RasBari.DrinkList)):

                self.grid_button_list.extend([QtWidgets.QPushButton(self.grid_layout_widget)])
                self.grid_button_list[i].setMinimumSize(QtCore.QSize(grid_button_width, grid_button_height))
                self.grid_button_list[i].setObjectName("Button_" + str(i))
                self.grid_button_list[i].setText(self.RasBari.DrinkList[i].getName())
                self.grid_button_list[i].clicked.connect(partial(self.production_thread_handler, i))
                self.ButtonGrid.addWidget(self.grid_button_list[i], line, column)

                column = column + 1

                if column == 4:
                    column = 0
                    line = line + 1

    def stdLabelSetUp(self, label):
        label.setAlignment(Qt.AlignCenter)
        label.setFrameShape(6)
        label.setStyleSheet("background-color: white")

    #### Functions for simplified GUI build end ####

    ####################################--Classes for simplyfied GUI design--###########################################

    class BottleLine():
        def __init__(self, Master, widget, Bottle, total_x, total_y):
            self.wg = widget
            self.Bottle_in = Bottle
            self.rev_x = total_x + 10
            self.rev_y = total_y
            self.main_gui = Master

            self.build_line()

        def build_line(self):

            self.BottleNameDsp = QtWidgets.QLabel(self.wg)
            self.BottleNameDsp.setGeometry(
                QtCore.QRect(self.rev_x, self.rev_y, self.main_gui.GUI_Width * 0.145, self.main_gui.button_height))
            self.BottleNameDsp.setObjectName("Bottle Name")
            self.BottleNameDsp.setText(self.Bottle_in.getname())
            self.stdLabelSetUp(self.BottleNameDsp)

            xLevel = self.rev_x + self.main_gui.GUI_Width * 0.145 + self.main_gui.top_space

            self.level = QtWidgets.QProgressBar(self.wg)
            self.level.setGeometry(
                QtCore.QRect(xLevel, self.rev_y, self.main_gui.GUI_Width * 0.3, self.main_gui.button_height))
            self.level.setProperty("value",
                                   (int(self.Bottle_in.getRest()) / (int(self.Bottle_in.getbottlesize()))) * 100)

            xClear = xLevel + self.main_gui.top_space + self.main_gui.GUI_Width * 0.3

            self.ClearButton = QtWidgets.QPushButton(self.wg)
            self.ClearButton.setGeometry(
                QtCore.QRect(xClear, self.rev_y, self.main_gui.button_width, self.main_gui.button_height))
            self.ClearButton.setText("Output")

            xResetbutton = xClear + self.main_gui.top_space + self.main_gui.button_width

            self.Resetbutton = QtWidgets.QPushButton(self.wg)
            self.Resetbutton.setGeometry(
                QtCore.QRect(xResetbutton, self.rev_y, self.main_gui.button_width, self.main_gui.button_height))
            self.Resetbutton.setText("RESET")

            self.Resetbutton.clicked.connect(lambda: self.placeNewBottle())
            self.ClearButton.clicked.connect(lambda: self.emptyBottle())

        def placeNewBottle(self):

            print("Reset Bottle")

            for i in range(len(UiGui.RasBari.Bottles)):

                if self.Bottle_in.getname() == UiGui.RasBari.Bottles[i].getname():
                    UiGui.RasBari.Bottles[i].putAmount(UiGui.RasBari.Bottles[i].getbottlesize())
                    print(UiGui.RasBari.Bottles[i].getlevel())
                    self.Bottle_in = UiGui.RasBari.Bottles[i]
                    break

            self.level.setProperty("value",
                                   (int(self.Bottle_in.getlevel()) / (int(self.Bottle_in.getbottlesize()))) * 100)

        def emptyBottle(self):

            print("empty Bottle")

            self.Bottle_in.getliqout()
            self.level.setProperty("value",
                                   (int(self.Bottle_in.getlevel()) / (int(self.Bottle_in.getbottlesize()))) * 100)

        def updateStatusBar(self):

            for i in range(len(UiGui.RasBari.Bottles)):
                if self.Bottle_in.getname() == UiGui.RasBari.Bottles[i].getname():

                    self.Bottle_in = UiGui.RasBari.Bottles[i]
                    value = int((int(UiGui.RasBari.Bottles[i].getlevel()) / int(self.Bottle_in.getbottlesize())) * 100)
                    if value < 0: value = 0
                    self.level.setProperty("value", value)
                    break

        def stdLabelSetUp(self, Label):
            Label.setAlignment(Qt.AlignCenter)
            Label.setFrameShape(6)
            Label.setStyleSheet("background-color: white")
