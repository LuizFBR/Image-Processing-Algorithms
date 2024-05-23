import skimage as ski
import numpy as np
from math import ceil
from scipy.ndimage import rotate
import matplotlib.pyplot as plt

def build_histogram(image,path): # Construir o histograma de uma imagem monocromática.

    plt.title('Histograma de projeção')
    plt.xlabel("Níveis de Cinza")
    plt.ylabel("Frequencia de níveis de cinza")
    print(image)
    x = np.arange(image.shape[0])
    y = np.sum(image,axis=1)
    print(x.shape,y.shape)
    print(y)
    plt.bar(x,y,align='center') # A bar chart
    for i in range(len(y)):
        plt.hlines(y[i],0,x[i]) # Here you are drawing the horizontal lines
    plt.savefig(path+"_histograma_proj.png")

def sum_sqr_of_diff(image): # soma dos quadrados das diferenças dos valores em células adjacentes do perfil de projeção
    sums = np.sum(image,axis=1)
    sums_shift = np.roll(sums,-1)[:-1]
    op = sums[:-1] - sums_shift
    op = op**2
    return np.sum(op)

def amplitude(image): # amplitude do histograma de projeção
    return np.max(np.sum(image,axis=1))

def text_align(image,func_objetivo):

    test_range = np.arange(-45,46,1) # testa 90 valores
    max_obj, best_theta = 0,0
    for theta in test_range:
        rotated = rotate(image, theta)
        obj = func_objetivo(rotated)
        if max_obj < obj: # maximiza função objetivo - raciocínio: quanto menor a soma dos quadrados das diferenças, menores são as diferenças, logo os vizinhos ou tem níveis de cinza alto (apresentando existência de vários caracteres na linha) ou possuem níveis de cinza baixo (apresentando poucos ou nenhum caracteres na linha).
            max_obj = obj
            best_theta = theta
    return best_theta


if __name__ == '__main__':
    image_paths = ['neg_4','neg_28','partitura','pos_24','pos_41','sample1','sample2']
    for image_path in image_paths:
        image = ski.io.imread('input\\'+image_path+'.png')
        build_histogram(image,'input\\'+image_path)
        objective_functions = [sum_sqr_of_diff,amplitude,] # lista de funções objetivos
        for obj_function in objective_functions:
            theta = text_align(image,obj_function) # apply text align using obj_function as the objective function to be maximized

            rotated = rotate(image, theta)
            build_histogram(rotated,'output\\'+obj_function.__name__+'\\'+image_path)
            print(image_path)
            
            ski.io.imsave("output\\"+obj_function.__name__+'\\'+image_path+'_out.png',rotated)

