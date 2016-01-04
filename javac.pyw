import sys
import tinycat
from qt_utilities import GenericThread
from PyQt4 import QtGui
from PyQt4 import QtCore

class JavacDialog(QtGui.QWidget):
	def __init__(self, parent = None):
		super(JavacDialog, self).__init__(parent)
		
		#create layout
		self.layout = QtGui.QFormLayout()
		self.setLayout(self.layout)
		
		#create widgets
		self.txtSourceDir = QtGui.QLineEdit()
		self.txtClassesDir = QtGui.QLineEdit()
		self.btnSelectSourceDir = QtGui.QPushButton('&Select')
		self.btnSelectClassesDir = QtGui.QPushButton('Selec&t')
		self.btnCompile = QtGui.QPushButton('&Compile')
		
		#populate widgets
		self.layout.addRow(self.btnSelectSourceDir, self.txtSourceDir)
		self.layout.addRow('', QtGui.QLabel('Top-level directory contains source code'))
		self.layout.addRow(self.btnSelectClassesDir, self.txtClassesDir)
		self.layout.addRow('', QtGui.QLabel('Top-level directory will contain .class files generated'))	
		
		#make inner layout for button compile
		innerLayout = QtGui.QHBoxLayout()
		innerLayout.addStretch(1)
		innerLayout.addWidget(self.btnCompile)
		self.layout.addRow(innerLayout)
		
		#listeners
		QtCore.QObject.connect(self.btnSelectSourceDir, QtCore.SIGNAL('released()'), self.selectSourceDir)
		QtCore.QObject.connect(self.btnSelectClassesDir, QtCore.SIGNAL('released()'), self.selectClassesDir)
		QtCore.QObject.connect(self.btnCompile, QtCore.SIGNAL('released()'), self.startCompiling)		
		
	def selectSourceDir(self):		
		self.txtSourceDir.setText(
			QtGui.QFileDialog.getExistingDirectory(
				self, 
				'Select directory'
			)
		)
		
	def selectClassesDir(self):
		self.txtClassesDir.setText(
			QtGui.QFileDialog.getExistingDirectory(
				self,
				'Select directory'
			)
		)
		
	def startCompiling(self):
		self.t_worker = QtCore.QThread(self.javac())
		QtCore.QObject.connect(self, QtCore.SIGNAL('javac'), self.javac)
		self.t_worker.start()
		
	#Wrapper of tinycat.javac	
	def javac(self):
		tinycat.javac(
			sourceDir = unicode(self.txtSourceDir.displayText()),
			classesDir = unicode(self.txtClassesDir.displayText()),
			successCallback = self.successCallback,
			errorCallback = self.errorCallback
		)
		
	def successCallback(self):
		QtGui.QMessageBox.information(
			self,
			'+info',
			'successs'
		)
		return
		
	def errorCallback(self):
		QtGui.QMessageBox.information(
			self,
			'+info',
			'failure'
		)
		return
	
app = QtGui.QApplication(sys.argv)
wnd = JavacDialog()
wnd.setGeometry(300, 300, 500, 250)
wnd.show()
sys.exit(app.exec_())
