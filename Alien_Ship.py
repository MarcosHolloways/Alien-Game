import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Uma classe que representa um único alienígena da frota."""
    def __init__(self, ai_settings, tela):
        """Inicializa o alienígena e define sua posição inicial."""
        super(Alien, self).__init__()
        self.tela = tela
        self.ai_settings = ai_settings

        # Carrega a imagem do alienígena e define seu atributo rect
        self.image = pygame.image.load('images/small_disc.bmp')
        self.rect = self.image.get_rect()

        # Inicia cada novo alienígena próximo à parte superior esquerda da tela
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Armazena a posição exata do alienígena
        self.x = float(self.rect.x)

    def blitme(self):
        """Desenha o alienígena em sua posição atual."""
        self.tela.blit(self.image, self.rect)

    def check_bordas(self):
        """Devolve True se o alienígena estiver na borda da tela."""
        tela_rect = self.tela.get_rect()
        if self.rect.right >= tela_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move o alienígena para a direita ou para a esquerda."""
        self.x += (self.ai_settings.alien_speed * self.ai_settings.frota_direction)
        self.rect.x = self.x