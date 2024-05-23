import skimage as ski
import numpy as np
import binascii
import copy
from math import ceil
import matplotlib.pyplot as plt

def passa_baixa(img_path,Do): # Do é a frequência de corte
    image = ski.io.imread(img_path) # (i) abrir uma imagem de entrada convertida para escala de cinza;
    transform = np.fft.fft2(image)  # (ii) aplicar a transformada rapida de Fourier;
    # ski.io.imsave('baboon_transform.png',transform)
    centralized = np.fft.fftshift(transform)      # (iii) centralizar o espectro de frequência
    # ski.io.imsave('baboon_centralized.png',centralized)

    shape = image.shape
    mask = np.ones(shape)
    grid = np.array(np.meshgrid(np.arange(-np.trunc(shape[0]/2),np.ceil(shape[0]/2)),np.arange(-np.trunc(shape[1]/2),np.ceil(shape[1]/2)))).T.reshape(-1,2)
    grid_mask = np.apply_along_axis(np.linalg.norm, axis=1, arr=grid).reshape(shape)
    mask[grid_mask > Do] = 0
    # mask = np.fft.ifft2(mask)
    filtered_image = np.fft.ifft2(np.multiply(centralized,mask)).real
    filtered_image = (filtered_image * 255).astype(np.uint8)
    print(filtered_image)
    return filtered_image

def passa_alta(img_path,Do): # Do é a frequência de corte
    image = ski.io.imread(img_path) # (i) abrir uma imagem de entrada convertida para escala de cinza;
    transform = np.fft.fft2(image)  # (ii) aplicar a transformada rapida de Fourier;
    # ski.io.imsave('baboon_transform.png',transform)
    centralized = np.fft.fftshift(transform)      # (iii) centralizar o espectro de frequência
    # ski.io.imsave('baboon_centralized.png',centralized)

    shape = image.shape
    mask = np.ones(shape)
    grid = np.array(np.meshgrid(np.arange(-np.trunc(shape[0]/2),np.ceil(shape[0]/2)),np.arange(-np.trunc(shape[1]/2),np.ceil(shape[1]/2)))).T.reshape(-1,2)
    grid_mask = np.apply_along_axis(np.linalg.norm, axis=1, arr=grid).reshape(shape)
    mask[mask < Do] = 0
    # mask = np.fft.ifft2(mask)
    filtered_image = np.fft.ifft2(np.multiply(centralized,mask)).real
    filtered_image = (filtered_image * 255).astype(np.uint8)
    print(filtered_image)
    return filtered_image


filtered_image = passa_baixa('baboon.png',5000000000000000000000000)
ski.io.imsave('baboon_passa_baixa.png',filtered_image)

filtered_image = passa_alta('baboon.png',1000000000000000000000000000000000)
ski.io.imsave('baboon_passa_alta.png',filtered_image)

filtered_image = passa_alta('butterfly.png',10)
ski.io.imsave('butterfly_passa_alta.png',filtered_image)

def test():
    image = ski.io.imread('butterfly.png') # (i) abrir uma imagem de entrada convertida para escala de cinza;
    transform = np.fft.fft2(image)  # (ii) aplicar a transformada rapida de Fourier;
    real = np.fft.ifft2(transform).real
    ski.io.imsave('butterfly_transform.png',(real * 255).astype(np.uint8))
    centralized = np.fft.fftshift(transform)
    real = np.fft.ifft2(centralized).real
    ski.io.imsave('butterfly_centralized.png',(real * 255).astype(np.uint8))
    real = np.fft.ifft2(centralized).real
    return (real * 255).astype(np.uint8)

test()