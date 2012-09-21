from serenoa.file import File
from markdown import Markdown
import re
import yaml

yaml_front_matter_re = re.compile(r'\A---\s+^(.+?)$\s+---\s*(.*)\Z', re.M | re.S)

class ContentFile(File):
	"""A file loader that reads a file with YAML front matter metadata and optionally, markdown.
       These files isn't necessarily supposed to be add()ed directly, but may be passed through
       a template first."""

	md=Markdown(['headerid', 'codehilite']) #headerid(level=2)

	def __init__(self, fname, **kwds):
		"""fname -- source filename (relative to context) 
		   keyword arguments are used as default metadata that can be overwritten by YAML front matter.
		   The `markdown` keyword can be used to enable/disable markdown."""
		super(ContentFile, self).__init__(fname)
		self.path = self.path.replace('.md', '.html')
		self.meta = kwds
		self.load()

	def load(self):
		"""Load the content and metadata."""
		data = super(ContentFile, self).data()
		match = yaml_front_matter_re.search(data)
		if match:
			frontmatter, content = match.groups()
			self.meta.update(yaml.safe_load(frontmatter.replace('\t', ' '*4)))
		else:
			print "No YAML front matter in {0}?".format(self.path)
			content = data
			self.meta = {}

		if self.meta.get('markdown', True):
			self.md.reset()
			self.content = self.md.convert(content)
		else:
			self.content = content

		if 'path' in self.meta:
			# allow the front matter to override path
			self.path = self.meta['path']

	def __getattr__(self, attr):
		"""Allow accessing metadata as properties."""
		try:
			return self.meta[attr]
		except:
			raise AttributeError(attr)

	def __hasattr__(self, attr):
		return attr in self.meta

	def data(self):
		return self.content
