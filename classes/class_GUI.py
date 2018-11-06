from PyQt5 import QtCore, QtGui, QtWidgets

from classes.class_Bar import *
from classes.class_eMailGuard import *
from classes.class_myThread import *


class Ui_GUI(QWidget,QObject):

    RasBari = Bar()
    EmailOrder = eMailGuard()

    Bottle_pages = []

    showBottlewidget = pyqtSignal()
    showDrinkwidget = pyqtSignal()
    updateGUI = pyqtSignal()

    def __init__(self,width,height,GlobalWidged):
        QObject.__init__(self)
        self.calculateGUI(width, height)
        self.threadpool = QThreadPool()
        self.GW = GlobalWidged

    def setupUi(self,StackedWidget):

        StackedWidget.setObjectName("StackedWidget")

        ################################### ---> START GUI SETUP <--- #################################################

        StackedWidget.setObjectName("GUI")
        StackedWidget.resize(self.GUI_Width, self.GUI_Height)
        StackedWidget.setMaximumSize(QtCore.QSize(self.GUI_Width, self.GUI_Height))

        ################################### ---> BUILD WIDGETS HER <--- ###############################################

        self.main_Widget(StackedWidget)
        self.bottle_Widget(StackedWidget)
        self.ingredient_Widget(StackedWidget)
        self.newDrink_Widget(StackedWidget)

        ################################### ---> END GUI OBJECTS <--- #################################################

        QtCore.QMetaObject.connectSlotsByName(StackedWidget)

        ############################### ---> START CONNECTION [CodeSignals]<--- #######################################

        self.RasBari.missingIngred.connect(self.showIngred_widget)
        self.RasBari.drinkunknown.connect(lambda:self.showmsgbox)
        self.RasBari.changedValSig.connect(self.upDateStatusBar)
        self.RasBari.changedAmountSig.connect(self.upDateTxt)
        self.RasBari.changedStatus.connect(self.UpdateStausTxt)

        self.EmailOrder.CheckMail.connect(self.exeOrder)

        ################################### ---> START TIMER <--- #####################################################

        self.MailTimer = QtCore.QTimer()
        self.MailTimer.setSingleShot(False)
        if getEmailGuardStat() & self.EmailOrder.status:self.MailTimer.start(3000)
        self.MailTimer.timeout.connect(lambda :self.check4order())

        ################################### ---> END TIMER <--- #######################################################

        MainWidgetIndex = StackedWidget.indexOf(self.Mainwig)
        StackedWidget.setCurrentIndex(MainWidgetIndex)
        QtCore.QMetaObject.connectSlotsByName(StackedWidget)

        ################################### ---> END setUp_Ui <--- ####################################################

    def main_Widget(self, StackedWidget):

        # Build of new widget

        self.Mainwig = QtWidgets.QWidget()
        self.Mainwig.setObjectName("Mainwig")
        StackedWidget.addWidget(self.Mainwig)

        # std. values

        std_y = self.setUpButtonPos
        std_txt_y = self.setUpTxTPos
        std_Hight = self.setUpButtonHeight
        std_Hight_txt = self.setUpTxTHeight
        std_Width = self.setUpButtonWith

        GridButton = []

        # Headline - Contains Software title

        self.buildHeader(self.Mainwig, StackedWidget)

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

        for i in range(len(self.RasBari.DrinkList)):

            GridButton.extend([QtWidgets.QPushButton(self.gridLayoutWidget)])
            GridButton[i].setMinimumSize(QtCore.QSize(gridButtonWidth, gridButtonHight))
            GridButton[i].setObjectName("Button_" + str(i))
            GridButton[i].setText(self.RasBari.DrinkList[i].getName())
            GridButton[i].clicked.connect(lambda: self.Button_Thread_Handler(i))
            self.ButtonGrid.addWidget(GridButton[i], line, column)

            column = column + 1

            if column == 4:
                column = 0
                line = line + 1

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

        ################################### END of main_Widget(self, StackedWidget) ####################################

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

            PageLeft = self.Bottle_pages[i - 1]

            try:
                PageRight = self.Bottle_pages[i + 1]
            except:
                PageRight = self.Bottle_pages[0]

            self.bottomNavigation(self.Bottle_pages[i], PageLeft, PageRight, MainWidgetIndex)

        # Build for every bottle one line thats shows - NAME - LEVEL + REST_Button + CLEAR_Button

        page = -1
        j = 0

        for i in range(len(self.RasBari.Bottles)):

            if i % 5 == 0:
                page += 1
                j = 0

            Line_y = Topspace + j * (self.setUpButtonHeight + self.space_Gen * 1.7)

            Lines.extend([self.BottleLine(self, self.Bottle_pages[page], self.RasBari.Bottles[i], 0, Line_y)])

            j += 1

        ############################ END of bottle_Widget(self, widgetA, widgetB, StackedWidget) #######################

    def ingredient_Widget(self, StackedWidget):

        # Build of new widget

        self.ingredWidg = QtWidgets.QWidget()
        self.ingredWidg.setObjectName("Missing_Ingred")
        StackedWidget.addWidget(self.ingredWidg)

        # Std. values

        std_width = self.setUpButtonWith
        std_hight = self.setUpButtonHeight

        # Headline - Contains Software title

        self.buildHeader(self.ingredWidg, StackedWidget)

        # YESBut - Button for navigation to the bottle widget

        YESBut_x = self.setUp_getin
        YESBut_y = self.GUI_Height / 2 - std_hight / 2
        FstBottleWidgetIndex = StackedWidget.indexOf(self.Bottle_pages[0])

        self.YESBut = QtWidgets.QPushButton(self.ingredWidg)
        self.YESBut.setGeometry(QtCore.QRect(YESBut_x, YESBut_y, std_width, std_hight))
        self.YESBut.setText("Yes")

        self.YESBut.clicked.connect(lambda: self.GW.setCurrentIndex(FstBottleWidgetIndex))

        # NOBut - Button for navigation to the main widget

        NOBut_x = self.GUI_Width - self.setUp_getin - self.setUpButtonWith
        NOBut_y = YESBut_y
        MainWidgetIndex = StackedWidget.indexOf(self.Mainwig)

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

        ############################ END of ingredient_Widget(self, widget, StackedWidget) #############################

    def newDrink_Widget(self, StackedWidget):

        # Build of new widget

        self.NewDrinkwig = QtWidgets.QWidget()
        self.NewDrinkwig.setObjectName("New_Drink")
        StackedWidget.addWidget(self.NewDrinkwig)

        # Std. values

        std_Hight = self.setUpButtonHeight
        std_Width = self.setUpButtonWith
        std_Y = self.setUpButtonPos

        # Headline - Contains Software title

        self.buildHeader(self.NewDrinkwig, StackedWidget)

        # ExitButton - Button to navigate from the first drink widget back to the main widget

        ExitButton_x = (self.GUI_Width / 2 - self.setUpButtonWith / 2)
        MainWidgetIndex = StackedWidget.indexOf(self.Mainwig)

        self.ExitButton = QtWidgets.QPushButton(self.NewDrinkwig)
        self.ExitButton.setGeometry(QtCore.QRect(ExitButton_x, std_Y, std_Width, std_Hight))
        self.ExitButton.setText("Exit")

        self.ExitButton.clicked.connect(lambda: StackedWidget.setCurrentIndex(MainWidgetIndex))

        # Save - Button to Save the current drink setup as a new drink

        self.Save = QtWidgets.QPushButton(self.NewDrinkwig)
        self.Save.setGeometry(QtCore.QRect(self.setUp_getin, std_Y, std_Width, std_Hight))
        self.Save.setText("Save Drink")

        # Reset - Button to reset the current choose

        Reset_x = self.GUI_Width - self.setUp_getin - self.setUpButtonWith

        self.Reset = QtWidgets.QPushButton(self.NewDrinkwig)
        self.Reset.setGeometry(QtCore.QRect(Reset_x, std_Y, std_Width, std_Hight))
        self.Reset.setText("Reset")

        ############################ END of newDrink_Widget(self, StackedWidget) #######################################

    def Button_Thread_Handler(self,Auswahl):

        self.RasBari.changeErrorFlag(False)

        if self.RasBari.getProductionFlag() == False:

            if self.RasBari.DrinkList[Auswahl] != False:

                thread = myThread(lambda:self.RasBari.mixIt(Auswahl))
                progressbar = myThread(self.upDateStatusBar)

                self.threadpool.start(thread)
                self.threadpool.start(progressbar)

            else:
                # TODO implement the drinkunknown widget her
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

        print("Check whats ordered..."+Order)

        if ((Order != None) & (self.RasBari.getProductionFlag()!=True)):

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

            if self.RasBari.getProductionFlag()==True:
                threadMail = myThread(lambda: self.EmailOrder.send_mail_to(self.EmailOrder.lastSenderAdress, self.EmailOrder.orderallreadrunning,
                                             "Automatic reply from RasBari"))
                self.threadpool.start(threadMail)

            else:
                threadMail = myThread(lambda: self.EmailOrder.send_mail_to(self.EmailOrder.lastSenderAdress, self.EmailOrder.unknownorder,
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

    def calculateGUI(self,width,height):

        self.GUI_Width = width*1.048*0.58 #TODO CHANGE THIS !!!
        self.GUI_Height = height*0.5479

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

    def setmyHtmlTitel(self,TitelObj,StackedWidget):

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
                                              "\">RasBari V2.0</span></p></body></html>"))

    def showBottlePage(self, Page):

        self.updateGUI.emit()
        self.GW.setCurrentIndex(self.GW.indexOf(Page))

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

        self.ExitButton.clicked.connect(lambda: self.GW.setCurrentIndex(destination_exit))

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

    ########### END of bottomNavigation(self,widget,destination_Left,destination_Right,destination_exit) ###############

    ####################################--Classes for simplyfied GUI design--##########################################

    class BottleLine():
        def __init__(self, Master, widget, Bottle, total_x,total_y):
            self.wg = widget
            self.Bottle_in = Bottle
            self.rev_x=total_x+10
            self.rev_y=total_y
            self.MAINGUI = Master

            self.buildline()

        def buildline(self):

            self.BottleNameDsp = QtWidgets.QTextBrowser(self.wg)
            self.BottleNameDsp.setGeometry(QtCore.QRect(self.rev_x, self.rev_y,self.MAINGUI.GUI_Width*0.145, self.MAINGUI.setUpButtonHeight))
            self.BottleNameDsp.setObjectName("Bottle Name")
            self.BottleNameDsp.setText(self.Bottle_in.getname())

            xLevel = self.rev_x+self.MAINGUI.GUI_Width*0.145+self.MAINGUI.space_Gen

            self.level = QtWidgets.QProgressBar(self.wg)
            self.level.setGeometry(QtCore.QRect(xLevel, self.rev_y,self.MAINGUI.GUI_Width*0.3, self.MAINGUI.setUpButtonHeight))
            self.level.setProperty("value", (int(self.Bottle_in.getRest())/(int(self.Bottle_in.getbottlesize())))*100)

            xClear = xLevel + self.MAINGUI.space_Gen + self.MAINGUI.GUI_Width*0.3

            self.ClearButton = QtWidgets.QPushButton(self.wg)
            self.ClearButton.setGeometry(QtCore.QRect(xClear, self.rev_y, self.MAINGUI.setUpButtonWith,self.MAINGUI.setUpButtonHeight))
            self.ClearButton.setText("Output")

            xResetbutton = xClear + self.MAINGUI.space_Gen + self.MAINGUI.setUpButtonWith

            self.Resetbutton = QtWidgets.QPushButton(self.wg)
            self.Resetbutton.setGeometry(QtCore.QRect(xResetbutton, self.rev_y, self.MAINGUI.setUpButtonWith, self.MAINGUI.setUpButtonHeight))
            self.Resetbutton.setText("RESET")

            self.Resetbutton.clicked.connect(lambda:self.placeNewBottle())
            self.ClearButton.clicked.connect(lambda:self.emptyBottle())

        def placeNewBottle(self):

            print("Reset Bottle")

            for i in range(len(Ui_GUI.RasBari.Bottles)):

                if self.Bottle_in.getname()==Ui_GUI.RasBari.Bottles[i].getname():
                    Ui_GUI.RasBari.Bottles[i].putAmount(Ui_GUI.RasBari.Bottles[i].getbottlesize())
                    print(Ui_GUI.RasBari.Bottles[i].getlevel())
                    self.Bottle_in=Ui_GUI.RasBari.Bottles[i]
                    break

            self.level.setProperty("value", (int(self.Bottle_in.getlevel())/(int(self.Bottle_in.getbottlesize())))*100)

        def emptyBottle(self):

            print("empty Bottle")

            self.Bottle_in.getliqout()
            self.level.setProperty("value",(int(self.Bottle_in.getlevel()) / (int(self.Bottle_in.getbottlesize()))) * 100)

        def updateStatusBar(self):

            for i in range(len(Ui_GUI.RasBari.Bottles)):
                if self.Bottle_in.getname()==Ui_GUI.RasBari.Bottles[i].getname():

                    self.Bottle_in = Ui_GUI.RasBari.Bottles[i]
                    value = int((int(Ui_GUI.RasBari.Bottles[i].getlevel())/int(self.Bottle_in.getbottlesize()))*100)
                    if value < 0:value=0
                    self.level.setProperty("value",value)
                    break






