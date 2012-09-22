import os.path

def sync(context, backend_type, dryrun = False, force_full=False, delete=False, **kwds):
	local = {}

	backend = backend_type(**kwds)

	for p, node in context.files.iteritems():
		local[p] = backend.hash(node)

		if backend.uses_directories:
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

	backend.connect()
	
	if force_full:
		remote = {}
	else:
		remote = backend.get_digest()
	
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
			backend.put_file(i, node)

	if added+updated+deleted and not (dryrun is True):
		if backend.store_digest:
			backend.put_digest(make_digest(local))
	backend.done()
	
	if dryrun == 'digest-only':
		print "UPDATING DIGEST: ",
	elif dryrun:
		print "DRY RUN: ",
	print "Synchronized %i files. (%i added; %i updated; %i deleted)" %(total, added, updated, deleted)
