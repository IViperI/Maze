#Game Maze
import pygame as pg

#Constants
WIDTH = 700
HEIGHT = 500
FPS = 75
MUSIC_VOLUME = 20#%0,100

#Class
class GSprite(pg.sprite.Sprite): #GameSprite
    def __init__(self, image, position, speed):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(image), (65,65))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def show(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(GSprite):
    def update(self):
        keys = pg.key.get_pressed()
        if  keys[pg.K_a] and self.rect.x >= 5:
            self.rect.x -= self.speed
        if keys[pg.K_d] and self.rect.x <= WIDTH-self.rect.width:
            self.rect.x += self.speed
        if  keys[pg.K_w] and self.rect.y >= 5:
            self.rect.y -= self.speed
        if keys[pg.K_s] and self.rect.y <= HEIGHT-self.rect.height:
            self.rect.y += self.speed

class Enemy(GSprite):
    def __init__(self, image, position, speed, horizontal = True, moveLength = 0, reverse = False):
        super().__init__(image, position, speed)
        self.horizontal = horizontal
        self.moveLength = moveLength
        self.reverse = reverse
        self.startPosition = position
        self.targetPosition = (self.rect.x+self.moveLength, self.rect.y+self.moveLength)

    def update(self):
        if self.horizontal == True:
            if self.rect.x >= self.targetPosition[0]:
                self.reverse = True
            if self.rect.x <= self.startPosition[0]:
                self.reverse = False

            if self.reverse == True:
                self.rect.x += -self.speed
            if self.reverse == False:
                self.rect.x += self.speed

        if self.horizontal == False:
            if self.rect.y >= self.targetPosition[1]:
                self.reverse = True
            if self.rect.y <= self.startPosition[1]:
                self.reverse = False

            if self.reverse == True:
                self.rect.y += -self.speed
            if self.reverse == False:
                self.rect.y += self.speed

class Wall(pg.sprite.Sprite):
    def __init__(self, color, size):
        super().__init__()
        self.color = color
        self.width = size[0]
        self.height = size[1]
        self.image = pg.Surface((self.width,self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def show(self, surface, position = (0,0)):
        self.rect.x = position[0]
        self.rect.y = position[1]
        surface.blit(self.image, (self.rect.x,self.rect.y))

class Treasure(GSprite):
    pass
        

# Pygame
pg.init()
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Maze')
background = pg.transform.scale(pg.image.load("background.jpg"),(WIDTH, HEIGHT))
pg.mixer.music.load('jungles.ogg')
pg.mixer.music.set_volume(MUSIC_VOLUME/100)
pg.mixer.music.play()
deathSound = pg.mixer.Sound('kick.ogg')
moneySound = pg.mixer.Sound('money.ogg')
text = pg.font.Font(None, 70)
victoryText = text.render("Victory", True, (255, 255, 100))
defeatText = text.render("Defeat", True, (255, 100, 100))
#Examples
player = Player('hero.png', (70,50), 2)

wallOptions = [
                        ((255,255,255),(10,300)),
                        ((100,100,100),(70,10)),
                        ((255,255,255),(60,10)),
                        ((255,255,255),(10,400)),
                        ((255,255,255),(10,430)),
                        ((255,255,255),(380,10)),
                        ((255,255,255),(270,10)),
                        ((255,255,255),(380,10)),
                        ((100,100,100),(10,90)),
                        ((255,255,255),(10,100)),
                        ((255,255,255),(10,100)),
                        ((255,255,255),(10,130)),
                        ((255,255,255),(10,130)),
                        ((255,255,255),(90,10)),
                        ((100,100,100),(10,90)),
                        ((100,100,100),(80,10)),
                        ]
wallPositions = [
                            (60,0),
                            (70,390),
                            (0,290),
                            (140,0),
                            (220,70),
                            (320,70),
                            (220,170),
                            (320,270),
                            (570,80),
                            (570,170),
                            (400,270),
                            (500,370),
                            (590,370),
                            (320,370),
                            (320,280),
                            (510,370),
                            ]
walls = []
for option in wallOptions:
    walls.append(Wall(option[0],option[1]))

enemyOptions = [
                            ['cyborg.png', (70,300), 1, False, 150, False],
                            ['cyborg.png', (520,300), 1, False, 125, True],
                            ['cyborg.png', (240,100), 1, True, 370, True],
                            ['cyborg.png', (245,300), 1, True, 100, True],
                            ]
enemies = []
for option in enemyOptions:
    enemies.append(Enemy(option[0],option[1],option[2],option[3],option[4],option[5]))

treasure = Treasure('treasure.png',(610,425), 0)

#Game
clocks = pg.time.Clock()
gameRun = 1
finish = False
victory = False
while gameRun:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameRun = 0
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
    if finish:
        if victory:
            window.blit(victoryText,(270,230))
        else:
            window.blit(defeatText,(270,230))
        if pg.key.get_pressed()[pg.K_r]:
            finish = False
            player.rect.x = 70
            player.rect.y = 50
    else:
        window.blit(background, (0,0))
        for enemy in enemies:    
            if pg.sprite.collide_rect(player, enemy):
                finish = True
                deathSound.play()

        player.update()
        player.show(window)
        for wall in walls:
            wall.show(window, wallPositions[walls.index(wall)])
            if pg.sprite.collide_rect(player,wall):
                player.rect.x,player.rect.y = 70,50
            if pg.sprite.collide_rect(player,treasure):
                finish, victory = True, True
        for enemy in enemies:
            enemy.update()
            enemy.show(window)
        treasure.show(window)
    pg.display.update()
    clocks.tick(FPS)