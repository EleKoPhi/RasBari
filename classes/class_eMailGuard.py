import easyimap
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from TxTMethoden import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from TxTMethoden import *
import classes.class_myThread



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

        self.imapper = easyimap.connect('imap.gmail.com', self.login, self.password)
        self.imapper.unseen()
        self.lastMessageID = self.getLastMessagelID()

        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.login, self.password)

        self.msg = MIMEMultipart()


        print("eMailGuard - Ini - Done")

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

        self.msg['From'] = self.login
        self.msg['To'] = to
        self.msg['Subject'] = subject

        body = message
        self.msg.attach(MIMEText(body, 'plain'))

        text = self.msg.as_string()
        self.server.sendmail(self.login, to, text)
