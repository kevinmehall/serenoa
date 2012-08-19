from serenoa.file import *
from serenoa.content_file import ContentFile
from serenoa.mustache_template import MustacheTemplate

import glob2
def glob(pattern):
	return glob2.iglob(abspath(pattern, False))
