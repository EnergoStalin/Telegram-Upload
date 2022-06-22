import os
import re


def keyfunc(x: str):
	rgx = r'[^\d]'
	bnwex = os.path.splitext(os.path.basename(x))[0]
	if(re.match(rgx, bnwex)):
		return 0
	return int(re.sub(rgx, '', bnwex))