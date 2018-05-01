###################################
####    Scientfic Calculator   ####
####    Written by Zijian Yao  ####
###################################

##  GUI Library used in this project is PyQt version4 
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from parser import acc
from convert import converter
from numpy import ndarray

#Buttons on the lower panel
LOWER_BUTTON_LABELS  = 	[['7','8','9','DEL','AC'],
						['4','5','6','*','/'],
						['1','2','3','+','-'],
						['0','.','E','Ans','=']]

#Buttons on the upper panel
UPPER_BUTTON_LABELS  = 	[['sum','x','<-','->','!','chs'],
						['dx','intg','intp','lstsq','frac', 'j'],
						['recip','sqrt','pow','log','log10', 'ln'],
						['gcd','lcm','sin','cos','tan','°'],
						['[', ']','(',')','<>',',']]

#Unary Functions
UPPER_UNARY_FUNCTION = {'recip','sqrt', 'log10','ln','sin','cos','tan'}

#Binary Functions
UPPER_BINARY_FUNCTION = {'log','pow', 'gcd', 'lcm', 'chs', 'frac'}

#All buttons have been implementented
#Buttons not implemented temporarily
UPPER_NOT_IMPLEMENTED = {}

#GUI: MainWindow
class Window(QMainWindow):

	def __init__(self):
		'''
			Class Constructor:
				set the window size and title
				configure the panels 
		'''
		super(Window, self).__init__()
		self.wid = QWidget(self)
		self.wid.setStyleSheet("background-color: white")
		self.setCentralWidget(self.wid)
		self.setGeometry(50,50,288,462)
		self.setWindowTitle("Scientfic Calculator")
		self.lowerButtonActions={'DEL':self.delDisplay(), 
								'AC':self.clearDisplay(),
								'=':self.evalDisplay()
								} # actions associated with control buttons
		self.upperButtonActions={'<-':self.stepbackward(), 
								'->':self.stepforward(),
								'<>':self.convDisplay()
								} # actions associated with control buttons
		self.configlayout()
		self.show()

	def configlayout(self):
		'''
			Configure the layout of each panel
			Add widgets to rach panel 
		'''
		
		def configureUpper():
			'''
				Configure the upper panel and add buttons to it
			'''
			upper = QGridLayout()
			for i in range(5):
				for j in range(6):
					label = UPPER_BUTTON_LABELS[i][j]
					btn = QPushButton(label)
					#btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
					#btn.setStyleSheet("background-color: rgb(255, 255, 255);"
					#	"border: 1px solid gray;")
					btn.setStyleSheet("background-color: rgb(225, 225, 255);"
					 "border-style: solid;"
					 "border-width:1px;"
					 "border-radius:15px;"
					 "border-color: grey;"
					 "max-width:30px;"
					 "max-height:30px;"
					 "min-width:30px;"
					 "min-height:30px;"
					 "font: 10pt Gill Sans")
					if label in self.upperButtonActions:
						btn.clicked.connect(self.upperButtonActions[label])
					elif label in UPPER_NOT_IMPLEMENTED:
						btn.clicked.connect(self.notimplemented)
					else:
						if label in UPPER_UNARY_FUNCTION:
							label += '('
						elif label in UPPER_BINARY_FUNCTION:
							label += '(,'
						btn.clicked.connect(self.appendDisplay(label))
					upper.addWidget(btn,i,j)
			return upper

		def configureLower():
			'''
				Configure the lower panel and add buttons to it
			'''
			lower = QGridLayout()
			for i in range(4):
				for j in range(5):
					label = LOWER_BUTTON_LABELS[i][j]
					btn = QPushButton(label)
					if label in self.lowerButtonActions:
						btn.clicked.connect(self.lowerButtonActions[label])
					else:
						btn.clicked.connect(self.appendDisplay(label))
					btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
					if j>=3:

						btn.setStyleSheet("background-color: rgb(255, 151, 57);"
						"border: 1px solid gray;"
						"font: 15pt Gill Sans")  
					else:
						btn.setStyleSheet("background-color: rgb(255, 225, 225);"
						"border: 1px solid gray;"
						"font: 15pt Gill Sans")
					lower.addWidget(btn,i,j)
			return lower

		def configureOuterMost():
			'''
				Configure the outermost panel 
				  which contains a text display and two button panels
			'''
			outer = QVBoxLayout()
			self.display =  QLineEdit()
			self.display.setStyleSheet("qproperty-alignment: 'AlignVCenter | AlignRight';"
						"border: 1px solid grey;"
						"min-height: 2em;"
						"font: 18pt Courier New"
						)
			upper = configureUpper()
			lower = configureLower()
			outer.addWidget(self.display)
			outer.addLayout(upper)
			outer.addLayout(lower)
			return outer 
		
		self.wid.setLayout(configureOuterMost())

	def appendDisplay(self, txt):
		'''
			Insert the input at the cursor of the display 
			shift the cursor to the next position
		'''
		
		def aux(ch):
			txt = self.display.text()
			pos = self.display.cursorPosition()
			self.display.setText(txt[:pos]+ch+txt[pos:])
			self.display.setCursorPosition(pos+len(ch))

		return lambda: aux(txt)

	def delDisplay(self):
		'''
			Delete a character at the cursor of the display 
			shift the cursor to the previous position
		'''
		
		def aux():
			txt = self.display.text()
			pos = self.display.cursorPosition()
			self.display.setText(txt[:pos-1]+txt[pos:])
			self.display.setCursorPosition(pos-1)
		
		return aux

	def clearDisplay(self):
		'''
			clear the display
		'''
		return lambda: self.display.setText('')

	def evalDisplay(self):
		'''
			evaluate the input 
		'''

		def aux():
			txt = self.display.text()
			try:
				result = acc.parse(txt)
			except SyntaxError:
				self.display.setText('Invalid Syntax')
			except:
				self.display.setText('Value Error')
			else:
				if type(result) is ndarray:
					result = list(result)
				self.display.setText(str(result))

		return aux

	def convDisplay(self):
		'''
			convert between fraction and decimal
			for complex number: between rect and polar forms
		'''
		def aux():
			txt = self.display.text()
			try:
				result = converter.parse(txt)
			except:
				return
			else:
				self.display.setText(str(result))

		return aux

	def stepbackward(self):
		'''
			move the cursor backward if possible
		'''
		return lambda: self.display.cursorBackward(False)

	def stepforward(self):
		'''
			move the cursor forward if possible
		'''
		return lambda: self.display.cursorForward(False)

	def notimplemented(self):
		'''
			placeholder for the button actions not implemented temporarily
		'''
		pass

