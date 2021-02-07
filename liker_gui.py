from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(800, 600)
        self.setWindowTitle("Video Liker GUI Test")
        self.initUI()

    def initUI(self):
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Start")
        self.b1.move(350,275)

