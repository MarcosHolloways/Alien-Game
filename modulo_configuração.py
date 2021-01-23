class configuration():
    def __init__(self):

        self.tela_largura = 1250
        self.tela_altura = 700
        self.bg_color = (255, 255, 255)
        # Configurações da espaçonave
        self.ship_limit = 3
        # Configurações dos projéteis
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 0, 240)
        self.bullets_allowed = 3
        # Configurações dos alienígenas
        self.falling = 10

        # Taxa com que a velocidade do jogo aumenta
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        self.alien_point = 50
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed = 1
        # para a direita(1), para a esquerda (-1)
        self.frota_direction = 1


    def aumentar_velocidade(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_point = int(self.alien_point * self.score_scale)

