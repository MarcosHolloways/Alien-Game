import sys
import pygame
from Bullet import Bullet
from Alien_Ship import Alien
from time import sleep
import json


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Responde a pressionamentos de tecla."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Responde a solturas de tecla"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, ship,
                 bullets, stats, play_button, aliens, confg, sb):
    """Responde a eventos de pressionamento de teclas e mouse"""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ship, confg, screen, sb)


def update_screen(ai_settings, tela, stats, ship, alien, bullets, play_button, sb):
    """Atualiza as imagens na tela e alterna para a nova tela"""
    # Redesenha a tela a cada passagem pelo laço
    tela.fill(ai_settings.bg_color)
    # Redesenha todos os projéteis atrás da espaçonave e dos alienígenas
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    alien.draw(tela)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(confg, tela, ship, aliens, bullets, stats, sb):
    """Atualiza a posição dos projéteis e se livra dos projéteis antigos."""
    # Atualiza as posições dos projéteis
    bullets.update()

    # Livra-se dos projéteis que desapareceram
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(confg, tela, aliens, ship, bullets, stats, sb)


def check_bullet_alien_collision(confg, tela, aliens, ship, bullets, stats, sb):
    collision = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collision:
        for aliens in collision.values():
            stats.score += confg.alien_point * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        start_new_level(confg, tela, aliens, ship, bullets, stats, sb)


def update_aliens(tela, stats, confg, ship, aliens, bullets, sb):
    check_limite_borda(confg, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(confg, tela, stats, ship, aliens, bullets, sb)
    check_alien_borda(tela, aliens, confg, stats, ship, bullets, sb)



def fire_bullet(ai_settings, screen, ship, bullets):
    """Dispara um projétil se o limite ainda não foi alcançado."""
    # Cria um novo projétil e o adiciona ao grupo de projéteis
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        pygame.mixer.music.load("Sounds/laser_shot.mp3.mp3")
        pygame.mixer.music.set_volume(0.2   )
        pygame.mixer.music.play(0)


def numero_linha(confg, ship_altura, alien_altura):
    espaco = confg.tela_altura - 3 * alien_altura - ship_altura
    number_linha = int(espaco / (2 * alien_altura))
    return number_linha


def get_number_aliens(confg, alien_width):
    """Determina o número de alienígenas que cabem em uma linha."""
    espaco = confg.tela_largura - 2 * alien_width
    number_aliens = int(espaco / (2 * alien_width))
    return number_aliens


def create_alien(confg, screen, aliens, alien_number, line):
    alien = Alien(confg, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * line
    aliens.add(alien)


def criar_fronta(confg, screen, aliens, ship):
    """Cria uma frota completa de alienígenas."""
    alien = Alien(confg, screen)
    number_aliens = get_number_aliens(confg, alien.rect.width)
    number_linha = numero_linha(confg, ship.rect.height, alien.rect.height, )
    for line in range(number_linha):
        for alien_number in range(number_aliens):
            create_alien(confg, screen, aliens, alien_number, line)


def check_limite_borda(confg, aliens):
    for alien in aliens.sprites():
        if alien.check_bordas():
            change_direction(confg, aliens)
            break


def change_direction(confg, aliens):
    for alien in aliens.sprites():
        alien.rect.y += confg.falling
    confg.frota_direction *= -1


def ship_hit(confg, tela, stats, ship, aliens, bullets, sb):
    if stats.ships_left > 0:
        # retira uma nave
        stats.ships_left -= 1
        sb.prep_ships()
        # retira todos aliens e balas
        aliens.empty()
        bullets.empty()
        # criar uma frota e centraliza a nave
        criar_fronta(confg, tela, aliens, ship)
        ship.center_ship()
        sleep(0.5)
    else:

        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ship, confg, screen, sb):
    button_click = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_click and not stats.game_active:
        confg.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        # reiniciar os dados estatisticos do jogo
        sb.prep_image()

        aliens.empty()
        bullets.empty()
        criar_fronta(confg, screen, aliens, ship)
        ship.center_ship()

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        with open("High_Score.json", 'w') as f_object:
            json.dump(stats.high_score, f_object)
        sb.prep_hight_score()

def check_alien_borda(tela, aliens, confg, stats, ship, bullets, sb):
    tela_rect = tela.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= tela_rect.bottom:
            ship_hit(confg, tela, stats, ship, aliens, bullets, sb)

def start_new_level(confg, tela, aliens, ship, bullets, stats, sb):
    bullets.empty()
    confg.aumentar_velocidade()
    stats.level += 1
    sb.prep_level()
    criar_fronta(confg, tela, aliens, ship)
