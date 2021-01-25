import time
import socket
import threading

users=[]
connections=[]

def sock_create():
    global port
    global host
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print(str(msg))


def sock_open():
    global port
    global host
    global s
    global t1
    host = "127.0.0.1"
    port = 9999
    try:
        s.bind((host, port))
        print("Listening on port: " + str(port))
        s.listen(5)

    except socket.error as msg:
        print(str(msg))


def Hello(msg,conn):
    if msg == "HELLO":
        smsg="HELLO"
        print("S: " + smsg)
        smsg=smsg.encode()
        conn.send(smsg)
    else:
        smsg="Server Closed Connection"
        smsg=smsg.encode()
        conn.send(smsg)
        conn.close()


def log(msg,conn):
    accepted=["AUTH:test1:p000","AUTH:test2:p000","AUTH:test3:p000","AUTH:djay:p928"]
    print("C: " + msg)
    if msg in accepted:
        smsg="AUTHYES\n"
        print("S: "+smsg,end="")
        smsg = smsg.encode()
        conn.send(smsg)
        return True
    else:
        smsg="AUTHNO\n"
        print("S: "+smsg,end="")
        smsg = smsg.encode()
        conn.send(smsg)
        return False


def signinUser(conn,username):
    global length
    users.append(username)
    connections.append(conn)
    msg = "SIGNIN:" + username + "\n"
    msg = msg.encode()
    for c in range(len(connections)):
        con=connections[c]
        con.send(msg)


def options(conn,user,num):
    logout=False
    while not logout:
        msg=conn.recv(1024)
        msg=msg.decode()
        if msg == "BYE":
            print("C: "+msg)
            smsg="SIGNOFF:"+user+"\n"
            print("S: " + smsg,end='')
            smsg=smsg.encode()
            for c in range(len(connections)):
                con=connections[c]
                con.send(smsg)
            users.remove(user)
            connections.remove(conn)
            conn.close()
            logout=True
        elif msg == "LIST":
            print("C: "+msg)
            smsg=",".join(users)
            smsg=smsg+"\n"
            print("S: "+smsg,end='')
            smsg=smsg.encode()
            conn.send(smsg)
        elif msg[:2] == "TO":
            print("C: "+msg)
            msg=msg.split(':')
            toname=msg[1]
            smsg="FROM:"+users[num-1] +":" + msg[2]+"\n"
            print("S: "+smsg,end="")
            smsg=smsg.encode()
            for u in range(len(users)):
                if toname == users[u] and u != num:
                    break
            if toname == users[u]:
                connections[u].send(smsg)
            else:
                print("S: User not Online")
        else:
            conn.close()




def sock_accept():
    global port
    global host
    global s
    loggedin=False
    conn, addr = s.accept()
    byte=conn.recv(1024)
    msg=byte.decode()
    msg.strip('\n')
    print("C: "+msg)
    Hello(msg,conn)
    while not loggedin:
        msg = conn.recv(1024)
        msg = msg.decode()
        user=msg.split(':')
        if len(user) > 1:
            username=user[1]
        loggedin=log(msg,conn)
    signinUser(conn,username)
    num=len(users)-1
    options(conn,username,num)


if __name__ == "__main__":
    sock_create()
    sock_open()
    while True:
        t1 = threading.Thread(target=sock_accept)
        t1.start()
        time.sleep(2)

