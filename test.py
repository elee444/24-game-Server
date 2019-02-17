rooms=[{'id': '2031139f-7546-4ecb-8932-374a22a17b3b',
        'name': 'Test_room_1', 'nb_players': 3, 'capacity': 10},
        {'id': '2e89bda2-e0f8-486c-aa32-76c1919c40e1',
        'name': 'Test_room_2', 'nb_players': 1, 'capacity': 10}]
y=list(filter(lambda room: room['name'] == 'Test_room_2', rooms))
print(y)
