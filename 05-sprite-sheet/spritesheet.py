import pygame
import sys


class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (frame * width, 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)

        return image


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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN and self.action > 0:
                        self.action -= 1
                        self.frame = 0
                    if event.key == pygame.K_UP and self.action < len(self.animation_list) - 1:
                        self.action += 1
                        self.frame = 0

            self.update()
            self.render()
            pygame.display.update()
            self.clock.tick(self.fps)

        self.shutdown()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.last_update = current_time
            self.frame += 1
            self.frame %= len(self.animation_list[self.action])

    def render(self):
        self.screen.fill((173, 216, 230))
        self.screen.blit(self.animation_list[self.action][self.frame], (0, 0))

    def shutdown(self):
        pygame.quit()

    def load_assets(self):
        dino_sheet_img = pygame.image.load('./img/DinoSprites - vita.png').convert_alpha()
        self.sprite_sheet = SpriteSheet(dino_sheet_img)
        self.animation_list = []
        self.animation_steps = [4, 6, 3, 4, 7]
        self.action = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 120
        self.frame = 0
        step_counter = 0
        for animation in self.animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(self.sprite_sheet.get_image(step_counter, 24, 24, 3, (0, 0, 0, 0)))
                step_counter += 1
            self.animation_list.append(temp_img_list)


game = Game(600, 400, 'Sprite Sheet Animation', 60)
game.run()
sys.exit()
