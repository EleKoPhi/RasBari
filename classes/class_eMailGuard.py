import easyimap
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from TxTMethoden import *

class eMailGuard(QObject):

    lastMessageID = 0

    login = getMailAdress()
    password = getMailPassword()

    CheckMail = pyqtSignal()

    def __init__(self):

        QObject.__init__(self)

        print("eMailGuard - Ini - Start")

        self.imapper = easyimap.connect('imap.gmail.com', self.login, self.password)
        self.imapper.unseen()
        self.lastMessageID = self.getLastMessagelID()

        print("eMailGuard - Ini - Done")

    def gotNewOrder(self):
        if self.lastMessageID != self.getLastMessagelID():
            self.lastMessageID = self.getLastMessagelID()
            self.ReceiveFlag = 1
            self.CheckMail.emit()

    def getLastMessagelID(self):
        for mail_id in self.imapper.listids(limit=1):
            mail = self.imapper.mail(mail_id)
            return mail.message_id

    def getLastMessageTitel(self):
        for mail_id in self.imapper.listids(limit=1):
            mail = self.imapper.mail(mail_id)
            return mail.title



