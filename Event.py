from datetime import datetime,timedelta
textGS = 'werden gelbe säcke abgeholt'
textAP = 'wird altpapier abgeholt'
textHM = 'wird hausmüll abgeholt'
class Event():
    def __init__(self, wd, tag, monat, jahr, text, vorab):
        if tag   != '*': tag   = int(tag)
        if monat != '*': monat = int(monat) - 1
        if jahr  != '*': jahr  = int(jahr)
        self.tag = tag
        self.monat = monat
        self.jahr = jahr
        self.text = text
        self.vorab = vorab
        self.wd = wd
        self.type = 0
        if wd >= 0:
            self.type = 1
        elif monat == '*':
            self.type = 2
        elif jahr == '*':
            self.type = 3
        elif text == textGS:
            self.type = 4
        elif text == textAP:
            self.type = 5
        elif text == textHM:
            self.type = 6

    def isObsolete(self):
        if self.type > 0 and self.type < 4: return False
        today = datetime.now()
        limit = today.day + (today.month - 1) * 31 + today.year * 366
        d = self.tag + self.monat * 31 + self.jahr * 366
        return d < limit
    def sortKey(self):
        if self.type == 1: return self.wd
        key = self.tag
        if self.monat != '*': key += self.monat * 31
        if self.jahr  != '*': key += self.jahr  * 366
        return key

class EventList():
    def __init__(self, filename):

        self.filename = filename
        self.allElements = []
        older = datetime.now() - timedelta(1)
        self.minJahr = older.year
        self.maxJahr = self.minJahr + 1
        if filename is not None: self.readMessageFile(filename)
        self.sort()

    def sort(self):
        self.allElements.sort(key=lambda x: x.sortKey())
    def getEventList(self, type):
        list = []
        for ev in self.allElements:
            if ev.type == type: list.append(ev)
        if len(list) > 0: return list
        today = datetime.now()
        if   type == 1: dummy = Event(0, '*', '*', '*', 'neuer Eintrag', True)
        elif type == 2: dummy = Event(-1, today.day, '*', '*', 'neuer Eintrag', True)
        elif type == 3: dummy = Event(-1, today.day, today.month, '*', 'neuer Eintrag', True)
        elif type == 4: dummy = Event(-1, today.day, today.month, today.year, textGS, True)
        elif type == 5: dummy = Event(-1, today.day, today.month, today.year, textAP, True)
        elif type == 6: dummy = Event(-1, today.day, today.month, today.year, textHM, True)
        else:           dummy = Event(-1, today.day, today.month, today.year, 'neuer Eintrag', True)
        self.addEvent(dummy)
        list.append(dummy)
        return list
    def saveData(self, file = None):
        if file is None: file = self.filename

        with open(file, 'w') as f:
            for ev in self.allElements:
                if ev.text == 'neuer Eintrag': continue
                if ev.type == 4:
                    text = textGS
                elif ev.type == 5:
                    text = textAP
                elif ev.type == 6:
                    text = textHM
                else:
                    text = ev.text
                if ev.vorab: text = '+' + text
                if ev.type == 1:
                    msg = self.monatNames[ev.wd] + ':' + text
                else:
                    m = ev.monat
                    if m != '*': m += 1
                    msg = f'{ev.jahr}-{m}-{ev.tag}:{text}'
                f.write(msg + '\n')
    def readMessageFile(self, messagesFile):
        self.monatNames = ['mo', 'di', 'mi', 'do', 'fr', 'sa', 'so']
        try:
            with open(messagesFile) as f:
                lines = f.readlines()
                for line in lines:
                    line = line.replace('\n', '')
                    entries = line.split(":")
                    if len(entries) == 2:
                        msg = entries[1]
                        vorab = False
                        if msg[0] == '+':
                            vorab = True
                            msg = msg[1:]
                        try:
                            first = entries[0].lower()
                            wdFlag = False
                            for wd, name in enumerate(self.monatNames):
                                if first == name:
                                    self.addEvent(Event(wd, '*', '*', '*', msg, vorab))
                                    wdFlag = True
                                    break
                            if not wdFlag:
                                spec = entries[0].split('-')
                                self.addEvent(Event(-1, spec[2], spec[1], spec[0], msg, vorab))
                        except:
                            print(f'Ignore date {line}')
                    else:
                        print(f'Ignore line {entries[0]}')
                print('Tagesnachrichten: ' , self.messages)
        except:
            return
    def addEvent(self, event):
        self.allElements.append(event)
        if event.jahr != '*':
            self.minJahr = min(self.minJahr, event.jahr)
            self.maxJahr = max(self.maxJahr, event.jahr)

    def remEvent(self, event):
        self.allElements.remove(event)