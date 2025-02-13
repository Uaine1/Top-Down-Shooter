from settings import *
from sprites import *
from player import Player
from pytmx.util_pygame import load_pygame
from groups import AllSprites

from random import randint

class Game():
    def __init__(self):
        #Setup
        pygame.init()
        self.screen_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vamps")
        self.running = True
        self.clock = pygame.time.Clock()

        #Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()

        #Sprites
        self.player = Player((500,300), self.all_sprites, self.collision_sprites)


    def setup(self):
        map = load_pygame(join("data", "maps", "world.tmx"))
        
        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name("Objects"):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for col in map.get_layer_by_name("Collisions"):
            CollisionSprite((col.x, col.y), pygame.Surface((col.width, col.height)), self.collision_sprites)


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
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()