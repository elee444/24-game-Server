import json
import threading
import socket
from client import *
import argparse

msgpack={"ready1":"R1", #"Rn"=ready to play with n players
         "ready2":"R2",
         "ready3":"R3",
         "ready3+":"R3+", #"Rn+"=ready to play with n or more players
         "submit":"Sn", #"Sn"=Submit a number for verification
         "question":"Qn,n,n,n" #"Qn,n,n,n"=The four numbers are n,n,n,n
         }

#get a msgpack from the master. Decode it.
#def decodempack(mp):



if __name__ == "__main__":

    #  Register on server
    gclient = Client('localhost', 1234, 1234, find_free_port())

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

    #signal the master I am ready1
    gclient.send({"name": "Client 1",
                  "message":msgpack["ready1"]})

    #  Main game loop
    while True:
        #  Send message to room (any serializable data)
        gclient.send({"name": "Client 1",
                      "message": "I'm just Number One..."})


        # get server data (only client 3)
        message = gclient.get_messages()
        if len(message) != 0:
            for message in message:
                message = json.loads(message.decode())
                sender, value = message.popitem()
                print("%s say %s" % (value["name"],value["message"]))
