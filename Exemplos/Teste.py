from math import sqrt
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray
import cv2
from ..Funcoes.AnaliseImagem import AplicarMask
import requests
import matplotlib.pyplot as plt

Mask = '/home/luis/Desktop/Tudo/Imagens/MascaraNova.jpg' # Mascara
imagem = '/home/luis/Desktop/Tudo/Imagens/SemMask/Dia 3/ImagemA000.jpg' # Imagem

































#################
# ~ blobs_log = blob_log(image_gray, max_sigma=3, num_sigma=10, threshold=.03,exclude_border=True)

# ~ # Compute radii in the 3rd column.
# ~ blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
# ~ print(blobs_log)

# ~ blobs_dog = blob_dog(image_gray, max_sigma=30, threshold=.1)
# ~ blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)

# ~ blobs_doh = blob_doh(image_gray, max_sigma=30, threshold=.01)

# ~ blobs_list = [blobs_log, blobs_dog, blobs_doh]
# ~ colors = ['yellow', 'lime', 'red']
# ~ titles = ['Laplacian of Gaussian', 'Difference of Gaussian',
          # ~ 'Determinant of Hessian']
# ~ sequence = zip(blobs_list, colors, titles)

# ~ fig, axes = plt.subplots(1, 3, figsize=(9, 3), sharex=True, sharey=True)
# ~ ax = axes.ravel()

# ~ for idx, (blobs, color, title) in enumerate(sequence):
    # ~ ax[idx].set_title(title)
    # ~ ax[idx].imshow(image)
    # ~ for blob in blobs:
        # ~ print(blob)
        # ~ y, x, r = blob
        # ~ c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
        # ~ ax[idx].add_patch(c)
    # ~ ax[idx].set_axis_off()

# ~ plt.tight_layout()
# ~ plt.show()


# ~ sites = ['http://www.gtc.iac.es/multimedia/netcam/camaraAllSky.jpg','http://200.131.64.207/allsky/imagens340/AllSkyCurrentImage.JPG']
# ~ Pastas = ['/home/luis/Desktop/Tudo/Imagens/SemMask/Dia 4/Site 1','/home/luis/Desktop/Tudo/Imagens/SemMask/Dia 4/Site 2']
# ~ r = requests.get(sites[1])
# ~ print(r.content)
