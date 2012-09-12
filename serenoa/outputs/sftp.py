import paramiko
import stat
from urlparse import urlparse
import os.path

# Digest format is compatibile with tinysync
DIGEST_NAME = '.tinysync_digest'

class SFTPBackend(object):
	def __init__(self, uri):
		self.uri = urlparse(uri)
		print self.uri
		
	def connect(self):
		self.transport = paramiko.Transport(self.uri.hostname)
		agent = paramiko.Agent()
		keys = agent.get_keys()
		if len(keys) != 0:
			self.transport.connect()
			for key in keys:
				try:
					self.transport.auth_publickey(self.uri.username, key)
				except:
					pass
				if self.transport.is_authenticated():
					break
		if not self.transport.is_authenticated():
			self.transport.auth_password(self.uri.username, self.uri.password)
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
			return self.sftp.open(DIGEST_NAME).read()
		except:
			return ''
			
	def put_digest(self, digest):
		self.put_file(DIGEST_NAME, digest)
			
	def put_file(self, path, content):
		f = self.sftp.open(path, 'w')
		f.write(content)
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

def outputSFTPDir(context, path, dryrun = False, force_full=False, delete=False):
	local = {}

	for p, node in context.files.iteritems():
		local[p] = node.sha1()

		# Generate virtual directories
		p = os.path.dirname(p)
		while p:
			exists = local.get(p, '')
			if exists == 'dir':
				break
			elif exists:
				print path, "is both a file and a directory"
				raise ValueError()
			else:
				local[p] = 'dir'
			p = os.path.dirname(p)

	backend = SFTPBackend(path)
	backend.connect()
	
	if force_full:
		remote = {}
	else:
		remote = parse_digest(backend.get_digest())
	
	added = updated = deleted = total = 0
	
	for i in sorted(remote, reverse=True):
		if delete and i not in local:
			print "Deleting %s"%(i)
			deleted += 1
			
			if dryrun: continue
			
			if remote[i] == 'dir':
				backend.delete_dir(i)
			else:
				backend.delete_file(i)

	for i in sorted(local):
		total += 1
		if i not in remote:
			print "Adding   %s"%(i)
			added += 1
		elif local[i] != remote[i]:
			print "Updating %s"%(i)
			updated += 1
		else:
			continue

		if dryrun: continue

		if local[i] == 'dir':
			if i in remote and remote[i] != 'dir':
				backend.delete_file(i)
			backend.mkdir(i)
		else:
			if i in remote and remote[i] == 'dir':
				backend.delete_dir(i)
			node = context.files[i]
			backend.put_file(i, node.data())

	if added+updated+deleted and not (dryrun is True):
		backend.put_digest(make_digest(local))
	backend.done()
	
	if dryrun == 'digest-only':
		print "UPDATING DIGEST: ",
	elif dryrun:
		print "DRY RUN: ",
	print "Synchronized %i files. (%i added; %i updated; %i deleted)" %(total, added, updated, deleted)
	
