def runOutput(context, backend, destspec):
	if backend is 'file':
		from serenoa.outputs.localfs import outputLocalDir
		return outputLocalDir(context, **destspec)
	elif backend is 'sftp':
		from serenoa.outputs.sftp import outputSFTPDir
		return outputSFTPDir(context, **destspec)

