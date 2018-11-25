from super_widget import *
from bottle_line import *

class bottle_display(my_widget):

    lines = []
    Bottle_pages = []

    def __init__(self, main_widget, program, GUI_layout,main_bar):
        super().__init__(main_widget, program, GUI_layout,main_bar)

        self.Bar = main_bar

        top_space = self.layout.GUI_Height * 0.16
        button_txt = ["<- Change left", "Exit", "Change right ->"]

        #self.updateGUI.connect(self.updateWidget)

        print(len(self.Bar.Bottles))

        nr_widgets = int(len(self.Bar.Bottles) / 5)

        if len(self.Bar.Bottles) % 5 != 0:
            nr_widgets += 1

        for i in range(nr_widgets-1):
            self.Bottle_pages.extend([my_widget(main_widget, program, GUI_layout,main_bar)])
            self.Bottle_pages[i].setObjectName("Bottlepage" + str(i))
            main_widget.addWidget(self.Bottle_pages[i].widget)

        self.Bottle_pages.extend([self])

        # Build the bottomNavigation for every bottle_Widget

        for i in range(len(self.Bottle_pages)):

            page_left = self.Bottle_pages[i - 1]

            try:
                page_right = self.Bottle_pages[i + 1]
            except:
                page_right = self.Bottle_pages[0]

            print(page_right)

            self.bottomNavigation(self.Bottle_pages[i].widget, page_left.widget, page_right.widget,
                                  self.program.main_menue.widget, button_txt)

        # Build for every bottle one line that's shows - NAME - LEVEL + REST_Button + CLEAR_Button

        page = -1
        j = 0

        for i in range(len(self.Bar.Bottles)):

            if i % 5 == 0:
                page += 1
                j = 0

            line_y = top_space + j * (self.layout.button_height + self.layout.top_space * 1.7)

            self.lines.extend([BottleLine(self, self.Bottle_pages[page].widget, self.Bar.Bottles[i], 0, line_y,self.layout)])

            j += 1

    def updateWidget(self):
        for i in range(0, len(self.lines)):
            self.lines[i].updateStatusBar()