class lo:

    def __init__(self, width, height):
        self.GUI_Width = width* 1.048 * 0.58  # TODO CHANGE THIS !!!
        self.GUI_Height = height * 0.5479

        self.button_space = self.GUI_Height / 100
        self.top_space = self.GUI_Height / 50
        self.bottom_button_getin = self.GUI_Width * 0.05

        self.button_width = self.GUI_Width / 4
        self.button_height = self.GUI_Height * 0.1
        self.txt_height = self.GUI_Height * 0.06

        self.bottom_button_y = self.GUI_Height * 0.84
        self.bottom_txt_y = self.GUI_Height * 0.83 - self.txt_height
