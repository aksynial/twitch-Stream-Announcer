# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Terrence\Desktop\updatedTabGUI.ui'
#
# Created: Wed Feb 18 00:25:19 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!
import json
import urllib
import urllib2
import requests
import webbrowser
import time as t
from bs4 import BeautifulSoup
from PySide import QtCore, QtGui
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import QWebView

class Ui_MainWindow(object):
    listOfStreamers = []
     
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 600)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(1000, 1000))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabGridLayout = QtGui.QGridLayout(self.centralwidget)
        self.tabGridLayout.setObjectName("tabGridLayout")
        self.buttonGridLayout = QtGui.QGridLayout()
        self.buttonGridLayout.setObjectName("buttonGridLayout")

        self.addGameButton = QtGui.QPushButton(self.centralwidget)
        self.addGameButton.setObjectName("addGameButton")
        self.deleteGameButton = QtGui.QPushButton(self.centralwidget)
        self.deleteGameButton.setObjectName("deleteButton")
        self.refreshButton = QtGui.QPushButton(self.centralwidget)
        self.refreshButton.setObjectName("refreshButton")
        self.loginButton = QtGui.QPushButton(self.centralwidget)
        self.loginButton.setObjectName("logInButton")
        spacerTop = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        spacerTab = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.nameLabel = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName("nameLabel")
    
        MainWindow.setCentralWidget(self.centralwidget)

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setMaximumSize(QtCore.QSize(600, 500))
        self.tabWidget.setMinimumSize(QtCore.QSize(100, 300))
        self.tabWidget.setObjectName("tabWidget")
        self.tabGridLayout.addItem(spacerTab, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.buttonGridLayout.addWidget(self.nameLabel, 0, 0, 1, 5)
        self.buttonGridLayout.addWidget(self.deleteGameButton, 1, 1, 1, 1)
        self.buttonGridLayout.addWidget(self.addGameButton, 1, 2, 1, 1)
        self.buttonGridLayout.addWidget(self.refreshButton, 1, 3, 1, 1)
        self.buttonGridLayout.addWidget(self.loginButton, 1, 4, 1, 1)
        self.tabGridLayout.addWidget(self.tabWidget, 3, 1, 1, 1)
        self.tabGridLayout.addItem(spacerTab, 2, 1, 1, 1)
        self.buttonGridLayout.addItem(spacerTop, 1, 0, 1, 1)
        self.tabGridLayout.addLayout(self.buttonGridLayout, 1, 1, 1, 1)

        self.workerThread = WorkerThread(self.tabWidget)
        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteGameButton.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.addGameButton.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.refreshButton.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.loginButton.setText(QtGui.QApplication.translate("MainWindow", "Log In", None, QtGui.QApplication.UnicodeUTF8))
        self.nameLabel.setText(QtGui.QApplication.translate("MainWindow", "TWITCH", None, QtGui.QApplication.UnicodeUTF8))
        self.addGameButton.clicked.connect(self.addGameTab)
        self.deleteGameButton.clicked.connect(self.deleteGameTab)
        self.loginButton.clicked.connect(showWebView)
        self.refreshButton.clicked.connect(self.refreshList)
        self.tabWidget.connect(self.tabWidget, QtCore.SIGNAL("currentChanged(int)"), self.changeTab)
        self.workerThread.connect(self.workerThread, QtCore.SIGNAL("listAcquired()"),self.showStreamList, Qt.QueuedConnection)

    def addGameTab(self):
        text,add = QtGui.QInputDialog.getText(MainWindow, 'Add A Game', 'Enter Game Name:')
        if add is True:
            self.listWidget = QtGui.QListWidget(self.tabWidget)
            self.listWidget.setGeometry(20, 0, self.tabWidget.width()-21, self.tabWidget.height()-1)
            self.tabWidget.setCurrentIndex(self.tabWidget.addTab(self.listWidget, text))
            self.tabWidget.currentWidget().itemDoubleClicked.connect(self.openInBrowser)
            #self.tabWidget.connect(self.tabWidget, QtCore.SIGNAL("currentChanged(int)"), self.showStreamList("Dota%202"))

    def addFollowsTab(self):
    	self.listWidget = QtGui.QListWidget(self.tabWidget)
        self.listWidget.setGeometry(20, 0, self.tabWidget.width()-21, self.tabWidget.height()-1)
        self.tabWidget.addTab(self.listWidget, "Following")
        self.tabWidget.currentWidget().itemDoubleClicked.connect(self.openInBrowser)

    #def addFollowsStreams(self):
    #	self.tabWidget.
            
    def deleteGameTab(self):
        self.tabWidget.removeTab(self.tabWidget.currentIndex())

    def startGettingStreams(self):
        if self.workerThread.isRunning() == True:
            self.workerThread.terminate()
        self.workerThread.start()
 
    def showStreamList(self):
        listView = self.tabWidget.widget(self.tabWidget.currentIndex())
        listView.clear()
        for item in Ui_MainWindow.listOfStreamers:
            listView.addItem(QtGui.QListWidgetItem(item))

    def refreshList(self):
    	self.workerThread.setGameName(self.tabWidget.tabText(self.tabWidget.currentIndex()))
        self.changeTab()
        

    def changeTab(self):
    	if self.tabWidget.tabText(self.tabWidget.currentIndex()) != "Following":
	        if self.tabWidget.count() == 0:
	            return
	        gameName = self.tabWidget.tabText(self.tabWidget.currentIndex()).replace(" ", "%20")
	        self.workerThread.setGameName(gameName)
	        
    	else:
	    	gameName = "Following"
	    	self.workerThread.setGameName(gameName)

    	self.startGettingStreams()


    def openInBrowser(self):
        name = self.tabWidget.currentWidget().currentItem().text()
        webbrowser.open("https://twitch.tv/" + name)

class loginWindow():
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 600)
        MainWindow.setMaximumSize(QtCore.QSize(400, 600))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.continueButton = QtGui.QPushButton(self.centralwidget)
        self.continueButton.setMinimumSize(QtCore.QSize(200, 50))
        self.continueButton.setMaximumSize(QtCore.QSize(200, 50))
        self.continueButton.setObjectName("continueButton")
        self.gridLayout.addWidget(self.continueButton, 6, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 75, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 8, 0, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 98))
        self.label.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setPointSize(47)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 5, 0, 1, 1)
        self.loginButton = QtGui.QPushButton(self.centralwidget)
        self.loginButton.setMinimumSize(QtCore.QSize(200, 50))
        self.loginButton.setMaximumSize(QtCore.QSize(200, 50))
        self.loginButton.setObjectName("loginButton")
        self.gridLayout.addWidget(self.loginButton, 3, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.gridLayout.setAlignment(self.loginButton, Qt.Alignment(Qt.AlignCenter))
        self.gridLayout.setAlignment(self.continueButton, Qt.Alignment(Qt.AlignCenter))
        self.gridLayout.setAlignment(self.label, Qt.Alignment(Qt.AlignCenter))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.continueButton.setText(QtGui.QApplication.translate("MainWindow", "Continue without logging in..", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "TWITCH", None, QtGui.QApplication.UnicodeUTF8))
        self.loginButton.setText(QtGui.QApplication.translate("MainWindow", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.loginButton.clicked.connect(showWebView)
        self.continueButton.clicked.connect(showMainGui)

class webView():
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 600)
        MainWindow.setMinimumSize(QtCore.QSize(400, 600))
        MainWindow.setMaximumSize(QtCore.QSize(400, 600))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.webView = QWebView(self.centralwidget)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))

