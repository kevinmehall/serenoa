import os
import hashlib
from mimetypes import guess_type

class File(object):
	def __init__(self, fname):
		self.path = fname
		self.abspath = os.path.join(Context.current.basepath, fname)
		
	def data(self):
		return open(self.abspath, 'rb').read()
	
	@property
	def deps(self):
		return [self.abspath]
	
	@property
	def content_type(self):
		n = guess_type(self.path)
		if not n:
			print("Error getting content-type")
			n = 'application/octet-stream'
		return n
		
	@property
	def mtime(self):
		try:
			return os.path.getmtime(self.abspath)
		except:
			print("Error getting mtime")
			return 0
		
	@property
	def sha1(self):
		if not self._sha1:
			h = hashlib.new('sha1')
			h.update(self.data())
			self._sha1 = h.hexdigest()
		return self._sha1
		
	@property
	def md5(self):
		if not self._md5:
			h = hashlib.new('md5')
			h.update(self.data())
			self._md5 = h.hexdigest()
		return self._md5


topvars = {
	'File': File,
}

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
			print(e)
		
		Context.current = prev_context
		
	current = None