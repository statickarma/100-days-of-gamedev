from engine.main import *


class DinoGame(Game):

    def __init__(self, height, width, title, fps):
        super().__init__(height, width, title, fps)
        self.dino_action = 0
        self.dino_sprites = []

    def load_assets(self):
        self.dino_sprites = self.get_sprites(
            './img/DinoSprites - vita.png',
            pygame.Vector2(24, 24),
            [4, 6, 3, 4, 7],
            3
        )

    def update(self, events, game_time):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
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


game = DinoGame(600, 400, 'Dino', 60)
game.run()
