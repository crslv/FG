import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize, Qt
from collections import Counter
import pylab 
import csv

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        self.eng_symbols = [
            'a', 'b', 'c', 'd', 'e',
            'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o',
            'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y',
            'z',
            'A', 'B', 'C', 'D', 'E',
            'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y',
            'Z',]

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('Collection of laboratory implementations')

        self.resize(760, 530)
        self.center()

        self.setWindowTitle('Fundamentals of cryptology')
        self.setWindowIcon(QIcon('cracken.png'))

        # actions for File and Method
        self.openAction = QAction('Open file')
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.triggered.connect(self.open_file)

        self.saveAction = QAction('Save file')
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.triggered.connect(self.save_file)

        self.lab1Action = QAction('Frequency analysis')   
        self.lab2Action = QAction('Soon')      

        #menu
        self.statusBar()
        self.menubar = self.menuBar()

        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)

        self.fileMenu = self.menubar.addMenu('&Method')
        self.fileMenu.addAction(self.lab1Action)
        self.fileMenu.addAction(self.lab2Action)

        #Frequency analysis
        self.browser = QTextBrowser(self)
        self.browser.resize(416, 100)
        self.browser.move(30, 50)
    
        self.label = QLabel('Frequency analysis', self)
        self.label.setFont(QFont('SansSerif', 20))
        self.label.resize(250, 30)
        self.label.move(485, 60)

        #buttons
        self.button_browse = QPushButton('Create a table', self)
        self.button_browse.resize(100, 30)
        self.button_browse.move(480, 120)
        self.button_browse.clicked.connect(self.create_table)

        self.combo_box = QComboBox(self)
        self.combo_box.addItems(["Sort by alphabet", "Sort by frequency"])
        self.combo_box.resize(110, 30)
        self.combo_box.move(615, 120)

        # table
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setRowCount(26)
        self.table.move(480, 180)
        self.table.resize(245, 320)
        self.table.setHorizontalHeaderLabels(["Letter", "Frequency"])

        # bar char
        self.label = QLabel(self)
        self.label.resize(416, 320)
        self.label.move(30, 180)  
        self.label.setPixmap(QPixmap('s.png'))

        self.show()

    def get_txt(self, file):
        txt = open(file, "r", encoding="utf8")
        return txt.read()

    def get_alp(self, txt):
        alp = []
        for a in txt:
            if a in self.eng_symbols:
                alp.append(a.lower())
        return alp

    def sort_alp(self, dictionary):
        return dict(sorted(dictionary.items(), key=lambda item: item[0]))

    def sort_frequency(self, dictionary):
        return dict(reversed(list(dict(sorted(dictionary.items(), key=lambda item: item[1])).items())))

    def open_file(self):
        self.file_name = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")
        if str(self.file_name) != "('', '')":
            self.browser.clear()
            self.txt_content = self.get_txt(self.file_name[0])
            self.browser.append(self.txt_content)

    def save_file(self):
        self.file_name = QFileDialog.getSaveFileName(self,"Save file", "" ,"CSV Files (*.csv)")
        if str(self.file_name) != "('', '')" and str(self.browser.toPlainText()) != "":
            with open(self.file_name[0], 'w') as file:
                for key in self.dictionary.keys():
                    file.write("%s,%s\n"%(key, self.dictionary[key]))

    def create_table(self):
        pylab.clf()
        if str(self.browser.toPlainText()) != "":
            if self.combo_box.currentText() == 'Sort by alphabet':
                self.dictionary = self.sort_alp(Counter(self.get_alp(self.get_txt(self.file_name[0]))))
            elif self.combo_box.currentText() == 'Sort by frequency':
                self.dictionary = self.sort_frequency(Counter(self.get_alp(self.get_txt(self.file_name[0]))))

            self.keys_arr = []
            for i in self.dictionary.keys():
                self.keys_arr.append(i)
            self.values_arr = []
            for i in self.dictionary.values():
                self.values_arr.append(round(i / sum(self.dictionary.values()), 5))

            for i in range(len(self.dictionary)):
                self.table.setItem(i, 0, QTableWidgetItem(self.keys_arr[i]))
                self.table.setItem(i, 1, QTableWidgetItem(str(self.values_arr[i])))
                
            pylab.bar(self.keys_arr, self.values_arr)
            pylab.savefig('d.png', dpi=65)
            self.label.setPixmap(QPixmap('d.png'))


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())