import hashlib

# --
# --
# --
def featuresFromContainer(container):
	return flattenContainer(
		container,inclroot=False
	).keys()

def updateContainer(root,keychain,newval,auto_expand=True):
	if(isinstance(keychain,str)):
		keychain = keychain.split('/')
	if(len(keychain)==0):
		return newval
	else:
		firstkey = keychain[0]
		root_is_tuple = None
		if(auto_expand):
			if(root is None):
				if(firstkey.isdigit()):
					firstkey = int(firstkey)
					root = [None,] * (firstkey+1)
					root_is_tuple = False
				else:
					root = {}
					root[firstkey] = None
			elif(isinstance(root,(tuple))):
				firstkey = int(firstkey)
				root = list(root) + [None,] * (firstkey-len(root)+1)
				root_is_tuple = True
			elif(isinstance(root,(list,tuple))):
				firstkey = int(firstkey)
				root = list(root) + [None,] * (firstkey-len(root)+1)
				root_is_tuple = False
			elif(isinstance(root,dict) and firstkey not in root):
				root[firstkey] = None
		else:
			if(isinstance(root,(tuple))):
				firstkey = int(firstkey)
				root = list(root)
				root_is_tuple = True
		root[firstkey] = updateContainer(root[firstkey],keychain[1:],newval,auto_expand)
		if(root_is_tuple):
			return tuple(root)
		else:
			return root

def flattenContainer(container,keychain=None,result=None,inclroot=True):
	if(keychain is None): keychain = []
	if(result is None): result = {}
	if(isinstance(container,dict)):
		if(len(container)==0):
			result['/'.join(keychain)] = container
		else:
			for k,v in container.items():
				flattenContainer(v,keychain+[k],result)
	elif(isinstance(container,list)):
		if(len(container)==0):
			result['/'.join(keychain)] = container
		else:
			for ii,v in enumerate(container):
				flattenContainer(v,keychain+[str(ii)],result)
	elif(isinstance(container,tuple)):
		if(len(container)==0):
			result['/'.join(keychain)] = container
		else:
			for ii,v in enumerate(container):
				flattenContainer(v,keychain+[str(ii)],result)
	else:
		# it is not a container, it is actual value
		result['/'.join(keychain)] = container
	if(inclroot and len(keychain)==0):
		result['/'] = type(container)()
	return result

def constructContainer(flatdict,auto_expand=True):
	result = flatdict['/']
	for k,v in flatdict.items():
		if(k=='/'): continue
		updateContainer(result,k,v,auto_expand=True)
	return result

def projectContainer(surface,flatdict,auto_expand=True):
	for k,v in flatdict.items():
		updateContainer(surface,k,v,auto_expand=True)
	return surface

def containerChecksum(dictionary):
	dictionary = flattenContainer(dictionary)
	md5sum = hashlib.md5()
	for pair in sorted(dictionary.items()):
		md5sum.update(str(pair).encode('utf-8'))
	checksum = md5sum.hexdigest()
	return checksum

def extractValue(container,*,keychain=None,path=None):
	if(path is not None): keychain = path.split('/')
	if(len(keychain)==0):
		return container
	firstkey = keychain[0]
	keychain = keychain[1:]
	if(isinstance(container,dict)):
		container = container[firstkey]
	else:
		container = container[int(firstkey)]
	return extractValue(container,keychain=keychain)

