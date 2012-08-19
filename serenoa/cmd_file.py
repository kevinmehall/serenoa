from serenoa.file import BaseFile, abspath
from subprocess import Popen, PIPE

class CommandFile(BaseFile):
	"""A file loader that runs a specified shell command"""

	def __init__(self, command, path=None):
		super(CommandFile, self).__init__(path)
		self.command = command
		self.cwd = abspath('')

	def data(self):
		process = Popen(self.command, stdout=PIPE, cwd=self.cwd, shell=isinstance(self.command, basestring))
		output = process.communicate()[0]
		process.wait()
		return output

def CoffeescriptFile(fname):
	return CommandFile(['coffee', '-c', '-p', abspath(fname)], fname.replace('.coffee', '.js'))

def LessFile(fname):
	return CommandFile(['lessc', abspath(fname)], fname.replace('.less', '.css'))
