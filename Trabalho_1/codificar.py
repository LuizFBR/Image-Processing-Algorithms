import skimage as ski
import numpy as np
import binascii
import copy
from math import ceil


def decode(image,mask):
    message = np.take(image,mask)
    least_bits = message & 1
    mess = "".join([str(i) for i in least_bits]).encode()
    mess = int(mess,base=2)
    ascii_text = binascii.unhexlify('%x' % mess)

    return ascii_text

def steganography(img_path,msg):
    image = ski.io.imread(img_path)
    message = ''.join(format(ord(i), '08b') for i in msg) # converte msg em binário
    message = [int(i) for i in message]
    # while len(message) %3 != 0: # adiciona zeros à direita até que se tenha um número divísivel por 3 de números binários.
    #     message = message.append(0)

    message = np.array(message)
    message_bits = message.size

    image_shape = image.shape
    image_pixels = image_shape[0]*image_shape[1]

    mask = np.random.choice(image_pixels*3,message_bits,replace=False)
    img_cpy = copy.deepcopy(image)
    np.put(img_cpy, mask, message)

    # np.put(image, mask, (image & ~1) | img_cpy)

    return (image & ~1) | img_cpy,mask


message = "Nao existe apenas uma forma de pensar. Se voce nao eh a favor de algo, voce nao precisa ser contra. Nao se posicionar contra algo nao te faz menos ou mais, mas sim te faz uma pessoa plural e que possui outras qualidades e preocupacoes."
message = message.strip()
image,mask = steganography('baboon.png',message)
print(decode(image,mask))





#------//------------------//---------------//------------------//---------------------//-----------------//-------------#




def aux(message,image_pixels):
    # calcula capacidade de informação utilizando-se n bit menos significativos de cada banda de cada pixel
    capacity_with_n_least_significant_bits = lambda n, image_pixels : image_pixels*3*2**(n-1) # para n>0
    message_bits = message.size
    print(f"message_bits: {message_bits}")

    i = 1
    while True: # calcula quantos bits significativos são necessários para codificar a mensagem (a saída é a variável i)
        cap = capacity_with_n_least_significant_bits(1,image_pixels)

        # compara a capacidade com a quantidade de bits necessários para codificar a mensagem
        if message_bits <= cap:
            break
        i += 1