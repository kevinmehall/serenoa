import os
import hashlib
from mimetypes import guess_type

from serenoa.core import context

def abspath(fname):
	p = os.path.join(context().basepath, fname)
	if not os.path.exists(p):
		raise OSError("File not found: {0}".format(p))
	return p

class BaseFile(object):
	def __init__(self, fname=None):
		self.path = fname
		
	def data(self):
		return ''

	@property
	def deps(self):
		return []
	
	@property
	def content_type(self):
		n = guess_type(self.path)
		if not n:
			print("Error getting content-type for {0}".format(self.pathn))
			n = 'application/octet-stream'
		return n
		
	@property
	def mtime(self):
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

class File(BaseFile):
	def __init__(self, fname):
		super(File, self).__init__(fname)
		self.abspath = abspath(fname)

	def data(self):
		return open(self.abspath, 'rb').read()

	@property
	def deps(self):
		return [self.abspath]

	@property
	def mtime(self):
		try:
			return os.path.getmtime(self.abspath)
		except:
			print("Error getting mtime for {0}".format(self.path))

class VFile(BaseFile):
	def __init__(self, content_type, data):
		super(VFile, self).__init__(None)
		self._content_type = content_type
		self._data = data

	@property
	def content_type(self): return self._content_type

	def data(self): return self._data