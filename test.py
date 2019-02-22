"""
rooms=[{'id': '2031139f-7546-4ecb-8932-374a22a17b3b',
        'name': 'Test_room_1', 'nb_players': 3, 'capacity': 10},
        {'id': '2e89bda2-e0f8-486c-aa32-76c1919c40e1',
        'name': 'Test_room_2', 'nb_players': 1, 'capacity': 10}]
y=list(filter(lambda room: room['name'] == 'Test_room_2', rooms))
print(y)
"""
"""
from threading import Thread
from time import sleep

def threaded_function(arg):
    for i in range(arg):
        print ("running")
        sleep(1)


if __name__ == "__main__":
    thread = Thread(target = threaded_function, args = (10, ))
    thread.start()
    thread.join()
    print ("thread finished...exiting")
"""
from contextlib import closing
import socket

def find_open_ports():
    for port in range(1024, 65535):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        #with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            res = sock.connect_ex(('localhost', port))
            if res == 0:
                yield port
def find_free_port():
    #with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', 0))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock.getsockname()[1]

if __name__=="__main__":
    """
    ports=find_open_ports()
    for i in ports:
        print(i)
    """
    print(find_free_port())
