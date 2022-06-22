import asyncio
import logging
from sorting.default import *
import os
from prepfs.default import *
from telethon import TelegramClient, errors
from alive_progress import alive_bar
from iterutils import pieces

async def sendAlbum(client: 'TelegramClient', caption: 'str', fl: 'list[str]', to: 'str' = 'me'):
	'''
		Sends album with caption before it
	'''
	if(to[0] in ('-', '+')):
		to = int(to)
	while True:
		try:
			await client.send_message(to, caption)
			await client.send_file(to, fl)
			break
		except errors.FloodWaitError as e:
			logging.warning(f"{e}")
			await asyncio.sleep(e.time)

async def sendFilesWithBarAsync(client: 'TelegramClient', tag: 'str', fl: 'list[str]', to: 'str' = 'me'):
	'''
		Send files in bulk by 10 files at once
		Bar updates onle when one bulk is compleated
	'''
	kwargs = {
		'ctrl_c': False,
		'title': f'Uploading {len(fl)} files with tag {tag}'
	}
	with alive_bar(len(fl), **kwargs) as bar:
		for (_ , e), portion in pieces(fl, 10):
			await sendAlbum(client, tag, portion, to=to)
			bar(e)

async def sendFileWithBarAsync(client: 'TelegramClient', caption: 'str', f: 'str', to: 'str' = 'me'):
	kwargs = {
		'ctrl_c': False,
		'title': f'Uploading {f}'
	}
	if(to[0] in ('-', '+')):
		to = int(to)
	with alive_bar(os.path.getsize(f), **kwargs) as bar:
		await client.send_file(to, f, caption=caption, progress_callback=lambda c, t: bar(c))

async def sendFileTreeAsync(root: 'str', client: 'TelegramClient', keyfunc: 'None' = keyfunc, ext: 'iter[str]' = None, to: 'str' = 'me'):
	uploads = await prepareSortedFileTreeAsync(root, keyfunc, extensions=ext)
	for k, v in uploads.items():
		await sendFilesWithBarAsync(client, k, v, to=to)