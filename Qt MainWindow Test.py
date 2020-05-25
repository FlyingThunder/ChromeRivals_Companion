from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import Output
import requests
from datetime import datetime, timezone, timedelta

class QtMainWindow(QtWidgets.QMainWindow, Output.Ui_MainWindow):
    check_box = None
    tray_icon = None

    def __init__(self, parent=None):
        self.key = '?apiKey=??????????'
        super(QtMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setupUx()
        self.hideWidgets()
        self.CR_API_Call_playercount()
        self.CR_API_Call_upcomingMS()
        self.servertime_clock()
        self.showTime()
        self.sysTrayTest()
        self.CR_API_Call_gameevent()
        self.testLabel()
        self.setStyleSheet("#MainWindow { border-image: url(6.png) 0 0 0 0 stretch stretch; }")

    def testLabel(self):
        pixmapANI = QtGui.QPixmap('ani.jpg')
        pixmap2ANI = pixmapANI.scaled(128, 128, QtCore.Qt.KeepAspectRatio)
        self.Label_ANI_Logo.setPixmap(pixmap2ANI)
        self.Label_ANI_Logo.setScaledContents(False)
        self.Label_ANI_Logo.show()
        pixmapBCU = QtGui.QPixmap('bcu.jpg')
        pixmap2BCU = pixmapBCU.scaled(128, 128, QtCore.Qt.KeepAspectRatio)
        self.Label_BCU_Logo.setPixmap(pixmap2BCU)
        self.Label_BCU_Logo.setScaledContents(False)
        self.Label_BCU_Logo.show()

    def hideWidgets(self):
        self.PlayerCountLabel_ANI.hide()
        self.PlayerCountLabel_BCU.hide()
        self.upcomingMSLabel_ANI.hide()
        self.upcomingMSLabel_ANI_Clock.hide()
        self.upcomingMSLabel_BCU.hide()
        self.upcomingMSLabel_BCU_Clock.hide()

    def setupUx(self):
        self.actionShow_Playercount.changed.connect(lambda: self.showPlayerCount())
        self.actionShow_upcoming_MS.changed.connect(lambda: self.showupcomingMS())
        self.menuRefresh.triggered.connect(lambda: self.CR_API_Call_upcomingMS())
        self.menuRefresh.triggered.connect(lambda: self.CR_API_Call_playercount())

    def showPlayerCount(self):
        if self.actionShow_Playercount.isChecked():
            self.PlayerCountLabel_ANI.show()
            self.PlayerCountLabel_BCU.show()
        else:
            self.PlayerCountLabel_ANI.hide()
            self.PlayerCountLabel_BCU.hide()

    def showupcomingMS(self):
        if self.actionShow_upcoming_MS.isChecked():
            self.upcomingMSLabel_ANI.show()
            self.upcomingMSLabel_BCU.show()
            self.upcomingMSLabel_ANI_Clock.show()
            self.upcomingMSLabel_BCU_Clock.show()
        else:
            self.upcomingMSLabel_ANI.hide()
            self.upcomingMSLabel_BCU.hide()
            self.upcomingMSLabel_ANI_Clock.hide()
            self.upcomingMSLabel_BCU_Clock.hide()

    def servertime_clock(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

    def showTime(self):
        utc_dt = datetime.now(timezone.utc)
        gmtPlusTwo = utc_dt + timedelta(0,0,0,0,0,2)
        self.timeTest.setText(str(gmtPlusTwo)[11:][:8])
        if int(str(gmtPlusTwo)[14:][:2]) % 5 == 1:
            if str(gmtPlusTwo)[17:][:2] == "15":
                self.CR_API_Call_playercount()

    def CR_API_Call_playercount(self):
        response = requests.get("https://api.chromerivals.net/info/server/usercount" + self.key)
        data = response.json()
        self.PlayerCountLabel_ANI.setText(str(data["result"]["ani"]))
        self.PlayerCountLabel_BCU.setText(str(data["result"]["bcu"]))
        print("showing player count - "+str(data["result"]["ani"])+str(data["result"]["bcu"]))

    def CR_API_Call_gameevent(self):
        response = requests.get("https://api.chromerivals.net/info/server/events" + self.key)
        data = response.json()
        if data["result"] == []:
            self.gameEvent.setText("No currently running game event")
            self.tray_icon.setIcon(QtGui.QIcon("icon_blue.png"))
            print("still running")
            print(datetime.now())
        else:
            self.gameEvent.setText(str(data["result"]))
            print("gamevent detected at"+str(data["result"]))
            if data["result"][0]["eventType"] == 27:
                self.tray_icon.setIcon(QtGui.QIcon("icon_red.png"))
            else:
                self.tray_icon.setIcon(QtGui.QIcon("icon_green.png"))
        QtCore.QTimer.singleShot(60000, lambda: self.CR_API_Call_gameevent())


    def CR_API_Call_upcomingMS(self):
        response = requests.get("https://api.chromerivals.net/info/motherships" + self.key)
        data = response.json()

        oldformatBCU = (data["result"]["bcu"])
        datetimeobjectBCU = datetime.strptime(oldformatBCU, '%Y-%m-%dT%H:%M:%S')
        newformatBCU = datetimeobjectBCU.strftime('%d.%m.%Y')
        newformatBCU_clock = datetimeobjectBCU.strftime('%H:%M:%S')
        oldformatANI = (data["result"]["ani"])
        datetimeobjectANI = datetime.strptime(oldformatANI, '%Y-%m-%dT%H:%M:%S')
        newformatANI = datetimeobjectANI.strftime('%d.%m.%Y')
        newformatANI_clock = datetimeobjectANI.strftime('%H:%M:%S')

        self.upcomingMSLabel_ANI.setText(newformatANI)
        self.upcomingMSLabel_ANI_Clock.setText(newformatANI_clock)
        self.upcomingMSLabel_BCU.setText(newformatBCU)
        self.upcomingMSLabel_BCU_Clock.setText(newformatBCU_clock)

    def sysTrayTest(self):
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon("icon_blue.png"))
        tray_menu = QtWidgets.QMenu()
        show_action = QtWidgets.QAction("Show", self)
        quit_action = QtWidgets.QAction("Exit", self)
        hide_action = QtWidgets.QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(QtWidgets.qApp.quit)
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = QtMainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()