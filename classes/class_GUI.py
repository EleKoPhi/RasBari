from PyQt5 import QtCore, QtGui, QtWidgets
from classes.class_Bar import *
from classes.class_myThread import *
from classes.class_eMailGuard import *




class Ui_GUI(QWidget):

    GUI_Width = int(getGuiWidth())
    GUI_Height = int(getGuiHight())

    SpaceBwOj = GUI_Height/100
    space = SpaceBwOj
    space_Gen = GUI_Height/50
    setUp_getin = GUI_Width*0.05

    ButtonWith = GUI_Width/4-space_Gen*1.3

    setUpButtonWith = GUI_Width/4
    setUpButtonHeight = GUI_Height*0.1
    setUpTxTHeight = GUI_Height*0.06

    setUpButtonPos = GUI_Height * 0.84
    setUpTxTPos = GUI_Height * 0.83 - setUpTxTHeight

    RasBari = Bar()
    EmailOrder = eMailGuard()

    def setupUi(self, GUI):

        GUI.setObjectName("GUI")
        GUI.resize(self.GUI_Width, self.GUI_Height)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GUI.sizePolicy().hasHeightForWidth())
        GUI.setSizePolicy(sizePolicy)
        GUI.setMinimumSize(QtCore.QSize(self.GUI_Width, self.GUI_Height))
        GUI.setMaximumSize(QtCore.QSize(self.GUI_Width, self.GUI_Width))
        GUI.setAnimated(True)





        self.threadpool = QThreadPool()

        self.centralwidget = QtWidgets.QWidget(GUI)
        self.centralwidget.setObjectName("centralwidget")

        self.Titel = QtWidgets.QTextBrowser(self.centralwidget)
        self.Titel.setGeometry(QtCore.QRect(0, self.space_Gen, self.GUI_Width, self.GUI_Height*0.1))
        self.Titel.setObjectName("Titel")

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, self.setUpButtonHeight+self.space_Gen, self.GUI_Width, self.GUI_Height*0.55))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.AuswahlGrid = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.AuswahlGrid.setObjectName("AuswahlGrid")

        self.Drink1_0 = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Drink1_0.sizePolicy().hasHeightForWidth())

        self.Drink1_0.setSizePolicy(sizePolicy)
        self.Drink1_0.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink1_0.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink1_0.setObjectName("Drink1_0")
        self.AuswahlGrid.addWidget(self.Drink1_0, 0, 0, 1, 1)

        self.Drink1_1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink1_1.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink1_1.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink1_1.setObjectName("Drink1_1")
        self.AuswahlGrid.addWidget(self.Drink1_1, 2, 0, 1, 1)

        self.Drink1_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink1_2.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink1_2.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink1_2.setObjectName("Drink1_2")
        self.AuswahlGrid.addWidget(self.Drink1_2, 3, 0, 1, 1)

        self.Drink2_0 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink2_0.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink2_0.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink2_0.setObjectName("Drink2_0")
        self.AuswahlGrid.addWidget(self.Drink2_0, 0, 1, 1, 1)

        self.Drink2_1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink2_1.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink2_1.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink2_1.setObjectName("Drink2_1")
        self.AuswahlGrid.addWidget(self.Drink2_1, 2, 1, 1, 1)

        self.Drink2_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink2_2.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink2_2.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink2_2.setObjectName("Drink2_2")
        self.AuswahlGrid.addWidget(self.Drink2_2, 3, 1, 1, 1)

        self.Drink3_0 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink3_0.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink3_0.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink3_0.setObjectName("Drink3_0")
        self.AuswahlGrid.addWidget(self.Drink3_0, 0, 2, 1, 1)

        self.Drink3_1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink3_1.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink3_1.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink3_1.setObjectName("Drink3_1")
        self.AuswahlGrid.addWidget(self.Drink3_1, 2, 2, 1, 1)

        self.Drink3_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink3_2.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink3_2.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink3_2.setObjectName("Drink3_2")
        self.AuswahlGrid.addWidget(self.Drink3_2, 3, 2, 1, 1)

        self.Drink4_0 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink4_0.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink4_0.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink4_0.setObjectName("Drink4_0")
        self.AuswahlGrid.addWidget(self.Drink4_0, 0, 3, 1, 1)

        self.Drink4_1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink4_1.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink4_1.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink4_1.setObjectName("Drink4_1")
        self.AuswahlGrid.addWidget(self.Drink4_1, 2, 3, 1, 1)

        self.Drink4_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Drink4_2.setMinimumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink4_2.setMaximumSize(QtCore.QSize(self.ButtonWith, self.GUI_Height*0.55*(1/4)))
        self.Drink4_2.setObjectName("Drink4_2")
        self.AuswahlGrid.addWidget(self.Drink4_2, 3, 3, 1, 1)

        self.AddAmount = QtWidgets.QPushButton(self.centralwidget)
        self.AddAmount.setGeometry(QtCore.QRect(self.setUp_getin+self.setUpButtonWith-self.setUpButtonHeight,  self.setUpButtonPos, self.setUpButtonHeight, self.setUpButtonHeight))
        self.AddAmount.setMinimumSize(QtCore.QSize(self.setUpButtonHeight, self.setUpButtonHeight))
        self.AddAmount.setMaximumSize(QtCore.QSize(self.setUpButtonHeight, self.setUpButtonHeight))

        self.SubtractAmount = QtWidgets.QPushButton(self.centralwidget)
        self.SubtractAmount.setGeometry(QtCore.QRect(self.setUp_getin,  self.setUpButtonPos, self.setUpButtonHeight, self.setUpButtonHeight))
        self.SubtractAmount.setMinimumSize(QtCore.QSize(self.setUpButtonHeight, self.setUpButtonHeight))
        self.SubtractAmount.setMaximumSize(QtCore.QSize(self.setUpButtonHeight, self.setUpButtonHeight))

        self.amount_LCD = QtWidgets.QLCDNumber(self.centralwidget)

        DigitWidth = self.setUpButtonWith-2*self.setUpButtonHeight-2*self.space
        DigitPos = self.setUp_getin + (self.setUpButtonWith / 2) - (DigitWidth / 2)

        self.amount_LCD.setGeometry(QtCore.QRect(DigitPos, self.setUpButtonPos,DigitWidth,self.setUpButtonHeight))
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

        self.Vortschritt = QtWidgets.QProgressBar(self.centralwidget)
        self.Vortschritt.setGeometry(QtCore.QRect(self.setUp_getin, self.setUpTxTPos*0.87,self.GUI_Width-2*self.setUp_getin, self.GUI_Height*0.08))
        self.Vortschritt.setProperty("value", 0)
        self.Vortschritt.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.Vortschritt.setObjectName("Vortschritt")

        self.Abbruch = QtWidgets.QPushButton(self.centralwidget)
        self.Abbruch.setGeometry(QtCore.QRect(self.GUI_Width/2-self.setUpButtonWith/2, self.setUpButtonPos, self.setUpButtonWith, self.setUpButtonHeight))
        self.Abbruch.setMinimumSize(QtCore.QSize(self.setUpButtonWith, self.setUpButtonHeight))
        self.Abbruch.setMaximumSize(QtCore.QSize(self.setUpButtonWith, self.setUpButtonHeight))
        self.Abbruch.setObjectName("Abbruch")

        self.DigitText = QtWidgets.QTextBrowser(self.centralwidget)
        self.DigitText.setGeometry(QtCore.QRect(self.setUp_getin, self.setUpTxTPos, self.setUpButtonWith, self.setUpTxTHeight))
        self.DigitText.setObjectName("Glasvolumen in ml")

        self.StatTxt = QtWidgets.QTextBrowser(self.centralwidget)
        self.StatTxt.setGeometry(QtCore.QRect(self.GUI_Width/2-self.setUpButtonWith/2, self.setUpTxTPos, self.setUpButtonWith, self.setUpTxTHeight))
        self.StatTxt.setObjectName("Status:")

        self.InitTxt = QtWidgets.QTextBrowser(self.centralwidget)
        self.InitTxt.setGeometry(QtCore.QRect(self.GUI_Width-self.setUp_getin-self.setUpButtonWith, self.setUpTxTPos, self.setUpButtonWith, self.setUpTxTHeight))
        self.InitTxt.setObjectName("Initialize")

        self.UnusedButton = QtWidgets.QPushButton(self.centralwidget)
        self.UnusedButton.setGeometry(QtCore.QRect(self.GUI_Width-self.setUp_getin-self.setUpButtonWith,self.setUpButtonPos, self.setUpButtonWith, self.setUpTxTHeight))
        self.UnusedButton.setMinimumSize(QtCore.QSize(self.setUpButtonWith, self.setUpButtonHeight))
        self.UnusedButton.setMaximumSize(QtCore.QSize(self.setUpButtonWith, self.setUpButtonHeight))
        self.UnusedButton.setObjectName("Abbruch")

        GUI.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(GUI)
        self.statusbar.setEnabled(False)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setObjectName("statusbar")
        GUI.setStatusBar(self.statusbar)

        self.retranslateUi(GUI)
        QtCore.QMetaObject.connectSlotsByName(GUI)

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

        self.RasBari.missingIngred.connect(self.showmsgboxempty)
        self.RasBari.drinkunknown.connect(lambda:self.showmsgbox)

        self.Vortschritt.setValue(0)

        self.RasBari.changedValSig.connect(self.upDateStatusBar)

        self.RasBari.changedAmountSig.connect(self.upDateTxt)

        self.EmailOrder.CheckMail.connect(self.exeOrder)

        self.MailTimer = QtCore.QTimer()
        self.MailTimer.setSingleShot(False)
        if getEmailGuardStat() & self.EmailOrder.status:self.MailTimer.start(3000)
        self.MailTimer.timeout.connect(lambda :self.check4order())

    def retranslateUi(self, GUI):

        _translate = QtCore.QCoreApplication.translate

        GUI.setWindowTitle(_translate("GUI", "Rasbari"))

        self.Titel.setHtml(_translate("GUI",    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:19pt; font-weight:600;\">RasBari V2.0</span></p></body></html>"))

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
        self.InitTxt.setText(_translate("GUI", "Unused Button Description"))
        self.UnusedButton.setText(_translate("GUI", "Unused Button"))



    def Button_Thread_Handler(self,Auswahl):

        self.RasBari.changeErrorFlag(False)

        if self.RasBari.getProductionFlag() == False:

            if self.RasBari.DrinkList[Auswahl] != False:

                thread = myThread(lambda:self.RasBari.mixIt(Auswahl))
                progressbar = myThread(self.upDateStatusBar)

                self.threadpool.start(thread)
                self.threadpool.start(progressbar)

            else:
                self.showmsgboxunknown()
                self.RasBari.changeProductionFlag(False)

        else:
            print("Production allready running")

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

        thread1 = myThread(lambda: self.EmailOrder.gotNewOrder())
        self.threadpool.start(thread1)

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

        msgBox = QMessageBox.information(self, 'Some empty bottles', "Would you like to change\nthe empty bottle",
                                         QMessageBox.No | QMessageBox.Yes, QMessageBox.No)

        #TODO INCLUDE THE RESET FUNKTION

    def showmsgboxunknown(self):
        msgBox = QMessageBox.information(self, 'Unknown drink', "Sorry, we can't mix\nthis drink.",QMessageBox.Close)



    #TODO http://zetcode.com/gui/pyqt5/firstprograms/ Center on desktop
    #TODO https://pythonspot.com/pyqt5-messagebox/ get messagebox function











