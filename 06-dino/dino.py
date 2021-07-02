import enum

import pygame.transform

from engine.main import *
import sys


class Sprite:
    def __init__(self, image, frame_size, total_frames):
        self.total_frames = total_frames
        self.frame_size = frame_size
        self.image = image
        self.frame = 0
        self.frame_time = 200
        self.last_update_time = 0

    def update(self, game_time):
        if game_time - self.last_update_time >= self.frame_time:
            self.last_update_time = game_time
            self.frame += 1
            self.frame %= self.total_frames

    def render(self, screen):
        screen.blit(self.image, (0, 0), (self.frame * self.frame_size.x, 0, self.frame_size.x, self.frame_size.y))


class SpriteSheet:
    def __init__(self, total_animations):
        self.total_animations = total_animations


class DinoGame(Game):

    def __init__(self, height, width, title, fps):
        super().__init__(height, width, title, fps)
        self.dino_action = 0
        self.dino_sprites = []

    def load_assets(self):
        dino_scale = 3
        dino_frame_width = 24
        dino_frame_height = 24
        dino_image = pygame.image.load('./img/DinoSprites - vita.png').convert_alpha()
        dino_rect = dino_image.get_rect()
        dino_image = pygame.transform.scale(dino_image, (dino_rect.width * dino_scale, dino_rect.height * dino_scale))

        # Idle
        idle_frames = 4
        image = pygame.Surface((dino_frame_width * dino_scale * idle_frames, dino_frame_height * dino_scale)).convert_alpha()
        image.blit(dino_image, (0, 0), (0, 0, dino_frame_width * dino_scale * idle_frames, dino_frame_height * dino_scale))
        image.set_colorkey((0, 0, 0))
        self.dino_sprites.append(
            Sprite(image, pygame.Vector2(dino_frame_width * dino_scale, dino_frame_height * dino_scale), 4))

        # Move
        move_frames = 6
        image = pygame.Surface((dino_frame_width * dino_scale * move_frames, dino_frame_height * dino_scale)).convert_alpha()
        image.blit(dino_image, (0, 0), (24 * 3 * (idle_frames), 0, dino_frame_width * dino_scale * 6, dino_frame_height * dino_scale))
        image.set_colorkey((0, 0, 0))
        self.dino_sprites.append(
            Sprite(image, pygame.Vector2(dino_frame_width * dino_scale, dino_frame_height * dino_scale), move_frames))

        # Kick
        kick_frames = 3
        image = pygame.Surface((dino_frame_width * dino_scale * kick_frames, dino_frame_height * dino_scale)).convert_alpha()
        image.blit(dino_image, (0, 0), (24 * 3 * (idle_frames + move_frames), 0, dino_frame_width * dino_scale * kick_frames, dino_frame_height * dino_scale))
        image.set_colorkey((0, 0, 0))
        self.dino_sprites.append(
            Sprite(image, pygame.Vector2(dino_frame_width * dino_scale, dino_frame_height * dino_scale), kick_frames))

        # Hurt
        hurt_frames = 4
        image = pygame.Surface((dino_frame_width * dino_scale * hurt_frames, dino_frame_height * dino_scale)).convert_alpha()
        image.blit(dino_image, (0, 0), (24 * 3 * (idle_frames + move_frames + kick_frames), 0, dino_frame_width * dino_scale * hurt_frames, dino_frame_height * dino_scale))
        image.set_colorkey((0, 0, 0))
        self.dino_sprites.append(
            Sprite(image, pygame.Vector2(dino_frame_width * dino_scale, dino_frame_height * dino_scale), hurt_frames))

        # Run
        run_frames = 7
        image = pygame.Surface((dino_frame_width * dino_scale * run_frames, dino_frame_height * dino_scale)).convert_alpha()
        image.blit(dino_image, (0, 0), (24 * 3 * (idle_frames + move_frames + kick_frames + hurt_frames), 0, dino_frame_width * dino_scale * run_frames, dino_frame_height * dino_scale))
        image.set_colorkey((0, 0, 0))
        self.dino_sprites.append(
            Sprite(image, pygame.Vector2(dino_frame_width * dino_scale, dino_frame_height * dino_scale), run_frames))

    def update(self, game_time):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.dino_action -= 1
                    self.dino_action %= len(self.dino_sprites)
                    self.dino_sprites[self.dino_action].frame = 0
                if event.key == pygame.K_RIGHT:
                    self.dino_action += 1
                    self.dino_action %= len(self.dino_sprites)
                    self.dino_sprites[self.dino_action].frame = 0

        self.dino_sprites[self.dino_action].update(game_time)

    def render(self):
        self.screen.fill((173, 216, 230))
        self.dino_sprites[self.dino_action].render(self.screen)


game = DinoGame(600, 400, 'Same', 60)
game.run()
sys.exit()
