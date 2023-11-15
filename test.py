import sys
print(sys.version)

items = [10, 11, 12, 13]
print(sum(1 for i in items if i > 10))


npc_list
sum(1 for npc in npc_list if npc.infected and npc.infectionStage >= 120)