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
