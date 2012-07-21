from serenoa.file import File
from markdown import Markdown
import re
import yaml

yaml_front_matter_re = re.compile(r'\A---\s+^(.+?)$\s+---\s*(.*)\Z', re.M | re.S)

class ContentFile(File):
	md=Markdown(['headerid', 'codehilite']) #headerid(level=2)

	def __init__(self, fname, markdown=True):
		super(ContentFile, self).__init__(fname)
		self.path = self.path.replace('.md', '.html')
		self.markdown = markdown
		self.meta = {}
		self.load()

	def load(self):
		data = super(ContentFile, self).data()
		match = yaml_front_matter_re.search(data)
		if match:
			frontmatter, content = match.groups()
			self.meta = yaml.load(frontmatter)
		else:
			print "No YAML front matter in {0}?".format(self.fname)
			content = data
			self.meta = {}

		if self.meta.get('markdown', self.markdown):
			self.md.reset()
			self.content = self.md.convert(content)
		else:
			self.content = content

	def __getattr__(self, attr):
		try:
			return self.meta[attr]
		except:
			raise AttributeError(attr)

	def __hasattr__(self, attr):
		return attr in self.meta

	def data(self):
		return self.content
