# title:   Shadow Ooze: Eclipse of Humanity
# author:  Hevanafa
# desc:    15-11-2023
# license: MIT License
# version: 0.1
# script:  python

import math
import random

# import sys

from typings import btn, cls, rect, spr, circb, key, rectb, print, trace

#trace(sys.version)

rand = random.random

b_top = 20
b_left = 10
b_right = 230
b_bottom = 126

sw = 240
sh = 136

# px = sw / 2
# py = sh / 2
# p_face true: right
p_face = False

p_squish = False
tl_squish = 0

class NPC:
	cx: float
	cy: float
	hp: float

	def __init__(self):
		self.infected = False
		self.infectionStage = 0
		self.vx = 0.0
		self.vy = 0.0
		self.spr = random.randint(4, 6)
		self.change_dir_tl = 0
		self.immunity_ttl = 0  # 30 on hit, in frames
		self.panic = False

npc_list: list[NPC] = []

for a in range(1, 21):
	p = NPC()
	p.cx = random.randint(10, 220)
	p.cy = random.randint(10, 116)
	p.hp = 3.0

	npc_list.append(p)

npc_count = len(npc_list)
infected_count = 0
tl_recalculate = 0
controlled_npc: NPC = NPC()

def getDist(x1, x2, y1, y2):
	return (x2 - x1) ** 2 + (y2 - y1) ** 2


def update():
	global controlled_npc, p_face, tl_squish, p_squish
	global tl_recalculate, infected_count
	global rand

	if btn(0) or key(23):
		controlled_npc.cy -= 0.5
	if btn(1) or key(19):
		controlled_npc.cy += 0.5

	if btn(2) or key(1):
		p_face = False
		controlled_npc.cx -= 0.5
	if btn(3) or key(4):
		p_face = True
		controlled_npc.cx += 0.5

	if controlled_npc.cx < b_left:
		controlled_npc.cx = b_left
	if controlled_npc.cx > b_right:
		controlled_npc.cx = b_right

	if controlled_npc.cy < b_top:
		controlled_npc.cy = b_top
	if controlled_npc.cy > b_bottom:
		controlled_npc.cy = b_bottom

	# update squish
	tl_squish -= 1

	if tl_squish <= 0:
		tl_squish = 30
		p_squish = not p_squish


	# update NPCs
	for npc in npc_list:
		if npc.infected and npc.infectionStage < 120:
			npc.infectionStage += 1
			continue

		npc.cx += npc.vx
		npc.cy += npc.vy

		if npc.cx < b_left:
			npc.cx = b_left
		if npc.cx > b_right:
			npc.cx = b_right

		if npc.cy < b_top:
			npc.cy = b_top
		if npc.cy > b_bottom:
			npc.cy = b_bottom

		# begin check dir
		npc.change_dir_tl -= 1

		if npc.change_dir_tl < 0:
			npc.change_dir_tl = random.randint(60, 120)
			npc.vx = math.sin(rand() * 2 * math.pi) / 4
			npc.vy = math.cos(rand() * 2 * math.pi) / 4

		# begin check immunity
		if npc.immunity_ttl > 0:
			npc.immunity_ttl -= 1
			continue

		if getDist(npc.cx, controlled_npc.cx, npc.cy, controlled_npc.cy) <= 64:
			if npc.hp > 0:
				npc.immunity_ttl = 15   # 30
				npc.hp -= 1
			else:
				npc.infected = True


	tl_recalculate -= 1

	if tl_recalculate <= 0:
		tl_recalculate = 60
		infected_count = len([1  for npc in npc_list  if npc.infected and npc.infectionStage >= 120])


def render():
	global controlled_npc, p_face, p_squish, infected_count, npc_count
	
	cls(0)

	spr(2 if p_squish else 1,
		int(controlled_npc.cx - 4), int(controlled_npc.cy - 4),
		0,
		flip = (0 if p_face else 1))

	for npc in npc_list:
		# circb(p["cx"], p["cy"], 4, 7)
		x = int(npc.cx - 4)
		y = int(npc.cy - 4)

		if npc.infected:
			if npc.infectionStage < 120:
				# spr(19 + int(p.infectionStage / 30), x, y, 0)
				spr(35 + int(npc.infectionStage / 30), x, y, 0)
			else:
				# spr(24, x, y, 0, flip = 1 if p.vx > 0 else 0)
				spr(39, x, y, 0, flip = 1 if npc.vx > 0 else 0)
		else:
			spr(npc.spr, x, y, 0, flip = 1 if npc.vx > 0 else 0)

			# HP bar
			perc = npc.hp / 3
			rectb(x, y - 4, 8, 3, 7)
			rect(x, y - 4, int(perc * 8), 3, 11)

	# progress bar
	perc = infected_count / npc_count
	spr(39, 10, 4, 0)
	print(f"{ round(perc * 100) }%", 20, 6, 7, alt = True)

	s = "Goal: Find a Host"
	w = print(s, y = -100)
	print(s, (sw - w) // 2, 4, 7)

def TIC():
	update()
	render()
