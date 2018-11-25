from Widgets.my_widget_class import *

class missing_ingeds_class(my_widget):

    def __init__(self, main_widget, program, GUI_layout,main_bar):
        super().__init__(main_widget, program, GUI_layout,main_bar)

        std_width = self.layout.button_width
        std_hight = self.layout.button_height

        YESBut_x = self.layout.bottom_button_getin
        YESBut_y = self.layout.GUI_Height / 2 - std_hight / 2

        self.YESBut = QtWidgets.QPushButton(self.widget)
        self.YESBut.setGeometry(QtCore.QRect(YESBut_x, YESBut_y, std_width, std_hight))
        self.YESBut.setText("Yes")
        self.YESBut.clicked.connect(lambda: self.show_widget(self.program.bottle_display.Bottle_pages[-1].widget,1))

        NOBut_x = self.layout.GUI_Width - self.layout.bottom_button_getin - self.layout.button_width
        NOBut_y = YESBut_y

        self.NOBut = QtWidgets.QPushButton(self.widget)
        self.NOBut.setGeometry(QtCore.QRect(NOBut_x, NOBut_y, std_width, std_hight))
        self.NOBut.setText("No")
        self.NOBut.clicked.connect(lambda: self.show_widget(self.program.main_menue.widget, 1))

        Message_x = self.layout.GUI_Width / 2 - std_width / 2
        Message_y = self.layout.GUI_Height / 2 - std_hight
        Message_hight = std_hight * 2
        Message_content = "You have missing ingredients\n\nDo you want to reset them?\nPlease make a desision"

        self.Message = QtWidgets.QTextBrowser(self.widget)
        self.Message.setGeometry(QtCore.QRect(Message_x, Message_y, std_width, Message_hight))
        self.Message.setText(Message_content)
