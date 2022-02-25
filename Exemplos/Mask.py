import os
import AnaliseImagem
import cv2

PastaInicial = '/home/luis/Desktop/Tudo/Imagens/SemMask' # Onde tao as pastas
PastaFinal = '/home/luis/Desktop/Tudo/Imagens/ComMask'
Mask = '/home/luis/Desktop/Tudo/Imagens/Mascara.jpg' # Mascara



###################################################################### 
Pastas = os.listdir(PastaInicial) #Lista de Pastas
Pastas.sort()
for Pasta in Pastas:
	Diretoria_Pasta_Inicial = PastaInicial + '/' + Pasta
	Diretoria_Pasta_Final = PastaFinal+'/'+Pasta
	
	if not os.path.exists(Diretoria_Pasta_Final):            # Cria Pasta Para Guardar Informaçao
		os.makedirs(Diretoria_Pasta_Final)
	
	ficheiros = os.listdir(Diretoria_Pasta_Inicial)
	ficheiros.sort()
	for ficheiro in ficheiros:
		imagem = Funcoes.AplicarMask(Diretoria_Pasta_Inicial+'/'+ficheiro,Mask)
		cv2.imwrite(Diretoria_Pasta_Final + '/' + ficheiro,imagem)

