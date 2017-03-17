from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules import LSTMLayer
from pybrain.supervised import RPropMinusTrainer
from pybrain.datasets import SequentialDataSet
from itertools import cycle
from pybrain.datasets import SupervisedDataSet,UnsupervisedDataSet
from sys import stdout
#import gtk
#import gtk.glade
from gi.repository import Gtk
import thread
import time
import threading
import random
import pickle

#Define a function/Dictionary that converts the classical notation into numbers, such as S=1, R=2 and so on....
#Consideration has not yet been made for -,tones,etc
def f(x):

	if x==1:
		return 'S'
	elif x==2:
		return 'R'
	elif x==3:
		return 'G'
	elif x==4:
		return 'M'
	elif x==5:
		return 'P'
	elif x==6:
		return 'D'
	elif x==7:
		return 'N'
	elif x==8:
		return '-'
		
		
class trainer:
	
	
	def __init__( self ):
		
		global i
		
		global builder2
		filename = "Train.glade"
		builder2 = Gtk.Builder()
		builder2.add_from_file(filename)
		#builder2.connect_signals(self)
		global window1
		window1 = builder2.get_object("train")
		window1.show_all()
		
		handlers = {
			"tr": self.check
			}
		
		builder2.connect_signals(handlers)
		
		#print("final error =", train_errors[-1])
		
	def check(self,*args):
		global i
		
		if i==0:
			i=i+1
			self.trainee()
		else:
			
			self.delete()
	
	def delete(self):
		global window1
		window1.destroy()
		
	def trainee(self):
		
		button=builder2.get_object("start")
		spin=builder2.get_object("spinner1")

		spin.start()
		
		def callback():
		
			ds = SequentialDataSet(1, 1) #Make a sequential data set which is capable of holding a sequence
			data=[1,8,7,6,7,1,2,3,5,8,4,8,3,8,8,2,2,8,8,8,3,4,5,3,2,1,7,6,2,1,1,8,2,6,3,2,3,5,4,2,3,4,5,6,5,4,7,6]
			# training data which is already converted into number notation holds a random music phrase, This is to be replaced with 			the appropriate and valid training data set
	
			for sample, next_sample in zip(data, cycle(data[1:])):
   				ds.addSample(sample, next_sample) #Adding the samples to the dataset
	
			net = buildNetwork(1, 24, 1,hiddenclass=LSTMLayer, outputbias=False, recurrent=True) #Building a LSTM network
   		                                  
			#print("Beggining to train the network\n")
			#The steps below are used to train the network                   
			trainer = RPropMinusTrainer(net, dataset=ds)
			train_errors = [] # save errors for plotting later
			EPOCHS_PER_CYCLE = 5
			CYCLES = 100
			EPOCHS = EPOCHS_PER_CYCLE * CYCLES
			for i in xrange(CYCLES):
				trainer.trainEpochs(EPOCHS_PER_CYCLE)
				train_errors.append(trainer.testOnData())
				epoch = (i+1) * EPOCHS_PER_CYCLE
				stdout.flush()
			spin.stop()
			button.set_label("Finish")
			
		thread = threading.Thread(target=callback)        		
		thread.start()
        	#thread.join()
		#(int(random.random() * 199999)) ** (int(random.random() * 1999999))
        	#while(thread.is_alive()!= True):
        	#	

		#print("Finished training network\n")
		
		
		
class execute:
	
	def __init__( self ):
		
		global inp,index
		inp=[0]*100
		index=0
		filename = "Execute.glade"
		builder3 = Gtk.Builder()
		builder3.add_from_file(filename)
		#builder3.connect_signals(self)
		window2 = builder3.get_object("execute")
		window2.show_all()
		global texy,buff
		texy=builder3.get_object("texy")
		buff = texy.get_buffer()
		handlers = {
			"s":self.addS,
			"r":self.addR,
			"g":self.addG,
			"m":self.addM,
			"p":self.addP,
			"d":self.addD,
			"n":self.addN,
			"-":self.addL,
			"exec":self.executer
		}
		builder3.connect_signals(handlers)
		
		Gtk.main()
		
	def addS(self,*args):
		global index,buff
		i = buff.get_end_iter()
		buff.insert(i, " S")
		inp[index]=1
		index=index+1
	
	def addR(self,*args):
		global index,buff
		i = buff.get_end_iter()
		buff.insert(i, " R")
		inp[index]=2
		index=index+1

	def addG(self,*args):
		global index,buff
		i = buff.get_end_iter()
		buff.insert(i, " G")
		inp[index]=3
		index=index+1

	def addM(self,*args):
		global index,buff
		i = buff.get_end_iter()
		buff.insert(i, " M")
		inp[index]=4
		index=index+1

	def addP(self,*args):
		global index,buff
		i = buff.get_end_iter()
		buff.insert(i, " P")
		inp[index]=5
		index=index+1

	def addD(self,*args):
		global index,buff
		i = buff.get_end_iter()
		buff.insert(i, " D")
		inp[index]=6
		index=index+1

	def addN(self,*args):
		global index,buff
		i = buff.get_end_iter()
		buff.insert(i, " N")
		inp[index]=7
		index=index+1

	def addL(self,*args):
		global index,buff
		i = buff.get_end_iter()
		buff.insert(i, " -")
		inp[index]=8
		index=index+1

	def executer(self,*args):
	
		thisisit=thefinalshow(inp)
		
