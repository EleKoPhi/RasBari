#import easyimap
#import smtplib
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText
from TxTMethoden import *
from classes.class_myThread import *


# noinspection PyBroadException
class eMailGuard(QObject):
    """header = "Automatic reply from RasBari"
    unknow_order_msg = "Sorry we could not handle your order\nPlease add one of the following to your mail titel\n\n"
    order_exe_msg = "Your order is executed - pleas collect in a few seconds"
    order_not_possible_msg = "Sorry at the moment, we are busy.\nPlease try in a few moments"

    missing_ingred_msg = "Sorry we can't mix your drink.\nSome ingredients are missing\n\nPlease check bottles"

    login = get_mail()
    password = get_password()

    CheckMail = pyqtSignal()

    check_now_flag = 0

    def __init__(self, main_bar, main_wig):
        QObject.__init__(self)
        self.bar = main_bar
        self.main_wig = main_wig

        if get_flag("mailorder"):

            print("e-mail guard initialization ...")

            try:
                self.threadpool = QThreadPool()

                self.imapper = easyimap.connect('imap.gmail.com', self.login, self.password)
                self.imapper.unseen()
                self.last_message_id = self.get_last_message_id()

                self.server = smtplib.SMTP('smtp.gmail.com', 587)
                self.server.ehlo()
                self.server.starttls()
                self.server.ehlo()
                self.server.login(self.login, self.password)

                self.MailTimer = QTimer()
                self.MailTimer.setSingleShot(False)
                self.MailTimer.start(500)
                self.MailTimer.timeout.connect(lambda: self.check_order())

                self.last_message_id = self.get_last_message_id()
                self.last_sender_address = self.get_last_sender_address()

                self.CheckMail.connect(self.execute_order)

                print("e-mail guard NOW initialized")
                self.status = True

            except:
                print("e-mail guard NOT initialized")
                self.status = False
        else:
            print("e-mail guard NOT initialized")
            self.status = False

    def check_new_order(self):

        self.check_now_flag = 1

        if self.last_message_id != self.get_last_message_id():
            self.last_message_id = self.get_last_message_id()
            self.last_sender_address = self.get_last_sender_address()
            self.CheckMail.emit()
        else:
            self.check_now_flag = 0

    def get_last_message_id(self):
        for mail_id in self.imapper.listids(limit=1):
            mail = self.imapper.mail(mail_id)
            return mail.message_id

    def get_last_message_title(self):
        for mail_id in self.imapper.listids(limit=1):
            mail = self.imapper.mail(mail_id)
            return mail.title

    def get_last_sender_address(self):
        for mail_id in self.imapper.listids(limit=1):
            mail = self.imapper.mail(mail_id)
            return mail.from_addr

    def send_mail_to(self, to, message, subject):

        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = to
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        text = msg.as_string()
        self.server.sendmail(self.login, to, text)

        self.check_now_flag = 0

    def execute_order(self):

        find = 99
        order = self.get_last_message_title()

        print("Whats ordered: " + order)

        if (order is not None) & (not self.bar.get_production_flag()):

            for i in range(len(self.bar.DrinkList)):
                if self.bar.DrinkList[i]:
                    if self.bar.DrinkList[i].get_name().upper() in order.upper():
                        find = i
                        break

        if find != 99:

            if self.bar.can_be_mixed(self.bar.DrinkList[find]):

                reply = self.order_exe_msg + "\n\nYour order: " + self.bar.DrinkList[find].get_name()
                thread_mail = myThread(lambda: self.send_mail_to(self.last_sender_address, reply, self.header))
                self.threadpool.start(thread_mail)
                self.main_wig.production_thread_handler(find)

            else:

                reply = self.missing_ingred_msg
                thread_mail = myThread(lambda: self.send_mail_to(self.last_sender_address, reply, self.header))
                self.threadpool.start(thread_mail)

        else:
            print("order received but cant offer - Sorry")

            if self.bar.get_production_flag():
                thread_mail = myThread(
                    lambda: self.send_mail_to(self.lastSenderAdress, self.order_not_possible_msg, self.header))
                self.threadpool.start(thread_mail)

            else:
                msg = self.unknow_order_msg + self.bar.get_all_drinks_string()
                thread_mail = myThread(
                    lambda: self.send_mail_to(self.EmailOrder.lastSenderAdress, msg, self.header))
                self.threadpool.start(thread_mail)

            print(self.lastSenderAdress)
            print("Mail sent")

    def check_order(self):

        if self.check_now_flag == 0:
            co_thread = myThread(lambda: self.check_new_order())
            self.threadpool.start(co_thread)

# finished 02.12.2018"""
