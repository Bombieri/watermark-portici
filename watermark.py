#!/usr/local/bin/python3.6
#watermark versione 1.2.4

import os
from PIL import Image, ImageDraw, ImageFont, ImageFile, ExifTags
import glob
import time
import sys
from pathlib import Path

#functions

#le seguenti funzioni servono a compensare la rotazione delle immagini dovute all'inclinazione del cellulare
def _fix_image_rotation(image):
 orientation_to_rotation_map = {
     3: Image.ROTATE_180,
     6: Image.ROTATE_270,
     8: Image.ROTATE_90,
 }
 try:
     exif = _get_exif_from_image(image)
     orientation = _get_orientation_from_exif(exif)
     rotation = orientation_to_rotation_map.get(orientation)
     if rotation:
         image = image.transpose(rotation)

 # except Exception as e:
     # Would like to catch specific exceptions, but PIL library is poorly documented on Exceptions thrown
     # Log error here

 finally:
     return image


def _get_exif_from_image(image):
 exif = {}

 if hasattr(image, '_getexif'):  # only jpegs have _getexif
     exif_or_none = image._getexif()
     if exif_or_none is not None:
         exif = exif_or_none

 return exif


def _get_orientation_from_exif(exif):
 ORIENTATION_TAG = 'Orientation'
 orientation_iterator = (
     exif.get(tag_key) for tag_key, tag_value in ExifTags.TAGS.items()
     if tag_value == ORIENTATION_TAG
 )
 orientation = next(orientation_iterator, None)
 return orientation
 
 #main
__location__ = os.path.abspath(os.path.dirname(sys.argv[0]))	#così l'eseguibile funziona in qualsiasi directory
os.chdir(__location__)

if not os.path.exists('pool'):  #creo directory pool se non esiste
	os.makedirs('pool')

if not os.path.exists('watermarked'):  #creo directory watermarked
	os.makedirs('watermarked')
	
for file in glob.glob("./logo/*"):
	LOGO = file
perc_logo = 18
#perc_wtm = 25

text1 = "Associazione Scout Laica"
text2 = "Portici"
margin = 7
textwidth1 = 10000

color = 'white'

#apertura logo
logoIm = Image.open(LOGO)

#apertura/creazione file log.txt
log = open('log.txt', 'a')

#scrittura data e orario in log.txt
log.write(time.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S") + '\n' )

#ammetto troncamento immagini
ImageFile.LOAD_TRUNCATED_IMAGES = True

#richiesta di resize e qualità immagine
resized = False
answer = ''
while  not (answer == "y" or answer == "n"):
	answer = input("Si desidera riscalare le immagini ad una dimensione inferiore a 1024 pixel quadrati? (y/n)\n")
if (answer == "y"):
	need_resizing = True
else:
	need_resizing = False
qual = 74
while not (qual <=95 and qual >=75):
	qual = int(input("Selezionare la qualità immagine finale dell'immagine su una scala da 75 a 95. Il valore di default è 75: "))
log.write("Qualità immagini salvate: %d \n" % qual)

#ciclo su tutte le immagini ricorsivamente in ./pool
for Filename in glob.iglob('./pool/**', recursive=True):														
	if not (Filename.lower().endswith(".png") or Filename.lower().endswith(".jpg") or Filename.lower().endswith(".jpeg") or Filename.lower().endswith(".bmp")) or Filename == LOGO:
		continue
	im = Image.open(Filename)
	s = Filename.split("/")		#
	l = len(s)					#			
	filename = s[l-1]			#
	f, e = filename.split(".")	# isolo solo il nome file
	
	print("Processando %s..." % filename)
	log.write("Processando %s...\n" % filename)
	
	im = _fix_image_rotation(im)
	width, height = im.size
	
	#riscalo l'immagine
	if need_resizing:
		if (width <= 300 or height <= 300):
			MAX_SIZE = 300
		else:
			MAX_SIZE = 1024
		if (width > MAX_SIZE or height > MAX_SIZE):										
			print("Riscalando %s..." % filename)
			log.write("Riscalando %s...\n" % filename)
			if width > MAX_SIZE:
				height = int((MAX_SIZE / width) * height)
				width = MAX_SIZE
			if height > MAX_SIZE:
				width = int((MAX_SIZE / height) * width)
				height = MAX_SIZE
		
			im = im.resize((width, height))
			resized = True


	#aggiungo logo e watermark
	print("Aggiunta logo e watermark a %s..." % filename)
	log.write("Aggiunta logo e watermark a %s...\n" % filename)
	logo_dim = int((width * perc_logo) / 100)
	this_logoIm = logoIm.resize((logo_dim, logo_dim), Image.ANTIALIAS)
	logoWidth, logoHeight = this_logoIm.size
	im.paste(this_logoIm, (width - logoWidth - margin, height - logoHeight - margin), this_logoIm)
	draw = ImageDraw.Draw(im)
	
	i = int((3 * 12) * logoWidth / (18 * 18))
	font = ImageFont.truetype(os.path.join(__location__, 'font/Montserrat-Italic.ttf'), i)
	textwidth1, textheight1 = draw.textsize(text1, font)
	textwidth2, textheight2 = draw.textsize(text2, font)

	draw.text((width - textwidth1  - 3 * margin - logo_dim, height - textheight1 / 2 -  3 * margin - logo_dim / 2 + 8), text1, font=font, fill=color)
	draw.text((width - textwidth2 - textwidth1 / 3 - 3 * margin - logo_dim, height + textheight2 / 2 -  3 * margin - logo_dim / 2 + 8), text2, font=font, fill=color)

	#salvataggio in ./watermarked
	print("Salvando %s in ./watermarked..." % filename)
	log.write("Salvando %s in ./watermarked...\n" % filename)
	percorso = ""
	if l > 3:
		for j in range(2, l-1):
			percorso = os.path.join(percorso, s[j])
		print(percorso)
	try:
		os.makedirs(os.path.join("watermarked", percorso))
	except FileExistsError:
		pass
	if resized:
		im.save(os.path.join("watermarked", percorso, f + "_r" + "_w." + e), quality=qual)
	else:
		im.save(os.path.join("watermarked", percorso, f + "_w." + e), quality=qual)

	#cancellazione file originario
	os.remove(Filename)
	print("Rimuovo %s da ./pool..." % filename)
	log.write("Rimuovo %s da ./pool...\n" % filename)

log.write("\n")

