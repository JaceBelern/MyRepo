import socket
import threading
import time

import pymysql

serverList = []


def sendMessage(info):
    for sock in serverList:
        sock.send(info.encode())


def link(sock, address):
    try:
        while True:
            RecvType = sock.recv(1024).decode()
            RecvUserName = sock.recv(1024).decode()
            RecvPassword = sock.recv(1024).decode()
            if RecvType == 'login':
                sql = "select USERPASSWORD from user where USERNAME='%s';" % RecvUserName
                ResNum = cursor.execute(sql)
                if ResNum == 0:
                    sock.send('not signup'.encode())
                    continue
                else:
                    Res = cursor.fetchall()
                    password = Res[0][0]
                    if password == RecvPassword:
                        sock.send('ok'.encode())
                        sql = "select * from message"
                        ResNum = cursor.execute(sql)
                        if ResNum >= 15:
                            Res = cursor.fetchall()
                            for i in range(-15, -1):
                                hisMessage = '[' + Res[i][2] + ']' + Res[i][0] + ':\n' + Res[i][1]
                                sock.send(hisMessage.encode())
                        serverList.append(sock)
                        loginInfo = '---' + RecvUserName + '已上线---\n'
                        sendMessage(loginInfo)
                        while True:
                            RecvInfo = sock.recv(1024).decode()
                            if not RecvInfo:
                                break
                            sql = "insert into message values ('%s','%s','%s')" % (
                                RecvUserName, RecvInfo, time.strftime('%H:%M', time.localtime()))
                            cursor.execute(sql)
                            conn.commit()
                            Info = '[' + time.strftime('%H:%M:%S',
                                                       time.localtime()) + ']' + RecvUserName + ':\n' + RecvInfo
                            sendMessage(Info)
                            print(Info.encode())
                        serverList.remove(sock)
                        leaveInfo = '***' + RecvUserName + '已下线***\n'
                        sendMessage(leaveInfo)
                        break
                    else:
                        sock.send('wrong'.encode())
                        continue
            elif RecvType == 'signup':
                sql = "insert into user values ('%s','%s')" % (RecvUserName, RecvPassword)
                cursor.execute(sql)
                conn.commit()
                sock.send('ok'.encode())
                continue
        sock.close()
    except ConnectionResetError:
        pass


if __name__ == '__main__':
    conn = pymysql.Connect(host='localhost', port=3306, user='root', password='714825936QY', database='messageDB')
    cursor = conn.cursor()
    ServiceSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ServiceSocket.bind(("", 8080))
    ServiceSocket.listen(128)
    while True:
        ConnectSocket, ip_port = ServiceSocket.accept()
        thread = threading.Thread(target=link, args=(ConnectSocket, ip_port))
        thread.start()
