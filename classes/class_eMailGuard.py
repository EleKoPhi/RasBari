import easyimap
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from TxTMethoden import *
from classes.class_myThread import *

class eMailGuard(QObject):
    last_message_id = 0
    last_sender_address = 0

    header = "Automatic reply from RasBari"

    unknow_order_msg = "Sorry we could not handle your order\nPlease add one of the following to your mail titel\n\n" + \
                       getAllNamesInList()
    order_exe_msg = "Your order is executed - pleas collect in a few seconds"
    order_not_possible_msg = "Sorry at the moment, we are busy.\nPlease try in a few moments"

    login = getMailAdress()
    password = getMailPassword()

    CheckMail = pyqtSignal()

    check_now_flag = 0

    def __init__(self,main_bar,main_wig):
        QObject.__init__(self)
        self.bar = main_bar
        self.main_wig = main_wig

        if getFlag("mailorder"):

            print("e-mail guard initialization ...")

            try:
                self.threadpool = QThreadPool()

                self.imapper = easyimap.connect('imap.gmail.com', self.login, self.password)
                self.imapper.unseen()
                self.last_message_id = self.getLastMessagelID()

                self.server = smtplib.SMTP('smtp.gmail.com', 587)
                self.server.ehlo()
                self.server.starttls()
                self.server.ehlo()
                self.server.login(self.login, self.password)

                self.MailTimer = QTimer()
                self.MailTimer.setSingleShot(False)
                self.MailTimer.start(500)
                self.MailTimer.timeout.connect(lambda: self.check_order())

                self.CheckMail.connect(self.exeOrder)

                print("e-mail guard NOW initialized")
                self.status = True

            except:
                print("e-mail guard NOT initialized")
                self.status = False
        else:
            print("e-mail guard NOT initialized")
            self.status = False

    def gotNewOrder(self):

        self.check_now_flag = 1

        if self.last_message_id != self.getLastMessagelID():
            self.last_message_id = self.getLastMessagelID()
            self.last_sender_address = self.getlastsenderadress()
            self.CheckMail.emit()
        else:
            self.check_now_flag = 0


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

        self.check_now_flag = 0

    def exeOrder(self):

        find = 99
        order = self.getLastMessageTitel()

        print("Whats ordered: " + order)

        if ((order != None) & (self.bar.getProductionFlag() == False)):

            for i in range(len(self.bar.DrinkList)):
                if self.bar.DrinkList[i]:
                    if self.bar.DrinkList[i].getName().upper() in order.upper():
                        find = i
                        break

        if find != 99:

            reply = self.order_exe_msg + "\n\nYour order: " + self.bar.DrinkList[find].getName()

            thread_mail = myThread(lambda: self.send_mail_to(self.last_sender_address, reply, self.header))
            self.threadpool.start(thread_mail)

            self.main_wig.production_thread_handler(find)

        else:
            print("order received but cant offer - Sorry")

            if self.bar.getProductionFlag():
                thread_mail = myThread(lambda: self.send_mail_to(self.lastSenderAdress, self.order_not_possible_msg, self.header))
                self.threadpool.start(thread_mail)

            else:
                thread_mail = myThread(
                    lambda: self.send_mail_to(self.EmailOrder.lastSenderAdress, self.unknow_order_msg, self.header))
                self.threadpool.start(thread_mail)

            print(self.lastSenderAdress)
            print("Mail sent")



    def check_order(self):

        if self.check_now_flag==0:

            co_thread = myThread(lambda: self.gotNewOrder())
            self.threadpool.start(co_thread)

