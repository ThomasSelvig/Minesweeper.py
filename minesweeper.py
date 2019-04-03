import time
import sys
import os
import random
import keyboard # pip install keyboard --user

width = 10
height = 10
minePercentage = 0.1 # 10% mines
mines = width * height * minePercentage
gameover = False


class slot:
	selectX = 0
	selectY = 0
	def __init__(self):
		# default settings: these are initialized before anything
		self.selected = False
		self.opened = False
		self.mine = False
		self.flag = False
		self.clear = True
		self.proximityMines = 0

		self.selectChar0 = "<"
		self.selectChar1 = ">"

	def prtStatus(self):

		if not self.opened:
			if self.selected:
				if self.flag:
					return (self.selectChar0 + "F" + self.selectChar1)
				return self.selectChar0+"~"+self.selectChar1
			if self.flag:
				return " F "
			return " ~ "

		elif self.opened:

			if self.selected:
				if self.mine:
					self.clear = False
					return self.selectChar0 + "@" + self.selectChar1

				for i in range(1,9):
					if self.proximityMines == i:
						self.clear = False
						return self.selectChar0 + str(i) + self.selectChar1
				if self.clear:
					return self.selectChar0 + " " + self.selectChar1

			if self.mine:
				self.clear = False
				return " @ "
			for i in range(1,9):
				if self.proximityMines == i:
					self.clear = False
					return " " + str(i) + " "
			if self.clear:
				return "   "

mfield = [[slot() for y in range(height)] for x in range(width)]

def cls():
	os.system("cls")
def quit():
	sys.exit(0)

# Hotkeys
def open():
	global gameover
	if not mfield[slot.selectX][slot.selectY].opened:
		if not mfield[slot.selectX][slot.selectY].flag:
			mfield[slot.selectX][slot.selectY].opened = True
		if mfield[slot.selectX][slot.selectY].mine:
			gameover = True
	main()

def flag():
	if not mfield[slot.selectX][slot.selectY].opened:
		if mfield[slot.selectX][slot.selectY].flag:
			mfield[slot.selectX][slot.selectY].flag = False
		elif not mfield[slot.selectX][slot.selectY].flag:
			mfield[slot.selectX][slot.selectY].flag = True
	main()

def move(dir):
	global mfield
	global width
	global height

	if   dir=="left":
		if slot.selectX > 0:
			mfield[slot.selectX][slot.selectY].selected = False
			slot.selectX -= 1

	elif dir=="right":
		if slot.selectX < width-1:
			mfield[slot.selectX][slot.selectY].selected = False
			slot.selectX += 1

	elif dir=="up":
		if slot.selectY > 0:
			mfield[slot.selectX][slot.selectY].selected = False
			slot.selectY -= 1

	elif dir=="down":
		if slot.selectY < height-1:
			mfield[slot.selectX][slot.selectY].selected = False
			slot.selectY += 1

	main()

keyboard.add_hotkey("a", move, args=("left",))
keyboard.add_hotkey("d", move, args=("right",))
keyboard.add_hotkey("w", move, args=("up",))
keyboard.add_hotkey("s", move, args=("down",))
keyboard.add_hotkey("space", open)
keyboard.add_hotkey("f", flag)

def getRandom(a, b):
	return random.randint(a,b)

def scramble():
	global minePercentage
	global mines
	minecount = 0

	while minecount < mines:
		for yloop in range(height):
			for xloop in range(width):
				if minecount < mines:
					#place an average of 1 mine every iteration of the mfield
					#string = str(mfield[xloop][yloop])
					if not mfield[xloop][yloop].mine:
						if getRandom(1, width*height) == 1:
							#place mine
							mfield[xloop][yloop].mine = True
							minecount+=1

def checkWin():
	mineCount = 0
	flagCount = 0
	for yl in range(height):
		for xl in range(width):
			if mfield[xl][yl].flag:
				flagCount += 1
				if mfield[xl][yl].mine:
					mineCount += 1
	if mineCount == mines and mineCount == flagCount:
		return True
	else:
		return False

def printMinefield():
	for yloop in range(height):
		for xloop in range(width):
			sys.stdout.write(str(mfield[xloop][yloop].prtStatus()))
		print("")

