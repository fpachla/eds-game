import pygame
import random
from src.constants import *
from typing import Dict, List

def place_dark_image(img_path: str, coodernadas: List[int] = None, img_size: int = 65) -> Dict:
    """
    Pega uma imagem e deixa ela inteiramente preta.
    Serve para fazer as imagens que servirão de encaixe para a sua imagem original
    
    Args:
        img_path (str): Caminho (relativo) da imagem 
        img_size (int): Tamanho em pixels da imagem
    
    Returns:
        dict: Dicionário contendo a imagem preta e suas coordenadas.
    """
    IMG_SIZE = img_size
    image = pygame.image.load(img_path)
    image = pygame.transform.scale(image, (IMG_SIZE, IMG_SIZE))
    image = image.convert_alpha()
    arr = pygame.surfarray.pixels3d(image)
    alpha_arr = pygame.surfarray.pixels_alpha(image)
    arr[:] = BLACK  # Preencher a imagem inteira com preto
    del arr
    pygame.surfarray.pixels_alpha(image)[:] = alpha_arr
    del alpha_arr
    
    return {'image': image, 'coodernadas': coodernadas}


def place_image(img_path: str, coodernadas: List[int] = None, img_size: int = 65) -> Dict:
    """
    Carrega uma imagem e retorna um dicionário com a imagem e suas coordenadas.
    
    Args:
        img_path (str): Caminho (relativo) da imagem 
        img_size (int): Tamanho em pixels da imagem
    
    Returns:
        dict: Dicionário contendo a imagem e suas coordenadas.
    """
    IMG_SIZE = img_size
    image = pygame.image.load(img_path)
    image = pygame.transform.scale(image, (IMG_SIZE, IMG_SIZE))
    image = image.convert_alpha()
    
    return {'image': image, 'coodernadas': coodernadas}

def retorna_imagens_linkadas_para_nivel(img_paths: Dict[str, str]) -> Dict[str, List]:
    """
    Cria uma lista linkada de sombras e imagens normais para um nível específico.

    Args:
        img_paths (Dict[str, str]): Dicionário com os nomes das imagens.

    Returns:
        Dict[str, List]: Dicionário linkado de sombras e imagens normais.
    """
    coordenadas_piramide = {
        'topo': [171, 134], 
        'meio-um': [120, 239],
        'meio-dois': [219, 239],
        'base-um': [78, 357],
        'base-dois': [172, 357],
        'base-tres': [269, 357],
    }
    
    # Verificar se todas as chaves de img_paths estão presentes em coordenadas_piramide
    if not all(key in coordenadas_piramide for key in img_paths.keys()):
        raise KeyError("Uma ou mais chaves em img_paths não estão presentes em coordenadas_piramide.")
    
    # Coordenadas aleatórias
    coordenadas_aleatorias = [[611, 313], [611, 206], [611, 115], [463, 309], [463, 202], [463, 111]]
    
    # Criar sombras com as coordenadas fornecidas
    sombras = {key: place_dark_image(img_path=img_paths[key], coodernadas=coordenadas_piramide[key]) for key in img_paths.keys()}
    
    # Embaralhar as coordenadas para garantir a aleatoriedade
    random.shuffle(coordenadas_aleatorias)
    
    # Atribuir coordenadas embaralhadas às imagens normais
    imagens_normais = {key: place_image(img_path=img_paths[key], coodernadas=coordenadas_aleatorias[i]) for i, key in enumerate(img_paths.keys())}
    
    # Dicionário para manter as sombras e imagens normais linkadas
    linked_images = {
        key: [sombras[key]['image'], sombras[key]['coodernadas'], imagens_normais[key]['image'], imagens_normais[key]['coodernadas']]
        for key in sombras.keys()
    }
    
    return linked_images
