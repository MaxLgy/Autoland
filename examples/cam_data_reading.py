import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '192.168.3.246'
PORT = 8000

s.connect((HOST, PORT))

def read():
    r = s.recv(9999999)
    try:
        c = str(r).split('*')[:-1]
        c = c[0].split(',')
    except:
        return {}
    data = {"id":int(c[1])}
    data["y"] = -float(c[2])*100
    data["x"] = -float(c[3])*100
    data["z"] = float(c[4])*100
    data["roll"] = float(c[5])
    data["pitch"] = float(c[6])
    data["yaw"] = float(c[7])
        
    return data
    


if __name__ == "__main__":
    while 1:
        print(read(), "\n")
        time.sleep(0.1)
