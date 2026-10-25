from PyQt5.QtWidgets import QFrame, QVBoxLayout, QToolBox, QWidget, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap

class Sidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("sidebar")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedWidth(250)

        sidebar_layout = QVBoxLayout()

        toolbox = QToolBox()
        sidebar_layout.addWidget(toolbox)

        tab_1_widget = QWidget()
        tab_1_layout = QVBoxLayout()

        image1 = QLabel()
        image1.setPixmap(QPixmap('image1.jpg'))
        image2 = QLabel()
        image2.setPixmap(QPixmap('image2.jpg'))

        tab_1_layout.addWidget(image1)
        tab_1_layout.addWidget(image2)

        tab_1_widget.setLayout(tab_1_layout)
        toolbox.addItem(tab_1_widget, 'Favourits')
        tab_2_widget = QWidget()
        tab_2_layout = QVBoxLayout()

        image3 = QLabel()
        image3.setPixmap(QPixmap('image3.jpg'))
        image4 = QLabel()
        image4.setPixmap(QPixmap('image4.jpg'))

        tab_2_layout.addWidget(image3)
        tab_2_layout.addWidget(image4)

        tab_2_widget.setLayout(tab_2_layout)
        toolbox.addItem(tab_2_widget, 'Recents')

        tab_3_widget = QWidget()
        tab_3_layout = QVBoxLayout()

        image5 = QLabel()
        image5.setPixmap(QPixmap('image5.jpg'))

        tab_3_layout.addWidget(image5)

        tab_3_widget.setLayout(tab_3_layout)
        toolbox.addItem(tab_3_widget, 'key')

        tab_4_widget = QWidget()
        tab_4_layout = QVBoxLayout()

        image6 = QLabel()
        image6.setPixmap(QPixmap('image6.jpg'))

        tab_4_layout.addWidget(image6)

        tab_4_widget.setLayout(tab_4_layout)
        toolbox.addItem(tab_4_widget, 'clef')

        tab_5_widget = QWidget()
        tab_5_layout = QVBoxLayout()

        image7 = QLabel()
        image7.setPixmap(QPixmap('image7.jpg'))

        tab_5_layout.addWidget(image7)
        toolbox.addItem(tab_5_widget, self.tr('Measures'))

        tab_6_widget = QWidget()
        tab_6_layout = QVBoxLayout()

        image8 = QLabel()
        image8.setPixmap(QPixmap('image8.jpg'))

        tab_6_layout.addWidget(image8)

        tab_6_widget.setLayout(tab_6_layout)
        toolbox.addItem(tab_6_widget, self.tr('Chord symbols'))

        tab_7_widget = QWidget()
        tab_7_layout = QVBoxLayout()

        image9 = QLabel()
        image9.setPixmap(QPixmap('image9.jpg'))

        tab_7_layout.addWidget(image9)

        tab_7_widget.setLayout(tab_7_layout)
        toolbox.addItem(tab_7_widget, self.tr('Guitar symbols'))

        tab_8_widget = QWidget()
        tab_8_layout = QVBoxLayout()

        image10 = QLabel()
        image10.setPixmap(QPixmap('image10.jpg'))

        tab_8_layout.addWidget(image10)

        tab_8_widget.setLayout(tab_8_layout)
        toolbox.addItem(tab_8_widget, self.tr('Note symbols'))

        tab_9_widget = QWidget()
        tab_9_layout = QVBoxLayout()

        image11 = QLabel()
        image11.setPixmap(QPixmap('image11.jpg'))

        tab_9_layout.addWidget(image11)

        tab_9_widget.setLayout(tab_9_layout)
        toolbox.addItem(tab_9_widget, self.tr('Dynamics'))

        tab_10_widget = QWidget()
        tab_10_layout = QVBoxLayout()

        image12 = QLabel()
        image12.setPixmap(QPixmap('image12.jpg'))

        tab_10_layout.addWidget(image12)

        tab_10_widget.setLayout(tab_10_layout)
        toolbox.addItem(tab_10_widget, self.tr('Lines'))

        tab_11_widget = QWidget()
        tab_11_layout = QVBoxLayout()

        image13 = QLabel()
        image13.setPixmap(QPixmap('image13.jpg'))

        tab_11_layout.addWidget(image13)

        tab_11_widget.setLayout(tab_11_layout)
        toolbox.addItem(tab_11_widget, self.tr('Other'))

        tab_12_widget = QWidget()
        tab_12_layout = QVBoxLayout()

        add_image = QPushButton(self.tr("New symbol"))
        # add_image.clicked.connect(self.open_file)

        tab_12_layout.addWidget(add_image)

        tab_12_widget.setLayout(tab_12_layout)
        toolbox.addItem(tab_12_widget, self.tr('User symbols'))

        toolbox.setCurrentIndex(1)

        spacer_sidebar = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        sidebar_layout.addSpacerItem(spacer_sidebar)

        self.setLayout(sidebar_layout)