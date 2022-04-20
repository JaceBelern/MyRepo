import socket
import threading
import time
from tkinter import *
from tkinter import messagebox


# if __name__ == '__main__':
#     UserName = input("请输入用户名：")
#     ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     ClientSocket.connect(("10.241.118.73", 8080))
#     while True:
#         SendInfo = UserName + ':' + input("请输入：")
#         if SendInfo == UserName + ':' + 'exit':
#             ClientSocket.close()
#             break
#         ClientSocket.send(SendInfo.encode())


def SignTF():
    root = Tk()
    root.title('welcome!')
    frm = Frame(root)
    root.geometry('450x300')

    # image
    canvas = Canvas(root, height=200, width=500)
    imgFile = PhotoImage(file='welcome.png')
    image = canvas.create_image(0, 0, anchor='nw', image=imgFile)
    canvas.pack(side='top')

    # info
    Label(root, text='用户名：').place(x=70, y=150)
    Label(root, text='密码：').place(x=70, y=190)

    varUserName = StringVar()
    entryUserName = Entry(root, width=30, textvariable=varUserName)
    entryUserName.place(x=160, y=150)

    varPassword = StringVar()
    entryPassword = Entry(root, width=30, textvariable=varPassword, show='*')
    entryPassword.place(x=160, y=190)

    # functions
    def login():
        userName = varUserName.get()
        password = varPassword.get()
        print(userName)
        print(password)
        if userName != '' and password != '':
            ClientSocket.send('login'.encode())
            time.sleep(0.001)
            ClientSocket.send(userName.encode())
            time.sleep(0.001)
            ClientSocket.send(password.encode())
        isCorrect = ClientSocket.recv(1024)
        if isCorrect.decode() == 'ok':
            root.destroy()
            ComTF()
        elif isCorrect.decode() == 'not signup':
            messagebox.showwarning(message='该用户未注册！')
        elif isCorrect.decode() == 'wrong':
            messagebox.showwarning(message='用户名或密码错误！')
        # root.destroy()
        # ComTF()

    def signup():
        SignupTF()

    # button
    btnLogin = Button(root, width=10, text='登陆', command=login)
    btnLogin.place(x=170, y=230)
    btnSignUp = Button(root, width=10, text='注册', command=signup)
    btnSignUp.place(x=270, y=230)

    frm.pack()
    root.mainloop()


def SignupTF():
    root = Toplevel()
    root.title('注册')
    frm = Frame(root)
    root.geometry('400x200')

    # label
    Label(root, text='用户名：').place(x=50, y=50)
    Label(root, text='密码：').place(x=50, y=80)
    Label(root, text='确认密码：').place(x=50, y=110)

    # entry
    varUserName = StringVar()
    entryUserName = Entry(root, width=30, textvariable=varUserName)
    entryUserName.place(x=110, y=50)

    varPassword = StringVar()
    entryUserName = Entry(root, width=30, textvariable=varPassword, show='*')
    entryUserName.place(x=110, y=80)

    varVerifyPassword = StringVar()
    entryUserName = Entry(root, width=30, textvariable=varVerifyPassword, show='*')
    entryUserName.place(x=110, y=110)

    def signupNow():
        userName = varUserName.get()
        password = varPassword.get()
        verifyPassword = varVerifyPassword.get()
        if password == verifyPassword:
            ClientSocket.send('signup'.encode())
            time.sleep(0.001)
            ClientSocket.send(userName.encode())
            time.sleep(0.001)
            ClientSocket.send(password.encode())
        status = ClientSocket.recv(1024).decode()
        if status == 'ok':
            messagebox.showinfo(message='注册成功！')
            root.destroy()

    # button
    btnCommit = Button(root, width=10, text='确认注册', command=signupNow)
    btnCommit.place(x=280, y=160)

    frm.pack()
    root.mainloop()


def ComTF():
    root = Tk()
    root.title('聊天室')
    frm = Frame(root)
    root.geometry('900x600')
    root.resizable(False, False)
    frm.pack()

    # textarea
    textarea = Text(root, width=150, height=15, bd=10, font=('Fangsong', 20), cursor='arrow')
    textarea.pack(side='top')

    # input
    inputArea = Text(root, width=150, height=20, bd=10, font=('Fangsong', 15))
    inputArea.pack(side='bottom')

    def send():
        message = inputArea.get('1.0', END)
        ClientSocket.send(message.encode())
        inputArea.delete('1.0', END)
        # RecvInfo = ClientSocket.recv(1024).decode()
        # print(RecvInfo)
        # textarea.insert(INSERT, RecvInfo)

    def close():
        root.destroy()
        ClientSocket.shutdown(2)
        ClientSocket.close()

    # button
    btnExit = Button(root, text='退出', width=12, cursor='hand2', command=close)
    btnExit.place(x=650, y=550)
    btnEnter = Button(root, text='发送', width=12, cursor='hand2', command=send)
    btnEnter.place(x=780, y=550)

    def RecvInfoFromServer():
        try:
            while True:
                RecvInfo = ClientSocket.recv(1024).decode()
                print(RecvInfo)
                textarea.insert(END, RecvInfo)
        except OSError:
            ClientSocket.close()

    display = threading.Thread(target=RecvInfoFromServer)
    display.setDaemon(True)
    display.start()
    root.mainloop()


if __name__ == '__main__':
    # connect
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ClientSocket.connect(("10.241.118.73", 8080))
    SignTF()
