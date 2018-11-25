from classes.class_Bar import *
from classes.class_eMailGuard import *
from classes.Layout_class import *
from widget_imports import *


class UiGui(QWidget, QObject):

    def __init__(self, width, height, global_widget):
        QObject.__init__(self)

        self.RasBari = Bar()
        self.EmailOrder = eMailGuard()
        self.threadpool = QThreadPool()

        self.globWig = global_widget
        self.MailTimer = QtCore.QTimer()

        self.updateGUI = pyqtSignal()

        self.GUI_layout = lo(width, height)

        self.globWig.setObjectName("stacked_widget")
        self.globWig.resize(self.GUI_layout.GUI_Width, self.GUI_layout.GUI_Height)
        self.globWig.setMaximumSize(QtCore.QSize(self.GUI_layout.GUI_Width, self.GUI_layout.GUI_Height))
        self.globWig.setMinimumSize(QtCore.QSize(self.GUI_layout.GUI_Width, self.GUI_layout.GUI_Height))

        self.main_container = main_widget_class(self.globWig, self, self.GUI_layout, self.RasBari)
        self.bottle_container = bottle_widget_class(self.globWig, self, self.GUI_layout, self.RasBari)
        self.drink_menue_container = drink_menue_class(self.globWig, self, self.GUI_layout, self.RasBari)
        self.included_drinks_container = included_drinks_class(self.globWig, self, self.GUI_layout, self.RasBari)
        self.new_drink_container = new_drink_widget_class(self.globWig, self, self.GUI_layout, self.RasBari)
        self.missing_ingreds_container = missing_ingeds_class(self.globWig, self, self.GUI_layout, self.RasBari)

        QtCore.QMetaObject.connectSlotsByName(self.globWig)

        self.MailTimer.setSingleShot(False)
        if getFlag("Mailorder") & self.EmailOrder.status: self.MailTimer.start(3000)
        self.MailTimer.timeout.connect(lambda: self.check4order())

        self.globWig.setCurrentIndex(self.globWig.indexOf(self.main_container.widget))
        QtCore.QMetaObject.connectSlotsByName(self.globWig)

        self.connect_system_signals()

    def connect_system_signals(self):

        self.RasBari.missingIngred.connect\
            (lambda:self.globWig.setCurrentIndex(self.globWig.indexOf(self.missing_ingreds_container.widget)))

        #self.EmailOrder.CheckMail.connect(self.EmailOrder.exeOrder())
