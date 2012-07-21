import pystache
from serenoa.file import BaseFile, abspath

class MustacheTemplate(object):
	def __init__(self, template, view=lambda x: x, content_type='text/html'):
		self.template = abspath(template)
		self.view = view
		self.content_type = content_type

	def __call__(self, obj, *args, **kwds):
		return MustachePage(self, obj, *args, **kwds)

class MustachePage(BaseFile):
	def __init__(self, tpl, obj, *args, **kwds):
		super(MustachePage, self).__init__()
		self.tpl = tpl
		self.obj = obj
		self.args = args
		self.kwds = kwds
		self._data = None

		if isinstance(obj, BaseFile):
			self.path = obj.path

	@property
	def deps(self):
		d = [self.tpl.template]
		if isinstance(obj, BaseFile):
			d += [self.tpl.template]
		return d

	@property
	def content_type(self):
		return self.tpl.content_type

	def load(self):
		tp = open(self.tpl.template).read()
		self._data = pystache.render(tp, self.tpl.view(self.obj), *self.args, **self.kwds)

	def data(self):
		if not self._data:
			self.load()
		return self._data

	# Passthrough other attr access to wrapped object (for e.g. ContentFile)
	def __getattr__(self, attr):
		return getattr(self.obj, attr)

	def __hasattr__(self, attr):
		return hasattr(self.obj, attr)