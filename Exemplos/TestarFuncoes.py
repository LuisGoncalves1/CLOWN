from Funcoes.AnaliseImagem import AplicarMask , EncontrarEstrelas

Mask = '/home/luis/Desktop/Tudo/Imagens/MascaraNova.jpg' # Mascara
imagem = '/home/luis/Desktop/Tudo/Imagens/SemMask/Dia 3/ImagemA000.jpg' # Imagem

image = AplicarMask(imagem,Mask)

EncontrarEstrelas(image)
