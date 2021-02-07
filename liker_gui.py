from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from video_liker import start_liking

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("Video Liker GUI Test")
        self.initUI()

    def initUI(self):
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Start")
        self.b1.move(350, 275)
        self.b1.clicked.connect(self.like_videos)

    def like_videos(self):
        start_liking()


app = QApplication(sys.argv)
main_win = MainWindow()
main_win.show()
sys.exit(app.exec_())


