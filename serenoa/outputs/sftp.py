import paramiko
import stat
from urlparse import urlparse
import os.path

# Digest format is compatibile with tinysync
DIGEST_NAME = '.tinysync_digest'

class SFTPBackend(object):
	uses_directories = True
	store_digest = True

	def __init__(self, path):
		self.uri = urlparse(path)

	def hash(self, node):
		return node.sha1()
		
	def connect(self):
		address = self.uri.hostname
		username = self.uri.username
		port = int(self.uri.port) if self.uri.port else 22

		agent = paramiko.Agent()
		keys = agent.get_keys()
		ssh_config = paramiko.SSHConfig() 
		try: 
			with open(os.path.join(os.path.expanduser('~'), '.ssh', 'config')) as f: 
				ssh_config.parse(f)
				config_lookup = ssh_config.lookup(address)
				if 'hostname' in config_lookup:
					address = config_lookup['hostname'] or address
				if 'user' in config_lookup:
					username = config_lookup['user'] or username
				if 'port' in config_lookup:
					port = config_lookup['port'] or port
		except:
			pass

		self.transport = paramiko.Transport((address, port))

		if len(keys) != 0:
			self.transport.connect()
			for key in keys:
				try:
					self.transport.auth_publickey(username, key)
				except:
					pass
				if self.transport.is_authenticated():
					break
		if not self.transport.is_authenticated():
			self.transport.auth_password(username, self.uri.password)
		self.sftp = paramiko.SFTPClient.from_transport(self.transport)
		
		print "Base is", self.uri.path
		try:
			self.sftp.mkdir(self.uri.path)
			print "Creating remote base directory"
		except Exception as e:
			pass
		self.sftp.chdir(self.uri.path)
		
	def done(self):
		self.sftp.close()
		self.transport.close()
		
	def get_digest(self):
		try:
			return parse_digest(self.sftp.open(DIGEST_NAME).read())
		except:
			return ''
			
	def put_digest(self, digest):
		self.put_file(DIGEST_NAME, make_digest(digest))
			
	def put_file(self, path, node):
		data = node if isinstance(node, str) else node.data()
		f = self.sftp.open(path, 'w')
		f.write(data)
		f.close()
		
	def mkdir(self, path):
		self.sftp.mkdir(path)
		
	def delete_dir(self, path):
		self.sftp.rmdir(path)
		
	def delete_file(self, path):
		self.sftp.unlink(path)

def make_digest(m):
	l=[]
	for path in m:
		l.append("%s  %s"%(m[path], path))
	return '\n'.join(l)

def parse_digest(c):
	r = {}
	for line in c.split('\n'):
		if not line: continue
		sha1, path =  line.split('  ')
		r[path] = sha1
	return r