class WorkerThread(QThread):
    def __init__(self, tabWidget):
        super(WorkerThread, self).__init__()
        self.gameName = ""
        self.tabWidget = tabWidget

    def setGameName(self, currGameName):
        self.gameName = currGameName

    def run(self):
    	if self.gameName is not "Following":
    		getSource = requests.get("https://api.twitch.tv/kraken/streams?game=" + self.gameName + "&limit=24")
	        loadSource = json.loads(getSource.text)
	       	Ui_MainWindow.listOfStreamers[:] = []
    		try:
		        for item in loadSource["streams"]:
		            streamName = item["channel"]["display_name"]
		            Ui_MainWindow.listOfStreamers.append(streamName)
    		except KeyError:
	        	Ui_MainWindow.listOfStreamers[:] = []
		    	Ui_MainWindow.listOfStreamers.append("Twitch API error. Please try again later.")
    	else:
	        getSource = requests.get("https://api.twitch.tv/kraken/users/" + userName + "/follows/channels?oauth_token=" + token)
	        loadSource = json.loads(getSource.text)
	       	Ui_MainWindow.listOfStreamers[:] = []
	       	checkOnlineUrl = "https://api.twitch.tv/kraken/streams?channel="
	        try:
		        for item in loadSource["follows"]:
					streamName = item["channel"]["name"]
					checkOnlineUrl = checkOnlineUrl + streamName +","
		        checkOnlineUrl = checkOnlineUrl[:-1]
		        getSource = requests.get(checkOnlineUrl)
		        loadSource = json.loads(getSource.text)
		        for item in loadSource["streams"]:
					Ui_MainWindow.listOfStreamers.append(item["channel"]["display_name"])
	        except KeyError:
	        	Ui_MainWindow.listOfStreamers[:] = []
		    	Ui_MainWindow.listOfStreamers.append("Twitch API error. Please try again later.")
        self.emit(QtCore.SIGNAL("listAcquired()"))

