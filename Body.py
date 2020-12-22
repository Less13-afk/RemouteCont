import os
import sys
import json
import glob
import time
import base64
import pyautogui
from PyQt5 import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets as qtw
from ServerWindow import *
from StartWindow import *
import socket
import threading
import signal
import os
import subprocess
import ctypes
import psutil
import pyHook
import pythoncom
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from msvcrt import getch
from base64 import b64encode, b64decode
import ast
from tkinter.messagebox import showerror
from tkinter import *
from datetime import datetime
#Генерация пароля из текущего часа
def keygen():
    key=datetime.now().strftime('%H')
    key = key.lstrip('0')
    if len(key) > 0 and key[-1] == '.':
        key = key[:-1]
    min=datetime.now().strftime('%M')
    min = min.lstrip('0')
    if len(min) > 0 and min[-1] == '.':
        min = min[:-1]
    if int(min)>=55:
        key=int(key)+1
    return int(key)
#Функция шифровки
def encrypt(plain_text, password):
    salt = get_random_bytes(AES.block_size)
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
    cipher_config = AES.new(private_key, AES.MODE_GCM)
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }
#Функция расшифровки
def decrypt(enc_dict, password):
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)
    return decrypted
#Обработчик потоков сервера
class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(list)
    def __init__(self, ip, port, parent=None):
        QtCore.QThread.__init__(self, parent)
        # Принимаем глобальные переменные
        self.active_socket = None
        self.ip = ip
        self.port = port
        self.command = 'screen'
        # Создаем TCP-Сервер
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.listen(0)      
    # Принимаем и обрабатываем изображение
    def run(self):
        # Принимаем входящее соединение
        self.data_connection, address = self.server.accept()
        self.active_socket = self.data_connection
        self.pas=str(port+keygen())
        while True:
            if self.command.split(' ')[0] != 'screen':
                self.send_json(self.command.split(' '))
                responce = self.receive_json()
                self.mysignal.emit([responce])
                self.command = 'screen'
            if self.command.split(' ')[0] == 'screen':
                self.send_json(self.command.split(' '))
                responce = self.receive_json()
                self.mysignal.emit([responce])
    # Отправка json-данных клиенту
    def send_json(self, data):     
        # Обрабатываем бинарные данные
        try: json_data = json.dumps(data.decode('utf-8'))
        except: json_data = json.dumps(data)    
        # В случае если клиент разорвал соединение но сервер отправляет команду
        try:
            self.active_socket.send(str(encrypt(str(json_data),self.pas)).encode('utf-8')) 
        except ConnectionResetError:
            # Отключаемся от текущей сессии
            Tk().withdraw()
            showerror(title='Ошибка!',message='Потеряно соединение с клиентом!')
            Tk().destroy()
            self.server.close()
            self.active_socket = None
            Server.close()
            sys.exit()
    # Получаем json данные от клиента
    def receive_json(self):
        json_data = ''
        while True:
            try:
                if self.active_socket != None:
                    json_data1 = self.active_socket.recv(100000000).decode('utf-8')
                    json_data1=ast.literal_eval(json_data1)
                    json_data1=decrypt(json_data1,self.pas)
                    json_data1=json_data1.decode('utf-8')
                    json_data1=str(json_data1)
                    json_data+=json_data1
                    if str(json_data1)=='"Error"':
                        Tk().withdraw()
                        showerror(title='Ошибка!',message='Команда введена неверно!')
                        Tk().destroy()
                    return json.loads(json_data)
                else: 
                    return None
            except ValueError:
                pass
            except ConnectionResetError:
                Tk().withdraw()
                showerror(title='Ошибка!',message='Потеряно соединение с клиентом!')
                Tk().destroy()
                Server.close()
                sys.exit()               
