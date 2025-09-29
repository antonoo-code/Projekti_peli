NPC_visited_ports = ['a','b']
in_range = ['a','b','c','d']
for i in NPC_visited_ports:
    if i in in_range:
        in_range.remove(i)
print(in_range)