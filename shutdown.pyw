import dbus
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

#http://stackoverflow.com/questions/23013274/shutting-down-computer-linux-using-python
sysBus = dbus.SystemBus()
ck_srv = sysBus.get_object(
	'org.freedesktop.ConsoleKit',
	'/org/freedesktop/ConsoleKit/Manager'
)
ck_iface = dbus.Interface(ck_srv, 'org.freedesktop.ConsoleKit.Manager')
stop_method = ck_iface.get_dbus_method("Stop")

def shutdownNow():
	stop_method()
	
class MainWindow(QtGui.QWidget):
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)
		self.dateEdit = QtGui.QDateEdit(QtCore.QDate.currentDate())
		self.timeEdit = QtGui.QTimeEdit(QtCore.QTime.currentTime())
		self.schedule = QtGui.QPushButton('Schedule')
		self.layout = QtGui.QFormLayout()
		self.setLayout(self.layout)
		
		#populate
		self.layout.addRow('Date', self.dateEdit)
		self.layout.addRow('Time', self.timeEdit)
		self.layout.addRow(self.schedule)
		
		#listener
		QtCore.QObject.connect(self.schedule, QtCore.SIGNAL('released()'), self.scheduleShutdown)
		
		#show
		self.setGeometry(300, 300, 200, 100)
		self.show()
		
	def scheduleShutdown(self):
		now = QtCore.QDateTime(QtCore.QDate.currentDate(), QtCore.QTime.currentTime())
		schedule = QtCore.QDateTime(
			self.dateEdit.date(),
			self.timeEdit.time()
		)	
		if now.secsTo(schedule) > 0:
			#shutdown computer off after xxx seconds
			pass
		else:
			#shutdown now
			shutdownNow()		

app = QtGui.QApplication(sys.argv)
wnd = MainWindow()
sys.exit(app.exec_())
