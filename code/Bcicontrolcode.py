import numpy as np

class Bcicontrolcode():
	def __init__(self):
		self.directions=np.asarray(['idle','left','right','forward']);

	def directions(self,direction):
		return  self.directions[direction]