class thefinalshow:
	
	def __init__( self , inp=[] ):
	
		self.inp=inp
		filename = "Output.glade"
		global builder4
		builder4 = Gtk.Builder()
		builder4.add_from_file(filename)
		builder4.connect_signals(self)
		window = builder4.get_object("Out")
		window.show_all()
	
		fileObject = open('net','r')
		net = pickle.load(fileObject)
		
		texy=builder4.get_object("outty")
		buff = texy.get_buffer()
		
		ch=["X","S","R","G","M","P","D","N","-"]
		z = buff.get_end_iter()
		buff.insert(z, "\tPREDICTOR OUTPUT FOR SEQUENCE\n\n")
		i=0
		valid=0
		while inp[i]!=0:
			if i%4==0 and i%8!=0 and i!=0:
				z = buff.get_end_iter()
				buff.insert(z, "\t|\t")
			if i%8==0 and i!=0:
				z = buff.get_end_iter()
				buff.insert(z, "\t||\n")
				valid=1
			if i==0 or valid==1:
				z = buff.get_end_iter()
				buff.insert(z, "||\t")
				valid=0
			net.activate(inp[i])
			z = buff.get_end_iter()
			x=inp[i]
			buff.insert(z, "\t"+ch[x])
			i=i+1
		
		temp=1
		x=i
		validate=1
		sample=inp[i-1]
		while temp+x<=256:
		
			predicted=net.activate(sample)
			pred=int(round(predicted))
			if i%4==0 and i%8!=0 and i!=0 and validate!=0:
				z = buff.get_end_iter()
				buff.insert(z, "\t|\t")
			if i%8==0 and i!=0 and validate!=0:
				z = buff.get_end_iter()
				buff.insert(z, "\t||\n")
				valid=1
			if i==0 or valid==1 and validate!=0:
				z = buff.get_end_iter()
				buff.insert(z, "||\t")
				valid=0
			
			if pred>=1 and pred<=8:
				z = buff.get_end_iter()
				buff.insert(z, "\t"+ch[pred])
				sample=pred
				temp=temp+1
				i=i+1	
				validate=1
			
			else:
				validate=0	
			
		z = buff.get_end_iter()
		buff.insert(z, "\t||\n")
		Gtk.main()

class Network:

	def __init__( self ):
	
		filename = "Network.glade"
		builder = Gtk.Builder()
		builder.add_from_file(filename)
		builder.connect_signals(self)
		window = builder.get_object("net")
		#window.set_default_size(400,400);
		window.show_all()
		Gtk.main()
		
class gui:
	
	def __init__( self ):
	
		filename = "mainPage.glade"
		builder = Gtk.Builder()
		builder.add_from_file(filename)
		builder.connect_signals(self)
		window = builder.get_object("composer")
		window.show_all()
		
		handlers = {
			"onDeleteWindow": self.delete,
			"about": self.about,
			"execute":self.execute,
			"train":self.train,
			"netty":self.netty
}
		builder.connect_signals(handlers)
		
		Gtk.main()
		
	def delete(self,*args):
		Gtk.main_quit
		exit(0)
		
	def netty(self,*args):
		info=Network()
	
	
	def about(self,*args):
		
		filename = "About.glade"
		builder = Gtk.Builder()
		builder.add_from_file(filename)
		builder.connect_signals(self)
		window = builder.get_object("about")
		window.show_all()
		

	
	def train(self,*args):
	
		dothis=trainer()

	def execute(self,*args):
	
		dothis=execute()
			
		print()

letsdothis = gui()
