from serenoa.outputs.sync import sync

def runOutput(context, backend, destspec):
	if backend is 'file':
		from serenoa.outputs.localfs import outputLocalDir
		return outputLocalDir(context, **destspec)
	elif backend is 'sftp':
		from serenoa.outputs.sftp import SFTPBackend
		return sync(context, SFTPBackend, **destspec)
	elif backend is 's3':
		from serenoa.outputs.s3 import S3Backend
		return sync(context, S3Backend, **destspec)
