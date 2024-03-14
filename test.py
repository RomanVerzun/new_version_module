import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSpinBox
from PyQt5.QtCore import QTimer

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.layout = QVBoxLayout()
        
        # Создаем QSpinBox
        self.spinBox = QSpinBox(self)
        self.spinBox.setMinimum(0) # Минимальное значение
        self.spinBox.setMaximum(100) # Максимальное значение
        
        self.layout.addWidget(self.spinBox)
        self.setLayout(self.layout)
        
        # Настройка QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateSpinBox)
        self.timer.start(50) # Задержка в миллисекундах
        
    def updateSpinBox(self):
        # Увеличиваем значение на 1, сбрасываем, если достигнуто максимальное
        currentValue = self.spinBox.value()
        if currentValue < self.spinBox.maximum():
            self.spinBox.setValue(currentValue + 1)
        else:
            self.spinBox.setValue(self.spinBox.minimum())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
