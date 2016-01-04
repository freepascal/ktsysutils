from PyQt4.QtCore import QThread

class GenericThread(QThread):
	def __init__(self, function, *args, **kwargs):
		super(GenericThread, self).__init__(self)
		self.function = function
		self.args = args
		self.kwargs = kwargs
		
	def __del__():
		self.wait()
		
	def run(self):
		if hasattr(self.function, '__call__'):
			function(*self.args, **self.kwargs)
		return
