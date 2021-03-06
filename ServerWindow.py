from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Сервер управления удаленным ПК")
        MainWindow.resize(1148, 729)
        MainWindow.setMouseTracking(True)
        MainWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMouseTracking(True)
        self.centralwidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMouseTracking(True)      
        self.label.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.label.setStyleSheet("QLabel{\n"
"border: 2px solid red;\n"
"}")
        self.pushButton0= QtWidgets.QPushButton(self.centralwidget)
        self.pushButton0.setGeometry(QtCore.QRect(0, 0, 95, 40))
        self.pushButton0.setObjectName("pushButton0")
        self.pushButton1= QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(0, 45, 95, 40))
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton2= QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(0, 45, 0, 0))
        self.pushButton2.setObjectName("pushButton2")
        self.pushButton3= QtWidgets.QPushButton(self.centralwidget)
        self.pushButton3.setGeometry(QtCore.QRect(0, 90, 95, 40))
        self.pushButton3.setObjectName("pushButton3")
        self.pushButton4= QtWidgets.QPushButton(self.centralwidget)
        self.pushButton4.setGeometry(QtCore.QRect(0, 135, 95, 40))
        self.pushButton4.setObjectName("pushButton4")
        self.pushButton5= QtWidgets.QPushButton(self.centralwidget)
        self.pushButton5.setGeometry(QtCore.QRect(0, 180, 95, 40))
        self.pushButton5.setObjectName("pushButton4")
        self.pushButton6= QtWidgets.QPushButton(self.centralwidget)
        self.pushButton6.setGeometry(QtCore.QRect(0, 225, 95, 40))
        self.pushButton6.setObjectName("pushButton4")
        self.pushButton7= QtWidgets.QPushButton(self.centralwidget)
        self.pushButton7.setGeometry(QtCore.QRect(0, 270, 95, 40))
        self.pushButton7.setObjectName("pushButton4")
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1148, 21))
        self.menubar.setMouseTracking(True)
        self.menubar.setAcceptDrops(True)
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Сервер управления удаленным ПК"))
        self.pushButton0.setText(_translate("MainWindow","Перезагрузить\nпк" ))
        self.pushButton1.setText(_translate("MainWindow","Отключить\nввод" ))
        self.pushButton2.setText(_translate("MainWindow","Включить\nввод" ))
        self.pushButton3.setText(_translate("MainWindow","Отключить\nэкран" ))
        self.pushButton4.setText(_translate("MainWindow","Открыть\nконсоль" ))
        self.pushButton5.setText(_translate("MainWindow","Сменить\nраскладку" ))
        self.pushButton6.setText(_translate("MainWindow","Открыть\nдисп.задач" ))
        self.pushButton7.setText(_translate("MainWindow","Заблокировать\nпользователя" ))