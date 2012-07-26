import os
import hashlib
from mimetypes import guess_type

from serenoa.core import context

def abspath(fname):
	"""Get the absolute path for fname relative to the base directory of the current context.
	   Also checks to make sure the file exists. """
	p = context().path(fname)
	if not os.path.exists(p):
		raise OSError("File not found: {0}".format(p))
	return p

class BaseFile(object):
	"""Abstract base class for a node that is accessed by a particular HTTP URL"""

	def __init__(self, suggestedpath=None):
		"""Derived classes can suggest a path (relative to the current context base)
		that is to be used if not overridden by Add()"""
		self.path = suggestedpath
		
	def data(self):
		"""The content for the URL."""
		return ''

	@property
	def deps(self):
		"""List of absolute pathnames for files on which this URL depends"""
		return []
	
	@property
	def content_type(self):
		"""Content-type in MIME format used to serve this URL"""
		n = guess_type(self.path)
		if not n:
			print("Error getting content-type for {0}".format(self.pathn))
			n = 'application/octet-stream'
		return n
		
	@property
	def mtime(self):
		"""The URL's modification date, if available"""
		return 0
	
	@property
	def sha1(self):
		"""SHA1 hash of the data() content"""
		if not self._sha1:
			h = hashlib.new('sha1')
			h.update(self.data())
			self._sha1 = h.hexdigest()
		return self._sha1
		
	@property
	def md5(self):
		"""MD5 hash of the data() content"""
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