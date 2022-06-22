import io
import logging
import os
from PIL import Image

def limitImgSize(img_filename: str, img_target_filename: str, target_filesize: int, tolerance: int=5):
	img = img_orig = Image.open(img_filename)
	aspect = img.size[0] / img.size[1]

	while True:
		with io.BytesIO() as buffer:
			ext = os.path.splitext(img_filename)[1].lower()
			img.save(buffer, format=("JPEG" if ext in [".jpg", ".jpeg"] else "PNG"))
			data = buffer.getvalue()
		filesize = len(data)	
		size_deviation = filesize / target_filesize
		logging.debug(f"Deviation {size_deviation}")

		if size_deviation <= (100 + tolerance) / 100:
			# filesize fits
			with open(img_target_filename, "wb") as f:
				f.write(data)
			break
		else:
			# filesize not good enough => adapt width and height
			# use sqrt of deviation since applied both in width and height
			new_width = img.size[0] / size_deviation**0.5	
			new_height = new_width / aspect

			logging.debug(f"{img.size} -> {(new_width, new_height)}")

			# resize from img_orig to not lose quality
			img = img_orig.resize((int(new_width), int(new_height)))