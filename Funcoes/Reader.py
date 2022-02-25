from astropy.io import fits
import cv2

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
					dic[B[0]] = B[1]
				
			if linha == "":
				break
	return dic
	
	
def ReadFile(Directory,image):
	if image[-5:] == 'fits':
			with fits.open(Directory+image) as f:
				Image = f[0].data
				timestamp = f[0].header["DATE-OBS"]
	else:
		Image = cv2.imread(Directory+image)
		timestamp = image[0:-5]
	
	return Image,timestamp



