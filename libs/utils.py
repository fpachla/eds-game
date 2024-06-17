import os
import pygame
import pandas as pd 
from datetime import datetime
from typing import Dict, Tuple


def concat_dicts(*args) -> Dict:
    """
    Concatena múltiplos dicionários em um único dicionário.
    
    Args:
        *args: Dicionários a serem concatenados.
    
    Returns:
        Um dicionário resultante da concatenação de todos os dicionários fornecidos.
    """
    result = {}
    for dictionary in args:
        if isinstance(dictionary, dict):
            result.update(dictionary)
        else:
            raise ValueError("Todos os argumentos devem ser dicionários.")
    return result


def mostrar_parabens(screen, font, screen_width, screen_height, n_fase, resto_do_texto):
    # Variáveis de configuração
    parabens_text_y = 175  # Altura do texto "Parabéns"
    button_y_position = screen_height // 2  # Altura do botão na tela
    button_bg_color = (0, 200, 0)  # Cor do botão de reset (um verde claro)
    bg_color_rect_parabens = (0, 0, 0)  # Cor de fundo do retângulo do "Parabéns"
    padding_horizontal = 100  # Padding horizontal
    padding_vertical = 20  # Padding vertical
    arrow_image_path = rf'imgs\right-arrow.png'  # Caminho para a imagem da seta

    # Desenhar o texto "Parabéns"
    text = rf"Parabéns! {resto_do_texto}"
    draw_text_with_background(screen, text, font, (255, 255, 255), bg_color_rect_parabens, (screen_width // 2, parabens_text_y), screen_width)
    
    # Medir o tamanho do texto do botão
    if n_fase != 3:
        button_text = "Ir para próxima fase"
    else:
        button_text = "Voltar para o menu"
        
    text_surface = font.render(button_text, True, (255, 255, 255))
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    
    button_width = text_width + padding_horizontal + 30  # Adiciona padding horizontal e espaço para a seta
    button_height = text_height + padding_vertical  # Adiciona padding vertical
    
    reset_button = pygame.Rect(screen_width // 2 - button_width // 2, button_y_position, button_width, button_height)
    corner_radius = 20  # Variável para controlar o quão arredondado o botão deve ser
    
    pygame.draw.rect(screen, button_bg_color, reset_button, border_radius=corner_radius)
    draw_text(screen, button_text, font, (255, 255, 255), (reset_button.centerx - 15, reset_button.centery))
    
    # Carregar, redimensionar e desenhar a imagem da seta
    try:
        arrow_image = pygame.image.load(arrow_image_path)
    except pygame.error:
        print(f"Falha ao carregar a imagem: {arrow_image_path}")
        return
    
    arrow_image = pygame.transform.scale(arrow_image, (30, 30))  # Redimensionar a seta
    arrow_rect = arrow_image.get_rect(center=(reset_button.right - 45, reset_button.centery))
    screen.blit(arrow_image, arrow_rect.topleft)
    
    return reset_button


def draw_text_with_background(surface, text, font, text_color, bg_color, pos, screen_width):
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=pos)
    bg_rect = pygame.Rect(0, text_rect.top - 5, screen_width, text_rect.height + 10)  # Background rect spanning the screen width
    pygame.draw.rect(surface, bg_color, bg_rect)
    surface.blit(text_surface, text_rect.topleft)
    return text_rect


def draw_text(surface, text, font, color, pos):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, text_rect.topleft)


def desenha_texto(screen, font, coords, concluido: bool, fase_atual: int):
    """
    Desenha um texto com fundo semitransparente na tela.

    Args:
        screen: A superfície onde o texto será desenhado.
        font: A fonte do texto.
        coords (tuple): Coordenadas ((top_left_x, top_left_y), (bottom_right_x, bottom_right_y)).
        texto (str): O texto a ser desenhado.
    """
    texto = "Fases concluídas" if concluido else f"Fase atual: {fase_atual} de 3"
    rgb_concluido = (0, 255, 00) if concluido else (255, 0, 0) 
    
    
    padding_horizontal = 130
    
    top_left, bottom_right = coords
    text_width, text_height = font.size(texto)
    text_x = (top_left[0] + bottom_right[0] - text_width) // 2
    text_y = top_left[1] - text_height - 10

    # Desenhar retângulo escuro semitransparente atrás do texto
    rect_surface = pygame.Surface((text_width + padding_horizontal, text_height + 10))
    rect_surface.set_alpha(192)  # Define a transparência
    rect_surface.fill(rgb_concluido)  # Preenche com cor preta
    screen.blit(rect_surface, (text_x - padding_horizontal // 2, text_y - 5))  # Desenha o retângulo

    # Desenhar o texto
    text_surface = font.render(texto, True, (255, 255, 255))  # Branco
    screen.blit(text_surface, (text_x, text_y))


def other_draw_text_with_background(surface, text, font, text_color, bg_color, pos, screen_width=None, is_middle=False):
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(topleft=pos)
    
    if is_middle and screen_width:
        text_rect.x = (screen_width - text_rect.width) // 2
    
    bg_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10)  # Ajuste o padding conforme necessário
    bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
    bg_surface.set_alpha(128)  # Define a transparência
    bg_surface.fill(bg_color)  # Preenche com a cor de fundo
    surface.blit(bg_surface, bg_rect.topleft)
    surface.blit(text_surface, text_rect.topleft)


def calcular_media_coluna_df(df: pd.DataFrame, col_name: str) -> float:
    if df[col_name].empty:
        return 0
    return df[col_name].mean()


def salvar_data_frames(
    df_tentativas: pd.DataFrame,
    df_tempos: pd.DataFrame,
    player_name: str,
    caminho_pasta_turma: str,
    data:str = datetime.now().strftime("%Y.%m.%d")
    ) -> None:
    
    if not os.path.exists(os.path.join(caminho_pasta_turma, data)):
        os.makedirs(os.path.join(caminho_pasta_turma, data))
    
    nome_arquivo = os.path.join(caminho_pasta_turma, data, rf'{player_name}.xlsx')
    
    with pd.ExcelWriter(nome_arquivo) as writer:
        df_tentativas.to_excel(writer, sheet_name='Pirâmide', index=False)
        df_tempos.to_excel(writer, sheet_name='Alimente o bicho', index=False)