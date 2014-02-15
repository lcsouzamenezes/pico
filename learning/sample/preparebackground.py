#
#
#

#
import os
import numpy
import Image
import struct
import argparse

#
parser = argparse.ArgumentParser()
parser.add_argument('src')
parser.add_argument('dst')
args = parser.parse_args()

#
def saveasrid(im, path):
	#
	h = im.shape[0]
	w = im.shape[1]

	#
	f = open(path, 'wb')

	#
	data = struct.pack('ii', w, h) 
	f.write(data)

	tmp = [None]*w*h
	for y in range(0, h):
		for x in range(0, w):
			tmp[y*w + x] = im[y, x]

	#
	data = struct.pack('%sB' % w*h, *tmp)
	f.write(data)

	#
	f.close()

#
srcfolder = args.src
dstfolder = args.dst

# create destination folder, if needed
if not os.path.exists(dstfolder):
   os.makedirs(dstfolder)

#
list = open(dstfolder + '/list.txt', 'w')

n = 0

for dirpath, dirnames, filenames in os.walk(srcfolder):
	for filename in filenames:
		#
		if not (filename.endswith('.jpg') or filename.endswith('.JPG') or filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.bmp')):
			continue

		#
		path = dirpath + '/' + filename

		#
		try:
			im = Image.open(path).convert('L')
		except:
			print 'CANNOT PROCESS ' + path
			continue

		#
		print path

		#
		im = numpy.asarray(im)

		name = ( 'img%05d' % n ) + '-' + filename + '.rid'
		saveasrid(im, dstfolder + '/' + name)

		list.write(name + '\n')
		list.flush()
		n = n+1

#
list.close()