import sys

import pygame


class Game:
    def __init__(self, height, width, title, fps):
        self.height = height
        self.width = width
        self.title = title
        self.fps = fps
        self.clock = None
        self.screen = None
        self.running = False

    def initialize(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.height, self.width))
        pygame.display.set_caption(self.title)
        self.running = True
        self.load_assets()

    def run(self):
        self.initialize()
        while self.running:
            self.update(pygame.event.get(), pygame.time.get_ticks())
            self.render()
            pygame.display.update()
            self.clock.tick(self.fps)

        self.shutdown()

    def update(self, events, game_time):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        pass

    def shutdown(self):
        pygame.quit()
        sys.exit()

    def load_assets(self):
        pass

    def get_sprites(self, image_path, frame_size, animation_steps, scale=1):
        frame = pygame.Vector2(frame_size * scale, frame_size * scale)

        sprite_sheet = pygame.image.load(image_path).convert_alpha()
        rect = sprite_sheet.get_rect()
        sprite_sheet = pygame.transform.scale(sprite_sheet, (rect.width * scale, rect.height * scale))
        cursor = 0
        sprites = []
        for steps in animation_steps:
            image = pygame.Surface((frame.x * steps, frame.y)).convert_alpha()
            image.blit(
                sprite_sheet,
                (0, 0),
                pygame.Rect(frame.x * cursor, 0, frame.x * steps, frame.y)
            )
            image.set_colorkey((0, 0, 0))
            sprites.append(Sprite(image, pygame.Vector2(frame.x, frame.y), steps))
            cursor += steps

        return sprites


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