#Окно сервера-удаленного управление
class VNCServer(QtWidgets.QMainWindow):
    def __init__(self, parent=None,ip=str, port=int):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton0.clicked.connect(self.btnClicked0)
        self.ui.pushButton1.clicked.connect(self.btnClicked1)
        self.ui.pushButton2.clicked.connect(self.btnClicked2)
        self.ui.pushButton3.clicked.connect(self.btnClicked3)
        self.ui.pushButton4.clicked.connect(self.btnClicked4)
        self.ui.pushButton5.clicked.connect(self.btnClicked5)
        self.ui.pushButton6.clicked.connect(self.btnClicked6)
        self.ui.pushButton7.clicked.connect(self.btnClicked7)
        # Создаем экземпляр обработчика       
        self.thread_handler = MyThread(ip, port)
        self.thread_handler.start()
        # Обработчик потока для обновление GUI
        self.thread_handler.mysignal.connect(self.screen_handler)
        #Обработчики конопок
    def btnClicked0(self):
        self.thread_handler.command=f'reload'
    def btnClicked1(self):
        self.thread_handler.command=f'off_keyboard'
        self.ui.pushButton1.setGeometry(0,45,0,0)
        self.ui.pushButton2.setGeometry(0,45,95,40)
    def btnClicked2(self):
        self.thread_handler.command=f'off_m'
        self.ui.pushButton2.setGeometry(0,45,0,0)
        self.ui.pushButton1.setGeometry(0,45,95,40)
    def btnClicked3(self):
        self.thread_handler.command=f'off_Kran'
    def btnClicked4(self):
        text=self.showDialog()
        if text!='':
            self.thread_handler.command=f'open_cmd {text}'
        else:pass
    #Окно ввода команд в консоль
    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input console',
            'Enter your command:')
        if ok and text!='':
            return text
        if ok and text=='':
            Tk().withdraw()
            showerror(title='Ошибка!',message='Введите команду, поле не может быть пустым!')
            Tk().destroy()
            self.showDialog()
    def btnClicked5(self):
        self.thread_handler.command=f'ras'
    def btnClicked6(self):
        self.thread_handler.command=f'disp'
    def btnClicked7(self):
        self.thread_handler.command=f'block'
    # Обработка и вывод изображения
    def screen_handler(self, screen_value):
        data = ['mouse_move_to', 'mouse_left_click','mouse_right_click', 'mouse_double_left_click','reload','off_keyboard','off_m','off_Kran','open_cmd','ras','disp','block']
        # В случае если это не скрин, пропускаем шаг
        if screen_value[0] not in data:
         try:
            decrypt_image = base64.b64decode(screen_value[0])
            with open('2.png', 'wb') as file:
                file.write(decrypt_image)
            # Выводим изображение в панель
            image = QtGui.QPixmap('2.png')
            self.ui.label.setPixmap(image)
         except Exception:
            pass
    # После закрытия сервера удаляем изображения
    def closeEvent(self, event):
        for file in glob.glob('*.png'):
            try: os.remove(file)
            except: pass
    # Обработка EVENT событий
    def event(self, event):
        # Обработка ЛКМ, ПКМ
        if event.type() == QtCore.QEvent.MouseButtonPress:
            current_button = event.button() # Определяем нажатую кнопку            
            if current_button == 1:  
                mouse_cord = f'mouse_left_click {event.x()} {event.y()}'
            elif current_button == 2:
                mouse_cord = f'mouse_right_click {event.x()} {event.y()}'
            self.thread_handler.command = mouse_cord
        # Движение мыши без нажатий
        elif event.type() == QtCore.QEvent.MouseMove:
            mouse_cord = f'mouse_move_to {event.x()} {event.y()}'
            self.thread_handler.command = mouse_cord
        # Обработка double-кликов
        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            mouse_cord = f'mouse_double_left_click {event.x()} {event.y()}'
            self.thread_handler.command = mouse_cord  
        # Обработка нажатий на системные,специальные и обычные клавиши на клавиатуре
        elif event.type()==QtCore.QEvent.KeyPress:
            if event.key()==16777220:
               event.namekey='Enter'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777219:
               event.namekey='Backspace'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777250:
               event.namekey='Win'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777216:
               event.namekey='Esc'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777248:
               event.namekey='Shift'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777249:
               event.namekey='Ctrl'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777252:
               event.namekey='Capslk'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777251:
               event.namekey='Alt'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777221:
               event.namekey='Enter'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777223:
               event.namekey='Del'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777264:
               event.namekey='F1'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777265:
               event.namekey='F2'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777266:
               event.namekey='F3'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777267:
               event.namekey='F4'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777268:
               event.namekey='F5'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777269:
               event.namekey='F6'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777270:
               event.namekey='F7'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777271:
               event.namekey='F8'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777272:
               event.namekey='F9'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777273:
               event.namekey='F10'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777274:
               event.namekey='F11'
               key_press=f'key_press {event.namekey}'
            elif event.key()==16777275:
               event.namekey='F12'
               key_press=f'key_press {event.namekey}'
            else:key_press=f'key_press {event.key()}'
            self.thread_handler.command=key_press
        return QtWidgets.QWidget.event(self, event)
