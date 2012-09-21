import pystache
from serenoa.file import BaseFile, abspath, context

def runMustache(tplname, *args, **kwds):
	if context(): tplname = abspath(tplname)
	tp = open(tplname).read()
	return pystache.render(tp, *args, **kwds)

def deferMustache(*args, **kwds):
	return lambda: runMustache(*args, **kwds)


class MustacheTemplate(object):
	"""Callable that wraps a Mustache template"""

	def __init__(self, template, view=lambda x: x, content_type='text/html'):
		"""
		template -- Mustache template file, relative to Context's basedir
		view     -- View function. This callable is passed the page object, and its
		            return value is used by the template. Default is identity function.
		content_type -- content-type for output pages. Default 'text/html'.
		"""
		self.template = abspath(template)
		self.view = view
		self.content_type = content_type

	def __call__(self, obj, *args, **kwds):
		"""Create a MustachePage using this template. Pass a page to be templated.
		   Additional args and keywords are passed to the template."""
		return MustachePage(self, obj, *args, **kwds)

class MustachePage(BaseFile):
	"""A templated page"""
	
	def __init__(self, tpl, obj, *args, **kwds):
		"""Private constructor. Call a MustacheTemplate to create a MustachePage"""
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
		self._data = runMustache(self.tpl.template,
			                     self.tpl.view(self.obj), *self.args, **self.kwds)

	def data(self):
		if not self._data:
			self.load()
		return self._data

	def __getattr__(self, attr):
		"""Passthrough other attr access to wrapped object (for e.g. ContentFile)"""
		return getattr(self.obj, attr)

	def __hasattr__(self, attr):
		return hasattr(self.obj, attr)