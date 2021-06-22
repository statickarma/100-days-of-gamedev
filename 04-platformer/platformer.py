import sys
import pygame
from pygame.locals import *
import pickle
from os import path

pygame.init()
clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800
tile_size = 40
game_over = 0
main_menu = True
level = 0
total_levels = 8

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')
run = True

bg_image = pygame.transform.scale(pygame.image.load('img/sky.png').convert(), (screen_width, screen_height))
sun_image = pygame.image.load('img/sun.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()
start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)

        return action


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 6
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 40:
            self.move_counter *= -1
            self.move_direction *= -1


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png').convert_alpha()
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit.png').convert_alpha()
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class World:
    def __init__(self, data):
        self.tile_list = []
        dirt_image = pygame.image.load('img/dirt.png').convert()
        grass_image = pygame.image.load('img/grass.png').convert()
        for row, tile_row in enumerate(data):
            for col, tile in enumerate(tile_row):
                if tile == 1:
                    img = pygame.transform.scale(dirt_image, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col * tile_size
                    img_rect.y = row * tile_size
                    self.tile_list.append((img, img_rect))
                elif tile == 2:
                    img = pygame.transform.scale(grass_image, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col * tile_size
                    img_rect.y = row * tile_size
                    self.tile_list.append((img, img_rect))
                elif tile == 3:
                    blob = Enemy(col * tile_size, row * tile_size)
                    blob_group.add(blob)
                elif tile == 6:
                    blob = Lava(col * tile_size, row * tile_size + (tile_size // 2))
                    lava_group.add(blob)
                elif tile == 8:
                    blob = Exit(col * tile_size, row * tile_size)
                    exit_group.add(blob)

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (0, 0, 255), tile[1], 2)


class Player:
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'img/guy{num}.png').convert_alpha()
            img_right = pygame.transform.scale(img_right, (32, 64))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.dead_image = pygame.image.load('img/ghost.png').convert_alpha()
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

    def update(self):
        global game_over
        dx = 0
        dy = 0
        walk_cool_down = 5

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[K_SPACE] and not self.jumped:
                self.vel_y = -15
                self.jumped = True
            if not key[K_SPACE] and not self.in_air:
                self.jumped = False
            if key[K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[K_RIGHT]:
                dx = 5
                self.counter += 1
                self.direction = 1
            if not key[K_LEFT] and not key[K_RIGHT]:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # animation
            if self.counter > walk_cool_down:
                self.counter = 0
                self.index += 1
                self.index %= len(self.images_right)
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # check for collision
            self.in_air = True
            for tile in world.tile_list:
                # check x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1

            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1

            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy
        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def reset(self, x, y):
        self.index = 0
        self.counter = 0
        self.image = self.images_right[self.index]
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.rect.x = x
        self.rect.y = y


blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
if not path.exists(f'level{level}_data'):
    print(f'Unable to load level {level}')
    pygame.quit()
    sys.exit()

pickle_in = open(f'level{level}_data', 'rb')
world_data = pickle.load(pickle_in)
world = World(world_data)
player = Player(80, screen_height - 104)
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 280, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 120, screen_height // 2, exit_img)


def reset_level(level_no):
    global pickle_in, world_data, world
    if not path.exists(f'level{level_no}_data'):
        print(f'Unable to load level {level_no}')
        pygame.quit()
        sys.exit()

    player.reset(80, screen_height - 104)
    blob_group.empty()
    lava_group.empty()
    exit_group.empty()
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
    world = World(world_data)


while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    screen.blit(bg_image, (0, 0))
    screen.blit(sun_image, (75, 75))
    if main_menu:
        if start_button.draw():
            main_menu = False
        if exit_button.draw():
            run = False
    else:
        world.draw()

        if game_over == 0:
            blob_group.update()
        elif game_over == 1:
            level += 1
            level %= total_levels
            world_data = []
            reset_level(level)
            game_over = 0
        elif game_over == -1:
            restart = restart_button.draw()
            if restart:
                game_over = 0
                player.reset(80, screen_height - 104)

        player.update()
        blob_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
sys.exit()
