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
    GridButton = []

    showBottlewidget = pyqtSignal()
    showDrinkwidget = pyqtSignal()
    updateGUI = pyqtSignal()
    clear = pyqtSignal()

    live_drink = 0

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

        ################################### ---> BUILD WIDGETS HER <--- ###############################################

        self.main_Widget(stacked_widget)
        self.bottle_Widget(stacked_widget)
        self.ingredient_Widget(stacked_widget)
        self.newDrink_Widget(stacked_widget)
        self.drinks_menue_widget(stacked_widget)
        self.included_Drinks_widget(stacked_widget)

        ################################### ---> END GUI OBJECTS <--- #################################################

        QtCore.QMetaObject.connectSlotsByName(stacked_widget)

        ############################### ---> START CONNECTION [CodeSignals]<--- #######################################

        self.RasBari.missingIngred.connect(self.showIngred_widget)
        self.RasBari.drinkunknown.connect(lambda: self.showmsgbox)
        self.RasBari.changedValSig.connect(self.upDateStatusBar)
        self.RasBari.changedAmountSig.connect(self.upDateTxt)
        self.RasBari.changedStatus.connect(self.UpdateStausTxt)

        self.EmailOrder.CheckMail.connect(self.exeOrder)

        ################################### ---> START TIMER <--- #####################################################

        self.MailTimer.setSingleShot(False)
        if getEmailGuardStat() & self.EmailOrder.status: self.MailTimer.start(3000)
        self.MailTimer.timeout.connect(lambda: self.check4order())

        ################################### ---> END TIMER <--- #######################################################

        main_widget_index = stacked_widget.indexOf(self.Mainwig)
        stacked_widget.setCurrentIndex(main_widget_index)
        QtCore.QMetaObject.connectSlotsByName(stacked_widget)

        ################################### ---> END setUp_Ui <--- ####################################################

    def main_Widget(self, stacked_widget):

        # Build of new widget

        self.Mainwig = QtWidgets.QWidget()
        self.Mainwig.setObjectName("Mainwig")
        stacked_widget.addWidget(self.Mainwig)

        # std. values

        std_y = self.setUpButtonPos
        std_txt_y = self.setUpTxTPos
        std_Hight = self.setUpButtonHeight
        std_Hight_txt = self.setUpTxTHeight
        std_Width = self.setUpButtonWith

        # Headline - Contains Software title

        self.buildHeader(self.Mainwig, stacked_widget)

        self.buildButtonGrid()

        # Progessbar that shows the progress of the mixture

        Progress_x = self.setUp_getin
        Progress_y = self.setUpTxTPos * 0.87
        Progress_width = self.GUI_Width - 2 * self.setUp_getin
        Progress_hight = self.GUI_Height * 0.08

        self.Progress = QtWidgets.QProgressBar(self.Mainwig)
        self.Progress.setGeometry(QtCore.QRect(Progress_x, Progress_y, Progress_width, Progress_hight))
        self.Progress.setProperty("value", 0)
        self.Progress.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.Progress.setObjectName("Progress")

        # AddAmount & SubtactAmount - Pushbutton to change the drink size

        AddAmount_x = self.setUp_getin + self.setUpButtonWith - self.setUpButtonHeight
        SubtracAmount_x = self.setUp_getin

        self.AddAmount = QtWidgets.QPushButton(self.Mainwig)
        self.AddAmount.setGeometry(QtCore.QRect(AddAmount_x, std_y, std_Hight, std_Hight))
        self.AddAmount.setText("+")

        self.AddAmount.clicked.connect(lambda: self.RasBari.change_volume(+10))

        self.SubtractAmount = QtWidgets.QPushButton(self.Mainwig)
        self.SubtractAmount.setGeometry(QtCore.QRect(SubtracAmount_x, std_y, std_Hight, std_Hight))
        self.SubtractAmount.setText("-")

        self.SubtractAmount.clicked.connect(lambda: self.RasBari.change_volume(-10))

        # LCD Display that shows the drink size

        amount_LCD_Width = std_Width - 2 * std_Hight - 2 * self.space
        amount_LCD_x = self.setUp_getin + (std_Width / 2) - (amount_LCD_Width / 2)

        self.amount_LCD = QtWidgets.QLCDNumber(self.Mainwig)
        self.amount_LCD.setGeometry(QtCore.QRect(amount_LCD_x, std_y, amount_LCD_Width, std_Hight))
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

        Exit_x = self.GUI_Width - self.setUp_getin - self.setUpButtonWith

        stopFont = QtGui.QFont()
        stopFont.setPointSize(26)
        stopFont.setBold(True)
        stopFont.setItalic(False)
        stopFont.setWeight(75)

        self.Exit = QtWidgets.QPushButton(self.Mainwig)
        self.Exit.setGeometry(QtCore.QRect(Exit_x, std_y, std_Width, std_Hight))
        self.Exit.setObjectName("Exit")
        self.Exit.setFont(stopFont)
        self.Exit.setText("STOP")
        self.Exit.setStyleSheet("background-color: red")

        self.Exit.clicked.connect(lambda: self.RasBari.errorFunction())

        # DigitText - Textbox that shows the dink size

        DigitText_x = self.setUp_getin

        self.DigitText = QtWidgets.QTextBrowser(self.Mainwig)
        self.DigitText.setGeometry(QtCore.QRect(DigitText_x, std_txt_y, std_Width, std_Hight_txt))
        self.DigitText.setObjectName("Glasvolume")

        GlasString = "Glass volume: " + str(self.RasBari.getAmount()) + " ml"

        self.DigitText.setText(GlasString)

        # StatTxt - Textbox in the bottom right corner - shows system status

        StatTxt_x = self.GUI_Width - self.setUp_getin - self.setUpButtonWith

        self.StatTxt = QtWidgets.QTextBrowser(self.Mainwig)
        self.StatTxt.setGeometry(QtCore.QRect(StatTxt_x, std_txt_y, std_Width, std_Hight_txt))
        self.StatTxt.setObjectName("Status-text-box")
        self.StatTxt.setText("Status: Wait for input...")

        # TxtBox_middle - Textbox in the center bottom of the main GUI

        TxtBox_middle_x = self.GUI_Width / 2 - self.setUpButtonWith / 2

        self.TxtBox_middle = QtWidgets.QTextBrowser(self.Mainwig)
        self.TxtBox_middle.setGeometry(QtCore.QRect(TxtBox_middle_x, std_txt_y, std_Width, std_Hight_txt))
        self.TxtBox_middle.setObjectName("Middle_Txt_Box")
        self.TxtBox_middle.setText("Welcome")

        # Bottles - Button for navigation from main widget to bottles widgt

        Bottles_x = (self.GUI_Width / 2 - self.setUpButtonWith / 2)
        Bottles_width = self.setUpButtonWith / 2 - self.space / 2

        self.Bottles = QtWidgets.QPushButton(self.Mainwig)
        self.Bottles.setGeometry(QtCore.QRect(Bottles_x, std_y, Bottles_width, std_Hight))
        self.Bottles.setText("Bottles")

        self.Bottles.clicked.connect(lambda: self.showBottlewidget.emit())

        # Drinks - Button for navigation from main widget to driks widget

        Drinks_x = (self.GUI_Width / 2 - self.setUpButtonWith / 2) + Bottles_width + self.space
        Drinks_width = Bottles_width

        self.Drinks = QtWidgets.QPushButton(self.Mainwig)
        self.Drinks.setGeometry(QtCore.QRect(Drinks_x, std_y, Drinks_width, std_Hight))
        self.Drinks.setText("Drinks")

        self.Drinks.clicked.connect(lambda: self.showDrinkwidget.emit())

        def updateWidget():

            self.GridLayout = self.Mainwig.findChild(QtWidgets.QWidget, "gridLayoutWidget")
            self.ButtonGrid = self.Mainwig.findChild(QtWidgets.QGridLayout, "AuswahlGrid")

            try:
                self.GridLayout.deleteLater()
                self.ButtonGrid.deleteLater()

                for i in range(len(self.GridButton)):
                    Button = self.Mainwig.findChild(QtWidgets.QPushButton, "Button_" + str(i))
                    Button.disconect()
                    Button.deleteLater()

                self.buildButtonGrid()

            except:
                self.buildButtonGrid()

        self.updateGUI.connect(lambda: updateWidget())

        ################################### END of main_Widget(self, stacked_widget) ####################################

    def buildButtonGrid(self):

        # gridWidget contains all buttons, that start a mixture

        gridWidget_x = 0
        gridWidget_y = self.setUpButtonHeight + self.space_Gen
        gridWidth = self.GUI_Width
        gridHight = self.GUI_Height * 0.55

        self.gridLayoutWidget = QtWidgets.QWidget(self.Mainwig)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(gridWidget_x, gridWidget_y, gridWidth, gridHight))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.ButtonGrid = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.ButtonGrid.setObjectName("AuswahlGrid")

        numberOfRows = -(-len(self.RasBari.DrinkList) // 4)
        gridButtonHight = gridHight / numberOfRows * 0.9
        gridButtonWidth = gridWidth / 4 * 0.8

        column = 0
        line = 0

        # include the buttons in the ButtonGrid

        i = 0

        self.GridButton.clear()

        for i in range(len(self.RasBari.DrinkList)):

            self.GridButton.extend([QtWidgets.QPushButton(self.gridLayoutWidget)])
            self.GridButton[i].setMinimumSize(QtCore.QSize(gridButtonWidth, gridButtonHight))
            self.GridButton[i].setObjectName("Button_" + str(i))
            self.GridButton[i].setText(self.RasBari.DrinkList[i].getName())
            self.GridButton[i].clicked.connect(partial(self.Button_Thread_Handler, i))
            self.ButtonGrid.addWidget(self.GridButton[i], line, column)

            column = column + 1

            if column == 4:
                column = 0
                line = line + 1

    def bottle_Widget(self, StackedWidget):

        # Function to update bottle_Widget (statusbar)

        def updateWidget():
            for i in range(0, len(Lines)):
                Lines[i].updateStatusBar()

        # std. values

        Lines = []
        Topspace = self.GUI_Height * 0.16
        MainWidgetIndex = StackedWidget.indexOf(self.Mainwig)

        # Signals for showing the fist bottle widget & updating all statusbar's

        self.showBottlewidget.connect(lambda: self.showBottlePage(self.Bottle_pages[0]))
        self.updateGUI.connect(updateWidget)

        # Calculate the necessary number of bottle_Widgets

        totalNr_Widgets = int(len(self.RasBari.Bottles) / 5)

        if len(self.RasBari.Bottles) % 5 != 0:
            totalNr_Widgets += 1

        # Build all necessary widgets, to show all bottles included in Rasbari

        for i in range(totalNr_Widgets):
            self.Bottle_pages.extend([QtWidgets.QWidget()])
            self.Bottle_pages[i].setObjectName("Bottlepage" + str(i))
            StackedWidget.addWidget(self.Bottle_pages[i])
            self.buildHeader(self.Bottle_pages[i], StackedWidget)

        # Build the bottomNavigation for every bottle_Widget

        for i in range(len(self.Bottle_pages)):

            page_left = self.Bottle_pages[i - 1]

            try:
                page_right = self.Bottle_pages[i + 1]
            except:
                page_right = self.Bottle_pages[0]

            self.bottomNavigation(self.Bottle_pages[i], page_left, page_right, MainWidgetIndex)

        # Build for every bottle one line thats shows - NAME - LEVEL + REST_Button + CLEAR_Button

        page = -1
        j = 0

        for i in range(len(self.RasBari.Bottles)):

            if i % 5 == 0:
                page += 1
                j = 0

            line_y = Topspace + j * (self.setUpButtonHeight + self.space_Gen * 1.7)

            Lines.extend([self.BottleLine(self, self.Bottle_pages[page], self.RasBari.Bottles[i], 0, line_y)])

            j += 1

        ############################ END of bottle_Widget(self, widgetA, widgetB, StackedWidget) #######################

    def ingredient_Widget(self, stacked_widget):

        # Build of new widget

        self.ingredWidg = QtWidgets.QWidget()
        self.ingredWidg.setObjectName("Missing_Ingred")
        stacked_widget.addWidget(self.ingredWidg)

        # Std. values

        std_width = self.setUpButtonWith
        std_hight = self.setUpButtonHeight

        # Headline - Contains Software title

        self.buildHeader(self.ingredWidg, stacked_widget)

        # YESBut - Button for navigation to the bottle widget

        YESBut_x = self.setUp_getin
        YESBut_y = self.GUI_Height / 2 - std_hight / 2
        FstBottleWidgetIndex = stacked_widget.indexOf(self.Bottle_pages[0])

        self.YESBut = QtWidgets.QPushButton(self.ingredWidg)
        self.YESBut.setGeometry(QtCore.QRect(YESBut_x, YESBut_y, std_width, std_hight))
        self.YESBut.setText("Yes")

        self.YESBut.clicked.connect(lambda: self.GW.setCurrentIndex(FstBottleWidgetIndex))

        # NOBut - Button for navigation to the main widget

        NOBut_x = self.GUI_Width - self.setUp_getin - self.setUpButtonWith
        NOBut_y = YESBut_y
        MainWidgetIndex = stacked_widget.indexOf(self.Mainwig)

        self.NOBut = QtWidgets.QPushButton(self.ingredWidg)
        self.NOBut.setGeometry(QtCore.QRect(NOBut_x, NOBut_y, std_width, std_hight))
        self.NOBut.setText("No")

        self.NOBut.clicked.connect(lambda: self.GW.setCurrentIndex(MainWidgetIndex))

        # Message - Textbrowser that shows the message for missing ingredients

        Message_x = self.GUI_Width / 2 - std_width / 2
        Message_y = self.GUI_Height / 2 - std_hight
        Message_hight = std_hight * 2
        Message_content = "You have missing ingredients\n\nDo you want to reset them?\nPlease make a desision"

        self.Message = QtWidgets.QTextBrowser(self.ingredWidg)
        self.Message.setGeometry(QtCore.QRect(Message_x, Message_y, std_width, Message_hight))
        self.Message.setText(Message_content)

        ############################ END of ingredient_Widget(self, widget, stacked_widget) #############################

    def newDrink_Widget(self, StackedWidget):

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


        std_Hight = self.setUpButtonHeight
        std_Width = self.setUpButtonWith
        std_Y = self.setUpButtonPos
        Topspace = self.GUI_Height * 0.16
        possible_spcae = self.setUpButtonWith * 1.8

        slider_width = std_Width * 0.9
        name_width = std_Width * 0.4
        amount_width = std_Width * 0.4

        page = 0
        j = 0

        totalNr_Widgets = int(len(self.RasBari.DrinkList) / 5)

        space_bt_elements = (possible_spcae - slider_width - name_width - amount_width) / 2
        slider_x = (self.GUI_Width / 2) - (slider_width + name_width + amount_width + 2 * space_bt_elements) / 2
        name_x = slider_x + space_bt_elements + slider_width
        amount_x = name_x + space_bt_elements + name_width
        Stat_x = self.GUI_Width - self.setUp_getin - self.setUpButtonWith

        if len(self.RasBari.DrinkList) % 5 != 0:
            totalNr_Widgets += 1

        for i in range(totalNr_Widgets):
            self.NewDrink_pages.extend([QtWidgets.QWidget()])
            self.NewDrink_pages[i].setObjectName("NewDrink_page" + str(i))
            StackedWidget.addWidget(self.NewDrink_pages[i])
            self.buildHeader(self.NewDrink_pages[i], StackedWidget)
            self.NewDrink_wig_bottom(slider, self.NewDrink_pages[i])

        for i in range(len(self.NewDrink_pages)):
            try:
                self.newDrinkNavigation(self.NewDrink_pages[i], self.NewDrink_pages[i - 1], self.NewDrink_pages[i + 1])

            except:
                self.newDrinkNavigation(self.NewDrink_pages[i], self.NewDrink_pages[i - 1], self.NewDrink_pages[0])

            self.s = QtWidgets.QTextBrowser(self.NewDrink_pages[i])
            self.s.setGeometry(QtCore.QRect(Stat_x, std_Y, std_Width, std_Hight))
            self.s.setText("Make your drink!")
            stats.extend([self.s])

        for i in range(len(self.RasBari.Bottles)):

            if ((i % 5 == 0) & (i != 0)):
                page = page + 1
                j = 0

            line_y = Topspace + j * (std_Hight + self.space_Gen * 1.7)

            self.s = QtWidgets.QSlider(Qt.Horizontal, self.NewDrink_pages[page])
            slider.extend([self.s])
            slider[i].setMaximum(100)
            slider[i].setMinimum(0)
            slider[i].setGeometry(QtCore.QRect(slider_x, line_y, slider_width, std_Hight))

            self.n = QtWidgets.QTextBrowser(self.NewDrink_pages[page])
            name.extend([self.n])
            name[i].setText(self.RasBari.Bottles[i].getname())
            name[i].setGeometry(QtCore.QRect(name_x, line_y, name_width, std_Hight))

            self.a = QtWidgets.QTextBrowser(self.NewDrink_pages[page])
            amount.extend([self.a])
            amount[i].setText("0")
            amount[i].setGeometry(QtCore.QRect(amount_x, line_y, amount_width, std_Hight))

            slider[i].valueChanged.connect(partial(Amount_Slider, i))
            slider[i].valueChanged.connect(partial(newMaxima, i))

            self.updateGUI.connect(lambda: self.resetSlder(slider))

            j = j + 1

        ############################ END of newDrink_Widget(self, StackedWidget) #######################################

    def NewDrink_wig_bottom(self, slider, widget):

        std_Hight = self.setUpButtonHeight
        std_Width = self.setUpButtonWith
        std_Y = self.setUpButtonPos

        # ExitButton - Button to navigate from the first drink widget back to the main widget

        ExitButton_x = (self.GUI_Width / 2 - self.setUpButtonWith / 2)

        self.ExitButton = QtWidgets.QPushButton(widget)
        self.ExitButton.setGeometry(QtCore.QRect(ExitButton_x, std_Y, std_Width, std_Hight))
        self.ExitButton.setText("Exit")

        self.ExitButton.clicked.connect(lambda: self.showWidget(self.Mainwig, 1))

        # Save - Button to Save the current drink setup as a new drink

        self.Save = QtWidgets.QPushButton(widget)
        self.Save.setGeometry(QtCore.QRect(self.setUp_getin, std_Y, std_Width, std_Hight))
        self.Save.setText("Save Drink")

        self.Save.clicked.connect(lambda: self.saveNewDrink(slider, self.RasBari.Bottles))

    def newDrinkNavigation(self, widget, destination_left, destination_right):

        possible_spcae = self.setUpButtonWith * 1.8

        Next_button_size = self.setUpButtonHeight * 1.5
        Next_button_y = self.GUI_Height / 2 - Next_button_size / 2
        Next_left_x = (self.GUI_Width / 2 - possible_spcae / 2) / 2 - Next_button_size / 2
        Next_right_x = self.GUI_Width - Next_left_x - Next_button_size

        self.Next_left = QtWidgets.QPushButton(widget)
        self.Next_left.setGeometry(QtCore.QRect(Next_left_x, Next_button_y, Next_button_size, Next_button_size))
        self.Next_left.setObjectName("change_left")
        self.Next_left.setText("<-")
        self.Next_left.clicked.connect(lambda: self.showWidget(destination_left, 0))

        self.Next_right = QtWidgets.QPushButton(widget)
        self.Next_right.setGeometry(QtCore.QRect(Next_right_x, Next_button_y, Next_button_size, Next_button_size))
        self.Next_right.setObjectName("change_right")
        self.Next_right.setText("->")
        self.Next_right.clicked.connect(lambda: self.showWidget(destination_right, 0))

    def saveNewDrink(self, Slider, Bottles):

        sum = 0

        for i in range(len(Slider)):
            sum = sum + Slider[i].value()

        if sum == 100:

            self.Ingredients = []

            NewDrinkName = ""

            for i in range(len(Slider)):
                if Slider[i].value() != 0:
                    name = Bottles[i].getname()
                    name = name[:3]
                    name = name + str(Slider[i].value())
                    NewDrinkName = NewDrinkName + name

            self.Ingredients.extend([("name", NewDrinkName)])

            for i in range(len(Slider)):
                Ingred = [Bottles[i].getname(), str(Slider[i].value())]
                self.Ingredients.extend([Ingred])

            NewDrink = Drink(self.Ingredients)

            self.RasBari.DrinkList.extend([NewDrink])

            self.resetSlder(Slider)
            self.showWidget(self.Mainwig, 1)

        else:
            print("Drink not completed")  # TODO change the reset button to an textbrowser that indictes status

    def resetSlder(self, Slider):
        for i in range(len(Slider)):
            Slider[i].setSliderPosition(0)

    def drinks_menue_widget(self, StackedWidget):

        self.showDrinkwidget.connect(lambda: self.showWidget(self.drinks_menue_widget, 1))

        # Build of new widget

        self.drinks_menue_widget = QtWidgets.QWidget()
        self.drinks_menue_widget.setObjectName("Drink_menue")
        StackedWidget.addWidget(self.drinks_menue_widget)

        # Std. values

        std_Hight = self.setUpButtonHeight
        std_Width = self.setUpButtonWith
        std_Width_menue = self.GUI_Width / 2 - self.setUp_getin * 1.5
        std_Y_menue = self.GUI_Height / 2 - std_Hight / 2
        std_Y = self.setUpButtonPos

        # Headline - Contains Software title

        self.buildHeader(self.drinks_menue_widget, StackedWidget)

        # NewDrink pushbutton to navigate to the newdrink widget

        self.NewDrink = QtWidgets.QPushButton(self.drinks_menue_widget)
        self.NewDrink.setGeometry(QtCore.QRect(self.setUp_getin, std_Y_menue, std_Width_menue, std_Hight))
        self.NewDrink.setText("Let me make a new drink!")

        self.NewDrink.clicked.connect(lambda: self.showWidget(self.NewDrink_pages[0], 1))

        # ShowDrink pushbutton to naviate to the widget that shows all included drinks

        ShowDrink_x = self.GUI_Width - self.setUp_getin - std_Width_menue

        self.ShowDrink = QtWidgets.QPushButton(self.drinks_menue_widget)
        self.ShowDrink.setGeometry(QtCore.QRect(ShowDrink_x, std_Y_menue, std_Width_menue, std_Hight))
        self.ShowDrink.setText("Show included drinks!")

        self.ShowDrink.clicked.connect(lambda: self.showWidget(self.included_Drinks_widget, 1))

        # ExitButton - Button to navigate back to the main widget

        ExitButton_x = (self.GUI_Width / 2 - self.setUpButtonWith / 2)

        self.ExitButton = QtWidgets.QPushButton(self.drinks_menue_widget)
        self.ExitButton.setGeometry(QtCore.QRect(ExitButton_x, std_Y, std_Width, std_Hight))
        self.ExitButton.setText("Exit")

        self.ExitButton.clicked.connect(lambda: self.showWidget(self.Mainwig, 1))

    def included_Drinks_widget(self, StackedWidget):

        std_Hight = self.setUpButtonHeight
        std_Width = self.setUpButtonWith
        std_Width_menue = self.GUI_Width / 2 - self.setUp_getin * 1.5
        std_Y_menue = self.GUI_Height / 2 - std_Hight / 2
        std_Y = self.setUpButtonPos

        # Build of new widget

        self.included_Drinks_widget = QtWidgets.QWidget()
        self.included_Drinks_widget.setObjectName("Drinks")
        StackedWidget.addWidget(self.included_Drinks_widget)

        # Headline - Contains Software title

        self.buildHeader(self.included_Drinks_widget, StackedWidget)

        DrinkTxt_width = self.setUpButtonWith * 1.8
        DrinkTxt_height = self.setUpButtonWith * 1.2
        DrinkTxt_x = self.GUI_Width / 2 - DrinkTxt_width / 2
        DrinkTxt_y = self.GUI_Height / 2 - DrinkTxt_height / 2

        self.DrinkTxt = QtWidgets.QTextBrowser(self.included_Drinks_widget)
        self.DrinkTxt.setGeometry(QtCore.QRect(DrinkTxt_x, DrinkTxt_y, DrinkTxt_width, DrinkTxt_height))
        self.DrinkTxt.setObjectName("Middle_Txt_Box")
        self.DrinkTxt.setText(self.RasBari.DrinkList[self.live_drink].getIngredientString())

        ExitButton_x = (self.GUI_Width / 2 - self.setUpButtonWith / 2)

        self.ExitButton = QtWidgets.QPushButton(self.included_Drinks_widget)
        self.ExitButton.setGeometry(QtCore.QRect(ExitButton_x, std_Y, std_Width, std_Hight))
        self.ExitButton.setText("Exit")

        self.ExitButton.clicked.connect(lambda: self.showWidget(self.Mainwig, 1))

        Next_button_size = self.setUpButtonHeight * 1.5
        Next_button_y = self.GUI_Height / 2 - Next_button_size / 2
        Next_left_x = (self.GUI_Width / 2 - DrinkTxt_width / 2) / 2 - Next_button_size / 2
        Next_right_x = self.GUI_Width - Next_left_x - Next_button_size

        self.Next_left = QtWidgets.QPushButton(self.included_Drinks_widget)
        self.Next_left.setGeometry(QtCore.QRect(Next_left_x, Next_button_y, Next_button_size, Next_button_size))
        self.Next_left.setObjectName("change_left")
        self.Next_left.setText("<-")
        self.Next_left.clicked.connect(lambda: self.changeDrinkTxt(0))

        self.Next_right = QtWidgets.QPushButton(self.included_Drinks_widget)
        self.Next_right.setGeometry(QtCore.QRect(Next_right_x, Next_button_y, Next_button_size, Next_button_size))
        self.Next_right.setObjectName("change_right")
        self.Next_right.setText("->")
        self.Next_right.clicked.connect(lambda: self.changeDrinkTxt(1))

    def changeDrinkTxt(self, direction):
        if direction == 1:
            self.live_drink = self.live_drink + 1
            if self.live_drink > len(self.RasBari.DrinkList) - 1: self.live_drink = 0
        if direction == 0:
            self.live_drink = self.live_drink - 1
            if self.live_drink < 0: self.live_drink = len(self.RasBari.DrinkList) - 1

        self.DrinkTxt.setText(self.RasBari.DrinkList[self.live_drink].getIngredientString())

    def Button_Thread_Handler(self, Auswahl):

        self.RasBari.changeErrorFlag(False)

        if self.RasBari.getProductionFlag() == False:

            if self.RasBari.DrinkList[Auswahl] != False:

                thread = myThread(lambda: self.RasBari.mixIt(Auswahl))
                progressbar = myThread(self.upDateStatusBar)

                self.threadpool.start(thread)
                self.threadpool.start(progressbar)

            else:
                print("Drink unknown")
                self.RasBari.changeProductionFlag(False)

        else:
            print("Production already running")

    def Exit_Thread_Handler(self):
        exitThread = myThread(self.RasBari.errorFunction)
        self.threadpool.start(exitThread)

    def upDateStatusBar(self):
        self.Progress.setValue(self.RasBari.getProgress())

    def upDateTxt(self):

        self.amount_LCD.display(self.RasBari.getAmount())
        GlasString = "Glass volume: " + str(self.RasBari.getAmount()) + " ml"
        self.DigitText.setText(GlasString)

    def UpdateStausTxt(self):

        if self.RasBari.getProductionFlag() == False:
            self.StatTxt.setText("Status: Wait for input...")
        else:
            self.StatTxt.setText("Status: Busy")

    def check4order(self):

        c4o_thread = myThread(lambda: self.EmailOrder.gotNewOrder())
        self.threadpool.start(c4o_thread)

    def exeOrder(self):

        Find = 99
        Order = self.EmailOrder.getLastMessageTitel()

        print("Check whats ordered..." + Order)

        if ((Order != None) & (self.RasBari.getProductionFlag() != True)):

            for i in range(len(self.RasBari.DrinkList)):
                if self.RasBari.DrinkList[i] != False:
                    if self.RasBari.DrinkList[i].getName().upper() in Order.upper():
                        Find = i
                        break

        if Find != 99:

            Replytxt = self.EmailOrder.orderexecuted + "\n\nYour order: " + self.RasBari.DrinkList[Find].getName()

            threadMail = myThread(lambda: self.EmailOrder.send_mail_to(self.EmailOrder.lastSenderAdress, Replytxt,
                                                                       "Automatic reply from RasBari"))
            self.threadpool.start(threadMail)

            self.Button_Thread_Handler(Find)

        else:
            print("Order received but cant offer - Sorry")

            if self.RasBari.getProductionFlag() == True:
                threadMail = myThread(lambda: self.EmailOrder.send_mail_to(self.EmailOrder.lastSenderAdress,
                                                                           self.EmailOrder.orderallreadrunning,
                                                                           "Automatic reply from RasBari"))
                self.threadpool.start(threadMail)

            else:
                threadMail = myThread(
                    lambda: self.EmailOrder.send_mail_to(self.EmailOrder.lastSenderAdress, self.EmailOrder.unknownorder,
                                                         "Automatic reply from RasBari"))
                self.threadpool.start(threadMail)

            print(self.EmailOrder.lastSenderAdress)
            print("Mail sended")

    def showIngred_widget(self):

        Ingred_Wig_Index = self.GW.indexOf(self.ingredWidg)
        self.GW.setCurrentIndex(Ingred_Wig_Index)

    def resetwindow(self):

        print("show bottle widget")
        self.showBottlewidget.emit()

    def calculateGUI(self, width, height):

        self.GUI_Width = width * 1.048 * 0.58  # TODO CHANGE THIS !!!
        self.GUI_Height = height * 0.5479

        self.SpaceBwOj = self.GUI_Height / 100
        self.space = self.SpaceBwOj
        self.space_Gen = self.GUI_Height / 50
        self.setUp_getin = self.GUI_Width * 0.05

        self.ButtonWith = self.GUI_Width / 4 - self.space_Gen * 1.3

        self.setUpButtonWith = self.GUI_Width / 4
        self.setUpButtonHeight = self.GUI_Height * 0.1
        self.setUpTxTHeight = self.GUI_Height * 0.06

        self.setUpButtonPos = self.GUI_Height * 0.84
        self.setUpTxTPos = self.GUI_Height * 0.83 - self.setUpTxTHeight

    def setmyHtmlTitel(self, TitelObj, StackedWidget):

        _translate = QtCore.QCoreApplication.translate
        StackedWidget.setWindowTitle(_translate("GUI", "Rasbari"))
        TitelObj.setHtml(_translate("GUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
                                           "\"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\""
                                           " /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; "
                                           "font-weight:400; font-style:normal;\">\n"
                                           "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px;"
                                           " margin-left:0px; margin-right:0px; -qt-block-indent:0;"
                                           " text-indent:0px;\"><span style=\" font-size:19pt; font-weight:600;"
                                           "\">RasBari V3.0</span></p></body></html>"))

    def showBottlePage(self, Page):

        self.updateGUI.emit()
        self.GW.setCurrentIndex(self.GW.indexOf(Page))

    def showWidget(self, widget, refresh):
        if (refresh): self.updateGUI.emit()
        self.GW.setCurrentIndex(self.GW.indexOf(widget))

    def buildHeader(self, widget, StackedWidget):
        self.Titel = QtWidgets.QTextBrowser(widget)
        self.Titel.setGeometry(QtCore.QRect(0, self.space_Gen, self.GUI_Width, self.GUI_Height * 0.1))
        self.setmyHtmlTitel(self.Titel, StackedWidget)

    def bottomNavigation(self, widget, destination_Left, destination_Right, destination_exit):

        std_width = self.setUpButtonWith
        std_hight = self.setUpButtonHeight
        std_y = self.setUpButtonPos

        ExitBUtton_x = self.GUI_Width / 2 - self.setUpButtonWith / 2
        Changeleft_x = self.setUp_getin
        Changeright_x = self.GUI_Width - self.setUp_getin - self.setUpButtonWith

        # ExitButton - for navigation from widget to destination_exit

        self.ExitButton = QtWidgets.QPushButton(widget)
        self.ExitButton.setGeometry(QtCore.QRect(ExitBUtton_x, std_y, std_width, std_hight))
        self.ExitButton.setText("Exit")

        self.ExitButton.clicked.connect(lambda: self.showWidget(self.Mainwig, 1))

        # Changeleft - for navigation from widget to destination_Left

        self.Changeleft = QtWidgets.QPushButton(widget)
        self.Changeleft.setGeometry(QtCore.QRect(Changeleft_x, std_y, std_width, std_hight))
        self.Changeleft.setText("<- Change page")

        self.Changeleft.clicked.connect(lambda: self.showBottlePage(destination_Left))

        # Changeright - for navigation from widget to destination_right

        self.Changeright = QtWidgets.QPushButton(widget)
        self.Changeright.setGeometry(QtCore.QRect(Changeright_x, std_y, std_width, std_hight))
        self.Changeright.setText("Change page ->")

        self.Changeright.clicked.connect(lambda: self.showBottlePage(destination_Right))

        ########### END of bottomNavigation(self,widget,destination_Left,destination_Right,destination_exit) ###########

    ####################################--Classes for simplyfied GUI design--###########################################

    class BottleLine():
        def __init__(self, Master, widget, Bottle, total_x, total_y):
            self.wg = widget
            self.Bottle_in = Bottle
            self.rev_x = total_x + 10
            self.rev_y = total_y
            self.MAINGUI = Master

            self.buildline()

        def buildline(self):

            self.BottleNameDsp = QtWidgets.QTextBrowser(self.wg)
            self.BottleNameDsp.setGeometry(
                QtCore.QRect(self.rev_x, self.rev_y, self.MAINGUI.GUI_Width * 0.145, self.MAINGUI.setUpButtonHeight))
            self.BottleNameDsp.setObjectName("Bottle Name")
            self.BottleNameDsp.setText(self.Bottle_in.getname())

            xLevel = self.rev_x + self.MAINGUI.GUI_Width * 0.145 + self.MAINGUI.space_Gen

            self.level = QtWidgets.QProgressBar(self.wg)
            self.level.setGeometry(
                QtCore.QRect(xLevel, self.rev_y, self.MAINGUI.GUI_Width * 0.3, self.MAINGUI.setUpButtonHeight))
            self.level.setProperty("value",
                                   (int(self.Bottle_in.getRest()) / (int(self.Bottle_in.getbottlesize()))) * 100)

            xClear = xLevel + self.MAINGUI.space_Gen + self.MAINGUI.GUI_Width * 0.3

            self.ClearButton = QtWidgets.QPushButton(self.wg)
            self.ClearButton.setGeometry(
                QtCore.QRect(xClear, self.rev_y, self.MAINGUI.setUpButtonWith, self.MAINGUI.setUpButtonHeight))
            self.ClearButton.setText("Output")

            xResetbutton = xClear + self.MAINGUI.space_Gen + self.MAINGUI.setUpButtonWith

            self.Resetbutton = QtWidgets.QPushButton(self.wg)
            self.Resetbutton.setGeometry(
                QtCore.QRect(xResetbutton, self.rev_y, self.MAINGUI.setUpButtonWith, self.MAINGUI.setUpButtonHeight))
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