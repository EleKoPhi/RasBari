StyleSheet = """



QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
    border: 1px solid #5c5c5c;
    width: 30px;
    margin: 0px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
    border-radius: 4px;
    
}

QSlider::groove:horizontal {
    border: 0px solid #999999;
   
    height: 20px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
    margin: 0px 0;

}

QSlider::handle:horizontal {
    height: 10px;
    background: grey;
    margin: 0 0px; /* expand outside the groove */
}

QSlider::add-page:horizontal {
    background: white;
}

QSlider::sub-page:horizontal {
    background: grey;
}



"""


def ApplyStyleSheets(App):
    App.setStyleSheet(StyleSheet)
