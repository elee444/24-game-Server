import json
import threading
import socket
from client import *
import argparse




if __name__ == "__main__":
    """
    Start a game server

    parser = argparse.ArgumentParser(description='Simple game client')
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
                        default="2")

    args = parser.parse_args()
    """


    """
    Example game client 1
    """
    #  Register on server
    gclient = Client("127.0.0.1", 1234, 1234, find_free_port())

    print("gClient  : %s" % gclient.identifier)


    #  Get rooms list
    rooms = gclient.get_rooms()
    selected_room = None
    if rooms is not None and len(rooms) != 0:
        for room in rooms:
            print("Room %s (%d/%d)" % (room["name"],
                                       int(room["nb_players"]),
                                       int(room["capacity"])))

        # Get first room for tests
        selected_room = rooms[0]['id']
    else:
        print("No rooms")

    #  Join client 1 room
    try:
        gclient.join_room(selected_room)
    except Exception as e:
        print("Error : %s" % str(e))

    print("gClient  join %s" % gclient.room_id)


    #  Main game loop
    while True:
        #  Send message to room (any serializable data)
        gclient.send({"name": "Client 2",
                      "message": "I'm just Number Two..."})


        # get server data (only client 3)
        message = gclient.get_messages()
        if len(message) != 0:
            for message in message:
                message = json.loads(message.decode())
                sender, value = message.popitem()
                print("%s say %s" % (value["name"],value["message"]))
