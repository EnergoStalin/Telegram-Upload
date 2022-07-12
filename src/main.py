import asyncio
import json
import logging
import os
from telethon import TelegramClient
from upload import *

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
					level=logging.WARNING)

async def main():
	with open(r'..\config.json') as f:
		CONFIG = json.load(f)
	async with TelegramClient('Telegram uploader', CONFIG['api_id'], CONFIG['api_hash']) as client:
		await client.connect()
		await client.start(CONFIG['phone'])

		await sendFileTreeAsync('.', client, ext=('.jpg', '.png'))
		

if __name__ == '__main__':
	loop = asyncio.new_event_loop()
	try:
		loop.run_until_complete(main())
	finally:
		loop.run_until_complete(loop.shutdown_asyncgens())
		loop.close()