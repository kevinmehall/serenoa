import os, errno, shutil

def mkdir(path):
	try:
		os.makedirs(path)
	except OSError as exc:
		if exc.errno != errno.EEXIST:
			raise

def outputLocalDir(context, basedir):
	if os.path.exists(basedir):
		if raw_input("{0} exists. Remove it y/(n)? ".format(basedir)) == 'y':
			shutil.rmtree(basedir)

	for fname, fobj in context.files.items():
		path = os.path.join(basedir, fname)
		mkdir(os.path.dirname(path))
		with open(path, 'wb') as f:
			f.write(fobj.data())
