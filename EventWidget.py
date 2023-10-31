from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QEvent
import socket
from os.path import exists
import glob
import os
import shutil
from PyQt5.uic.properties import QtCore, QtGui, QtWidgets

from Event import Event, EventList

class ComboJahr(QComboBox):
    def __init__(self, parent, event, minJahr, maxJahr):
        super().__init__(parent)
        for jahr in range(minJahr, maxJahr + 1):
            self.addItem(str(jahr))
        self.event = event
        self.currentIndexChanged.connect(self.getComboValue)
        self.setCurrentIndex(event.jahr - minJahr)

    def getComboValue(self):
        self.event.jahr = int(self.currentText())
class ComboMonat(QComboBox):
    def __init__(self, parent, event):
        super().__init__(parent)
        self.addItems(['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'])
        self.event = event
        self.currentIndexChanged.connect(self.getComboValue)
        self.setCurrentIndex(event.monat)
    def getComboValue(self):
        self.event.monat = self.currentIndex()
class ComboWochentag(QComboBox):
    def __init__(self, parent, event):
        super().__init__(parent)
        self.addItems(['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'])
        self.event = event
        self.currentIndexChanged.connect(self.getComboValue)
        self.setCurrentIndex(event.wd)
    def getComboValue(self):
        self.event.wd = int(self.currentIndex())
class EventTable(QTableWidget):
    def __init__(self, events, type):
        super().__init__()
        self.events = events
        self.type = type
        self.ignoreChanges = False
        self.setFont(QFont('Arial', 12))

        if type == 0:
            self.setColumnCount(7)
            self.setHorizontalHeaderLabels(['Tag', 'Monat', 'Jahr', 'Vortag', 'Nachricht', '', ''])
            self.textCol = 4
            width = [80,120,120,100, 800]
        elif type == 1 or type == 2:
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(['Tag', 'Vortag', 'Nachricht', '', ''])
            self.textCol = 2
            width = [200, 100, 600]
        elif type == 3:
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Tag', 'Monat', 'Vortag', 'Nachricht', '', ''])
            self.textCol = 3
            width = [80, 120, 100, 800]
        else:
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(['Tag', 'Monat', 'Jahr', 'Vortag', '', ''])
            self.textCol = 4
            width = [80,120,120,100]

        for i in range(len(width)):
           self.setColumnWidth(i, width[i])

        self.itemChanged.connect(self.cellChanged)
        self.update()

    def cellChanged(self):
        if self.ignoreChanges: return
        if self.currentColumn() == 0:
            self.list[self.currentRow()].tag = int(self.currentItem().text())
        elif self.currentColumn() == self.textCol:
            self.list[self.currentRow()].text = self.currentItem().text()
        elif self.currentColumn() == self.textCol - 1:
            print(self.currentItem())

    def copyData(self):
        ev = self.list[self.currentRow()]
        event = Event(ev.wd, ev.tag, ev.monat+1, ev.jahr, ev.text, ev.vorab)
        self.events.addEvent(event)
        self.events.sort()
        self.update()

    def rmData(self):
        self.events.remEvent(self.list[self.currentRow()])
        self.update()
    def setVorab(self, value):
        self.list[self.currentRow()].vorab = value

    def update(self):
        self.list = self.events.getEventList(self.type)
        self.ignoreChanges = True
        self.setRowCount(len(self.list))
        for i,ev in enumerate(self.list):
            if self.type == 1:
                self.setCellWidget(i, 0, ComboWochentag(self, ev))
            else:
                item = QTableWidgetItem(str(ev.tag))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(i, 0, item)
            nextCol = 1
            if self.type != 2 and self.type != 1:
                self.setCellWidget(i, nextCol, ComboMonat(self, ev))
                nextCol += 1

            if self.type != 2 and self.type !=3 and self.type != 1:
                self.setCellWidget(i, nextCol, ComboJahr(self, ev, self.events.minJahr, self.events.maxJahr))
                nextCol += 1

            item = QCheckBox()
            item.setChecked(ev.vorab)
            item.clicked.connect(self.setVorab)
            self.setCellWidget(i, nextCol, item)

            nextCol += 1
            if self.type < 4:
                item =QTableWidgetItem(ev.text)
                if ev.isObsolete():
                    item.setForeground(QColor(200, 200, 200))
                self.setItem(i, nextCol, item)
                nextCol += 1
            btn = QPushButton('kopieren')
            btn.clicked.connect(self.copyData)
            self.setCellWidget(i, nextCol, btn)

            btn = QPushButton('löschen')
            btn.clicked.connect(self.rmData)
            self.setCellWidget(i, nextCol+1, btn)
        self.ignoreChanges = False

class EventWidget(QWidget):
    def __init__(self, main, events, type, parent=None):
        QWidget.__init__(self, parent)
        self.main = main
        self.events = events
        self.type = type
        self.tableWidget = EventTable(events, type)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)


        self.controlWidget = QWidget()
        self.ctlLayout = QVBoxLayout()
        self.controlWidget.setLayout(self.ctlLayout)


        button = QPushButton('Chronoloisch sortieren')
        button.clicked.connect(self.sortData)
        self.ctlLayout.addWidget(button)

        button = QPushButton('Daten sichern')
        button.clicked.connect(self.saveData)
        self.ctlLayout.addWidget(button)

        button = QPushButton('Änderungen verwerfen')
        button.clicked.connect(self.reloadData)
        self.ctlLayout.addWidget(button)

        button = QPushButton('Programm abbrechen')
        button.clicked.connect(self.abortPgm)
        self.ctlLayout.addWidget(button)

        button = QPushButton('Daten speichern, Programm beenden')
        button.clicked.connect(self.exitPgm)

        self.ctlLayout.addWidget(button)

        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(self.controlWidget)

    def sortData(self):
        self.events.sort()
 #       self.tableWidget.list = self.events.getEventList(self.type)
        self.tableWidget.update()

    def saveData(self):
        self.events.saveData()
    def reloadData(self):
        print('reloadData')
    def abortPgm(self):
        self.main.close()
    def exitPgm(self):
        self.saveData()
        self.abortPgm()
