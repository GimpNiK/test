import sys
from PyQt6.QtWidgets import QApplication, QMainWindow,QTableWidgetItem, QListWidget, QLabel, QPushButton, QProgressBar, QStackedWidget,QWidget,QVBoxLayout,QComboBox,QTableWidget
from PyQt6.QtCore import QTimer

lang = "eng"
class LabelState:

    def __init__(self, widget, state,states):
        self.widget = widget
        self.state = state
        self.states = states
    
    def setState(self, key, args=()):
        try:
            self.state = self.states[key][lang](*args)
        except:
            self.state = self.states[key][lang]
        self.widget.setText(self.state)

app = QApplication(sys.argv)

mainwindow = QMainWindow()
mainwindow.setWindowTitle("Lab 5")


pages = QStackedWidget()
mainwindow.setCentralWidget(pages)


page1 = QWidget()
page1_layout = QVBoxLayout(page1)

input_os_descr = QLabel()
input_os_descr_state = LabelState(input_os_descr,"select",{"select":{"ru":"Выберите операционную систему:","eng":"Select os:"}})
input_os = QComboBox()




input_os.addItems(["Windows", "Linux", "MacOS"])

install_btn = QPushButton("Установить")

page1_layout.addWidget(input_os_descr)
page1_layout.addWidget(input_os)
page1_layout.addWidget(install_btn)

pages.addWidget(page1)


page2 = QWidget()
page2_layout = QVBoxLayout(page2)

progress_bar_descr = QLabel()
progress_bar_state = LabelState(progress_bar_descr,"start",states = {
        "start": {"ru":"Готов к установке","eng": "ready to install"},
        "start_install": {"ru": lambda os_name: f"Начинаем установку для {os_name}...", "eng": lambda os_name: f"Start intall for {os_name}..."}, 
        "continue_install": {"ru":lambda current_os, elapsed_time: f"Идет установка для {current_os}.\nПрошло времени: {elapsed_time} секунд","eng":lambda current_os, elapsed_time: f"Running install {current_os}.\nElipsed time: {elapsed_time} seconds",},
        "done": {"ru":lambda current_os, elapsed_time: f"Install for {current_os} done!\nAll time: {elapsed_time} seconds","eng":lambda current_os, elapsed_time: f"Установка для {current_os} завершена!\nAll time: {elapsed_time} seconds"}
    })
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
    def update_time():
        nonlocal elapsed_time
        elapsed_time += 1
    def update_progress_bar():
        current_os = input_os.currentText()
        
        progress_bar_state.setState("continue_install",(current_os,elapsed_time))

        
        progress_value = min(elapsed_time * 10, 100)
        progress_bar.setValue(progress_value)
        
        if progress_value >= 100:
            timer.stop()
            progress_bar_state.setState("done",(current_os,elapsed_time))

    def run():
        update_time()
        update_progress_bar()
    return run

def start_installation():    
    progress_bar_state.setState("start_install", (input_os.currentText(),))
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
print()