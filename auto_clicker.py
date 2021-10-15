import sys
from PySide6 import QtCore, QtWidgets, QtGui
from pynput import keyboard
import threading
from pynput.mouse import Button,Controller
import time


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.mouse=Controller()
        global clicker_state
        clicker_state = False
        self.listener()
        self.setWindowTitle('Auto_clicker v1.0')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.onlyint = QtGui.QIntValidator()
        self.label = QtWidgets.QLabel('Status:',self)
        self.label.move(20,5)
        self.label_2 = QtWidgets.QLabel('Not running', self)
        self.label_2.move(70,5.5)
        self.label_3 = QtWidgets.QLabel('Delay(Miliseconds): ',self)
        self.label_3.move(20,30)
        self.line = QtWidgets.QLineEdit('5',self)
        self.line.setValidator(self.onlyint)
        self.line.move(150,25)
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.addItem("Left mouse button")
        self.comboBox.addItem("Middle mouse button")
        self.comboBox.addItem("Right mouse button")
        self.comboBox.move(20, 80)
        self.label_4 = QtWidgets.QLabel('Start/Stop shortcut:',self)
        self.label_4.move(20,55)
        self.shortcut = QtWidgets.QLabel('v',self)
        self.shortcut.move(150,55)
        self.start = QtWidgets.QPushButton('Start',self)
        self.start.move(20,110)
        self.start.clicked.connect(self.clicker)
        self.stop = QtWidgets.QPushButton('Stop',self)
        self.stop.move(105,110)
        self.stop.clicked.connect(self.stop_clicker)
    def listener(self):
        listener = keyboard.Listener(
        on_press=self.key_check)
        listener.start()

    def main_clicker(self,delay,button):
        delay=int(delay)
        delay=delay/1000
        while True:
            global clicker_state
            if clicker_state:
                self.mouse.click(button)
                time.sleep(delay)
            else:
                break

    def clicker(self):
        global clicker_state
        delay=self.line.text()
        if not clicker_state :
            button=self.comboBox.currentText()
            if button == 'Left mouse button':
                button=Button.left
            elif button == 'Middle mouse button':
                button=Button.middle
            else: 
                button=Button.right
            clicker_state = True
            self.t = threading.Thread(target=self.main_clicker,args=[delay,button])
            self.t.start()
        elif clicker_state:
            self.stop_clicker()

    def key_check(self,key):
        key=str(key)
        if key == "'v'":
            self.clicker()
            
    def stop_clicker(self):
        global clicker_state
        clicker_state=False
        self.t.join()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(300, 150)
    
    widget.show()
    
    sys.exit(app.exec())