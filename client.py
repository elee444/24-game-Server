import json
import threading
import socket


class Client:

    def __init__(self,
                 server_host,
                 server_port_tcp=1234,
                 server_port_udp=1234,
                 client_port_udp=1235):
        """
        Create a game server client
        """
        self.identifier = None
        self.server_message = []
        self.room_id = None
        self.client_udp = ("0.0.0.0", client_port_udp)
        self.lock = threading.Lock()
        self.server_listener = SocketThread(self.client_udp,
                                            self,
                                            self.lock)
        self.server_listener.start()
        self.server_udp = (server_host, server_port_udp)
        self.server_tcp = (server_host, server_port_tcp)

        self.register()

    def create_room(self, room_name=None):
        """
        Create a new room on server
        """
        message = json.dumps({"action": "create",
                              "payload": room_name,
                              "identifier": self.identifier})
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.connect(self.server_tcp)
        self.sock_tcp.send(message.encode('utf-8'))
        data = self.sock_tcp.recv(1024)
        self.sock_tcp.close()
        message = self.parse_data(data)
        self.room_id = message

    def join_room(self, room_id):
        """
        Join an existing room
        """
        self.room_id = room_id
        message = json.dumps({"action": "join",
                              "payload": room_id,
                              "identifier": self.identifier})
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.connect(self.server_tcp)
        self.sock_tcp.send(message.encode('utf-8'))
        data = self.sock_tcp.recv(1024)
        self.sock_tcp.close()
        message = self.parse_data(data)
        self.room_id = message

    def autojoin(self):
        """
        Join the first non-full room  - not working well
        """
        message = json.dumps({"action": "autojoin",
                              "identifier": self.identifier})
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.connect(self.server_tcp)
        # self.sock_tcp.send(message)
        self.sock_tcp.send(message.encode('utf-8'))
        data = self.sock_tcp.recv(1024)
        self.sock_tcp.close()
        message = self.parse_data(data)
        self.room_id = message

    def leave_room(self):
        """
        Leave the current room
        """
        message = json.dumps({"action": "leave",
                              "room_id": self.room_id,
                              "identifier": self.identifier})
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.connect(self.server_tcp)
        self.sock_tcp.send(message.encode('utf-8'))
        data = self.sock_tcp.recv(1024)
        self.sock_tcp.close()
        message = self.parse_data(data)

    def get_rooms(self):
        """
        Get the list of (all) remote rooms
        E.g. returns two rooms in a list of dict -
        [{'id': '2031139f-7546-4ecb-8932-374a22a17b3b',
        'name': 'Test_room_1', 'nb_players': 3, 'capacity': 10},
        {'id': '2e89bda2-e0f8-486c-aa32-76c1919c40e1',
        'name': 'Test_room_2', 'nb_players': 1, 'capacity': 10}]
        """
        message = json.dumps({"action": "get_rooms",
                              "identifier": self.identifier})
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.connect(self.server_tcp)
        self.sock_tcp.send(message.encode('utf-8'))
        data = self.sock_tcp.recv(1024)
        self.sock_tcp.close()
        message = self.parse_data(data)
        return message

    def send(self, message):
        """
        Send data to all players in the same room
        """
        message = json.dumps({"action": "send",
                              "payload": {"message": message},
                              "room_id": self.room_id,
                              "identifier": self.identifier})
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode('utf-8'), self.server_udp)

    def sendto(self, recipients, message):
        """
        Send data to one or more player in room
        """
        message = json.dumps({"action": "sendto",
                              "payload": {"recipients": recipients,
                                          "message": message},
                              "room_id": self.room_id,
                              "identifier": self.identifier})
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode('utf-8'), self.server_udp)

    def register(self):
        """
        Register the client to server and get a uniq identifier
        """
        message = json.dumps({"action": "register",
                              "payload": self.client_udp[1]})
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.connect(self.server_tcp)
        self.sock_tcp.send(message.encode('utf-8'))  # (message)
        data = self.sock_tcp.recv(1024)
        self.sock_tcp.close()
        message = self.parse_data(data)
        self.identifier = message

    def parse_data(self, data):
        """
        Parse response from server
        """
        try:
            data = json.loads(data)
            if data['success'] == "True":
                return data['message']
            else:
                raise Exception(data['message'])
        except ValueError:
            print(data)

    def get_messages(self):
        """
        Get recieved messages from server
        """
        message = self.server_message
        self.server_message = []
        return set(message)


class SocketThread(threading.Thread):
    def __init__(self, addr, client, lock):
        """
        Client udp connection
        """
        threading.Thread.__init__(self)
        self.client = client
        self.lock = lock
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(addr)

    def run(self):
        """
        Get responses from server
        """
        while True:
            data, addr = self.sock.recvfrom(1024)
            self.lock.acquire()
            try:
                self.client.server_message.append(data)
            finally:
                self.lock.release()

    def stop(self):
        """
        Stop thread
        """
        self.sock.close()


if __name__ == "__main__":
    """
    Example with 3 clients
    """
    print("Start testing ....")
    #  Register on server
    client1 = Client("127.0.0.1", 1234, 1234, 1235)
    print("Client 1 : %s" % client1.identifier)
    client2 = Client("127.0.0.1", 1234, 1234, 1236)
    print("Client 2 : %s" % client2.identifier)
    client3 = Client("127.0.0.1", 1234, 1234, 1237)
    print("Client 3 : %s" % client3.identifier)



    #  Create a room on server
    client1.create_room("Test_room_1")
    print("Client1 create room  %s" % client1.room_id)


    #  Get rooms list
    rooms = client1.get_rooms()
    selected_room1 = None
    if rooms is not None and len(rooms) != 0:
        # print("# rooms = ",len(rooms))
        for room in rooms:
            print("Room %s (%d/%d)" % (room["name"],
                                       int(room["nb_players"]),
                                       int(room["capacity"])))

        # Get first room for tests
        selected_room1 = rooms[0]['id']  # first room


        print("Rooms are ", selected_room1)
    else:
        print("No rooms")

    #  Join client 1 room
    try:
        client2.join_room(selected_room1)
        client3.join_room(selected_room1)
    except Exception as e:
        print("Error : %s" % str(e))

    print("Client 2 join %s" % client2.room_id)
    print("Client 3 join %s" % client3.room_id)



    autoclient = Client("127.0.0.1", 1234, 1234, 1350)
    print("Client auto : %s" % autoclient.identifier)
    autorooms = autoclient.get_rooms()
    print("Client auto rooms:", autorooms)
    #autoclient.autojoin()
    #print("Slave Client  join %s " % autoclient.room_id)

    #  Main game loop
    while True:
        #  Send message to room (any serializable data)
        client1.send({"name": "John D.",
                      "message": "I'm just John Doe..."})
        client2.send({"name": "Linus T.",
                      "message": "My name is Linus, and I am your God."})
        client3.send({"name": "Richard S.",
                      "message": "I love emacs"})


        # get server data (only client 3)
        message = client1.get_messages()
        if len(message) != 0:
            for message in message:
                message = json.loads(message.decode())
                sender, value = message.popitem()
                print("%s say %s" % (value["name"], value["message"]))
