### test map generation
### as it stands, the code is FUNCTIONAL, strictly speaking, but there is a big flaw. Each room reciprocates orientation to one another, but they don't see their own NEIGHBORS' neighbors. So if blue builds itself west of cyan, and then yellow builds itself north of blue, yellow doesn't realize it is northwest of cyan. Although... maybe I don't want it to be connected like that? It doesn't have to be, now that I think about it... hmm...

import random

cardinals = ["north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest"]
opposing = ["south", "southwest", "west", "northwest", "north", "northeast", "east", "southeast"]

room_names = ["blue", "red", "green", 'yellow', 'white', 'black', 'cyan', 'magenta']
random.shuffle(room_names)

class Map:
    # pull from list of random rooms
    # iterate to create adjacent rooms, using Room.adjacent() to maintain consistency
    # when rooms run out, stop
    # random starting location for player
    # should this be a class or just a function?
    # does the map need to do anything, or is it static once created?
    def __init__(self):
        self.room_set = set()
        room_name = room_names.pop()
        # create seed room
        seed_room = Room(room_name)
        self.room_set.add(seed_room)
        self.build_map()

    # populate the map with a few rooms.
    # Rooms must be adjacent with at least one other,
    # so that player can move through map.
    # Should room_set be set or dict? I think set works better at the moment
    # Dictionary implementation just in case:
    # self.room_set = {} # goes in __init__ method
    # room_name = room_names.pop()
    # self.room_set[room_name] = Room(room_name)
    def build_map(self):
        while len(room_names) > 0:
            room_name = room_names.pop()
            new_room = Room(room_name)
            #print "new room type: %r" % type(new_room)
            self.add_room(new_room)
            #print "room_set: %r" % self.room_set
            new_room.populate(self)
            
    def add_room(self, room):
        self.room_set.add(room)

class Room:
    # initialize rooms
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.neighbors = {}
        
    def __str__(self):
        return "%s room with the following neighbors:\n%r" % (self.name, self.neighbors)

    # called by map during initialization of game
    # build a dictionary attribute that has {other_room_object: 'north'}
    # then call other_room_object.neighbors and add to its dictionary
    # {this_room_object: 'south'}
    def populate(self, my_map):
        attach_to = random.sample(my_map.room_set, 1)[0]
        #print attach_to
        #print type(attach_to)
        j = random.randrange(8)
        while cardinals[j] in self.neighbors.values():
            j = random.randrange(8)
        #print dir1, dir2
        self.build_neighbors(attach_to, cardinals[j])
        attach_to.build_neighbors(self, opposing[j])
        #self.neighbors[attach_to] = cardinals[j]
        #attach_to.neighbors[self] = opposing[j]
        
    def build_neighbors(self, other_room, dir):
        #print "other room is: %r" % other_room
        self.neighbors[other_room] = dir

my_map = Map()

for k in my_map.room_set:
    print "%s room's neighbors:" % k.name
    for m in k.neighbors.keys():
        print m.name + ": " + k.neighbors[m]
