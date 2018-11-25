from Widgets.my_widget_class import *


class drink_menue_class(my_widget):

    def __init__(self, stacked_widget, ui_gui, ui_layout, master_bar):
        super().__init__(stacked_widget, ui_gui, ui_layout, master_bar)

        std_height = self.layout.button_height
        std_width = self.layout.button_width
        std_width_menue = self.layout.GUI_Width / 2 - self.layout.bottom_button_getin * 1.5
        std_y_menue = self.layout.GUI_Height / 2 - std_height / 2
        std_y = self.layout.bottom_button_y

        # NewDrink pushbutton to navigate to the newdrink widget

        self.newdrink_button = QtWidgets.QPushButton(self.widget)
        self.newdrink_button.setGeometry(
            QtCore.QRect(self.layout.bottom_button_getin, std_y_menue, std_width_menue, std_height))
        self.newdrink_button.setText("Let me make a new drink!")
        self.newdrink_button.clicked.connect(lambda: self.show_widget(self.ui_gui.new_drink_container.NewDrink_pages[0].widget, 1))

        # ShowDrink pushbutton to naviate to the widget that shows all included drinks

        show_drink_x = self.layout.GUI_Width - self.layout.bottom_button_getin - std_width_menue

        self.showdrink_button = QtWidgets.QPushButton(self.widget)
        self.showdrink_button.setGeometry(QtCore.QRect(show_drink_x, std_y_menue, std_width_menue, std_height))
        self.showdrink_button.setText("Show included drinks!")

        self.showdrink_button.clicked.connect(lambda: self.show_widget(self.ui_gui.included_drinks_container.widget, 1))

        # ExitButton - Button to navigate back to the main widget

        exit_button_x = (self.layout.GUI_Width / 2 - self.layout.button_width / 2)

        self.exit_button = QtWidgets.QPushButton(self.widget)
        self.exit_button.setGeometry(QtCore.QRect(exit_button_x, std_y, std_width, std_height))
        self.exit_button.setText("Exit")

        self.exit_button.clicked.connect(lambda: self.show_widget(self.ui_gui.main_container.widget, 1))
