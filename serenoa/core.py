import os
import traceback

def context():
	return Context.current

import serenoa.script_defines
topvars = serenoa.script_defines.__dict__

class Context(object):
	def __init__(self, basepath, vars=topvars):
		self.basepath = basepath
		self.globals = vars.copy()
		
		for i in ['set', 'add', 'include']:
			self.globals[i] = getattr(self, i)
		
		self.files = {}
		
	def path(self, path):
		return os.path.abspath(os.path.join(self.basepath, path))
		
	def set(self, var, value):
		self.globals[var] = value
		
	def add(self, file, path=None):
		if path is None:
			path = file.path
		self.files[path] = file
		
	def include(self, path, bind):
		c = Context(self.path(path), self.globals)
		c.run()
		for k, v in c.files.items():
			p = os.path.join(bind, k)
			self.files[p] = v
		 
	def run(self):
		prev_context = Context.current
		Context.current = self
		
		self.files = {}
		
		try:
			scriptname = os.path.join(self.basepath, '.site')
			exec(
				compile(open(scriptname).read(), scriptname, 'exec'),
				self.globals,
				{}
			)

		except Exception as e:
			print("Error processing", self.basepath)
			traceback.print_exc()
		
		Context.current = prev_context
		
	current = None