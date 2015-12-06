from sklearn import svm
from sklearn.externals import joblib
from sklearn import preprocessing
import numpy as np

class Bciclassifier():
	def __init__(self):
		self.classfier = svm.LinearSVC()
		#self.tarin()
	
	def preprocess(unnormalized_data):
		return preprocessing.normalize(unnormalized_data, norm='l2')

	def tarin(self,instances,label):
		self.classfier.fit(preprocess(instances),np.array(label))

	def predict(self,test_data):
		return self.classfier.predict(preprocess(test_data))

	def load_model(self,path):
		self.classfier = joblib.load('path') 

	def save_model(path):
		path+="/filename.pkl"
		joblib.dump(clf, path)
	
