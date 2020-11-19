import random


class Dice:

	def __init__(self):
		self.die1 = random.randint(1, 6)
		self.die2 = random.randint(1, 6)

	def roll(self):
		self.die1 = random.randint(1, 6)
		self.die2 = random.randint(1, 6)

	def setRoll(self, die1, die2):
		self.die1 = die1
		self.die2 = die2

	def getDice(self):
		return self.die1, self.die2

	def getDie1(self):
		return self.die1

	def getDie2(self):
		return self.die2

	def isDoubles(self):
		return self.die1 == self.die2

	def __str__(self):
		return "Dice: " + str(self.getDice())
