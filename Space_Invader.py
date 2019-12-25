# space invader
# by RestlessPuppet
#
# Icons by:
# <div>Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
# <div>Icons made by <a href="https://www.flaticon.com/authors/photo3idea-studio" title="photo3idea_studio">photo3idea_studio</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
# <div>Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
# <div>Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>


import random
import pygame
from pygame import mixer
import math

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Create the screen
screen = pygame.display.set_mode((800, 600))

#Background
background=pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('icon.png')

# player
player_image = pygame.image.load('spaceship.png')
player_x = 368
player_y = 480
player_dx = 0

# enemy
enemy_speed = []
enemy_image = []
enemy_x = []
enemy_y = []
enemy_dx = []
enemy_dy = 15
num_of_enemies = 6
enemy_speed = [-.25, .25]

def add_enemy():
    enemy_image.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 730))
    enemy_y.append(random.randint(6, 200))
    enemy_dx.append(random.choice(enemy_speed))

for i in range(num_of_enemies):
    add_enemy()

# bullet
bullet_image = pygame.image.load('bullet.png')
bullet_y = player_y
bullet_x = player_x
bullet_dx = 0
bullet_dy = 1.5
bullet_state = 'ready'
bullets_fired = 0

# font
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# gameover text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_accuracy(x, y):
    score = font.render('Accuracy: ' + str(score_value/bullets_fired), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render('Game Over', True, (255, 255, 255))
    screen.blit(over_text, (200, 200))


def player(x, y):
    screen.blit(player_image, (int(x), int(y)))


def enemy(x, y, i):
    screen.blit(enemy_image[i], (int(x), int(y)))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_image, (int(x+16), int(y)))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 32:
        return True
    else:
        return False


# Game loop
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check if right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_dx = -0.75
            if event.key == pygame.K_RIGHT:
                player_dx = 0.75
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bullets_fired += 1
                    bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_dx = 0

    # Checking boundaries
    player_x += player_dx
    if player_x <= 6:
        player_x = 6
    if player_x >= 730:
        player_x = 730

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemy_y[i] > 430:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_dx[i]
        if enemy_x[i] <= 0:
            enemy_dx[i] *= (-1)
            enemy_y[i] += enemy_dy
        if enemy_x[i] >= 736:
            enemy_dx[i] *= (-1)
            enemy_y[i] += enemy_dy

        # Collision
        if bullet_state == 'fire':
            collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
            if collision:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bullet_y = 480
                bullet_state = 'ready'
                for n in range (num_of_enemies):
                    if enemy_dx[n] >= 0:
                        enemy_dx[n] += .03
                    else:
                        enemy_dx[n] -= .03
                score_value += 1
                if score_value % 10 == 0:
                    add_enemy()
                    num_of_enemies += 1
                enemy_x[i] = random.randint(6, 730)
                enemy_y[i] = random.randint(6, 200)

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet Movement
    if bullet_state == 'fire':
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_dy

        if bullet_y <= 0:
            bullet_state = 'ready'
            bullet_y = 480

    show_score(text_x, text_y)
    if bullets_fired > 0:
        show_accuracy(text_x + 500, text_y)
    player(player_x, player_y)
    pygame.display.update()
