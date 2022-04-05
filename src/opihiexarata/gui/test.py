import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PIL import ImageQt


class getColorLabel(QLabel):
    def __init__(self, widget):
        super(getColorLabel, self).__init__(widget)
        self.main = widget

    def mousePressEvent(self, event):
        self.main.get(event.pos())


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle('Drop Event Test')

        # Get Position
        self.label = getColorLabel(self)
        self.label.setGeometry(200, 250, 400, 300)
        self.label.setPixmap(QPixmap('test.png'))
        self.label.setScaledContents(True)

        # Display
        self.displayLabel = QLabel(self)
        self.displayLabel.setGeometry(300, 0, 200, 200)
        self.displayLabel.setStyleSheet('background-color: rgb(255, 255, 255);')

    def get(self, pos):
        index = pos.y()*self.label.size().width()+pos.x()
        image = ImageQt.fromqpixmap(self.label.pixmap())
        image = image.resize((self.label.size().width(), self.label.size().height()))
        image_data = image.getdata()
        r, g, b = image_data[index]
        self.displayLabel.setStyleSheet('background-color: rgb({},{},{});'.format(r, g, b))


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())