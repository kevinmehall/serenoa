import os
import hashlib
import mimetypes

from serenoa.core import context

def abspath(fname, check=True):
	"""Get the absolute path for fname relative to the base directory of the current context.
	   Also checks to make sure the file exists. """
	p = context().path(fname)
	if check and not os.path.exists(p):
		raise OSError("File not found: {0}".format(p))
	return p

def guess_type(name):
	"""Content-type in MIME format used to serve this URL"""
	n, encoding = mimetypes.guess_type(name)
	if not n:
		print("Error getting content-type for {0}".format(name))
		n = 'application/octet-stream'
	return n

class BaseFile(object):
	"""Abstract base class for a node that is accessed by a particular HTTP URL"""

	def __init__(self, suggestedpath=None):
		"""Derived classes can suggest a path (relative to the current context base)
		that is to be used if not overridden by Add()"""

		# strip the basepath from absolute paths
		if suggestedpath:
			basepath = context().basepath
			if suggestedpath[0] == '/' and suggestedpath.startswith(basepath):
					suggestedpath = suggestedpath[len(basepath):].lstrip('/')

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
		return guess_type(self.path)
	def mtime(self):
		"""The URL's modification date, if available"""
		return 0
	
	def sha1(self):
		"""SHA1 hash of the data() content"""
		if not hasattr(self, '_sha1'):
			h = hashlib.new('sha1')
			h.update(self.data())
			self._sha1 = h.hexdigest()
		return self._sha1
		
	def md5(self):
		"""MD5 hash of the data() content"""
		if not hasattr(self, '_md5'):
			h = hashlib.new('md5')
			h.update(self.data())
			self._md5 = h.hexdigest()
		return self._md5

class File(BaseFile):
	def __init__(self, fname):
		super(File, self).__init__(fname)
		self._content_type = guess_type(fname)
		self.abspath = abspath(fname)

	def data(self):
		return open(self.abspath, 'rb').read()

	@property
	def content_type(self):
		return self._content_type

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