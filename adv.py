from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# traversal_path = []


def add_edge(direction):
    if direction == 'e':
        return 'w'
    if direction == 'w':
        return 'e'
    if direction == 'n':
        return 's'
    if direction == 's':
        return 'n'


def traverse_maze():
    results = []
    graph = {}
    backtrack = []
    while len(graph) < len(room_graph):
        exits = player.current_room.get_exits()
        curr_room = player.current_room.id

        if curr_room not in graph:
            if backtrack:
                exits.remove(backtrack[-1])
            graph[curr_room] = exits

        if graph[curr_room]:
            choice = random.choice(graph[curr_room])
            graph[curr_room].remove(choice)
            player.travel(choice)
            results.append(choice)
            backtrack.append(add_edge(choice))

        else:
            direction = backtrack.pop()
            player.travel(direction)
            results.append(direction)
    return results


res = []
for _ in range(10000):
    player = Player(world.starting_room)
    res.append(traverse_maze())
min_moves = len(res[0])
path = res[0]
for r in res:
    if len(r) < min_moves:
        min_moves = len(r)
        path = r
traversal_path = path


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
