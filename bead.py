# -*- coding: UTF-8 -*-

import re

class Szamla:
    accountid = ""
    name = ""
    lastchage = ""
    ballance = 0
    def __init__(self, line):
        words = line.split(" ")
        self.accountid = words[0]
        name = ""
        i = 1
        while (True):
            m = re.search('^[0-9]{4}\.[0-9]{2}\.[0-9]{2}\.$', words[i])
            if m is None:
                name += words[i] + " "
            else:
                break
            i = i + 1
        self.name = name[:-1]
        self.lastchage = words[i]
        if (words[i + 1][-1] == " " || words[i + 1][:-1] == "\n"):
            self.ballance = int(words[i + 1][:-1])
        else:
            self.ballance = int(words[i + 1])
    def toString(self):
        stri = self.accountid + " " + self.name + " " + self.lastchage + " " + str(self.ballance)
        return stri
    def addBallance(self, changedate, newBallance):
        self.ballance += newBallance
        self.lastchage = changedate
    
class Bank:
    szamlak = []
    def loadFromFile(self, filename):
        self.loadData(open(filename, "r"))
    def loadData(self, data):
        for line in data:
            self.newAccount(line)
    def newAccount(self, line):
        self.szamlak.append(Szamla(line));
    def getAccountCount(self):
        return len(self.szamlak)
    def printData(self):
        self.orderByAccountId()
        for item in self.szamlak:
            print item.toString()
    def saveToFile(self, filename):
        self.orderByAccountId()
        fls = open(filename, "w")
        for i in range(len(self.szamlak)):
            fls.write(self.szamlak[i].toString())
            if (i != len(self.szamlak) - 1):
                fls.write("\n")
        fls.close()
    def processChangeLine(self, date, line):
        words = line.split(" ")
        for i in range(len(self.szamlak)):
            if (self.szamlak[i].getAccountId() == words[0]):
                addblc = int(words[-1])
                self.szamlak[i].addBallance(date, addblc)
                return
        newl = ""
        for i in range(len(words)):
            newl += words[i] + " "
            if (i == len(words) - 2):
                newl += date + " "
        self.newAccount(newl)
    def processChanges(self, changes):
        currentDate = ""
        for line in changes:
            datum = re.search('^[0-9]{4}\.[0-9]{2}\.[0-9]{2}\.$', line)
            if datum is not None:
                currentDate = line[:-1]
            else:
                if (currentDate == ""):
                    raise Exception('No date given')
                self.processChangeLine(currentDate, line)
    def processChangesFromFile(self, filename):
        self.processChanges(open(filename, "r"))
    def orderByAccountId(self):
        self.szamlak.sort(key=lambda x: x.accountid)
        
bank = Bank()
bank.loadFromFile("data.txt")
bank.processChangesFromFile("update")
bank.saveToFile("newdata")
