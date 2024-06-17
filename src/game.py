import sys
import pygame
import random
import numpy as np
import pandas as pd

from libs.utils import *
from src.constants import *
from libs.manip_imgs import *
from libs.manip_videos import *

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.width, self.height = WIN_WIDHT, WIN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 36)
        self.font_parabens = pygame.font.Font(None, 45)
        self.running = True
        self.clock = pygame.time.Clock()
        self.current_screen = 'fase_dois'
        self.player_name = 'Pachla'
        self.fase_um_nivel = 1
        self.fase_um_concluido = False
        self.fase_dois_nivel = 1
        self.caminho_pasta_turma = rf"C:\Users\{USER}\Documents\Pasta compartilhas - Turma"
        self.fase_dois_concluido = False
        self.parabens_text_height = 150  # Variável para controlar a altura do texto "Parabéns"
        self.proximity_threshold = 15  # Variável para controlar a proximidade necessária para encaixar
        self.parabens_bg_color = BLACK  # Variável para controlar a cor do retângulo de fundo
        self.tentando_entrar_na_fase = None
        self.times_df = pd.DataFrame(columns=['nome_da_fase', 'tempo'])  # DataFrame para armazenar os tempos das fases
        self.tentativas_df = pd.DataFrame(columns=['nome_da_fase', 'tentativas'])  # DataFrame para o número de tentativas das fases
        self.start_time = None  # Variável para armazenar o tempo de início da fase
        self.video_link = "https://youtu.be/dyIHYKt0dMU"

        
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
            elif self.current_screen == 'video_explicativo':
                self.video_explicativo()
    
    
    def video_explicativo(self):
        bg_image = pygame.image.load(r'imgs/background-video-explicativo.jpg')
        bg_image = pygame.transform.scale(bg_image, (self.width, self.height))
        
        quadrado_sim = ((258, 358), (356, 416))  
        quadrado_nao = ((391, 360), (485, 418))
        
        while self.running and self.current_screen == 'video_explicativo':
            for event in pygame.event.get():
                self.try_exit(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # print(mouse_pos)
                    
                    if (quadrado_sim[0][0] <= mouse_pos[0] <= quadrado_sim[1][0] and
                        quadrado_sim[0][1] <= mouse_pos[1] <= quadrado_sim[1][1]):
                        video_explicativo(self.video_link)
                        self.current_screen = self.tentando_entrar_na_fase
                                
                    elif (quadrado_nao[0][0] <= mouse_pos[0] <= quadrado_nao[1][0] and
                        quadrado_nao[0][1] <= mouse_pos[1] <= quadrado_nao[1][1]):
                            self.current_screen = self.tentando_entrar_na_fase
            
            self.screen.blit(bg_image, (0, 0))
            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(30)


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
                        # print(f'nome coletado: {self.player_name}')
                        self.current_screen = 'menu_inicial'
                        # print("Mudando de tela")
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
                    # print(mouse_pos)
                    if (quadrado_fase_1_coords[0][0] <= mouse_pos[0] <= quadrado_fase_1_coords[1][0] and
                        quadrado_fase_1_coords[0][1] <= mouse_pos[1] <= quadrado_fase_1_coords[1][1]):
                        self.current_screen = 'video_explicativo'
                        self.tentando_entrar_na_fase = 'fase_um'
                        
                    elif (quadrado_fase_2_coords[0][0] <= mouse_pos[0] <= quadrado_fase_2_coords[1][0] and
                        quadrado_fase_2_coords[0][1] <= mouse_pos[1] <= quadrado_fase_2_coords[1][1]):
                        self.current_screen = 'video_explicativo'
                        self.tentando_entrar_na_fase = 'fase_dois'

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

            # Desenha: Escolha uma fase
            other_draw_text_with_background(self.screen, "Escolha um jogo", self.font, WHITE, BLACK, (17, 75), WIN_WIDHT, True)
            
            
            # Médias das fases
            media_fase_um = calcular_media_coluna_df(self.times_df, 'tempo')
            media_fase_dois = calcular_media_coluna_df(self.tentativas_df, 'tentativas')
            
            other_draw_text_with_background(self.screen, rf"Média: {media_fase_um:.0f} segundos", self.font, WHITE, BLACK, (70, 165))
            other_draw_text_with_background(self.screen, rf"Média: {media_fase_dois:.0f} tentativas", self.font, WHITE, BLACK, (455, 165))
            

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
        tempo_pausado = 0
        pausado = False

        while self.running and self.current_screen == 'fase_um':
            self.screen.blit(bg_image, (0, 0))

            for event in pygame.event.get():
                self.try_exit(event)

                if event.type == pygame.ACTIVEEVENT:
                    if event.gain == 0:  # Jogo perdeu o foco
                        pausado = True
                        tempo_pausado = pygame.time.get_ticks()
                    elif event.gain == 1 and pausado:  # Jogo ganhou o foco
                        pausado = False
                        self.start_time += pygame.time.get_ticks() - tempo_pausado

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if (sair_esquerdo_top_left[0] <= mouse_pos[0] <= sair_esquerdo_bottom_right[0] and
                        sair_esquerdo_top_left[1] <= mouse_pos[1] <= sair_esquerdo_bottom_right[1]):
                        self.current_screen = 'menu_inicial'
                        

                    if self.check_all_images_locked(locked_images, len(img_paths)):
                        if reset_button.collidepoint(mouse_pos):
                            if self.fase_um_nivel == 3:
                                self.current_screen = 'menu_inicial'
                                self.fase_um_nivel = 1
                                self.fase_um_concluido = True
                                return
                            else:
                                self.fase_um_nivel += 1
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
        bg_image = pygame.image.load(rf'imgs/background-fase-dois.jpg')
        bg_image = pygame.transform.scale(bg_image, (self.width, self.height))
        
        dict_coordenadas = {
            'animal-principal': (325, 93),
            'caixa-um': (96, 322),
            'caixa-dois': (337, 322),
            'caixa-tres': (568, 322)
        }
        
        dict_fases = {
            1 : {
                'animal-principal' : 'imgs/tubarao.png',
                'escolha-correta' : 'imgs/peixe.png',
                'caixa-errada-um' : 'imgs/grilo.png',
                'caixa-errada-dois' : 'imgs/grama.png',
            },
            2 : {
                'animal-principal' : 'imgs/leao.png',
                'escolha-correta' : 'imgs/cervo.png',
                'caixa-errada-um' : 'imgs/galho.png',
                'caixa-errada-dois' : 'imgs/borboleta.png',
            },
            3 : {
                'animal-principal' : 'imgs/aguia.png',
                'escolha-correta' : 'imgs/coelho.png',
                'caixa-errada-um' : 'imgs/camarao.png',
                'caixa-errada-dois' : 'imgs/pinguim.png',
            }
        }
        
        fase_atual = dict_fases[self.fase_dois_nivel]
        nome_animal_principal = fase_atual['animal-principal'].split("/")[-1].split(".")[0].upper()
        
        animal_principal_image = pygame.image.load(fase_atual['animal-principal'])
        animal_principal_image = pygame.transform.scale(animal_principal_image, (100, 100))
        
        escolha_correta_image = pygame.image.load(fase_atual['escolha-correta'])
        escolha_correta_image = pygame.transform.scale(escolha_correta_image, (80, 80))
        
        caixa_errada_um_image = pygame.image.load(fase_atual['caixa-errada-um'])
        caixa_errada_um_image = pygame.transform.scale(caixa_errada_um_image, (80, 80))
        
        caixa_errada_dois_image = pygame.image.load(fase_atual['caixa-errada-dois'])
        caixa_errada_dois_image = pygame.transform.scale(caixa_errada_dois_image, (80, 80))
        
        reset_button = pygame.Rect(self.width // 2 - 75, self.height // 2 + 50, 150, 50)
        
        # Configurações do botão de voltar ao menu
        sair_esquerdo_top_left = (592, 14)  # Coordenadas do canto superior esquerdo
        sair_esquerdo_bottom_right = (736, 56)  # Coordenadas do canto inferior direito
        
        escolha_clicada = False
        tentativa = 1  # Contador de tentativas

        # Coordenadas disponíveis para as opções
        coordenadas_opcoes = [
            dict_coordenadas['caixa-um'],
            dict_coordenadas['caixa-dois'],
            dict_coordenadas['caixa-tres']
        ]
        
        random.shuffle(coordenadas_opcoes)
        
        while self.running and self.current_screen == 'fase_dois':
            self.screen.blit(bg_image, (0, 0))
            self.screen.blit(animal_principal_image, dict_coordenadas['animal-principal'])
            self.screen.blit(escolha_correta_image, coordenadas_opcoes[0])
            if caixa_errada_um_image:
                self.screen.blit(caixa_errada_um_image, coordenadas_opcoes[1])
            if caixa_errada_dois_image:
                self.screen.blit(caixa_errada_dois_image, coordenadas_opcoes[2])
            
            # Desenhar retângulo semitransparente atrás do texto "Tentativas"
            tentativas_text = f"Tentativas: {tentativa}"
            other_draw_text_with_background(self.screen, tentativas_text, self.font, WHITE, BLACK, (20, 15))
            
            for event in pygame.event.get():
                self.try_exit(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if (sair_esquerdo_top_left[0] <= mouse_pos[0] <= sair_esquerdo_bottom_right[0] and
                        sair_esquerdo_top_left[1] <= mouse_pos[1] <= sair_esquerdo_bottom_right[1]):
                        self.current_screen = 'menu_inicial'
                    
                    escolha_correta_rect = pygame.Rect(coordenadas_opcoes[0][0], coordenadas_opcoes[0][1], escolha_correta_image.get_width(), escolha_correta_image.get_height())
                    
                    if escolha_correta_rect.collidepoint(mouse_pos):
                        escolha_clicada = True
                        new_row = pd.DataFrame({'nome_da_fase': [f'Jogo 2 - nível {self.dict_tipo_da_fase[self.fase_dois_nivel]}'], 'tentativas': [tentativa]})
                        self.tentativas_df = pd.concat([self.tentativas_df, new_row], ignore_index=True)
                    
                    if caixa_errada_um_image:
                        caixa_errada_um_rect = pygame.Rect(coordenadas_opcoes[1][0], coordenadas_opcoes[1][1], caixa_errada_um_image.get_width(), caixa_errada_um_image.get_height())
                        if caixa_errada_um_rect.collidepoint(mouse_pos):
                            caixa_errada_um_image = None
                            tentativa += 1
                    
                    if caixa_errada_dois_image:
                        caixa_errada_dois_rect = pygame.Rect(coordenadas_opcoes[2][0], coordenadas_opcoes[2][1], caixa_errada_dois_image.get_width(), caixa_errada_dois_image.get_height())
                        if caixa_errada_dois_rect.collidepoint(mouse_pos):
                            caixa_errada_dois_image = None
                            tentativa += 1
                    
                    if escolha_clicada and reset_button.collidepoint(mouse_pos):
                        if self.fase_dois_nivel == 3:
                            self.current_screen = 'menu_inicial'
                            self.fase_dois_nivel = 1
                            self.fase_dois_concluido = True
                            return
                        else:
                            self.fase_dois_nivel += 1
                            self.fase_dois_alimente_o_bicho()
                            return
                        
            temp_text = rf"O que o {nome_animal_principal} come?"
            other_draw_text_with_background(self.screen, rf"{temp_text}", self.font, WHITE, BLACK, (17, 240), WIN_WIDHT, True)
            
            if escolha_clicada:
                reset_button = mostrar_parabens(self.screen, self.font_parabens, WIN_WIDHT, WIN_HEIGHT, n_fase=self.fase_dois_nivel, resto_do_texto=rf" Tentativas: {tentativa}")
            
            
            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(30)
  
            
    def try_exit(self, event):
        if event.type == pygame.QUIT:
            salvar_data_frames(
                df_tentativas=self.tentativas_df,
                df_tempos= self.times_df,
                player_name= self.player_name,
                caminho_pasta_turma= self.caminho_pasta_turma,
            )
            
            self.running = False
            
            pygame.quit()
            sys.exit()
            

    def draw_text(self, surface, text, font, color, pos):
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)


if __name__ == "__main__":
    g = Game()
    g.run()  # Call the run method to start the game
