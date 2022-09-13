

def CircularMask(ficheiro,raio):
	#Recebe a diretoria do ficheiro, devolve imagem com mask aberta
	imagem=cv2.imread(ficheiro)
	height, width, layers = imagem.shape
	Centrox=height/2
	Centroy=width/2

	for y in range(0,height):
		for x in range(0,width):
			if math.sqrt((x-Centrox)**2 + (y-Centroy)**2) > raio:
				imagem[y][x]=[0,0,0]
	
	return imagem
	
def CircularMask2(imagem,raio,valor):
	#Recebe a diretoria do ficheiro, devolve imagem com mask aberta
	Shape = imagem.shape
	Centrox=Shape[1]/2
	Centroy=Shape[0]/2


	for y in range(0,Shape[0]):
		for x in range(0,Shape[1]):
			if math.sqrt((x-Centrox)**2 + (y-Centroy)**2) > raio:
				imagem[y][x]=valor
	
	return imagem
