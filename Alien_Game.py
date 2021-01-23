import pygame
from pygame.sprite import Group
from modulo_configuração import configuration
from Ship import Ship
import funcoes_alien as gf
from Games_Stats import Games_Stats
from button import Button
from Score_Board import ScoreBoard
def run_game():
    # Cria uma espaçonave, um grupo de projéteis e um grupo de alienígenas
    pygame.init()
    confg = configuration()
    tela = pygame.display.set_mode((confg.tela_largura,
                                    confg.tela_altura))
    play_button = Button(confg, tela, "Play")
    pygame.display.set_caption('Alien Invasion')
    stats = Games_Stats(confg)
    ship = Ship(confg, tela)
    sb = ScoreBoard(confg, tela, stats)
    bullets = Group()
    aliens = Group()
    gf.criar_fronta(confg, tela, aliens, ship)
    while True:
        gf.check_events(confg, tela, ship,
                        bullets, stats, play_button, aliens, confg, sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(confg, tela, ship, aliens, bullets, stats, sb)
            gf.update_aliens(tela, stats, confg, ship, aliens, bullets, sb)

        gf.update_screen(confg, tela, stats, ship, aliens, bullets, play_button, sb)


run_game()
