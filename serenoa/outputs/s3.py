import s3lib as S3
import json
import os, os.path, stat

CREDENTIAL_FILE = '~/.aws_credentials'

def credential_file():
	fname = os.path.expanduser(CREDENTIAL_FILE)
	try:
		st = os.stat(fname)
	except OSError:
		print "Key name used, but credential file {0} does not exist!".format(fname)
		return {}

	if st.st_mode & (stat.S_IRGRP | stat.S_IROTH):
		print "Warning: unsafe permissions on credential file. To fix, run:"
		print "\tchmod 600 {0}".format(fname)
	with open(fname, 'r') as f:
		data = json.load(f)
	return data

	
class S3Backend(object):
	uses_directories = False
	store_digest = False
	
	def __init__(self, key_name=None, key_id=None, secret=None, bucket='', prefix=''):
		if key_name:
			creds = credential_file()
			try:
				self.key_id = str(creds[key_name]['id'])
				self.secret = str(creds[key_name]['secret'])
			except KeyError:
				raise KeyError("Credentials not found for '{0}'".format(key_name))
		else:
			self.key_id = key_id
			self.secret = secret
		self.bucket = bucket
		self.prefix = prefix
		self.conn = None

	def connect(self):
		self.conn = S3.AWSAuthConnection(self.key_id, self.secret)
		if not self.conn.check_bucket_exists(self.bucket).status == 200:
			raise IOError('Bucket does not exist')

	def hash(self, node):
		return node.md5()
							
	def done(self):
		pass

	def get_digest(self):
		contents = {}
		res = self.conn.list_bucket(self.bucket) #TODO: prefix
		for i in res.entries:
			contents[i.key] = i.etag.replace('"', '')
		return contents
			
	def put_digest(self, digest):
		pass
			
	def put_file(self, path, node):
		data = node.data()
		headers = { 'x-amz-acl': 'public-read' , 'Content-Type': node.content_type}
		self.conn.put(self.bucket, path, S3.S3Object(data), headers)

	def delete_file(self, path):
		self.conn.delete(self.bucket, path)
		
	def mkdir(self, path):
		raise IOError("No directories on S3")
		
	def delete_dir(self, path):
		raise IOError("No directories on S3")