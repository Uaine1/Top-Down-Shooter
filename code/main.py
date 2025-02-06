from settings import *
from player import Player

class Game():
    def __init__(self):
        #Setup
        pygame.init()
        self.screen_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vamps")
        self.running = True
        self.clock = pygame.time.Clock()

        #Groups
        self.all_sprites = pygame.sprite.Group()

        #Sprites
        self.player = Player((400,300), self.all_sprites)


    def run(self):
        while self.running:
            # Dt
            dt = self.clock.tick() / 1000

            #Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #Update the game
            self.all_sprites.update(dt)

            #Draw the game
            self.screen_display.fill("#2f3036")
            self.all_sprites.draw(self.screen_display)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()