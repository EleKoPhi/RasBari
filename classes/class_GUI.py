from classes.class_Bar import *
from classes.class_eMailGuard import *
from classes.Layout_class import *

from widget_imports import *

class UiGui(QWidget, QObject):

    updateGUI = pyqtSignal()
    clear = pyqtSignal()

    def __init__(self, width, height, global_widget):
        QObject.__init__(self)

        self.RasBari = Bar()
        self.EmailOrder = eMailGuard()
        self.threadpool = QThreadPool()

        self.globWig = global_widget
        self.MailTimer = QtCore.QTimer()

        self.GUI_layout = self.calculateGUI(width, height)

        self.main_container = main_widget_class(self.globWig, self, self.GUI_layout, self.RasBari)
        self.bottle_container = bottle_widget_class(self.globWig, self, self.GUI_layout, self.RasBari)
        self.drink_menue_container = drink_menue_class(self.globWig, self, self.GUI_layout, self.RasBari)
        self.included_drinks_contrainer = included_drinks_class(self.globWig, self, self.GUI_layout, self.RasBari)
        self.new_drink_container = new_drink_widget_class(self.globWig, self, self.GUI_layout, self.RasBari)
        self.mssing_ingreds_container = missing_ingeds_class(self.globWig, self, self.GUI_layout, self.RasBari)

        self.setupUi(self.globWig)

    def setupUi(self, stacked_widget):
        stacked_widget.setObjectName("stacked_widget")

        stacked_widget.setObjectName("GUI")
        stacked_widget.resize(self.GUI_layout.GUI_Width, self.GUI_layout.GUI_Height)
        stacked_widget.setMaximumSize(QtCore.QSize(self.GUI_layout.GUI_Width, self.GUI_layout.GUI_Height))
        stacked_widget.setMinimumSize(QtCore.QSize(self.GUI_layout.GUI_Width, self.GUI_layout.GUI_Height))

        QtCore.QMetaObject.connectSlotsByName(stacked_widget)

        # self.RasBari.missingIngred.connect(lambda: self.show_widget(self.ingredWidg, 1))
        # self.RasBari.drinkunknown.connect(lambda: self.showmsgbox)
        # self.RasBari.changedAmountSig.connect(self.update_glass_txt)
        # self.RasBari.changedStatus.connect(self.update_status_txt)

        # self.EmailOrder.CheckMail.connect(self.exeOrder)

        self.MailTimer.setSingleShot(False)
        if getFlag("Mailorder") & self.EmailOrder.status: self.MailTimer.start(3000)
        self.MailTimer.timeout.connect(lambda: self.check4order())

        self.globWig.setCurrentIndex(self.globWig.indexOf(self.main_container.widget))
        QtCore.QMetaObject.connectSlotsByName(stacked_widget)

    @staticmethod
    def calculateGUI(width, height):
        return lo(width, height)
