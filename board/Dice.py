import random


class Dice:

	def __init__(self, die1=None, die2=None):
		if die1 is None:
			self.die1 = random.randint(1, 6)
		else:
			self.die1 = die1

		if die2 is None:
			self.die2 = random.randint(1, 6)
		else:
			self.die2 = die2

	def roll(self):
		self.die1 = random.randint(1, 6)
		self.die2 = random.randint(1, 6)

	def rollNoDoubles(self):
		self.roll()
		while self.isDoubles():
			self.roll()

	def setRoll(self, dice: tuple):
		die1, die2 = dice
		self.die1 = die1
		self.die2 = die2

	def getDistances(self):
		if self.isDoubles():
			return {self.die1: 4}
		else:
			return {self.die1: 1, self.die2: 1}

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
