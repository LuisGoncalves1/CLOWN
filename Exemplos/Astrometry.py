import AnaliseImagem
import os


# ~ PastaInicial = '/home/luis/Desktop/Tudo/Imagens/ComMask' # Onde tao as pastas
# ~ PastaFinal = '/home/luis/Desktop/Tudo/Imagens/Astrometry' # Onde se vai guardar

# ~ Pastas = os.listdir(PastaInicial)
# ~ Pastas.sort()
# ~ for Pasta in Pastas:
	# ~ Diretoria_Pasta_Inicial = PastaInicial + '/' + Pasta
	# ~ Diretoria_Pasta_Final = PastaFinal+ '/' +Pasta
	
	# ~ if not os.path.exists(Diretoria_Pasta_Final):            # Cria Pasta Para Guardar Informaçao
		# ~ os.makedirs(Diretoria_Pasta_Final)
			
	# ~ ficheiros = os.listdir(Diretoria_Pasta_Inicial)
	# ~ ficheiros.sort()
	# ~ for ficheiro in ficheiros:
		# ~ Resultado=Funcoes.AnalisarImagem(Diretoria_Pasta_Inicial+'/'+ficheiro)
		# ~ with open (Diretoria_Pasta_Final + '/' + ficheiro,'wb') as escrever:
				# ~ escrever.write(Resultado)
	
	
PastaInicial = '/home/luis/Desktop/Tudo/Imagens/ComMask/Dia 3'
PastaFinal = '/home/luis/Desktop/Tudo/Imagens/Astrometry/Dia 3' # Onde se vai guardar

if not os.path.exists(PastaFinal):            # Cria Pasta Para Guardar Informaçao
	os.makedirs(PastaFinal)
ficheiros = os.listdir(PastaInicial)
ficheiros.sort()
for ficheiro in ficheiros:
	Resultado=Funcoes.AnalisarImagem(PastaInicial+'/'+ficheiro)
	with open (PastaFinal + '/' + ficheiro,'wb') as escrever:
			escrever.write(Resultado)
