
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QCheckBox, QFormLayout, QTabWidget
import sys
from EventWidget import EventWidget
from Event import Event, EventList
class MainWindow(QTabWidget):
    def __init__(self, events):
        super(MainWindow, self).__init__()

        self.setStyleSheet('font-size: 14pt; font-family: Arial;')
        self.setWindowTitle("Tagenachrichten")
        self.addTab(EventWidget(self, events, 0)  , "Einmalig")
        self.addTab(EventWidget(self, events, 1)  , "Wöchentlich")
        self.addTab(EventWidget(self, events, 2)  , "Monatlich")
        self.addTab(EventWidget(self, events, 3)  , "Jährlich")
        self.addTab(EventWidget(self, events, 4)  , "Gelbe Säcke")
        self.addTab(EventWidget(self, events, 5)  , "Hausmüll")
        self.addTab(EventWidget(self, events, 6)  , "Altpapier")
        self.resize(2200, 1600)

def main():
    app = QApplication(sys.argv)
    events = EventList('messages.text')
    main = MainWindow(events)
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()