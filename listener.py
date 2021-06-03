import socket
def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.4', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 50001))
i = 1
while i == 1:
    s.listen()
    conn, addr = s.accept()
    #print('conected', flush=True)
    data = conn.recv(1024)
    #print('data receved', flush=True)
    out = data.decode()
    #print('data decoded', flush=True)
    print(out, flush=True)
    conn.close()

