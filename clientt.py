import tkinter
from time import sleep
import socket
import threading
from tkinter import messagebox
from os import path
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
    return path.join(base_path, relative_path)



username = "AAAAAA"
sglob = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
lastline=0
msg_font = ("Arial",15)
usr_font = ("Arial",15,"bold")
usercolorsls = list({
    '#503eff',  #blue
    '#D2691E',  #orange
    '#9f2dee',  #purple like twitch
    '#1dd161',  #green
})
color_count:int = 0


def serverdisconnected(connTV:tkinter.StringVar,
                       t:tkinter.Text,labelconn:tkinter.Label,
                       sockThread):
    global sglob
    connTV.set('NOT CONNECTED')
    labelconn.config(bg='#CC0000')
    t.pack_forget()
    labelconn.pack(fill='x',side='top')
    t.pack()
    sglob.close()
    sglob = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sockThread(labelconn)
    return

def receive_messages(t:tkinter.Text,
                     connTV:tkinter.StringVar,labelconn:tkinter.Label,
                     sockThread):
    global lastline,color_count
    while True:
        try:
            chatline = sglob.recv(1024).decode()
        except ConnectionResetError:
            serverdisconnected(connTV,t,labelconn,sockThread)
            return
        t['state']='normal'
        t.insert("end",chatline[5:]+' \n')
        lastline+=1; color_count=(color_count+1)%len(usercolorsls)
        t.tag_add('username',f'{lastline}.0',f'{lastline}.{chatline.find(":")-4}')
        t.tag_config('username',foreground=usercolorsls[color_count],font=usr_font)
        t['state']='disabled'


def sendcommand(e:tkinter.Entry,s:socket.socket,connTV:tkinter.StringVar):
    textmsg = e.get().strip()
    if textmsg == '': return
    if connTV.get()=='CONNECTED': 
        s.send(bytes(textmsg,"utf-8"))
        e.delete(0,'end')

def close_main(window:tkinter.Tk,s:socket.socket,connTV:tkinter.StringVar):
    global username
    result = messagebox.askokcancel("Confirm", "Are you sure you want to close the window?")
    if result:
        if connTV.get()=="CONNECTED":
            try:
                s.send(bytes(f"{username},DISCONNECT","utf-8"))
            except ConnectionResetError:
                pass
        window.destroy()

def login_window():
    def subusername():
        global username
        input =  em.get().strip()
        if input=="": return
        username=input
        logwin.destroy()
        afterlogin()

    logwin = tkinter.Tk()
    app_icon = tkinter.PhotoImage(file=resource_path("appIcon240.png"))
    logwin.geometry(f"250x150+{logwin.winfo_screenwidth()//2-125}+{logwin.winfo_screenheight()//2-200}")
    logwin.resizable(False,False)
    logwin.title("Login")
    logwin.iconphoto(True,app_icon)
    tkinter.Label(logwin,text="Enter Your Username",font=("Arial",15),pady=10).pack()
    em = tkinter.Entry(logwin,font=("Arial",15),width=15)
    em.focus_set()
    em.bind("<Return>",lambda x :subusername())
    em.pack()
    tkinter.Label(text="        ",pady=3).pack()
    tkinter.Button(logwin,command=subusername,font=("Arial",15),text="Ok",width=10).pack()
    logwin.mainloop()


def afterlogin():

    global username
    
    main = tkinter.Tk()
    main.focus()
    app_icon = tkinter.PhotoImage(file=resource_path("appIcon240.png"))
    send_icon = tkinter.PhotoImage(file=resource_path("appIcon50.png"))
    connTV = tkinter.StringVar(value="NOT CONNECTED")
    main.iconphoto(True,app_icon)
    scwidth = main.winfo_screenwidth()
    scheight = main.winfo_screenheight()
    wmax = int(scwidth/2)
    w = 400
    hmax = int(scheight)
    wmin = w-50
    hmin = int(scheight/2)

    main.title(username)
    main.geometry(f"{w}x{scheight-100}+{scwidth-w-15}+{0}")
    main.maxsize(width=wmax,height=hmax)
    main.minsize(width=wmin,height=hmin)
    main.configure(bg="#009999")

    ####################### send_frame #############################
    send_frame = tkinter.Frame(main,bg="#009999",)
    message_entry = tkinter.Entry(master=send_frame,width= 300,font=("Arial",15),selectbackground="#006666",fg="#002222",border=0,)
    message_entry.focus_set()
    send_button = tkinter.Button(master=send_frame
                        ,image=send_icon,border=0
                        ,bg="#009999",activebackground="#009999",padx=19
                        ,text=" "
                        ,foreground="#009999",activeforeground="#009999"
                        ,compound="center",command=lambda: sendcommand(message_entry,sglob,connTV))
    send_button.pack(side="right")
    message_entry.pack(side="left")
    send_frame.pack(side="bottom",pady=15,padx=20)
    message_entry.bind("<Return>",lambda x: sendcommand(message_entry,sglob,connTV))
    ####################### send_frame #############################

    labelconn = tkinter.Label(master=main,textvariable=connTV,bg= "#CC0000",fg="#F0F0F0",font=("Arial",13,"bold"))
    labelconn.pack(fill='x',side='top')

    t = tkinter.Text(master=main,
                     state='disabled',
                     height=hmax,
                     font=msg_font,fg= "#00CCCC",bg="#003333",padx=10,pady=10)

    t.pack()

    # t.insert('end',"sadfffff")

    # scrollbar = tkinter.Scrollbar(master=t,)
    # scrollbar.pack(side="right",fill='y',)
    # t.config(yscrollcommand=scrollbar.set)




    
    def sockThread(labelconn:tkinter.Label):

        def fun():
            try:
                print(f"socket.gethostname() is :{socket.gethostname()}")
                print(f"socket.gethostbyname('Abdullah') is :{socket.gethostbyname('Abdullah')}")
                sglob.connect(('192.168.1.3',1253))
                return 1
            except ConnectionRefusedError:
                return 0
            except TimeoutError:
                return 0

        while True:
            rs = fun()
            if rs==1: 
                def nnn():
                    sleep(5)
                    if connTV.get()=='CONNECTED':
                        labelconn.pack_forget()
                connTV.set("CONNECTED")
                labelconn.config(bg="#00AA00")
                threading.Thread(target=nnn).start()
                break
            else:
                sleep(2)
        threading.Thread(target=receive_messages, args=(t,connTV,labelconn,sockThread),daemon=True).start()
        sglob.sendall(bytes(f"{username}","utf-8"))
    
    threading.Thread(target=sockThread,args=(labelconn,),daemon=True).start()
    main.protocol("WM_DELETE_WINDOW", lambda:close_main(main,sglob,connTV))
    main.mainloop()

if __name__=="__main__":
    login_window()