import pygame
import json
pygame.init()

with open("Delivery!/level1.json", "r") as file:
    level = json.load(file)

lev = 1
maxlevel = 3

chances = 3

death = pygame.mixer.Sound("Sound of music/Bunny Screaming.mp3")
death.set_volume(10)

pygame.mixer.music.load("Sound of music/natural_nature.wav")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

def nextlevel():
    babybun.rect.x = 100
    babybun.rect.y = height-130
    wisp_group.empty()
    salty_group.empty()
    bye.empty()
    with (open(f"Delivery!/level{lev}.json", "r") as file):
        level = json.load(file)
    lev1 = world(level)
    return lev1
width = 800
height = 800
game_over = 0
tile_size = 40
clock = pygame.time.Clock()
fps = 60
display = pygame.display.set_mode((width,height))
pygame.display.set_caption("Gamer")

class wisp(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        img = pygame.image.load("Pictured/wispy.png")
        self.image = pygame.transform.scale(img,(tile_size,tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class collectables(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        img = pygame.image.load("Pictured/newstar.png").convert_alpha()
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

class salt(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        img = pygame.image.load("Pictured/water.png")
        self.image = pygame.transform.scale(img,(tile_size,tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
wisp_group = pygame.sprite.Group()
salty_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()


class world:
    def __init__(self, data):
        grass_image = pygame.image.load("Pictured/grass.png")
        stone_image = pygame.image.load("Pictured/stone.png")
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1 or tile == 2:
                    images = {1:stone_image, 2:grass_image}
                    img = pygame.transform.scale(images[tile], (46, 50))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img,img_rect)
                    self.tile_list.append(tile)
                elif tile == 6:
                    ghosty = wisp(col_count * tile_size, row_count * tile_size + (tile_size//2))
                    wisp_group.add(ghosty)
                elif tile == 3:
                    salty = salt(col_count * tile_size, row_count * tile_size + (tile_size//2))
                    salty_group.add(salty)
                elif tile == 4:
                    bye1 = powerup(col_count * tile_size, row_count * tile_size + (tile_size//2))
                    bye.add(bye1)
                elif tile == 9:
                    dusty = collectables(col_count * tile_size, row_count * tile_size + (tile_size//2))
                    star_group.add(dusty)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            display.blit(tile[0],tile[1])

class button:
    def __init__ (self,x,y,image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image,(160,60))
        self.rect = self.image.get_rect(center=(x,y))

    def draw(self):
        action = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        display.blit(self.image,self.rect)
        return action

restart = button(width //2, height //2, "Pictured/restart.png")
exit = button(width //2, height //2+50, "Pictured/exit.png")
start = button(width //2, height //2-50, "Pictured/start.png")

class player:
    def __init__(self):
        self.image = pygame.image.load("Pictured/baby2.png")
        self.image = pygame.transform.scale(self.image,(tile_size,tile_size))
        self.dead = pygame.image.load("Pictured/dead.jpeg")
        self.image = pygame.transform.scale(self.image,(50, 70))
        self.dead = pygame.transform.scale(self.dead,(55, 70))
        self.rect = self.image.get_rect()
        self.gravity = 0
        self.jumped = False
        self.rect.x = 100
        self.rect.y = 130
        self.width = self.image.get_width()
        self.height = self.image.get_height()


    def update(self):
        global game_over
        y = 0
        x = 0
        if game_over == 0:


            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.gravity = -15
                self.jumped = True
            if key[pygame.K_a]:
                x -= 3
            if key[pygame.K_d]:
                x += 3

            self.gravity += 1
            if self.gravity > 10:
                self.gravity = 10
            y += self.gravity
            if pygame.sprite.spritecollide(self, wisp_group, False) or pygame.sprite.spritecollide(self, salty_group, False):
                game_over = -1
                death.play()
            if pygame.sprite.spritecollide(self, bye, False):
                game_over = 1
        elif game_over == -1:
            self.image = self.dead
            if self.rect.y > 0:
                self.rect.y -= 5
        display.blit(self.image, self.rect)
        for tile in lev1.tile_list:
            if tile[1].colliderect(self.rect.x + x, self.rect.y, self.width, self.height):
                x = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + y, self.width, self.height):
                if self.gravity < 0:
                    y = tile[1].bottom - self.rect.top
                    self.gravity = 0
                elif self.gravity >= 0:
                    y = tile[1].top - self.rect.bottom
                    self.gravity = 0
                    self.jumped = False


        self.rect.x += x
        self.rect.y += y
        if self.rect.bottom >height:
            self.rect.bottom = height

class powerup(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        image = pygame.image.load("Pictured/door.png")
        self.image = pygame.transform.scale(image,(46,70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

bye = pygame.sprite.Group()

lev1 = world(level)

background = pygame.image.load("Pictured/ruinedgate.webp")
background = pygame.transform.scale(background,(width,870))
second = pygame.image.load("Pictured/castle.jpeg")
second = pygame.transform.scale(second, (width, 870))
backrect = background.get_rect()
babybun = player()
run = True

beginning = True

while run:
    clock.tick(fps)
    display.fill("#783b69")
    if lev == 1:
        display.blit(background, backrect)
    if lev == 2:
        display.blit(second, backrect  )
    if beginning:
        if start.draw():
            beginning = False
            chances = 3
            lev = 1
            lev1 = nextlevel()
        if exit.draw():
            run = False
    else:
        babybun.update()
        lev1.draw()
        wisp_group.draw(display)
        star_group.draw(display)
        salty_group.draw(display)
        bye.draw(display)
        wisp_group.update()

        if game_over == -1:
            if restart.draw():
                chances -= 1
                if chances == 0:
                    beginning = True
                babybun = player()
                lev = lev
                game_over = 0

        if game_over == 1:
            game_over = 0
            if lev == 2:
                display.blit(second, backrect)
            if lev < maxlevel:
                lev += 1
                lev1 = nextlevel()
            else:
                print("Congrats! You accomplished something!")
                beginning = True


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()