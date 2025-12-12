import sys
from PyQt6.QtWidgets import QApplication, QMainWindow,QTableWidgetItem, QListWidget, QLabel, QPushButton, QProgressBar, QStackedWidget,QWidget,QVBoxLayout,QComboBox,QTableWidget
from PyQt6.QtCore import QTimer

app = QApplication(sys.argv)

mainwindow = QMainWindow()
mainwindow.setWindowTitle("Lab 5")


pages = QStackedWidget()
mainwindow.setCentralWidget(pages)


page1 = QWidget()
page1_layout = QVBoxLayout(page1)

input_os_descr = QLabel("Выберите операционную систему:")
input_os = QComboBox()
input_os.addItems(["Windows", "Linux", "MacOS"])

install_btn = QPushButton("Установить")

page1_layout.addWidget(input_os_descr)
page1_layout.addWidget(input_os)
page1_layout.addWidget(install_btn)

pages.addWidget(page1)



mainwindow.adjustSize()
mainwindow.show()
app.exec()
