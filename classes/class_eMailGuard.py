import easyimap
from PyQt5.QtCore import QObject, pyqtSignal
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from TxTMethoden import *

class eMailGuard(QObject):

    lastMessageID = 0
    lastSenderAdress = 0

    unknownorder = "Sorry we could not handle your order\nPlease add one of the following to your mail titel\n\n" + \
                   getAllNamesInList()

    orderexecuted = "Your order is executed - pleas collect in a few seconds"

    orderallreadrunning = "Sorry at the moment, we are busy.\nPlease try in a few moments"

    login = getMailAdress()
    password = getMailPassword()

    CheckMail = pyqtSignal()

    def __init__(self):

        QObject.__init__(self)

        print("eMailGuard - Ini - Start")

        try:
            #self.imapper = easyimap.connect('imap.gmail.com', self.login, self.password)
            self.imapper.unseen()
            self.lastMessageID = self.getLastMessagelID()

            self.server = smtplib.SMTP('smtp.gmail.com', 587)
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
            #self.server.login(self.login, self.password)

            #self.status = True

            print("eMailGuard - Ini - Done")

        except:
            print("eMailGuard - Ini - Fail")

            self.status = False

    def gotNewOrder(self):
        if self.lastMessageID != self.getLastMessagelID():
            self.lastMessageID = self.getLastMessagelID()
            self.lastSenderAdress = self.getlastsenderadress()
            self.CheckMail.emit()

    def getLastMessagelID(self):
        for mail_id in self.imapper.listids(limit=1):
            mail = self.imapper.mail(mail_id)
            return mail.message_id

    def getLastMessageTitel(self):
        for mail_id in self.imapper.listids(limit=1):
            mail = self.imapper.mail(mail_id)
            return mail.title

    def getlastsenderadress(self):
        for mail_id in self.imapper.listids(limit=1):
            mail = self.imapper.mail(mail_id)
            return mail.from_addr

    def send_mail_to(self, to, message, subject):

        self.msg = MIMEMultipart()

        self.msg['From'] = self.login
        self.msg['To'] = to
        self.msg['Subject'] = subject

        body = message
        self.msg.attach(MIMEText(body, 'plain'))

        text = self.msg.as_string()
        self.server.sendmail(self.login, to, text)


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


    def check4order(self):

        c4o_thread = myThread(lambda: self.EmailOrder.gotNewOrder())
        self.threadpool.start(c4o_thread)
