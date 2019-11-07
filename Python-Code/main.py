import pygame as pg
from os import path
import sys
from settings import*
from sprites import*
from tilemap import*


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.counter = 1
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, 'map.txt'))
        #Lichteffekte
        self.fog =  pg.Surface((WIDTH,HEIGHT))
        self.fog.fill(BLACK)
        self.light_mask = pg.image.load(path.join(game_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                elif tile == 'P':
                    self.player = Player(self, col, row)
                elif tile =='2':
                    Candle(self,col,row)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
   
    def render_fog(self):
        # die Maske wird auf den Bildschirm gemalt und der Lichtkreis ermöglicht Sicht um den Spieler 
          self.fog.fill(BLACK)
          self.light_rect.center = self.camera.apply(self.player).center
          self.fog.blit(self.light_mask, self.light_rect)
          self.screen.blit(self.fog, (0,0), special_flags = pg.BLEND_MULT)


    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.render_fog()
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.USEREVENT:
                self.counter += 1
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
 

g = Game()
while True:
    g.new()
    g.run()
