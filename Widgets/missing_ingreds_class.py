from Widgets.my_widget_class import *

class missing_ingeds_class(my_widget):

    def __init__(self, stacked_widget, ui_gui, ui_layout, master_bar):
        super().__init__(stacked_widget, ui_gui, ui_layout, master_bar)

        std_width = self.layout.button_width
        std_hight = self.layout.button_height

        YESBut_x = self.layout.bottom_button_getin
        YESBut_y = self.layout.GUI_Height / 2 - std_hight / 2

        NOBut_x = self.layout.GUI_Width - self.layout.bottom_button_getin - self.layout.button_width
        NOBut_y = YESBut_y

        Message_x = self.layout.GUI_Width / 2 - std_width / 2
        Message_y = self.layout.GUI_Height / 2 - std_hight
        Message_hight = std_hight * 2
        Message_content = "You have missing ingredients"

        self.YESBut = QtWidgets.QPushButton(self.widget)
        self.YESBut.setGeometry(QtCore.QRect(YESBut_x, YESBut_y, std_width, std_hight))
        self.YESBut.setText("Restore bottles")
        self.YESBut.clicked.connect(lambda: self.show_widget(self.ui_gui.bottle_container.Bottle_pages[0].widget,1))

        self.NOBut = QtWidgets.QPushButton(self.widget)
        self.NOBut.setGeometry(QtCore.QRect(NOBut_x, NOBut_y, std_width, std_hight))
        self.NOBut.setText("Back to main")
        self.NOBut.clicked.connect(lambda: self.show_widget(self.ui_gui.main_container.widget, 1))

        self.Message = QtWidgets.QLabel(self.widget)
        self.stdLabelSetUp(self.Message)
        self.Message.setGeometry(QtCore.QRect(Message_x, Message_y, std_width, Message_hight))
        self.Message.setText(Message_content)
