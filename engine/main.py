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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update(pygame.time.get_ticks())
            self.render()
            pygame.display.update()
            self.clock.tick(self.fps)

        self.shutdown()

    def update(self, game_time):
        pass

    def render(self):
        pass

    def shutdown(self):
        pygame.quit()

    def load_assets(self):
        pass
