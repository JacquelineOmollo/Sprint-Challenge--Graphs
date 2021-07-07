from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)
    
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# Smap_file = "maps/test_loop_fork.txt"
#map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# traversal_path = ['n', 'n']
traversal_path = []
empty_rooms = []

unexplored = set()

def bft(player):
    q = Queue()
    visited =set()
    # start of vertex 
    q.enqueue([("n", player.current_room.id)])
    
    while q.size() > 0:
        path = q.dequeue()
        #last vertex in the path
        explored_room = path[-1]
        
        if player.current_room not in visited:
            visited.add(player.current_room.id)
            
        # Itertate to the exits
        for direction in world.rooms[explored_room[1]].get_exits():
        # Checks if explored rooms neighbors in unexplored
            if world.rooms[explored_room[1]].get_room_in_direction(direction) not in unexplored:
        # Append room direction
                path.append((direction, world.rooms[explored_room[1]].get_room_in_direction(direction).id))
                print(path)
                return path
        # Check rooms neighbor to see if it's been visited
            if world.rooms[explored_room[1]].get_room_in_direction(direction).id not in visited:
                new_room = world.rooms[explored_room[1]].get_room_in_direction(direction)
                new_path = path.copy()
        # Append room and direction
                new_path.append((direction, new_room.id))
                visited.add(new_room.id)
                q.enqueue(new_path)
            
def connection(path):
        # Iterates through path and get direction to add traversal path
    for i in range(1, len(path)):
        direction = path[i][0]
        player.travel(direction)
        # Triggers the test
        traversal_path.append(direction)
        unexplored.add(player.current_room)
    
while(len(unexplored) != len(room_graph)):
        # Looks for shortest connectiion
    connection(bft(player))



# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
