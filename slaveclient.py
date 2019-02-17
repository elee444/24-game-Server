#Slave client - join and play game managed by the master

import post24obj
#import game24Aux
import client

#The central game server info
serverAdd="127.0.0.1"
serverTCPPort=1234
serverUDPPort=1234

#The port of this -
ThisPort=1305

num_boxes=4
N=[None] *num_boxes #4 numbers

if __name__=="__main__":

    #The slave does the magic and join the room to play either
    #1) by himself or
    #2) against others
    slaveclient=client.Client(serverAdd, serverTCPPort,
                              serverUDPPort,ThisPort)
    slaveclient2=client.Client(serverAdd, serverTCPPort,
                              serverUDPPort,ThisPort+5)

    #Find roomname='Game24Room'
    rooms=list(filter(lambda room: room['name'] == 'Game24Room',
                          slaveclient.get_rooms()))
    theroomid=rooms[0]['id']
    #  auto join a room
    slaveclient.join_room(theroomid)
    slaveclient2.join_room(theroomid)
    print ("Slave Clients  join room ",rooms[0])

    #main loop
    #while True:
    #    slaveclient.sendto()