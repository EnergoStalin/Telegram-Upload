from itertools import repeat
import logging
import multiprocessing
import os
import re
from turtle import pos
import humanize
from limitsize import limitImgSize

def _reducePostfix(f: str, postfix: str) -> str:
	sp = os.path.split(f)
	return sp[0] + re.sub(f"(?:{postfix})+", postfix, sp[1])

def _insertPostfix(f: str, postfix: str) -> str:
	a = os.path.splitext(f)
	f"{a[0]}{postfix}{a[1]}"

def _getCompressedName(f: str):
	postfix = "-compressed"

	_reducePostfix(f, postfix)

	return _insertPostfix(f, postfix)

def _worker(f: str, size: int, error: int):
	nf = _getCompressedName(f)
	logging.debug(f"Compressing '{f}' {humanize.naturalsize(os.path.getsize(f))}")
	limitImgSize(
		f,
		nf,
		size,
		error
	)
	logging.debug(f"{humanize.naturalsize(os.path.getsize(f))} '{f}' Compressed -> '{nf}' {humanize.naturalsize(os.path.getsize(nf))}")
	logging.debug(f"Removing '{f}'")
	os.remove(f)

def compress(files: 'list[str]', concurrency: int = 4, max_size: int = 9.9e+6, error: int = 0):
	with multiprocessing.Pool(concurrency) as p:
		p.starmap(_worker, zip(files, repeat(max_size), repeat(error)))