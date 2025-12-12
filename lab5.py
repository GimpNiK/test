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


page2 = QWidget()
page2_layout = QVBoxLayout(page2)

progress_bar_descr = QLabel("Готов к установке")
progress_bar = QProgressBar()
progress_bar.setRange(0, 100)
progress_bar.setValue(0)
show_results_btn = QPushButton("Показать результаты")

page2_layout.addWidget(progress_bar_descr)
page2_layout.addWidget(progress_bar)
page2_layout.addWidget(show_results_btn)

pages.addWidget(page2)

page3 = QWidget()
page3_layout = QVBoxLayout(page3)
page3_table = QTableWidget()

page3_table.setHorizontalHeaderLabels(["Имя файла","Время установки"])
data = [
    ['encoding_utils.py',1.2],
    ['archive_utils.py',3.2],
    ['gui.py',4.2]
]

page3_table.setRowCount(len(data))
page3_table.setColumnCount(len(data[0])) 
for row in range(len(data)):
            for col in range(len(data[0])):
                item = QTableWidgetItem(str(data[row][col]))
                page3_table.setItem(row, col, item)
page3_table.resizeColumnsToContents()

page3_layout.addWidget(page3_table)
pages.addWidget(page3)

timer = QTimer()
def update_progress():
    elapsed_time = 0
    def run():
        nonlocal elapsed_time
        elapsed_time += 1
        
        current_os = input_os.currentText()
        
        progress_bar_descr.setText(
            f"Идет установка для {current_os}.\n"
            f"Прошло времени: {elapsed_time} секунд"
        )
        
        
        progress_value = min(elapsed_time * 10, 100)
        progress_bar.setValue(progress_value)
        
        if progress_value >= 100:
            timer.stop()
            progress_bar_descr.setText(
                f"Установка для {current_os} завершена!\n"
                f"Общее время: {elapsed_time} секунд"
            )
    return run

def start_installation():    
    progress_bar_descr.setText(f"Начинаем установку для {input_os.currentText()}...")
    progress_bar.setValue(0)
    
    pages.setCurrentIndex(1)

    timer.start(1000)
    timer.timeout.connect(update_progress())

def show_results():
     pages.setCurrentIndex(2)

install_btn.clicked.connect(start_installation)
show_results_btn.clicked.connect(show_results)


mainwindow.adjustSize()
mainwindow.show()
app.exec()
