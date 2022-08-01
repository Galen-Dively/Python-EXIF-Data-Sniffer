# --Features--
# Collect avaliable metadata from either directory or specific photo
# 
# --How to Use--
# path: direotry or specfic photo that will be scanned
# In a terminal, write "python3 metadata.py {path}"
# If everything goes well it should output all the metadata info

from PIL import Image
from PIL.ExifTags import TAGS

from termcolor import colored	

import sys
import os

import enum

class ScraperModes(enum.Enum):
		multiimage = 0
		singleimage = 1

class Scraper:
	def __init__(self, path):
		self.path = path
		self.mode = self.getMode()
		self.fileextentions = {".JPG": ".jpg", ".PNG": ".png"}

		if self.mode == ScraperModes.singleimage:
			self.image = self.path
		else:
			self.images = {}
			self.images = self.getFiles()


	def getMode(self):
		if os.path.isdir(self.path):
			return ScraperModes.multiimage
		else:
			return ScraperModes.singleimage

	def getFiles(self):
		# go through each file in directory and save it to dictionary
		images = {}
		otherfiles = {}
		for file in os.listdir(self.path):
			for upper, lower in self.fileextentions.items():
				if file.endswith(upper) or file.endswith(lower):
					try:
						imagepath = self.path+file
						image = Image.open(imagepath)
						images = images | {f"{file}": image}
					except:
						print(colored(f"Could not find file {file, self.path}", "red"))
				else:
					# otherfiles.append(f"{file}", f"{self.path}/{file}")
					pass
		return images

	def getExifData(self):
		for file, image in self.images.items():
			exifdata = image._getexif()
			print(colored(f"Metadata for {file}", "green"))
			for tag in exifdata:
				tags = TAGS.get(tag, tag)
				data = exifdata.get(tag)

				try:
					if isinstance(data, bytes):
						data = data.decode()
				except UnicodeDecodeError as e:
					data = data.decode()

				print(colored(f"{tags}: {data}", "cyan"))
			# except Exception as e:
			# 	print(colored(f"Could not get data from {file}", "red"), str(e))




def getPath(): 
	return sys.argv[1]

s = Scraper(getPath())
s.getExifData()