#Клиентская часть программы
class VNCClient:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.client.connect((ip, port))
                self.pas=str(port+keygen())
                print('connect - yes')
                break
            except:
                print('connect -not')
                time.sleep(5)
    # Переместить мышь по заданным координатам
    def mouse_active(self, mouse_flag, x, y):
        print(mouse_flag)
        if mouse_flag == 'mouse_left_click':
            pyautogui.leftClick(int(x), int(y))
            return "mouse_left_click"
        elif mouse_flag == 'mouse_right_click':
            pyautogui.rightClick(int(x), int(y))
            return "mouse_right_click"
        elif mouse_flag == 'mouse_double_left_click':
            pyautogui.doubleClick(int(x), int(y))
            return "mouse_double_left_click"
        elif mouse_flag == 'mouse_move_to':
            pyautogui.moveTo(int(x),int(y))
            return "mouse_move_to" 
    # Обработать изображение с экрана
    def screen_handler(self):
        pyautogui.screenshot('1.png')
        with open('1.png', 'rb') as file:
            reader = base64.b64encode(file.read())
        os.remove('1.png')
        return reader
    #Reload PK
    def reload(self):
        print("reload")
        subprocess.call(["shutdown", "/r"])
        return "reload"
    #Отключить клавиатуру удаленного пк
    def off_keyboard(self):
        print("input_off")
        ctypes.windll.user32.BlockInput(True) 
        return "off_keyboard"
    #Отключить мыш удаленного пк
    def off_mouse(self):
        print("input_on")
        ctypes.windll.user32.BlockInput(False)
        return "off_m"
    #Отключить экран удаленного пк
    def off_monitor(self):
        print("off_monitor")
        WM_SYSCOMMAND = 0x0112
        SC_MONITORPOWER = 0xF170
        window = ctypes.windll.kernel32.GetConsoleWindow()
        ctypes.windll.user32.SendMessageA(window, WM_SYSCOMMAND, SC_MONITORPOWER, 2)     
        return "off_Kran"
    #Открыть консоль удаленного пк
    def open_cmd(self,text):
        print("open_cmd")
        text.remove("open_cmd")
        print(text)
        try:
            subprocess.Popen([text],shell=True)
            print('OK')
            return f'open_cmd'
        except:
            print('Error')
            return f'Error'
    #Смена раскладки
    def Rasklad(self):
        print("smena_rask")
        pyautogui.hotkey('shift','alt')
        pyautogui.hotkey('ctrl','shift')
        return "ras"
    #Запуск диспетчера задач
    def Disp(self):
        print("disp_open")
        subprocess.Popen(['Taskmgr'])
        return "disp"
    #Блокировка пользователя
    def BlockUser(self):
        print("block_user")
        ctypes.windll.user32.LockWorkStation()
        return "block"
    #Обработка нажатий клавиш
    def key_press(self,key):
        key=str(key)
        if key=='Enter':pyautogui.keyDown(key)
        elif key=='Backspace':pyautogui.keyDown(key)
        elif key=='Win':pyautogui.hotkey(key)
        elif key=='Esc':pyautogui.keyDown(key)
        elif key=='Shift':pyautogui.keyDown(key)
        elif key=='Ctrl':pyautogui.keyDown(key)
        elif key=='Capslk':pyautogui.keyDown(key)
        elif key=='Alt':pyautogui.keyDown(key)
        elif key=='Del':pyautogui.keyDown(key)
        elif key=='F1':pyautogui.keyDown(key)
        elif key=='F2':pyautogui.keyDown(key)
        elif key=='F3':pyautogui.keyDown(key)
        elif key=='F4':pyautogui.keyDown(key)
        elif key=='F5':pyautogui.keyDown(key)
        elif key=='F6':pyautogui.keyDown(key)
        elif key=='F7':pyautogui.keyDown(key)
        elif key=='F8':pyautogui.keyDown(key)
        elif key=='F9':pyautogui.keyDown(key)
        elif key=='F10':pyautogui.keyDown(key)
        elif key=='F11':pyautogui.keyDown(key)
        elif key=='F12':pyautogui.keyDown(key)
        else:
            key=str(chr(int(key)))
            pyautogui.typewrite(key)
        print('press: ',key)
        return "key_press"
    # Обработка входящих команд
    def execute_handler(self):
        while True:
            responce = self.receive_json()
            if responce[0] == 'screen':result = self.screen_handler()
            elif 'mouse' in responce[0]:result = self.mouse_active(responce[0], responce[1], responce[2])
            elif 'reload' in responce[0]:result= self.reload()
            elif 'off_keyboard' in responce[0]:result=self.off_keyboard()
            elif 'off_m' in responce[0]:result=self.off_mouse()
            elif 'off_Kran' in responce[0]:result=self.off_monitor()
            elif 'open_cmd' in responce[0]:result=self.open_cmd(responce)
            elif 'key_press' in responce[0]:result=self.key_press(responce[1])
            elif 'ras' in responce[0]:result=self.Rasklad()
            elif 'disp' in responce[0]:result=self.Disp()
            elif 'block' in responce[0]:result=self.BlockUser()
            self.send_json(result)
    # Отправляем json данные серверу
    def send_json(self, data):
        # Если данные окажутся строкой
        try:
            json_data = json.dumps(data.decode('utf-8'))
        except:
            json_data = json.dumps(data) 
        try:self.client.send(str(encrypt(str(json_data),self.pas)).encode('utf-8'))
        except ConnectionResetError:
            Tk().withdraw()
            showerror(title='Ошибка!',message='Потеряно соединение с сервером!')
            Tk().destroy()
            self.client.close()
            sys.exit()
    # Получаем json данные от сервера
    def receive_json(self):
        json_data = ''
        while True:
            try:
                json_data1 = self.client.recv(2048).decode('utf-8')
                json_data1=ast.literal_eval(json_data1)
                json_data1=decrypt(json_data1,self.pas)
                json_data1=json_data1.decode('utf-8')
                json_data1=str(json_data1)
                json_data+=json_data1
                return json.loads(json_data)
            except ValueError:
                pass
            except ConnectionResetError:
                Tk().withdraw()
                showerror(title='Ошибка!',message='Потеряно соединение с сервером!')
                Tk().destroy()
                self.client.close()
                sys.exit()
