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
	
	
def ReadFile(image,UTC,FileNameFormat):
	if image[-5:] == 'fits' or image[-4:] == 'fit':
			with fits.open(image) as f:
				Image = f[0].data
				timestamp = f[0].header["DATE-OBS"]
	else:
		Image = cv2.imread(image)
		
		timestamp = image.split('/')[-1]
		timestamp = datetime.strptime(timestamp, FileNameFormat)
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
