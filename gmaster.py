import json
import threading
import socket
from client import *
import argparse
from server import *
from time import sleep

gserver=None  #The central game server
gmaster=None  #The game master client

##find freed port
from contextlib import closing
#import socket

def find_open_ports():
    for port in range(1, 8081):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        #with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            res = sock.connect_ex(('localhost', port))
            if res == 0:
                yield port
###

def game_server(args):
    rooms = Rooms(int(args.room_capacity))
    main_loop(args.tcp_port, args.udp_port, rooms)
    #main_loop(t_port,u_port,rms)

def game_master(t_port,u_port,this_port):
    gmaster = Client("127.0.0.1", int(t_port),int(u_port),this_port) #1234, 1234, 1245)
    print("gMaster  : %s" % gmaster.identifier)
    gmaster.create_room("24 game room")
    print("Master create room  %s" % gmaster.room_id)
    #  Main game loop
    while True:
        #  Send message to room (any serializable data)
        gmaster.send({"name": "Master",
                      "message": "I'm the 24 game master..."
                      })
        # get server data (only client 3)
        message = gmaster.get_messages()
        if len(message) != 0:
            for message in message:
                message = json.loads(message.decode())
                sender, value = message.popitem()
                #rint("%s say %s" % (value["name"], value["message"]))

if __name__ == "__main__":
    """
    Start a game server
    """
    parser = argparse.ArgumentParser(description='Simple game server')
    parser.add_argument('--tcpport',
                        dest='tcp_port',
                        help='Listening tcp port',
                        default="1234")
    parser.add_argument('--udpport',
                        dest='udp_port',
                        help='Listening udp port',
                        default="1234")
    parser.add_argument('--capacity',
                        dest='room_capacity',
                        help='Max players per room',
                        default="5")

    args = parser.parse_args()
    #rooms = Rooms(int(args.room_capacity))
    #main_loop(args.tcp_port, args.udp_port, rooms)


    #start the central game server
    thread1 =threading.Thread(target = game_server,args = (args,))
    thread1.start()
    sleep(2) #wait for awhile to make sure the server is up and is_running

    #now time to start the game master

    thread2 = threading.Thread(target = game_master,
                               args = (args.tcp_port, args.udp_port,find_free_port() ))
    thread2.start()

    thread1.join()
    thread2.join()

    print ("Clean up and stop ....")
