from PyQt5 import QtCore, QtGui, QtWidgets

from classes.class_Bar import *
from classes.class_eMailGuard import *
from classes.class_myThread import *


class Ui_GUI(QWidget,QObject):

    RasBari = Bar()
    EmailOrder = eMailGuard()

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

        ################################### ---> DEFINE WIDGETS HER <--- ##############################################

        self.Mainwig = QtWidgets.QWidget()
        self.Mainwig.setObjectName("Mainwig")
        StackedWidget.addWidget(self.Mainwig)

        self.Bottlewig = QtWidgets.QWidget()
        self.Bottlewig.setObjectName("Bottlewig")
        StackedWidget.addWidget(self.Bottlewig)

        self.Bottlewig_1 = QtWidgets.QWidget()
        self.Bottlewig_1.setObjectName("Bottlewig_1")
        StackedWidget.addWidget(self.Bottlewig_1)

        self.MissingIngriwig = QtWidgets.QWidget()
        self.MissingIngriwig.setObjectName("Missing_Ingred")
        StackedWidget.addWidget(self.MissingIngriwig)

        self.Unknownwig = QtWidgets.QWidget()
        self.Unknownwig.setObjectName("UnknownDrink")
        StackedWidget.addWidget(self.Unknownwig)

        self.NewDrinkwig = QtWidgets.QWidget()
        self.NewDrinkwig.setObjectName("New_Drink")
        StackedWidget.addWidget(self.NewDrinkwig)

        ################################### ---> BUILD WIDGETS HER <--- ###############################################

        self.main_Widget(self.Mainwig, StackedWidget)
        self.bottle_Widget(self.Bottlewig, self.Bottlewig_1, StackedWidget)
        self.ingredient_Widget(self.MissingIngriwig, StackedWidget)
        self.newDrink_Widget(self.NewDrinkwig, StackedWidget)

        ################################### ---> END GUI OBJECTS <--- #################################################

        self.retranslateUi(StackedWidget)
        QtCore.QMetaObject.connectSlotsByName(StackedWidget)

        ############################# ---> START CONNECTION [BUTTONS]<--- #############################################

        self.Drink1_0.clicked.connect(lambda: self.Button_Thread_Handler(0))
        self.Drink2_0.clicked.connect(lambda: self.Button_Thread_Handler(1))
        self.Drink3_0.clicked.connect(lambda: self.Button_Thread_Handler(2))
        self.Drink4_0.clicked.connect(lambda: self.Button_Thread_Handler(3))

        self.Drink1_1.clicked.connect(lambda: self.Button_Thread_Handler(4))
        self.Drink2_1.clicked.connect(lambda: self.Button_Thread_Handler(5))
        self.Drink3_1.clicked.connect(lambda: self.Button_Thread_Handler(6))
        self.Drink4_1.clicked.connect(lambda: self.Button_Thread_Handler(7))

        self.Drink1_2.clicked.connect(lambda: self.Button_Thread_Handler(8))
        self.Drink2_2.clicked.connect(lambda: self.Button_Thread_Handler(9))
        self.Drink3_2.clicked.connect(lambda: self.Button_Thread_Handler(10))
        self.Drink4_2.clicked.connect(self.RasBari.sendSignal)

        self.Abbruch.clicked.connect(lambda:self.RasBari.errorFunction())

        self.AddAmount.clicked.connect(lambda:self.RasBari.change_volume(+10))
        self.SubtractAmount.clicked.connect(lambda:self.RasBari.change_volume(-10))

        self.RasBari.changedStatus.connect(self.UpdateStausTxt)

        ############################### ---> START CONNECTION [CodeSignals]<--- #######################################

        self.RasBari.missingIngred.connect(self.showmsgboxempty)
        self.RasBari.drinkunknown.connect(lambda:self.showmsgbox)
        self.RasBari.changedValSig.connect(self.upDateStatusBar)
        self.RasBari.changedAmountSig.connect(self.upDateTxt)

        self.EmailOrder.CheckMail.connect(self.exeOrder)

        ################################### ---> START TIMER <--- #####################################################

        self.MailTimer = QtCore.QTimer()
        self.MailTimer.setSingleShot(False)
        if getEmailGuardStat() & self.EmailOrder.status:self.MailTimer.start(3000)
        self.MailTimer.timeout.connect(lambda :self.check4order())

        ################################### ---> END TIMER <--- #######################################################

        StackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(StackedWidget)

        ################################### ---> END setUp_Ui <--- ####################################################

    def retranslateUi(self, StackedWidget):

        _translate = QtCore.QCoreApplication.translate

        StackedWidget.setWindowTitle(_translate("GUI", "Rasbari"))

        self.Drink1_0.setText(_translate("GUI", getDrinkName("Drink1")))
        self.Drink2_0.setText(_translate("GUI", getDrinkName("Drink2")))
        self.Drink3_0.setText(_translate("GUI", getDrinkName("Drink3")))
        self.Drink4_0.setText(_translate("GUI", getDrinkName("Drink4")))

        self.Drink1_1.setText(_translate("GUI", getDrinkName("Drink5")))
        self.Drink2_1.setText(_translate("GUI", getDrinkName("Drink6")))
        self.Drink3_1.setText(_translate("GUI", getDrinkName("Drink7")))
        self.Drink4_1.setText(_translate("GUI", getDrinkName("Drink8")))

        self.Drink1_2.setText(_translate("GUI", getDrinkName("Drink9")))
        self.Drink2_2.setText(_translate("GUI", getDrinkName("Drink10")))
        self.Drink3_2.setText(_translate("GUI", getDrinkName("Drink11")))
        self.Drink4_2.setText(_translate("GUI", getDrinkName("Drink12")))

        stopFont = QtGui.QFont()
        stopFont.setPointSize(26)
        stopFont.setBold(True)
        stopFont.setItalic(False)
        stopFont.setWeight(75)

        self.Abbruch.setFont(stopFont)
        self.Abbruch.setText(_translate("GUI", "STOP"))
        self.Abbruch.setStyleSheet("background-color: red")

        self.AddAmount.setText(_translate("GUI", "+"))
        self.SubtractAmount.setText(_translate("GUI", "-"))

        GlasString = "Glass volume: " + str(self.RasBari.getAmount()) + " ml"

        self.DigitText.setText(_translate("GUI", GlasString))
        self.StatTxt.setText(_translate("GUI", "Status: Wait for input"))
        self.InitTxt.setText(_translate("GUI", "Welcome!"))

    def main_Widget(self, widget, StackedWidget):

        stdHight = self.setUpButtonHeight
        std_Y = self.setUpButtonPos

        self.TitelMain = QtWidgets.QTextBrowser(widget)
        self.TitelMain.setGeometry(QtCore.QRect(0, self.space_Gen, self.GUI_Width, self.GUI_Height * 0.1))
        self.TitelMain.setObjectName("TitelMain")
        self.setmyHtmlTitel(self.TitelMain, StackedWidget)

        self.gridLayoutWidget = QtWidgets.QWidget(widget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, self.setUpButtonHeight + self.space_Gen, self.GUI_Width,
                                                       self.GUI_Height * 0.55))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.AuswahlGrid = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.AuswahlGrid.setObjectName("AuswahlGrid")

        self.Drink1_0 = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Drink1_0.sizePolicy().hasHeightForWidth())

        self.Drink1_0.setSizePolicy(sizePolicy)
        self.Drink1_0.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink1_0.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink1_0.setObjectName("Drink1_0")
        self.AuswahlGrid.addWidget(self.Drink1_0, 0, 0, 1, 1)

        self.Drink1_1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink1_1.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink1_1.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink1_1.setObjectName("Drink1_1")
        self.AuswahlGrid.addWidget(self.Drink1_1, 2, 0, 1, 1)

        self.Drink1_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink1_2.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink1_2.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink1_2.setObjectName("Drink1_2")
        self.AuswahlGrid.addWidget(self.Drink1_2, 3, 0, 1, 1)

        self.Drink2_0 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink2_0.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink2_0.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink2_0.setObjectName("Drink2_0")
        self.AuswahlGrid.addWidget(self.Drink2_0, 0, 1, 1, 1)

        self.Drink2_1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink2_1.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink2_1.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink2_1.setObjectName("Drink2_1")
        self.AuswahlGrid.addWidget(self.Drink2_1, 2, 1, 1, 1)

        self.Drink2_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink2_2.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink2_2.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink2_2.setObjectName("Drink2_2")
        self.AuswahlGrid.addWidget(self.Drink2_2, 3, 1, 1, 1)

        self.Drink3_0 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink3_0.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink3_0.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink3_0.setObjectName("Drink3_0")
        self.AuswahlGrid.addWidget(self.Drink3_0, 0, 2, 1, 1)

        self.Drink3_1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink3_1.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink3_1.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink3_1.setObjectName("Drink3_1")
        self.AuswahlGrid.addWidget(self.Drink3_1, 2, 2, 1, 1)

        self.Drink3_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink3_2.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink3_2.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink3_2.setObjectName("Drink3_2")
        self.AuswahlGrid.addWidget(self.Drink3_2, 3, 2, 1, 1)

        self.Drink4_0 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink4_0.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink4_0.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink4_0.setObjectName("Drink4_0")
        self.AuswahlGrid.addWidget(self.Drink4_0, 0, 3, 1, 1)

        self.Drink4_1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink4_1.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink4_1.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink4_1.setObjectName("Drink4_1")
        self.AuswahlGrid.addWidget(self.Drink4_1, 2, 3, 1, 1)

        self.Drink4_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink4_2.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink4_2.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height * 0.55 * (1 / 4)))
        self.Drink4_2.setObjectName("Drink4_2")
        self.AuswahlGrid.addWidget(self.Drink4_2, 3, 3, 1, 1)

        self.AddAmount = QtWidgets.QPushButton(widget)
        self.AddAmount.setGeometry(QtCore.QRect(self.setUp_getin + self.setUpButtonWith - self.setUpButtonHeight,
                                                self.setUpButtonPos, self.setUpButtonHeight, self.setUpButtonHeight))
        self.AddAmount.setMinimumSize(QtCore.QSize(self.setUpButtonHeight, self.setUpButtonHeight))
        self.AddAmount.setMaximumSize(QtCore.QSize(self.setUpButtonHeight, self.setUpButtonHeight))

        self.SubtractAmount = QtWidgets.QPushButton(widget)
        self.SubtractAmount.setGeometry(QtCore.QRect(self.setUp_getin, self.setUpButtonPos, self.setUpButtonHeight,
                                                     self.setUpButtonHeight))
        self.SubtractAmount.setMinimumSize(QtCore.QSize(self.setUpButtonHeight, self.setUpButtonHeight))
        self.SubtractAmount.setMaximumSize(QtCore.QSize(self.setUpButtonHeight, self.setUpButtonHeight))

        self.amount_LCD = QtWidgets.QLCDNumber(widget)

        DigitWidth = self.setUpButtonWith - 2 * self.setUpButtonHeight - 2 * self.space
        DigitPos = self.setUp_getin + (self.setUpButtonWith / 2) - (DigitWidth / 2)

        self.amount_LCD.setGeometry(QtCore.QRect(DigitPos, self.setUpButtonPos, DigitWidth, self.setUpButtonHeight))
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

        self.Vortschritt = QtWidgets.QProgressBar(widget)
        self.Vortschritt.setGeometry(QtCore.QRect(self.setUp_getin, self.setUpTxTPos * 0.87,
                                                  self.GUI_Width - 2 * self.setUp_getin, self.GUI_Height * 0.08))
        self.Vortschritt.setProperty("value", 0)
        self.Vortschritt.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.Vortschritt.setObjectName("Vortschritt")

        self.Abbruch = QtWidgets.QPushButton(widget)
        self.Abbruch.setGeometry(
            QtCore.QRect(self.GUI_Width - self.setUp_getin - self.setUpButtonWith, self.setUpButtonPos,
                         self.setUpButtonWith, self.setUpButtonHeight))
        self.Abbruch.setMinimumSize(QtCore.QSize(self.setUpButtonWith, self.setUpButtonHeight))
        self.Abbruch.setMaximumSize(QtCore.QSize(self.setUpButtonWith, self.setUpButtonHeight))
        self.Abbruch.setObjectName("Abbruch")

        self.DigitText = QtWidgets.QTextBrowser(widget)
        self.DigitText.setGeometry(QtCore.QRect(self.setUp_getin, self.setUpTxTPos,
                                                self.setUpButtonWith, self.setUpTxTHeight))
        self.DigitText.setObjectName("Glasvolumen in ml")

        self.StatTxt = QtWidgets.QTextBrowser(widget)
        self.StatTxt.setGeometry(
            QtCore.QRect(self.GUI_Width - self.setUp_getin - self.setUpButtonWith, self.setUpTxTPos,
                         self.setUpButtonWith, self.setUpTxTHeight))
        self.StatTxt.setObjectName("Status:")

        self.InitTxt = QtWidgets.QTextBrowser(widget)
        self.InitTxt.setGeometry(QtCore.QRect(self.GUI_Width / 2 - self.setUpButtonWith / 2,
                                              self.setUpTxTPos, self.setUpButtonWith, self.setUpTxTHeight))
        self.InitTxt.setObjectName("Initialize")

        # Bottles - Button for navigation from main widget to bottles widgt

        Bottles_x = (self.GUI_Width / 2 - self.setUpButtonWith / 2)
        Bottles_width = self.setUpButtonWith / 2 - self.space / 2

        self.Bottles = QtWidgets.QPushButton(widget)
        self.Bottles.setGeometry(QtCore.QRect(Bottles_x, std_Y, Bottles_width, stdHight))
        self.Bottles.setText("Bottles")

        self.Bottles.clicked.connect(lambda: self.showBottlewidget.emit())

        # Drinks - Button for navigation from main widget to driks widget

        Drinks_x = (self.GUI_Width / 2 - self.setUpButtonWith / 2) + Bottles_width + self.space
        Drinks_width = Bottles_width

        self.Drinks = QtWidgets.QPushButton(widget)
        self.Drinks.setGeometry(QtCore.QRect(Drinks_x, std_Y, Drinks_width, stdHight))
        self.Drinks.setText("Drinks")

        self.Drinks.clicked.connect(lambda: self.showDrinkwidget.emit())

    def bottle_Widget(self, widgetA, widgetB, StackedWidget):

        Lines = []

        def updateWidget():
            for i in range(0, len(Lines)):
                Lines[i].updateStatusBar()

        self.updateGUI.connect(updateWidget)

        self.showBottlewidget.connect(lambda: self.showBottlePage(1))

        # Headline - Contains Software title on bottle_WidgetA

        self.buildHeader(widgetA, StackedWidget)

        # Headline - Contains Software title on bottle_WidgetB

        self.buildHeader(widgetB, StackedWidget)

        Topspace = self.GUI_Height * 0.16

        if len(self.RasBari.Bottles) > 5:
            FirstPageElements = int(len(self.RasBari.Bottles) / 2)

            for i in range(FirstPageElements):
                Lines.extend([self.BottleLine(self, widgetA, self.RasBari.Bottles[i], 0,
                                              Topspace + i * (self.setUpButtonHeight + self.space_Gen * 1.7))])

            space = 0

            for i in range(FirstPageElements, len(self.RasBari.Bottles)):
                Lines.extend([self.BottleLine(self, widgetB, self.RasBari.Bottles[i], 0,
                                              Topspace + space * (self.setUpButtonHeight + self.space_Gen * 1.7))])
                space = space + 1

        else:
            for i in range(self.RasBari.Bottles):
                Lines.extend([self.BottleLine(self, widgetA, self.RasBari.Bottles[i], 0,
                                              Topspace + i * (self.setUpButtonHeight + self.space_Gen * 1.7))])

        self.bottomNavigation(widgetA, 2, 2, 0)
        self.bottomNavigation(widgetB, 1, 1, 0)  # TODO make that automatic

    def ingredient_Widget(self, widget, StackedWidget):

        std_width = self.setUpButtonWith
        std_hight = self.setUpButtonHeight

        # Headline - Contains Software title

        self.buildHeader(widget, StackedWidget)

        # YESBut - Button for navigation to the bottle widget

        YESBut_x = self.setUp_getin
        YESBut_y = self.GUI_Height / 2 - std_hight / 2

        self.YESBut = QtWidgets.QPushButton(widget)
        self.YESBut.setGeometry(QtCore.QRect(YESBut_x, YESBut_y, std_width, std_hight))
        self.YESBut.setText("Yes")

        self.YESBut.clicked.connect(lambda: self.GW.setCurrentIndex(1))

        # NOBut - Button for navigation to the main widget

        NOBut_x = self.GUI_Width - self.setUp_getin - self.setUpButtonWith
        NOBut_y = YESBut_y

        self.NOBut = QtWidgets.QPushButton(widget)
        self.NOBut.setGeometry(QtCore.QRect(NOBut_x, NOBut_y, std_width, std_hight))
        self.NOBut.setText("No")

        self.NOBut.clicked.connect(lambda: self.GW.setCurrentIndex(0))

        # Message - Textbrowser that shows the message for missing ingredients

        Message_x = self.GUI_Width / 2 - std_width / 2
        Message_y = self.GUI_Height / 2 - std_hight
        Message_hight = std_hight * 2
        Message_content = "You have missing ingredients\n\nDo you want to reset them?\nPlease make a desision"

        self.Message = QtWidgets.QTextBrowser(widget)
        self.Message.setGeometry(QtCore.QRect(Message_x, Message_y, std_width, Message_hight))
        self.Message.setText(Message_content)

        ############################ END of ingredient_Widget(self, widget, StackedWidget) #############################

    def newDrink_Widget(self, widget, StackedWidget):

        std_Hight = self.setUpButtonHeight
        std_Width = self.setUpButtonWith
        std_Y = self.setUpButtonPos

        self.showDrinkwidget.connect(lambda: StackedWidget.setCurrentIndex(5))

        # Headline - Contains Software title

        self.buildHeader(widget, StackedWidget)

        # ExitButton - Button to navigate from the first drink widget back to the main widget

        ExitButton_x = (self.GUI_Width / 2 - self.setUpButtonWith / 2)

        self.ExitButton = QtWidgets.QPushButton(widget)
        self.ExitButton.setGeometry(QtCore.QRect(ExitButton_x, std_Y, std_Width, std_Hight))
        self.ExitButton.setText("Exit")

        self.ExitButton.clicked.connect(lambda: StackedWidget.setCurrentIndex(0))

        # Save - Button to Save the current drink setup as a new drink

        self.Save = QtWidgets.QPushButton(widget)
        self.Save.setGeometry(QtCore.QRect(self.setUp_getin, std_Y, std_Width, std_Hight))
        self.Save.setText("Save Drink")

        # Reset - Button to reset the current choose

        Reset_x = self.GUI_Width - self.setUp_getin - self.setUpButtonWith

        self.Reset = QtWidgets.QPushButton(widget)
        self.Reset.setGeometry(QtCore.QRect(Reset_x, std_Y, std_Width, std_Hight))
        self.Reset.setText("Reset")

        ############################ END of newDrink_Widget(self,widget,StackedWidget) ################################

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
            self.Vortschritt.setValue(self.RasBari.getProgress())

    def upDateTxt(self):

            self.amount_LCD.display(self.RasBari.getAmount())
            GlasString = "Glass volume: " + str(self.RasBari.getAmount()) + " ml"
            self.DigitText.setText(GlasString)

    def UpdateStausTxt(self):

            if self.RasBari.getProductionFlag() == False:
                self.StatTxt.setText("Status: Wait for input")
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

    def showmsgboxempty(self):

        self.GW.setCurrentIndex(3)

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

    def showBottlePage(self, Auswahl):

        self.updateGUI.emit()

        if Auswahl == 2:
            self.GW.setCurrentIndex(2)
        else:
            self.GW.setCurrentIndex(1)

    def showBottlePage_Start(self, Lines):
        self.showBottlePage(1, Lines)

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






