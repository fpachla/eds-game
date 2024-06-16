import sys
import pygame
import random
import numpy as np
import pandas as pd

from libs.utils import *
from src.constants import *
from libs.manip_imgs import *

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.width, self.height = WIN_WIDHT, WIN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 36)
        self.font_parabens = pygame.font.Font(None, 45)
        self.running = True
        self.clock = pygame.time.Clock()
        self.current_screen = 'menu_inicial'  # Initial screen is 'login'
        self.player_name = 'Pachla'  # Variable to store the player's name
        self.fase_um_nivel = 3
        self.fase_um_concluido = False
        self.fase_dois_nivel = 1
        self.fase_dois_concluido = False
        self.parabens_text_height = 150  # Variável para controlar a altura do texto "Parabéns"
        self.proximity_threshold = 15  # Variável para controlar a proximidade necessária para encaixar
        self.parabens_bg_color = BLACK  # Variável para controlar a cor do retângulo de fundo
        self.times_df = pd.DataFrame(columns=['nome_da_fase', 'tempo'])  # DataFrame para armazenar os tempos das fases
        self.start_time = None  # Variável para armazenar o tempo de início da fase

        self.dict_tipo_da_fase = {
            1 : "Terrestre",
            2 : "Aquatico",
            3 : "Aereo"
        }


    def run(self):
        while self.running:
            if self.current_screen == 'login':
                self.tela_login()
            elif self.current_screen == 'menu_inicial':
                self.menu_inicial()
            elif self.current_screen == 'fase_um':
                self.fase_um_piramide()
            elif self.current_screen == 'fase_dois':
                self.fase_dois_alimente_o_bicho()


    def check_all_images_locked(self, locked_images, total_images):
        return len(locked_images) == total_images
    
    
    def tela_login(self) -> None:
        bg_image = pygame.image.load(rf'imgs\tela-login.jpg')
        bg_image = pygame.transform.scale(bg_image, (self.width, self.height))

        color = COLOR_INACTIVE
        active = True
        text = ''
        input_box_width = 300
        offset_x = 125  # Adjust this value to move elements to the right
        input_box = pygame.Rect((self.width - input_box_width) // 2 + offset_x, 215, input_box_width, 50)
        submit_button = pygame.Rect((self.width - 153) // 2 + offset_x, 315, 153, 45)

        while self.running and self.current_screen == 'login':
            self.screen.blit(bg_image, (0, 0))
            for event in pygame.event.get():
                self.try_exit(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Se o usuário clicar na caixa de entrada
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = COLOR_ACTIVE if active else COLOR_INACTIVE
                    # Se o usuário clicar no botão de continuar
                    if submit_button.collidepoint(event.pos):
                        self.player_name = text
                        print(f'nome coletado: {self.player_name}')
                        self.current_screen = 'menu_inicial'
                        print("Mudando de tela")
                elif event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.draw_text(self.screen, "Olá, seja bem vindo(a):", self.font, WHITE, ((self.width - self.font.size("Olá, seja bem vindo(a):")[0]) // 2 + offset_x, 75))
            self.draw_text(self.screen, "Digite seu nome:", self.font, WHITE, ((self.width - self.font.size("Digite seu nome:")[0]) // 2 + offset_x, 125))
            
            pygame.draw.rect(self.screen, color, input_box, 3)
            
            txt_surface = self.font.render(text, True, color)
            self.screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            
            input_box.w = max(300, txt_surface.get_width()+10)
            input_box.x = (self.width - input_box.w) // 2 + offset_x  # Ensure the input box stays centered

            pygame.draw.rect(self.screen, GRAY, submit_button)
            self.draw_text(self.screen, "Continuar", self.font, BLACK, (submit_button.x + 15, submit_button.y + 10))

            pygame.display.flip()
            self.clock.tick(30)


    def menu_inicial(self) -> None:
        bg_image = pygame.image.load(rf'imgs\menu-inicial.jpg')
        bg_image = pygame.transform.scale(bg_image, (self.width, self.height))

        quadrado_fase_1_coords = ((17, 239), (345, 426))  
        quadrado_fase_2_coords = ((404, 240), (732, 424))
        

        while self.running and self.current_screen == 'menu_inicial':
            self.screen.blit(bg_image, (0, 0))
            for event in pygame.event.get():
                self.try_exit(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    print(mouse_pos)
                    if (quadrado_fase_1_coords[0][0] <= mouse_pos[0] <= quadrado_fase_1_coords[1][0] and
                        quadrado_fase_1_coords[0][1] <= mouse_pos[1] <= quadrado_fase_1_coords[1][1]):
                        self.current_screen = 'fase_um'
                        
                    elif (quadrado_fase_2_coords[0][0] <= mouse_pos[0] <= quadrado_fase_2_coords[1][0] and
                        quadrado_fase_2_coords[0][1] <= mouse_pos[1] <= quadrado_fase_2_coords[1][1]):
                        self.current_screen = 'fase_dois'

            welcome_message = f"Muito bem vindo(a), {self.player_name}!"
            text_width, text_height = self.font.size(welcome_message)
            text_x = (self.width - text_width) // 2
            text_y = 20

            # Desenhar retângulo escuro semitransparente atrás do texto "Muito bem vindo(a)"
            rect_surface = pygame.Surface((text_width + 20, text_height + 10))
            rect_surface.set_alpha(128)  # Define a transparência
            rect_surface.fill((0, 0, 0))  # Preenche com cor preta
            self.screen.blit(rect_surface, (text_x - 10, text_y - 5))  # Desenha o retângulo

            self.draw_text(self.screen, welcome_message, self.font, WHITE, (text_x, text_y))

            # Usar a função desenha_texto para desenhar "não concluído" acima do quadrado_fase_1
            desenha_texto(self.screen, self.font, quadrado_fase_1_coords, self.fase_um_concluido, self.fase_um_nivel)
            desenha_texto(self.screen, self.font, quadrado_fase_2_coords, self.fase_dois_concluido, self.fase_dois_nivel)

            pygame.display.flip()
            self.clock.tick(30)

            
            
    def fase_um_piramide(self):
        if self.fase_um_nivel == 1:
            img_paths = {
                'topo': rf'imgs\leao.png',
                'meio-um': rf'imgs\zebra.png',
                'meio-dois': rf'imgs\cervo.png',
                'base-um': rf'imgs\galho.png',
                'base-dois': rf'imgs\maca.png',
                'base-tres': rf'imgs\grama.png',
            }
        elif self.fase_um_nivel == 2:
            img_paths = {
                'topo': rf'imgs\tubarao.png',
                'meio-um': rf'imgs\polvo.png',
                'meio-dois': rf'imgs\pinguim.png',
                'base-um': rf'imgs\algas.png',
                'base-dois': rf'imgs\cavalo-marinho.png',
                'base-tres': rf'imgs\camarao.png',
            }
        elif self.fase_um_nivel == 3:
            img_paths = {
                'topo': rf'imgs\aguia.png',
                'meio-um': rf'imgs\cobra.png',
                'meio-dois': rf'imgs\coelho.png',
                'base-um': rf'imgs\besouro.png',
                'base-dois': rf'imgs\borboleta.png',
                'base-tres': rf'imgs\grilo.png',
            }

        # Configurações do botão de voltar ao menu
        sair_esquerdo_top_left = (602, 20)  # Coordenadas do canto superior esquerdo
        sair_esquerdo_bottom_right = (736, 64)  # Coordenadas do canto inferior direito
        
        linked_images = retorna_imagens_linkadas_para_nivel(img_paths)

        bg_image = pygame.image.load(rf'imgs\\background-fase-um.jpg')
        bg_image = pygame.transform.scale(bg_image, (self.width, self.height))

        # Carregar e redimensionar a imagem do cronômetro
        timer_image = pygame.image.load(rf'imgs\cronometro.png')
        timer_image = pygame.transform.scale(timer_image, (30, 30))

        dragging = False
        dragged_pair = None
        offset_x = 0
        offset_y = 0
        locked_images = set()
        original_positions = {key: normal_pos[:] for key, (_, _, _, normal_pos) in linked_images.items()}  # Guardar posições originais

        reset_button = pygame.Rect(self.width // 2 - 75, self.height // 2 + 50, 150, 50)

        self.start_time = pygame.time.get_ticks()  # Inicializar o cronômetro
        cronometro_parado = False  # Variável para controlar se o cronômetro foi parado

        while self.running and self.current_screen == 'fase_um':
            self.screen.blit(bg_image, (0, 0))

            for event in pygame.event.get():
                self.try_exit(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if (sair_esquerdo_top_left[0] <= mouse_pos[0] <= sair_esquerdo_bottom_right[0] and
                        sair_esquerdo_top_left[1] <= mouse_pos[1] <= sair_esquerdo_bottom_right[1]):
                        self.current_screen = 'menu_inicial'
                        

                    if self.check_all_images_locked(locked_images, len(img_paths)):
                        if reset_button.collidepoint(mouse_pos):
                            if self.fase_um_nivel == 3:
                                print(self.times_df)  # Imprimir o DataFrame quando todas as fases forem concluídas
                                self.current_screen = 'menu_inicial'
                                self.fase_um_nivel = 1
                                self.fase_um_concluido = True
                                return
                            else:
                                self.fase_um_nivel += 1
                                print(f"Nível atual: {self.fase_um_nivel}")
                                self.fase_um_piramide()
                                return
                    else:
                        if dragging:
                            # Soltar a imagem
                            shadow_image, shadow_pos, normal_image, normal_pos = linked_images[dragged_pair]
                            if ((normal_pos[0] - shadow_pos[0]) ** 2 + (normal_pos[1] - shadow_pos[1]) ** 2) ** 0.5 < self.proximity_threshold:
                                linked_images[dragged_pair][3] = shadow_pos
                                locked_images.add(dragged_pair)
                            dragging = False
                            dragged_pair = None
                        else:
                            # Restaurar posições originais se um novo animal for clicado e o arrasto anterior não estava correto
                            for key in linked_images:
                                if key not in locked_images:
                                    linked_images[key][3] = original_positions[key][:]
                            
                            # Iniciar arrasto
                            for key, (shadow_image, shadow_pos, normal_image, normal_pos) in linked_images.items():
                                if key in locked_images:
                                    continue
                                if normal_pos[0] <= mouse_pos[0] <= normal_pos[0] + 50 and normal_pos[1] <= mouse_pos[1] + 50:
                                    dragging = True
                                    dragged_pair = key
                                    offset_x = normal_pos[0] - mouse_pos[0]
                                    offset_y = normal_pos[1] - mouse_pos[1]
                                    break

                elif event.type == pygame.MOUSEMOTION and dragging:
                    mouse_pos = event.pos
                    linked_images[dragged_pair][3][0] = mouse_pos[0] + offset_x
                    linked_images[dragged_pair][3][1] = mouse_pos[1] + offset_y

                    # Verificar se o objeto está próximo da sombra enquanto é arrastado
                    shadow_image, shadow_pos, normal_image, normal_pos = linked_images[dragged_pair]
                    if ((normal_pos[0] - shadow_pos[0]) ** 2 + (normal_pos[1] - shadow_pos[1]) ** 2) ** 0.5 < self.proximity_threshold:
                        linked_images[dragged_pair][3] = shadow_pos
                        locked_images.add(dragged_pair)
                        dragging = False
                        dragged_pair = None

            for shadow_image, shadow_pos, normal_image, normal_pos in linked_images.values():
                self.screen.blit(shadow_image, shadow_pos)
                self.screen.blit(normal_image, normal_pos)

            if self.check_all_images_locked(locked_images, len(img_paths)):
                if not cronometro_parado:
                    end_time = pygame.time.get_ticks()  # Tempo de término
                    elapsed_time = (end_time - self.start_time) / 1000  # Tempo decorrido em segundos
                    new_row = pd.DataFrame({'nome_da_fase': [f'Jogo 1 - nível {self.dict_tipo_da_fase[self.fase_um_nivel]}'], 'tempo': [elapsed_time]})
                    self.times_df = pd.concat([self.times_df, new_row], ignore_index=True)
                    cronometro_parado = True  # Parar o cronômetro
                    
                reset_button = mostrar_parabens(self.screen, self.font_parabens, WIN_WIDHT, WIN_HEIGHT, n_fase=self.fase_um_nivel, resto_do_texto=rf" Tempo utilizado: {elapsed_time:.0f} segundos")

            # Desenhar a imagem do cronômetro no canto superior esquerdo
            self.screen.blit(timer_image, (10, 10))

            # Atualizar e desenhar o tempo decorrido, se o cronômetro não foi parado
            if not cronometro_parado:
                current_time = pygame.time.get_ticks()
                elapsed_time = (current_time - self.start_time) / 1000  # Tempo decorrido em segundos
                timer_text = self.font.render(f"{elapsed_time:.0f} segundos", True, (255, 255, 255))
                self.screen.blit(timer_text, (50, 15))  # Ajustar a posição do texto do cronômetro

            
            
            pygame.display.flip()
            self.clock.tick(30)
        
        
    def fase_dois_alimente_o_bicho(self) -> None:
        bg_image = pygame.image.load(rf'imgs\background-fase-um.jpg')
        bg_image = pygame.transform.scale(bg_image, (self.width, self.height))

        while self.running and self.current_screen == 'fase_dois':
            print("aaa")
            self.screen.blit(bg_image, (0, 0))
            for event in pygame.event.get():
                self.try_exit(event)
     
     
    def try_exit(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            pygame.quit()
            sys.exit()


    def draw_text(self, surface, text, font, color, pos):
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)


if __name__ == "__main__":
    g = Game()
    g.run()  # Call the run method to start the game
