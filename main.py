import pygame
import os

WIDTH = 800
HEIGHT = int(WIDTH*0.8)
clock = pygame.time.Clock()
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SHOOTER')

# player Variables
moving_left = False
moving_right = False
shoot = False


# Images
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

# defining Colors
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# game_variable
GRAVITY = 0.75


def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (WIDTH, 300))


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammp = ammo
        self.shoot_cooldown = 0
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air =False
        self.flip = False
        self.action = 0
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # load  alll images for player
        animation_types = ['Idle', 'Run', 'Jump']
        for animation in animation_types:
            number_of_images = len(os.listdir(
                f'img/{self.char_type}/{animation}'))
            temp_list = []
            for i in range(number_of_images):
                img = pygame.image.load(
                    f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(
                    img, (int(img.get_width()*scale), int(img.get_height()*scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.upadate_animation()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # movement variables
        dx = 0
        dy = 0
        # assigning movement variables when moving right or left
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1  # -1 means to face on the left side
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += int(self.vel_y)

        # Check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        # updating rect position
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            bullet = Bullet(
                self.rect.centerx+(0.6*self.rect.size[0]*self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)

    def upadate_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:

            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # Bullet Movement
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()


bullet_group = pygame.sprite.Group()


player = Soldier('player', 200, 200, 3, 5, 20)
enemy = Soldier('enemy', 200, 200, 3, 5, 20)


running = True
while running:
    clock.tick(FPS)
    draw_bg()

    bullet_group.update()
    bullet_group.draw(screen)

    if player.alive:
        if shoot:
            player.shoot()
        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1)  # 1 means running
        else:
            player.update_action(0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                moving_left = True

            if event.key == pygame.K_RIGHT:
                moving_right = True

            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True

            if event.key == pygame.K_TAB:
                shoot = True

            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_RIGHT:
                moving_right = False

            if event.key == pygame.K_LEFT:
                moving_left = False

            if event.key == pygame.K_TAB:
                shoot = False

    player.move(moving_left, moving_right)
    player.draw()
    player.update()

    pygame.display.update()


pygame.quit()
