from PyQt5 import QtCore, QtGui, QtWidgets
from functions import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.itemsToLaunch = []
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        MainWindow.setStyleSheet("QMainWindow {"
                                 "background-color: white;"
                                 "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(".QPushButton {"
                                         "border: 0 solid;"
                                         "border-radius: 8px;"
                                         "color: white;"
                                         "font-size: 13px;"
                                         "font-weight: bold;"
                                         "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(178, 99, 252, 255), stop:0.5 rgba(251, 162, 213, 255), stop:1 rgba(182, 242, 221, 255));"
                                         "}"
                                         ".QPushButton:hover {"
                                         "font-size: 14px;"
                                         "}"
                                         ".QListWidget {"
                                         "    background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(178, 99, 252, 100), stop:0.5 rgba(251, 162, 213, 100), stop:1 rgba(182, 242, 221, 100));\n"
                                         "    border-radius: 8px}")
        self.centralwidget.setObjectName("centralwidget")
        self.settingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.settingsButton.setGeometry(QtCore.QRect(20, 260, 401, 41))
        self.settingsButton.setStyleSheet("")
        self.settingsButton.setObjectName("settingsButton")
        self.checkAccountsButton = QtWidgets.QPushButton(self.centralwidget)
        self.checkAccountsButton.setGeometry(QtCore.QRect(20, 20, 401, 41))
        self.checkAccountsButton.setStyleSheet("")
        self.checkAccountsButton.setObjectName("checkAccountsButton")
        self.addAccountsButton = QtWidgets.QPushButton(self.centralwidget)
        self.addAccountsButton.setGeometry(QtCore.QRect(20, 80, 401, 41))
        self.addAccountsButton.setStyleSheet("")
        self.addAccountsButton.setObjectName("addAccountsButton")
        self.addMaFilesButton = QtWidgets.QPushButton(self.centralwidget)
        self.addMaFilesButton.setGeometry(QtCore.QRect(20, 140, 401, 41))
        self.addMaFilesButton.setStyleSheet("")
        self.addMaFilesButton.setObjectName("addMaFilesButton")
        self.startFarmButton = QtWidgets.QPushButton(self.centralwidget)
        self.startFarmButton.setGeometry(QtCore.QRect(20, 200, 401, 41))
        self.startFarmButton.setStyleSheet("")
        self.startFarmButton.setObjectName("startFarm")
        self.accountsList = QtWidgets.QListWidget(self.centralwidget)
        self.accountsList.setGeometry(QtCore.QRect(445, 21, 331, 281))
        self.accountsList.setObjectName("accountsList")
        self.logList = QtWidgets.QListWidget(self.centralwidget)
        self.logList.setGeometry(QtCore.QRect(25, 330, 751, 251))
        self.logList.setObjectName("logList")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.addAccountsF()
        self.addMaFilesF()
        self.checkAccountsF()
        self.chooseItems()
        self.startFarmF()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Obl1Que\'s Panel CS:GO"))
        self.settingsButton.setText(_translate("MainWindow", "НАСТРОЙКИ"))
        self.checkAccountsButton.setText(_translate("MainWindow", "ПРОВЕРКА АККАУНТОВ"))
        self.addAccountsButton.setText(_translate("MainWindow", "ДОБАВИТЬ АККАУНТЫ"))
        self.addMaFilesButton.setText(_translate("MainWindow", "ДОБАВИТЬ MAFILE"))
        self.startFarmButton.setText(_translate("MainWindow", "НАЧАТЬ ФАРМ"))

    def addAccountsF(self):
        self.addAccountsButton.clicked.connect(lambda: self.addAccounts())
    def addAccounts(self):
        os.system('logpass.txt')
    def addMaFilesF(self):
        self.addMaFilesButton.clicked.connect(lambda: self.addMaFiles())
    def addMaFiles(self):
        path = os.path.abspath('maFiles')
        autoit.run(f'explorer.exe {os.path.abspath(path)}')
    def checkAccountsF(self):
        self.checkAccountsButton.clicked.connect(lambda: self.checkAccounts())
    def checkAccounts(self):
        OnStart()
        CreateAccounts()
        self.itemsToLaunch.clear()
        self.accountsList.clear()
        self.steamAccounts = []
        info = readJson('accounts.json')
        info2 = readJson('launched_accounts.json')

        for account in info:
            self.accountsList.addItem(account)

        for accountInfo in info:
            for accountView in range(self.accountsList.count()):
                if info[accountInfo]["shared_secret"] is None and accountInfo == self.accountsList.item(accountView).text():
                    self.accountsList.item(accountView).setBackground(QtGui.QColor(255, 166, 166, 255))

        for accountInfo in info2:
            for accountView in range(self.accountsList.count()):
                if self.accountsList.item(accountView).text() == accountInfo:
                    self.accountsList.item(accountView).setBackground(QtGui.QColor(166, 255, 167, 255))
    def chooseItems(self):
        self.accountsList.itemClicked.connect(self.choosenItems)
    def choosenItems(self, clItem):
        if clItem.background().color().getRgb() != (255, 166, 166, 255) and clItem.background().color().getRgb() != (166, 255, 167, 255):
            if clItem.text() not in self.itemsToLaunch:
                self.itemsToLaunch.append(clItem.text())
                clItem.setBackground(QtGui.QColor(235, 242, 255, 150))

            else:
                self.itemsToLaunch.remove(clItem.text())
                clItem.setBackground(QtGui.QColor(0, 0, 0, 0))

            if self.itemsToLaunch != []:
                self.LogWrite(f'Выбрано аккаунтов для запуска: {len(self.itemsToLaunch)}')
            else:
                self.LogWrite('Ни одного аккаунта не выбрано!')

        elif clItem.background().color().getRgb() == (166, 255, 167, 255):
            info = readJson('launched_accounts.json')
            for pid in info:
                if pid == clItem.text():
                    os.kill(info[pid]["win_csgo_PID"], signal.SIGTERM)
                    self.LogWrite(f'- {info[pid]["login"]} был выключен.')
            clItem.setBackground(QtGui.QColor(0, 0, 0, 0))
            OnStart()

        self.accountsList.clearSelection()
    def LogWrite(self, sentense):
        self.logList.addItem(sentense)
        self.logList.scrollToBottom()
    def startFarmF(self):
        self.startFarmButton.clicked.connect(lambda: self.startFarm())
    def startFarm(self):
        self.steamAccounts = []
        info = readJson('accounts.json')
        for i in self.itemsToLaunch:
            for account in info:
                if i == account:
                    self.steamAccounts.append(SteamAccount(info[account]["login"], info[account]["password"], info[account]["shared_secret"]))
        self.itemsToLaunch.clear()
        for account in self.steamAccounts:
            account.CSGOLaunch()
            for i in range(self.accountsList.count()):
                if account.login == self.accountsList.item(i).text():
                    self.accountsList.item(i).setBackground(QtGui.QColor(166, 255, 167, 255))
            self.logList.addItem(f'+ {account.login} - запущен!')