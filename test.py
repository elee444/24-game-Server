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
import threading
from time import sleep

def function01(arg,name):
    for i in range(arg):
        print(name,'i---->',i,'\n')
        print (name,"arg---->",arg,'\n')
        sleep(1)


def test01():
    thread1 =threading.Thread(target = function01, args = (10,'thread1', ))
    thread1.start()
    thread2 = threading.Thread(target = function01, args = (10,'thread2', ))
    thread2.start()
    thread1.join()
    thread2.join()
    print ("thread finished...exiting")


if __name__ == "__main__":
    test01()