def showWebView():
	MainWindow.hide()
	webWindow.show()
	webViewUi.webView.load(QUrl("https://api.twitch.tv/kraken/oauth2/authorize?response_type=token&client_id=" + appClientID + "&redirect_uri=" + redirectURI + "&scope=user_read+channel_read+user_follows_edit"))
	webViewUi.webView.show()

def showMainGui():
	removeLoginWindow()
	MainWindow.show()

def detectLoginSuccess(self):
	detectSuccess = webViewUi.webView.url().toString()
	print detectSuccess
	if "#access_token" in detectSuccess:
		import re
		result = re.search("token=(.*)&", detectSuccess)
		global token
		token = result.group(1)
		getUserName = requests.get("https://api.twitch.tv/kraken?oauth_token=" + token)
		loadSource = json.loads(getUserName.text)
		global userName
		userName = loadSource["token"]["user_name"]
		ui.addFollowsTab()
		webViewUi.webView.close()
		webWindow.close()
		ui.loginButton.setHidden(True)
		showMainGui()
        		#self.view.load(QUrl(url))

def removeLoginWindow():
	displayLoginWindow.close()

if __name__ == "__main__":
    import sys
    #Setting up the GUI for Login Window and Main Window
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    displayLoginWindow = QtGui.QMainWindow()
    loginUi = loginWindow()
    loginUi.setupUi(displayLoginWindow)
    displayLoginWindow.show()
    webWindow = QtGui.QMainWindow()
    webViewUi = webView()
    webViewUi.setupUi(webWindow)

    #Setting User and App Information
    token = ""
    appClientID = "og75lgi0c66xgw6uqsq606xsdc3tnpf"
    redirectURI = "http://www.twitch.tv/"
    scopeList = "user_read+channel_read+user_follows_edit"
    userName = ""

    displayLoginWindow.connect(loginUi.loginButton, QtCore.SIGNAL("clicked()"), removeLoginWindow)
    displayLoginWindow.connect(webViewUi.webView, QtCore.SIGNAL("urlChanged(const QUrl&)"), detectLoginSuccess)

    sys.exit(app.exec_())

