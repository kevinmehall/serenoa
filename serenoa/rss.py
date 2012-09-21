from serenoa.file import BaseFile
import pystache

class RSSFeed(BaseFile):
	"""A virtual file that generates a RSS feed containing specified items.
	   Items should have the following properties:
		   title
		   link
		   content
		   date
		   author
	"""

	def __init__(self, title, baseurl, description, language, items):
		super(RSSFeed, self).__init__('rss.xml')
		self.title = title
		self.baseurl = baseurl
		self.description = description
		self.language = language
		self.items = items

	@property
	def content_type(self): return 'text/xml'

	def data(self):
		return pystache.render(RSSTEMPLATE, self)

RSSTEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xml:base="{{baseurl}}"  xmlns:dc="http://purl.org/dc/elements/1.1/">
	<channel>
	<title>{{title}}</title>
	<link>{{baseurl}}</link>
	<description>{{description}}</description>
	<language>{{language}}</language>

	{{#items}}
	<item>
		<title>{{title}}</title>
		<link>{{baseurl}}/{{path}}</link>
		<description>{{content}}</description>
		<pubDate>{{date}}</pubDate>
		<dc:creator>{{author}}</dc:creator>
		<guid isPermaLink="true">{{baseurl}}/{{path}}</guid>
	</item>
	{{/items}}

	</channel>
</rss>
"""