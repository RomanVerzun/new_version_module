from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

def replace_button():
    # Удалить старую кнопку
    layout.removeWidget(button)
    button.deleteLater()
    
    # Создать и добавить новую кнопку
    new_button = QPushButton('Новая кнопка')
    layout.addWidget(new_button)
    new_button.clicked.connect(lambda: print("Новая кнопка нажата"))

app = QApplication([])

window = QWidget()
layout = QVBoxLayout()

button = QPushButton('Старая кнопка')
button.clicked.connect(replace_button)

layout.addWidget(button)
window.setLayout(layout)

window.show()

app.exec_()
