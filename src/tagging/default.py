import os


def getTag(f):
	return f'#t{os.path.basename(os.path.dirname(f))}'