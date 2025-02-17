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
        self.load_images()

        #Groups
        self.all_sprites = AllSprites()
        self.bullet_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()

        #Gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.shoot_cd = 100


    def load_images(self):
        self.bullet_surf = pygame.image.load(join("images", "gun", "bullet.png")).convert_alpha()


    def setup(self):
        map = load_pygame(join("data", "maps", "world.tmx"))
        
        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name("Objects"):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name("Collisions"):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)

    
    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 60
            Bullet(self.bullet_surf, pos , self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

        self.gun_timer()


    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.shoot_cd:
                self.can_shoot = True      

    def run(self):
        while self.running:
            # Dt
            dt = self.clock.tick() / 1000

            #Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #Update the game
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)

            #Draw the game
            self.screen_display.fill("#2f3036")
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()