#Стартовое окно
class StartWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
         QtWidgets.QWidget.__init__(self, parent)
         super(StartWindow,self).__init__()
         self.ui=Ui_MainStartWindow()
         self.ui.setupUi(self)
         self.ui.pushButton.clicked.connect(self.bntClicked)
         self.ui.pushButton_2.clicked.connect(self.bntClicked_2)
#обработка исключений при работе как клиент
    def bntClicked(self):
         global w
         a=False
         if self.ui.lineEdit.text()!='' and self.ui.lineEdit_2.text()!='': 
          if self.ui.lineEdit_2.text().isdigit() is True:
           try:
            socket.inet_aton(self.ui.lineEdit.text())
            a=True
           except socket.error:
            Tk().withdraw()
            showerror(title='Ошибка!',message='Поля IP и PORT не могут быть пустыми! Или они заполнены неверно! Поле порт должно иметь только числовое значение. Поле IP должно быть введено в формате IPv4')
            Tk().destroy()
           if a is True:
            w.close()
            myclient = VNCClient(self.ui.lineEdit.text(), int(self.ui.lineEdit_2.text()))
            t1=threading.Thread(myclient.execute_handler())
            t1.setDaemon(True)
            t1.start()
            k=1
          else:
            Tk().withdraw()
            showerror(title='Ошибка!',message='Поля IP и PORT не могут быть пустыми! Или они заполнены неверно! Поле порт должно иметь только числовое значение. Поле IP должно быть введено в формате IPv4')
            Tk().destroy()
         else:
            Tk().withdraw()
            showerror(title='Ошибка!',message='Поля IP и PORT не могут быть пустыми! Или они заполнены неверно! Поле порт должно иметь только числовое значение. Поле IP должно быть введено в формате IPv4')
            Tk().destroy()
#обработка исключений при работе как сервер           
    def bntClicked_2(self):
         global w
         k=0
         global ip
         global port
         a=False
         if self.ui.lineEdit.text()!='' and self.ui.lineEdit_2.text()!='':
          if self.ui.lineEdit_2.text().isdigit() is True:
           try:
            socket.inet_aton(self.ui.lineEdit.text())
            a=True
           except socket.error:
            Tk().withdraw()
            showerror(title='Ошибка!',message='Поля IP и PORT не могут быть пустыми! Или они заполнены неверно! Поле порт должно иметь только числовое значение. Поле IP должно быть введено в формате IPv4')
            Tk().destroy()
           if a is True:
            ip=self.ui.lineEdit.text()
            port=int(self.ui.lineEdit_2.text())
            w.close()
          else:
            Tk().withdraw()
            showerror(title='Ошибка!',message='Поля IP и PORT не могут быть пустыми! Или они заполнены неверно! Поле порт должно иметь только числовое значение. Поле IP должно быть введено в формате IPv4')
            Tk().destroy()
         else:
            Tk().withdraw()
            showerror(title='Ошибка!',message='Поля IP и PORT не могут быть пустыми! Или они заполнены неверно! Поле порт должно иметь только числовое значение. Поле IP должно быть введено в формате IPv4')
            Tk().destroy()
#Запуск окна сервера          
def ServerWindow():
      if __name__ == "__main__":
        global Server
        app = QtWidgets.QApplication(sys.argv)
        Server = VNCServer(None,ip,port)
        Server.show()
        app.exec_()
#Запуск стартового окна
def startwindow():
 global w
 global app
 app = QtWidgets.QApplication(sys.argv)
 w = StartWindow()
 w.show()
 app.exec_()
k=0
startwindow()
if k==0:ServerWindow()