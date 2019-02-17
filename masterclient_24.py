#Master client - creates a room for others (Slave clients) to join and play
#The client who created the room acts as the master.
#Those who join the room act as the slaves.
#The master moderates the game and determine who wins
import post24obj
#import game24Aux
import client
import random

#The central game server info
serverAdd="127.0.0.1"
serverTCPPort=1234
serverUDPPort=1234

#The port of this -
ThisPort=1300

num_boxes=4
N=[None] *num_boxes #4 numbers
title='Master'
slavelist=[] #ids.

if __name__=="__main__":
    #Create post24 server and set up the game parameters.
    #Other clients joint the room and play the game.

    #24 game parameters


    #The master does the magic and set up room for others
    masterclient=client.Client(serverAdd, serverTCPPort,
                               serverUDPPort,ThisPort)

    #  Create a room on server
    masterclient.create_room("Game24Room")
    for i in range(num_boxes):
        N[i]=str(random.randint(1,10))
    print("Master: ", masterclient.identifier,
          " has created a 24 game room - ",N)


    #Main loop
    #while True:
    #    if
