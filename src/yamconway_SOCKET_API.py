import socket
import sys
from yamconwaylib import YamConway
from time import sleep


HOST = 'localhost'  # Symbolic name meaning all available interfaces
PORT = 5002  # Arbitrary non-privileged port

yc = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print(
        'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    )
    sys.exit()
print('Socket bind complete')

s.listen(1)
print('Socket now listening.')

# s.setblocking(False)
# s.settimeout(1)

conn = None
addr = None
loops = 300
# wait to accept a connection - non blocking call
while loops > 0:
    loops = loops - 1
    try:
        print("Trying to get connection.")
        conn, addr = s.accept()
        if addr:
            break
    except BlockingIOError as error:
        print(error)
        pass
    except socket.timeout as error:
        print(error)
        pass
    # sleep(0.1)


# display client information
if addr:
    print('Connected with ' + addr[0] + ':' + str(addr[1]))

""" Main loop."""
while conn:
    print("main loop")
    data = conn.recv(262144).decode('utf-8')
    print(data)
    if data.startswith('Init'):  # example format 'Init99x100'
        try:
            r = int(data[4:data.find('x')])
            c = int(data[data.find('x')+1:])
            # print("Creating board {} x {}".Format(r, c))
            yc = YamConway(rows=r, columns=c)  # This is our simulation
        except:
            conn.close()
            s.close()
    if data == 'NextTurn':
        yc.next_turn()
        # print(yc.get_network_board())
        conn.send(yc.get_network_board().encode())
    if not data:
        print("no data")
        # break
    sleep(0.1)

    # conn.sendall(reply.encode(encoding="utf-8"))

if conn:
    conn.close()
    s.close()


