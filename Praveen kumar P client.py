import socket
import threading
from tkinter import *
PORT=60000
HOST="127.0.0.1"
ADDRESS=(HOST,PORT)
FORMAT="utf-8"
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDRESS)
class chatbox:
    def __init__(self):
        self.window=Tk()
        self.window.withdraw()
        self.login=Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False,height=False)
        self.login.configure(width=400,height=300)
        self.label=Label(self.login,text="Please login to continue",justify=CENTER,font="Arial 14 bold")
        self.label.place(relheight=0.15,relx=0.2,rely=0.07)
        self.labelname=Label(self.login,text="Name: ",font="Arial 12")
        self.labelname.place(relheight=0.2,relx=0.1,rely=0.2)
        self.entryname=Entry(self.login,font="Arial 14")
        self.entryname.place(relwidth=0.4,relheight=0.12,relx=0.35,rely=0.2)
        self.entryname.focus()
        self.go=Button(self.login,text="CONTINUE",font="Arial 14 bold",command=lambda :self.toChatWindow(self.entryname.get()))
        self.go.place(relx=0.4,rely=0.55)
        self.window.mainloop()
    def toChatWindow(self,name):
        self.login.destroy()
        self.layout(name)
        rcv=threading.Thread(target=self.receive)
        rcv.start()
    def layout(self,name):
        self.name=name
        self.window.deiconify()
        self.window.title("CHATROOM")
        self.window.resizable(width=False,height=False)
        self.window.configure(width=470,height=550,bg="#17202A")
        self.labelhead=Label(self.window,bg="#17202A",fg="#EAECEE",text=self.name,font="Helvetica 13 bold",pady=5)
        self.labelhead.place(relwidth=1)
        self.line=Label(self.window,width=450,bg="#ABB2B9")
        self.line.place(relwidth=1,rely=0.07,relheigth=0.012)
        self.textcons = Text(self.window,width=20,height=2, bg="#17202A", fg="#EAECEE",font="Helvetica 14",padx=5, pady=5)
        self.textcons.place(relheight=0.745,relwidth=1,rely=0.08)
        self.labelbottom=Label(self.window,bg="#ABB2B9",height=80)
        self.labelbottom.place(relwidth=1,rely=0.825)
        self.entrymsg=Entry(self.labelbottom,bg="#2C3E50",fg="#EAECEE",font="Helvetica 13")
        self.entrymsg.place(relwidth=0.74,relheight=0.06,rely=0.008,relx=0.011)
        self.entrymsg.focus()
        self.buttonmsg=Button(self.labelbottom,text="Send",font="Helvetica 10 bold",width=20,bg="#ABB2B9",command=lambda :self.sendbutton(self.entrymsg.get()))
        self.buttonmsg.place(relx=0.77,rely=0.008,relheight=0.06,relwidth=0.22)
        self.textcons.config(cursor="arrow")
        scrollbar=Scrollbar(self.textcons)
        scrollbar.place(relheight=1,relx=0.974)
        scrollbar.config(command=self.textcons.yview())
        self.textcons.config(state=DISABLED)
    def sendbutton(self,msg):
        self.textcons.config(state=DISABLED)
        self.msg=msg
        self.entrymsg.delete(0,END)
        snd=threading.Thread(target=self.sendmessage)
        snd=start()
    def receive(self):
        while True:
            try:
                message=client.recv(1024).decode(FORMAT)
                if message== 'Name':
                    client.send(self.name.encode(FORMAT))
                else:
                    self.textcons.config(state=NORMAL)
                    self.textcons.insert(END,message + "\n\n")
                    self.textcons.config(state=DISABLED)
                    self.textcons.see(END)
            except:
                print("An error occured")
                client.close()
                break
    def sendmessage(self):
        self.textcons.config(state=DISABLED)
        while True:
            message=(f"{self.name}:{self.msg}")
            client.send(message.encode(FORMAT))
            break
g=chatbox()
