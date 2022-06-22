import os
from itertools import chain


def getFiles(root: 'str', ext: 'iter[str]' = None) -> 'iter[str]':
	'''
		Get files from sub directories optionally filter by extension
	'''
	files = chain(*[[os.path.join(p, f) for f in fl] for p, _, fl in os.walk(root)])
	if(ext == None):
		return files
	return filter(
		lambda x: os.path.splitext(x)[1].lower() in ext,
		files
	)

def getImages(root: 'str') -> 'iter[str]':
	return getFiles(root, ('.png', '.jpg', '.jpeg'))