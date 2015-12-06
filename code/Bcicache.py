from numpy import *

class cache():
	def __init__(self):
		self.cache=[]
	def write_catche(slef,data):
		self.cache.append(data)

	def getalldata(self):
		m=self.cache
		self.cache=[]
		return m

	def get_data(self,length):
		m = self.cache[0:length]
		del self.cache[0:length]
		return m