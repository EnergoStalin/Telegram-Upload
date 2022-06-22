import fsutil
from tagging.default import getTag
from sorting.default import keyfunc

async def prepareSortedFileTreeAsync(root: str, keyfunc: 'None', extensions: 'iter[str]' = None) -> dict[str, list[str]]:
	tree = dict()
	for f in fsutil.getFiles(root, extensions):
		tree.setdefault(getTag(f), []).append(f)
	for k, v in tree.items():
		tree[k] = sorted(v, key=keyfunc)
	return tree