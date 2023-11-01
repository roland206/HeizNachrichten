import os
import platform
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QCheckBox, QFormLayout, QTabWidget
import sys
from EventWidget import EventWidget
from Event import Event, EventList
class MainWindow(QTabWidget):
    def __init__(self, events):
        super(MainWindow, self).__init__()

        self.setStyleSheet('font-size: 14pt; font-family: Arial;')
        self.setWindowTitle("Tagenachrichten")
        self.addTab(EventWidget(self, events, 0, images = ['klavier.png', 'untersuchung.png'])  , "Einmalig")
        self.addTab(EventWidget(self, events, 1, images = ['blumen.png'])  , "Wöchentlich")
        self.addTab(EventWidget(self, events, 2, images = ['spuelen.png'])  , "Monatlich")
        self.addTab(EventWidget(self, events, 3, images = ['party.png'])  , "Jährlich")
        self.addTab(EventWidget(self, events, 4, images = ['gelbesaecke.png'])  , "Gelbe Säcke")
        self.addTab(EventWidget(self, events, 6, images = ['Hausmuell.png'])  , "Hausmüll")
        self.addTab(EventWidget(self, events, 5, images = ['altpapier.png'])  , "Altpapier")
        self.resize(2400, 1600)

def main():
    app = QApplication(sys.argv)
    if platform.system() == 'Windows':
        os.chdir(sys.argv[0].replace('\\main.py', ''))
    else:
        os.chdir(sys.argv[0].replace('/main.py', ''))
    events = EventList('/home/roland/Heizung/Plannung/messages.text')
    main = MainWindow(events)
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()