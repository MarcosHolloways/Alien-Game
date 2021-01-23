import pygame.font
from pygame.sprite import Group
from Ship import Ship
class ScoreBoard():
    def __init__(self, confg, tela, stats):
        self.tela = tela
        self.tela_rect = tela.get_rect()
        self.confg = confg
        self.stats = stats
        self.hight_score = 0
        # Configurações de fonte, para informa pontuação
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_image()

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.confg.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.tela_rect.right - 20
        self.score_rect.top = 20


    def show_score(self):
        self.tela.blit(self.score_image, self.score_rect)
        self.tela.blit(self.high_score_image, self.high_score_rect)
        self.tela.blit(self.level_image, self.level_rect)
        self.ships.draw(self.tela)

    def prep_hight_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.confg.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.tela_rect.centerx
        self.high_score_rect.top = self.tela_rect.top
    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.confg.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.confg, self.tela)
            ship.image = pygame.image.load("Images/Ship_Draw.bmp")
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
    def prep_image(self):
        self.prep_score()
        self.prep_hight_score()
        self.prep_level()
        self.prep_ships()


