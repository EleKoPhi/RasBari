from Widgets.my_widget_class import *
from classes.bottle_line import *

# Widget where your can see all bottles in the System
# Displays, bottle name, how much is left
# Button clear, to output the remaining liquid
# Button reset, need to be pressed after a new bottle is loaded

class bottle_widget_class(my_widget):

    def __init__(self, stacked_widget, ui_gui, ui_layout, master_bar):
        super().__init__(stacked_widget, ui_gui, ui_layout, master_bar)

        self.ui_gui.updateGUI_global.connect(self.updateWidget)

        self.Bottle_pages = []
        self.lines = []

        top_space = self.layout.GUI_Height * 0.16
        button_txt = ["<- Change left", "Exit", "Change right ->"]

        nr_widgets = int(len(self.bar.Bottles) / 5)

        if len(self.bar.Bottles) % 5 != 0:
            nr_widgets += 1

        for i in range(nr_widgets-1):
            self.Bottle_pages.extend([my_widget(stacked_widget, ui_gui, ui_layout, master_bar)])
            self.Bottle_pages[i].setObjectName("Bottlepage" + str(i))
            stacked_widget.addWidget(self.Bottle_pages[i].widget)

        self.Bottle_pages.extend([self])

        # Build the bottomNavigation for every bottle_Widget

        for i in range(len(self.Bottle_pages)):

            page_left = self.Bottle_pages[i - 1]

            try:
                page_right = self.Bottle_pages[i + 1]
            except:
                page_right = self.Bottle_pages[0]

            self.bottomNavigation(self.Bottle_pages[i].widget, page_left.widget, page_right.widget,
                                  self.ui_gui.main_container.widget, button_txt)

        # Build for every bottle one line that's shows - NAME - LEVEL + REST_Button + CLEAR_Button

        page = -1
        j = 0

        for i in range(len(self.bar.Bottles)):

            if i % 5 == 0:
                page += 1
                j = 0

            line_y = top_space + j * (self.layout.button_height + self.layout.top_space * 1.7)

            self.lines.extend([BottleLine(self, self.Bottle_pages[page].widget, self.bar.Bottles[i], 0, line_y,self.layout,self.bar)])

            j += 1

    def updateWidget(self):
        for i in range(0, len(self.lines)):
            self.lines[i].updateStatusBar()