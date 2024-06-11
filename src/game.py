import sys
import pygame
from src.constants import *

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.width, self.height = WIN_WIDHT, WIN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.clock = pygame.time.Clock()
        self.player_name = ''

    def tela_login(self) -> None:
        bg_image = pygame.image.load(rf'imgs\menu-inicial.jpg')
        bg_image = pygame.transform.scale(bg_image, (self.width, self.height))

        color = COLOR_INACTIVE
        active = True
        text = ''
        input_box_width = 300
        offset_x = 125  # PARA MOVER PARA A DIREITA, AJUSTAR ESSA VARIÁVEL (FOI O QUE EU CONSEGUIR)
        input_box = pygame.Rect((self.width - input_box_width) // 2 + offset_x, 215, input_box_width, 50)
        submit_button = pygame.Rect((self.width - 153) // 2 + offset_x, 315, 153, 45)

        while self.running:
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


    def try_exit(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            pygame.quit()
            sys.exit()

    # Função para desenhar texto na tela
    def draw_text(self, surface, text, font, color, pos):
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)

if __name__ == "__main__":
    g = Game()
    g.tela_login()
