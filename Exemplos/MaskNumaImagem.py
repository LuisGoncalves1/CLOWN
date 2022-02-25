import AnaliseImagem as AI
import matplotlib.pyplot as plt
import cv2
import numpy as np

Mask = '/home/luis/Desktop/Tudo/Imagens/MascaraNova.jpg' # Mascara
Imagem = '/home/luis/Desktop/Tudo/Imagens/SemMask/Dia 3/ImagemA000.jpg' # Imagem

A = AI.AplicarMask(Imagem,Mask)

plt.imshow(A)
plt.show()

