# Slave client - join and play game managed by the master

import post24obj
#import game24Aux
import client
import json


# The central game server info
serverAdd = "127.0.0.1"
serverTCPPort = 1234
serverUDPPort = 1234

# The port of this -
ThisPort = 1315

num_boxes = 4
N = [None] * num_boxes  # 4 numbers
clienttitle = 'Slave'
clientname ='slave2'
mastertitle = None  # id of the master

if __name__ == "__main__":

    # The slave does the magic and join the room to play either
    # 1) by himself or
    # 2) against others
    slaveclient = client.Client(serverAdd, serverTCPPort,
                                serverUDPPort, ThisPort)

    # Find roomname='Game24Room'
    rooms = list(filter(lambda room: room['name'] == 'Game24Room',
                        slaveclient.get_rooms()))
    theroomid = rooms[0]['id']
    #  join a room
    try:
        slaveclient.join_room(theroomid)
    except Exception as e:
        print("Error : %s" % str(e))

    #print('Slave Client ',slaveclient.identifier,
    #      ' join room ', rooms[0], slaveclient.get_rooms())

    # main loop
    while True:
        #  Send message to room (any serializable data)
        data={"name":clientname,"title":clienttitle,
              "message":"Start?","this_id":slaveclient.identifier}
        slaveclient.send(data)

        # get server data
        messages = slaveclient.get_messages()
        #messages=messages.decode("utf-8")
        if len(messages) != 0:
            for message in messages:
                message = json.loads(message.decode)
                sender, value = message.popitem()
                print(clientname," received : "
                      "%s say %s" % (value["name"], value["message"]))
