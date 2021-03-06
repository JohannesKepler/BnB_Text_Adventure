import random

#abida is here!
#try to edit again.
# when you call cardinals[i] on a room, you can call
# opposing[i] on the other so they are correctly oriented
cardinals = ["north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest"]
opposing = ["south", "southwest", "west", "northwest", "north", "northeast", "east", "southeast"]

room_names = ["blue", "red", "green", 'yellow', 'white', 'black', 'cyan', 'magenta']

# dir_map takes results from vector_to_dir() func and uses them to map english words
# to math answers
dir_map = {
    "-1.57": 'south',
    "1.57": 'north',
    "0.00": 'west',
    "3.14": 'east',
    "-2.36": 'southeast',
    "2.36": 'northeast',
    "-0.79": 'southwest',
    "0.79": 'northwest'
}

# vector_to_dir() func uses dir_map to return an english cardinal direction
def vector_to_dir(p, q):
    dist = math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
    x = math.atan2((p[1] - q[1]), (p[0] - q[0]))
    y = "%.2f" % x
    if y in dir_map and dist < 2:
        return dir_map[y]
    elif dist >= 2:
        return None

# dictionary of commands, displayed with help call
helpful = {
    'go': "Moves you around. Use 'look' to see where you can go.",
    'look': "See where you can go based on room layout.",
    'x': "Examine something - type a word after x for something specific,\n or just x for a list of what is around you.",
    'take': "Pick something up if it is near you.",
    'i': "Check the items you are holding.",
    'map': "Get a summary of the rooms you've visited.",
    'whereami': "Check where you are.",
    'use': "You may need to use the things you find down here..."
}

class Map:
    # pull from list of random rooms
    # iterate to create adjacent rooms, using Room.adjacent() to maintain consistency
    # when rooms run out, stop
    # random starting location for player
    # should this be a class or just a function?
    # does the map need to do anything, or is it static once created?
    def __init__(self):
        self.room_set = set()
        self.room_set_pos = []
        room_name = room_names.pop()
        # create seed room
        seed_room = Room(room_name, 0, 0)
        self.room_set.add(seed_room)
        self.room_set_pos.append([0, 0])

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
            while True:
                attach_to = random.sample(self.room_set, 1)[0]
                if attach_to.check_neighbors:
                    break
            attach_to_pos = attach_to.get_pos()
            offset_x = random.choice([-1, 0, 1])
            offset_y = random.choice([-1, 0, 1])
            new_pos_x = attach_to_pos[0] + offset_x          
            new_pos_y = attach_to_pos[1] + offset_y
            while offset_x == 0 and offset_y == 0 or ([new_pos_x, new_pos_y] in self.room_set_pos):
                offset_x = random.choice([-1, 0, 1])
                offset_y = random.choice([-1, 0, 1])
                new_pos_x = attach_to_pos[0] + offset_x          
                new_pos_y = attach_to_pos[1] + offset_y
            new_room = Room(room_name, attach_to_pos[0] + offset_x, attach_to_pos[1] + offset_y)
            self.room_set.add(new_room)
            self.room_set_pos.append([new_pos_x, new_pos_y])
            new_room.add_neighbors()

class Room:
    # initialize rooms
    def __init__(self, name, pos_x, pos_y):
        self.name = name
        self.pos = [pos_x, pos_y]
        self.inventory = []
        self.neighbors = {}
        
    def __str__(self):
        return "%s room with the following neighbors:\n%r" % (self.name, self.neighbors)

    # called by map during initialization of game
    # build a dictionary attribute that has {other_room_object: 'north'}
    # then call other_room_object.neighbors and add to its dictionary
    # {this_room_object: 'south'}
    def add_neighbors(self):
        global my_map
        for i in my_map.room_set:
            if i == self:
                continue
            neighbor_dir = vector_to_dir(self.get_pos(), i.get_pos())
            if neighbor_dir != None:
                self.neighbors[i] = neighbor_dir
                i.neighbors[self] = opposing[cardinals.index(neighbor_dir)]
        
        #for i in random.randrange(3):
        #    room_names.pop()
        #    new_room = Room(room_name)
        #    j = random.randrange(9)
        #    while cardinals[j] in self.neighbors.values():
        #        j = random.randrange(9)
        #    self.neighbors[new_room] = cardinals[j]
        #    new_room.neighbors[self] = opposing[j]

    # return true if there is an empty space for another neighbor
    def check_neighbors(self):
        if len(self.neighbors) < 8:
            return True
        else:
            return False
            
    def get_pos(self):
        return self.pos
    # there is one active room at a time (this is the room the player is in).
    # active room dictates what can be interacted with and where player can go
    def activate(self):
        pass

    # opposite of the activate method
    def deactivate(self):
        pass


class Player:
    # initialize player. New player if new game; load player if load game
    # Player class contains all commands that can be issued by user (except help)
    # The idea behind "mod = None" in all the commands is that the player
    # could input > take sword OR just > take, and the code is general enough
    # that it accepts both inputs (the more general "take" then prompting
    # the player with "what to take?")
    # Not sure how well it will work, honestly!
    def __init__(self, name):
        self.name = name
        self.inventory = []
        # random starting location
        self.active_room = random.choice(map.room_set)

    # move in a cardinal direction
    # check active room. get adjacent rooms. check if move is legal. 
    def move(self, mod = None):
        pass

    # go directly to a discovered room
    def goto(self, mod = None):
        pass

    # pick something up
    def take(self, mod = None):
        pass

    # drop something on the ground
    def drop(self, mod = None):
        pass

    # check something out
    def examine(self, mod = None):
        pass
    
    # 
    def get_active_room(self):
        pass

    # call when game ends to save variables so player can load game
    def save_player(self, mod = None):
        pass

class Puzzle:
    # initialize puzzles
    def __init__(self):
        self.solved = False
        
    # set puzzle state to solved
    def solve(self):
        self.solved = True
        
    # check puzzle state. upon solving, reward player.
    def get_state(self):
        return self.solved
        
# display list of commands
def help(i = ''):
    if i in helpful:
        print i + ":"
        print helpful[i] + '\n'
    elif i != '' and i not in helpful:
        print "Sorry, I don't think that's a possible command! Try one of these:"
        for j in helpful:
            print j
        print
    else:
        print "Here are a list of commands.\nFor help with a specific command, type 'help [command]' without punctuation."
        for j in helpful:
            print j
        print


def main():
    # create map
    map = Map()
    
    # create player
    name = raw_input("Please enter your name: ")
    player = Player(name)

    # loop so always waiting on user input
    while True:
        prompt = '> '
        next = raw_input(prompt).lower()
        # there has to be a fancier way to do this than a giant if/elif statement.
        # I'm thinking, using .split(), .find(), getattr()
        #next2 = next.split()
        #getattr(player, next2[0])(next2[1:])
        #works if the command has two words. what if it's just one? what if 3?
        if "move" in next or "go" in next:
            player.move()
        elif "help" in next:
                help(next[5:])
        else:
            print "I don't know what that means. Type help for list of commands.\n"

# get things rolling
if __name__ == "__main__":
    main()
