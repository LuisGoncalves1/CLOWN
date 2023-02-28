from astropy.io import fits
import cv2
from datetime import datetime, timedelta
import numpy as np


def ReadConfig(config):
	dic = {}
	with open(config,'r') as texto:
		while True:
			linha = texto.readline()
			if len(linha)!= 0 and linha[0] != '#' and linha[0]!= '\n':
				B = linha.strip().split()
				try:
					dic[B[0]] = float(B[1])
				except:
					if B[1] == 'False':
						dic[B[0]] = False
					elif B[1] == 'True':
						dic[B[0]] = True
					else:						
						dic[B[0]] = B[1]
				
			if linha == "":
				break
	return dic
	
	
def ReadFile(Directory,image,UTC):
	if image[-5:] == 'fits':
			with fits.open(Directory+image) as f:
				Image = f[0].data
				timestamp = f[0].header["DATE-OBS"]
	else:
		Image = cv2.imread(Directory+image)
		# ~ timestamp = image[0:-5]
		
		timestamp = image[1:20]
		timestamp = list(timestamp)
		timestamp[13] = ':'
		timestamp[16] = ':'
		timestamp = "".join(timestamp)
		
		date_format_str = '%Y-%m-%dT%H:%M:%S'
		timestamp = datetime.strptime(timestamp, date_format_str)
		timestamp = timestamp - timedelta(hours=UTC)
		
	return Image,timestamp


def ReadCoordinates(File):
	A = []
	B = []
	with open(File,'r') as texto:
		while True:
			linha = texto.readline()
			if len(linha)!= 0 and linha[0] != '#' and linha[0]!= '\n':
				C = linha.strip().split(',')
				A.append(float(C[0]))
				B.append(float(C[1]))
				
			if linha == "":
				break
			
	return np.array(A),np.array(B)
