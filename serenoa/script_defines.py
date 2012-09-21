from serenoa.file import *
from serenoa.content_file import ContentFile
from serenoa.mustache_template import MustacheTemplate, runMustache, deferMustache
from serenoa.cmd_file import CommandFile, LessFile, CoffeescriptFile

import glob2
def glob(*patterns):
	base = abspath('', False) + '/'
	matches = []
	for pattern in patterns:
		matches += glob2.iglob(abspath(pattern, False))
	return (m.replace(base, '', 1) for m in matches)


class memoized(object):
  def __init__(self, function):
    self.function = function
    self.memoized = {}

  def __call__(self, *args):
    try:
      return self.memoized[args]
    except KeyError:
      self.memoized[args] = self.function(*args)
      return self.memoized[args]
