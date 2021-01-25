import socket
import sys
import threading
import time

def create_socket():
    try:
        global host
        global port
        global s
        host="localhost"
        port=9999
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error as msg:
        print(str(msg))

def connect():
    try:
        global s
        global host
        global port
        s.connect((host,port))
        print("Connection established to " + host + " (IP :" + str(socket.gethostbyname(host)) + " ,Port :" + str(port) + ")")
    except socket.error as msg:
        print(str(msg))

def close_socket():
    global s
    s.close() 

def listen_user(name):
    global s
    while True:
        byte=s.recv(1024)
        data=byte.decode()
        signin_msg="SIGNIN:" + name + "\n"
        signout_msg="SIGNOFF:" + name + "\n"
        if data[:4] == "FROM":
            full_name=False
            full_msg=False
            data=data[5:]
            uname=''
            while True:

                if not full_name:
                    for i in range(len(data)):
                        if data[i] == ':':
                            full_name=True
                            data=data[i+1:]
                            break
                        uname=uname+data[i]

                if full_name:
                    print("Message from: " + uname)
                    print("Message: ",end="")
                    if not full_msg:
                        print(data,end="")

                if data[-1] =="\n":
                    full_msg=True
                    break
                else:
                    byte=s.recv(8)
                    data=byte.decode()
            continue
        
        elif data == signin_msg :
            print("You have signed in");

        elif data[:6] == "SIGNIN":
            data=data[7:]
            data=data[:-1]
            print()
            print(data + " has signed in.")
            print()

        
    
        elif data == signout_msg :
            break 

        elif data[:7] == "SIGNOFF":
            data=data[8:]
            data=data[:-1]
            print()
            print(data + " has signed off.")
            print()

        else:
            print(data,end='')

def send_Hello():
    global s
    data="HELLO"
    data=data.encode()
    s.send(data)
    byte=s.recv(1024)
    msg=byte.decode()
    print(msg)


def send_Bye():
    global s
    data="BYE"
    data=data.encode()
    s.send(data)


def authorize():
    global s
    ans="AUTHNO"
    while ans:
        username=input("Please enter a username: ")
        password=input("Please enter a password: ")
        auth="AUTH:" + username + ":" + password
        data=auth.encode()
        s.send(data)
        byte=s.recv(1024)
        ans=byte.decode()
        if ans == "AUTHYES\n":
            print("You are now authenticated")
            global t1
            t1=threading.Thread(target=listen_user,args=[username])
            t1.start()
            time.sleep(0.2)
            break
        else:
            print("Incorrect Username or Password. Please Try Again !!")


def send_List():
    global s
    data="LIST".encode()
    s.send(data)

def send_msg():
    global s
    user=input('User you would like to message :')
    msg=input("Message :")
    data="TO:" + user + ":" + msg
    data=data.encode()
    s.send(data)

def options():
    print("Choose an Option")
    print("1. List Online Users")
    print("2. Send Someone a message")
    print("3. Sign off")
    ans=input()
    return ans

if __name__ == "__main__":
    
    global host
    global port
    global t1
    create_socket()
    connect()
    send_Hello()
    authorize()
    while True:
        ans = options() 
       
        if ans == '1':
            send_List()
            time.sleep(0.2)

        elif ans == '2':
            send_msg()
            time.sleep(0.2)
        
        elif ans == '3':
            send_Bye()
            t1.join()
            break
    close_socket()