def findProximity():
	global width
	global height

	# start with the corners

	if mfield[1][1].mine:
		mfield[0][0].proximityMines += 1
	if mfield[1][0].mine:
		mfield[0][0].proximityMines += 1
	if mfield[0][1].mine:
		mfield[0][0].proximityMines += 1

	if mfield[width-2][0].mine:
		mfield[width-1][0].proximityMines += 1
	if mfield[width-2][1].mine:
		mfield[width-1][0].proximityMines += 1
	if mfield[width-1][1].mine:
		mfield[width-1][0].proximityMines += 1

	if mfield[width-2][height-2].mine:
		mfield[width-1][height-1].proximityMines += 1
	if mfield[width-1][height-2].mine:
		mfield[width-1][height-1].proximityMines += 1
	if mfield[width-2][height-1].mine:
		mfield[width-1][height-1].proximityMines += 1

	if mfield[1][height-2].mine:
		mfield[0][height-1].proximityMines += 1
	if mfield[0][height-2].mine:
		mfield[0][height-1].proximityMines += 1
	if mfield[1][height-1].mine:
		mfield[0][height-1].proximityMines += 1

	# Then the edges
	# top
	for i in range(1, width-1):
		if mfield[i-1][0].mine:
			mfield[i][0].proximityMines += 1
		if mfield[i+1][0].mine:
			mfield[i][0].proximityMines += 1

		if mfield[i-1][1].mine:
			mfield[i][0].proximityMines += 1
		if mfield[i+1][1].mine:
			mfield[i][0].proximityMines += 1
		if mfield[i][1].mine:
			mfield[i][0].proximityMines += 1
	# bottom
	for i in range(1, width-1):
		if mfield[i-1][height-1].mine:
			mfield[i][height-1].proximityMines += 1
		if mfield[i+1][height-1].mine:
			mfield[i][height-1].proximityMines += 1

		if mfield[i-1][height-2].mine:
			mfield[i][height-1].proximityMines += 1
		if mfield[i+1][height-2].mine:
			mfield[i][height-1].proximityMines += 1
		if mfield[i][height-2].mine:
			mfield[i][height-1].proximityMines += 1
	# left
	for i in range(1, height-1):
		if mfield[0][i-1].mine:
			mfield[0][i].proximityMines += 1
		if mfield[0][i+1].mine:
			mfield[0][i].proximityMines += 1

		if mfield[1][i-1].mine:
			mfield[0][i].proximityMines += 1
		if mfield[1][i+1].mine:
			mfield[0][i].proximityMines += 1
		if mfield[1][i].mine:
			mfield[0][i].proximityMines += 1
	# right
	for i in range(1, height-1):
		if mfield[width-1][i-1].mine:
			mfield[width-1][i].proximityMines += 1
		if mfield[width-1][i+1].mine:
			mfield[width-1][i].proximityMines += 1

		if mfield[width-2][i-1].mine:
			mfield[width-1][i].proximityMines += 1
		if mfield[width-2][i+1].mine:
			mfield[width-1][i].proximityMines += 1
		if mfield[width-2][i].mine:
			mfield[width-1][i].proximityMines += 1

	# Then the middle
	for yl in range(1, height-1):
		for xl in range(1, width-1):
			# starting top left, going clockwise
			if mfield[xl-1][yl-1].mine:
				mfield[xl][yl].proximityMines += 1
			if mfield[xl][yl-1].mine:
				mfield[xl][yl].proximityMines += 1
			if mfield[xl+1][yl-1].mine:
				mfield[xl][yl].proximityMines += 1
			if mfield[xl+1][yl].mine:
				mfield[xl][yl].proximityMines += 1
			if mfield[xl+1][yl+1].mine:
				mfield[xl][yl].proximityMines += 1
			if mfield[xl][yl+1].mine:
				mfield[xl][yl].proximityMines += 1
			if mfield[xl-1][yl+1].mine:
				mfield[xl][yl].proximityMines += 1
			if mfield[xl-1][yl].mine:
				mfield[xl][yl].proximityMines += 1


def setup():
	global width
	global height
	global gameover
	global mfield
	cls()
	width = int(input("Width: "))
	height = int(input("Height: "))
	cls()

	mfield = [[slot() for y in range(height)] for x in range(width)]
	gameover = False
	scramble()
	findProximity()
	main()

def main():
	cls()
	mfield[slot.selectX][slot.selectY].selected = True

	if gameover:
		print("You Lost! Press Enter to restart. ")
		input()
		setup()
	else:
		if checkWin():
			print("You Won! Press Enter to restart. ")
			input()
			setup()

		print("Minecount: " + str(mines))
		print("Position: " + str(slot.selectX) + ", " + str(slot.selectY))
		print("-"*width*3)
		printMinefield()
		print("-"*width*3)

setup()

# This code is here to keep the main thread alive
while True:
	True
