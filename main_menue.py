from super_widget import *

class main_widget(my_widget):

    grid_button_list = []

    def __init__(self, main_widget, program, GUI_layout,main_bar):
        super().__init__(main_widget, program, GUI_layout)

        self.Bar = main_bar
        self.Bar.changedValSig.connect(self.update_progressbar)

        # std. values

        std_y = self.layout.bottom_button_y
        std_txt_y = self.layout.bottom_txt_y
        std_hight = self.layout.button_height
        std_hight_txt = self.layout.txt_height
        std_width = self.layout.button_width

        self.button_grid()

        # Progessbar that shows the progress of the mixture

        Progress_x = self.layout.bottom_button_getin
        Progress_y = self.layout.bottom_txt_y * 0.87
        Progress_width = self.layout.GUI_Width - 2 * self.layout.bottom_button_getin
        Progress_hight = self.layout.GUI_Height * 0.08

        self.Progress = QtWidgets.QProgressBar(self.widget)
        self.Progress.setGeometry(QtCore.QRect(Progress_x, Progress_y, Progress_width, Progress_hight))
        self.Progress.setProperty("value", 0)
        self.Progress.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.Progress.setObjectName("Progress")

        # AddAmount & SubtactAmount - Pushbutton to change the drink size

        AddAmount_x = self.layout.bottom_button_getin + self.layout.button_width - self.layout.button_height
        SubtracAmount_x = self.layout.bottom_button_getin

        self.AddAmount = QtWidgets.QPushButton(self.widget)
        self.AddAmount.setGeometry(QtCore.QRect(AddAmount_x, std_y, std_hight, std_hight))
        self.AddAmount.setText("+")

        #self.AddAmount.clicked.connect(lambda: self.RasBari.change_volume(+10))

        self.SubtractAmount = QtWidgets.QPushButton(self.widget)
        self.SubtractAmount.setGeometry(QtCore.QRect(SubtracAmount_x, std_y, std_hight, std_hight))
        self.SubtractAmount.setText("-")

        #self.SubtractAmount.clicked.connect(lambda: self.RasBari.change_volume(-10))

        # LCD Display that shows the drink size

        amount_LCD_Width = std_width - 2 * std_hight - 2 * self.layout.button_space
        amount_LCD_x = self.layout.bottom_button_getin + (std_width / 2) - (amount_LCD_Width / 2)

        self.amount_LCD = QtWidgets.QLCDNumber(self.widget)
        self.amount_LCD.setGeometry(QtCore.QRect(amount_LCD_x, std_y, amount_LCD_Width, std_hight))
        self.amount_LCD.setAutoFillBackground(False)
        self.amount_LCD.setFrameShape(QtWidgets.QFrame.Panel)
        self.amount_LCD.setFrameShadow(QtWidgets.QFrame.Raised)
        self.amount_LCD.setLineWidth(2)
        self.amount_LCD.setMidLineWidth(1)
        self.amount_LCD.setSmallDecimalPoint(True)
        self.amount_LCD.setDigitCount(3)
        self.amount_LCD.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.amount_LCD.setProperty("intValue", self.Bar.getAmount())
        self.amount_LCD.setObjectName("amount_LCD")

        # Exit - Pushbutton to stop the production thread

        Exit_x = self.layout.GUI_Width - self.layout.bottom_button_getin - self.layout.button_width

        stopFont = QtGui.QFont()
        stopFont.setPointSize(26)
        stopFont.setBold(True)
        stopFont.setItalic(False)
        stopFont.setWeight(75)

        self.Exit = QtWidgets.QPushButton(self.widget)
        self.Exit.setGeometry(QtCore.QRect(Exit_x, std_y, std_width, std_hight))
        self.Exit.setObjectName("Exit")
        self.Exit.setFont(stopFont)
        self.Exit.setText("STOP")
        self.Exit.setStyleSheet("background-color: red")

        #self.Exit.clicked.connect(lambda: self.RasBari.errorFunction())

        # DigitText - Textbox that shows the dink size

        DigitText_x = self.layout.bottom_button_getin

        self.DigitText = QtWidgets.QLabel(self.widget)
        self.DigitText.setGeometry(QtCore.QRect(DigitText_x, std_txt_y, std_width, std_hight_txt))
        self.DigitText.setObjectName("Glasvolume")
        self.stdLabelSetUp(self.DigitText)

        GlasString = "Glass volume: " + str(self.Bar.getAmount()) + " ml"

        self.DigitText.setText(GlasString)

        # StatTxt - Textbox in the bottom right corner - shows system status

        StatTxt_x = self.layout.GUI_Width - self.layout.bottom_button_getin - self.layout.button_width

        self.StatTxt = QtWidgets.QLabel(self.widget)
        self.StatTxt.setGeometry(QtCore.QRect(StatTxt_x, std_txt_y, std_width, std_hight_txt))
        self.StatTxt.setObjectName("Status-text-box")
        self.StatTxt.setText("Status: Wait for input...")
        self.stdLabelSetUp(self.StatTxt)

        # TxtBox_middle - Textbox in the center bottom of the main GUI

        TxtBox_middle_x = self.layout.GUI_Width / 2 - self.layout.button_width / 2

        self.TxtBox_middle = QtWidgets.QLabel(self.widget)
        self.TxtBox_middle.setGeometry(QtCore.QRect(TxtBox_middle_x, std_txt_y, std_width, std_hight_txt))
        self.TxtBox_middle.setObjectName("Middle_Txt_Box")
        self.TxtBox_middle.setText("Welcome")
        self.stdLabelSetUp(self.TxtBox_middle)

        # Bottles - Button for navigation from main widget to bottles widgt

        Bottles_x = (self.layout.GUI_Width / 2 - self.layout.button_width / 2)
        Bottles_width = self.layout.button_width / 2 - self.layout.button_space / 2

        self.Bottles = QtWidgets.QPushButton(self.widget)
        self.Bottles.setGeometry(QtCore.QRect(Bottles_x, std_y, Bottles_width, std_hight))
        self.Bottles.setText("Bottles")

        #self.Bottles.clicked.connect(lambda: self.show_widget(self.Testwig1.widget, 1))

        # Drinks - Button for navigation from main widget to driks widget

        Drinks_x = (self.layout.GUI_Width / 2 - self.layout.button_width / 2) + Bottles_width + self.layout.button_space
        Drinks_width = Bottles_width

        self.Drinks = QtWidgets.QPushButton(self.widget)
        self.Drinks.setGeometry(QtCore.QRect(Drinks_x, std_y, Drinks_width, std_hight))
        self.Drinks.setText("Drinks")
        self.Drinks.clicked.connect(lambda: self.show_widget(self.program.drink_menue_widget.widget, 1))

        #self.updateGUI.connect(lambda: self.updateWidget())

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

    def update_progressbar(self):
        self.Progress.setValue(self.Bar.getProgress())

    def button_grid(self):

        # gridWidget contains all buttons, that start a mixture

        if 0 != len(self.Bar.DrinkList):

            grid_widget_x = 0
            grid_widget_y = self.layout.button_height + self.layout.top_space
            grid_width = self.layout.GUI_Width
            grid_height = self.layout.GUI_Height * 0.55

            self.grid_layout_widget = QtWidgets.QWidget(self.widget)
            self.grid_layout_widget.setGeometry(QtCore.QRect(grid_widget_x, grid_widget_y, grid_width, grid_height))
            self.grid_layout_widget.setObjectName("gridLayoutWidget")

            self.ButtonGrid = QtWidgets.QGridLayout(self.grid_layout_widget)
            self.ButtonGrid.setObjectName("buttongrid")

            number_of_rows = -(-len(self.Bar.DrinkList) // 4)
            grid_button_height = grid_height / number_of_rows * 0.9
            grid_button_width = grid_width / 4 * 0.8

            column = 0
            line = 0

            # include the buttons in the ButtonGrid

            self.grid_button_list.clear()

            for i in range(len(self.Bar.DrinkList)):

                self.grid_button_list.extend([QtWidgets.QPushButton(self.grid_layout_widget)])
                self.grid_button_list[i].setMinimumSize(QtCore.QSize(grid_button_width, grid_button_height))
                self.grid_button_list[i].setObjectName("Button_" + str(i))
                self.grid_button_list[i].setText(self.Bar.DrinkList[i].getName())
                self.grid_button_list[i].clicked.connect(partial(self.production_thread_handler, i))
                self.ButtonGrid.addWidget(self.grid_button_list[i], line, column)

                column = column + 1

                if column == 4:
                    column = 0
                    line = line + 1

    def production_thread_handler(self, drink_nr):

        self.Bar.changeErrorFlag(False)

        if not self.Bar.getProductionFlag():

            if self.Bar.DrinkList[drink_nr]:

                thread = myThread(lambda: self.Bar.mixIt(drink_nr))
                progressbar = myThread(self.update_progressbar)
                self.program.threadpool.start(thread)
                self.program.threadpool.start(progressbar)
            else:

                print("Drink unknown")
                self.Bar.changeProductionFlag(False)

        else:
            print("Production already running")


