import os
import traceback

def context():
	""" Return the currently-executing Context, or None if a Context is not executing a script """
	return Context.current

import serenoa.script_defines
topvars = serenoa.script_defines.__dict__

class Context(object):
	"""A context manages the set of pages under a particular directory,
		generated from a source directory's script."""

	def __init__(self, basepath, vars=topvars):
		"""
		basepath -- the source, filesystem directory in which to look for the script.
		vars -- variable bindings to use when executing the script.
		        Only used for internal include() recursion
		"""

		self.basepath = basepath
		self.globals = vars.copy()
		
		for i in ['set', 'add', 'include', 'destination']:
			self.globals[i] = getattr(self, i)
		
		self.files = {}
		self.destinations = {}
		
	def path(self, path):
		"""Return an absolute path for the relative path, using this Context's basepath."""
		return os.path.abspath(os.path.join(self.basepath, path))
		
	def set(self, var, value):
		"""Set a variable binding for the rest of the script, and to be inherited by included scripts"""
		self.globals[var] = value
		
	def add(self, file, path=None):
		"""Add a BaseFile-derived object as a file in the output directory.
		   `path` is relative to the Context's output directory. If path is None, the
		   file's suggested path is used."""
		
		if path is None:
			path = file.path

		if path is None:
			print "Error:", file, "has no name. Ignoring this file."
			return

		file.path = path
		self.files[path] = file
		
	def include(self, path, bind):
		"""Include the tree based at `path` (filesystem path relative to basedir), run its script, and
		   bind its generated pages at `bind` (relative to the output directory) """
		c = Context(self.path(path), self.globals)
		c.run()
		for k, v in c.files.items():
			p = os.path.join(bind, k)
			self.files[p] = v
		 
	def run(self):
		"""Execute the script for this context."""
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

	def destination(self, name, backend, **kwds):
		self.destinations[name] = (backend, kwds)

		
	current = None