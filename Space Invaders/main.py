import pygame
import os
import time
import random
import sys

pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "b4.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 20

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj) :
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+15, self.y-35, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.n=0


    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        self.lasers.remove(laser)
                        objs.remove(obj)
                        self.n=self.n+5

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+27, self.y+50, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def game(n,s):
    run = True
    FPS = 60
    level = 0
    lives = 5
    ok1=0
    def_ship = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
    ship1 = pygame.image.load(os.path.join("assets", "ship1.png"))
    ship2 = pygame.image.load(os.path.join("assets", "ship2.png"))
    ship3 = pygame.image.load(os.path.join("assets", "ship3.png"))
    ship4 = pygame.image.load(os.path.join("assets", "ship4.png"))
    ship5 = pygame.image.load(os.path.join("assets", "ship5.png"))
    ship6 = pygame.image.load(os.path.join("assets", "ship6.png"))
    ship7 = pygame.image.load(os.path.join("assets", "ship7.png"))
    space_list=[def_ship,ship1,ship2,ship3,ship4,ship5,ship6,ship7]

    b1 = pygame.image.load(os.path.join("assets", "b1.png"))
    b2 = pygame.image.load(os.path.join("assets", "b2.png"))
    b3 = pygame.image.load(os.path.join("assets", "b3.png"))
    b4 = pygame.image.load(os.path.join("assets", "b4.png"))
    laser_list=[b1,b2,b3,b4,b1,b2,b3,b4]
    c_no=n
    game_font = pygame.font.SysFont("Corbel", 45)
    lost_font = pygame.font.SysFont("Corbel", 45)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 10
    laser_vel = 5

    player = Player(300, 630)
    player.ship_img=space_list[s]
    player.laser_img=laser_list[s]
    player.n = n
    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window(ok1):
        WIN.blit(BG, (0,0))
        for enemy in enemies:
            enemy.draw(WIN)

        lives_icon=pygame.image.load(os.path.join("assets", "live.png"))
        level_icon=pygame.image.load(os.path.join("assets", "level.png"))
        lives_label = game_font.render(f"{lives}", 1, (255, 255, 255))
        level_label = game_font.render(f"{level}", 1, (0, 0, 0))
        settings=pygame.image.load(os.path.join("assets", "settings.png"))
        coin = pygame.image.load(os.path.join("assets", "coins.png"))
        WIN.blit(lives_icon,(WIDTH - level_label.get_width() - 200, 18))
        WIN.blit(lives_label,(WIDTH - level_label.get_width() - 230, 5))
        WIN.blit(level_icon, (0, 6))
        WIN.blit(settings, (WIDTH - level_label.get_width() - 20, 15))
        WIN.blit(level_label, (22, 12))
        coin_number = game_font.render(f"{c_no}", 1, (255, 255, 255))
        WIN.blit(coin_number,(WIDTH - level_label.get_width() - 133, 10))
        WIN.blit(coin,(WIDTH - level_label.get_width() - 90, 0))
        player.draw(WIN)

        if ok1==1:
            main_menu(player.n, state,buyed,s)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window(ok1)

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y=event.pos
                if x>=710 and x<=730 and y>=14 and y<=46:
                    ok1=1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)


        player.move_lasers(-laser_vel, enemies)
        c_no=player.n



def store_game(n, state, buyed,s):
    run = True
    FPS = 60
    game_font = pygame.font.SysFont("Corbel", 50)
    coin = pygame.image.load(os.path.join("assets", "coins.png"))
    back = pygame.image.load(os.path.join("assets", "back.png"))
    def_ship=pygame.image.load(os.path.join("assets/store", "my_deffault_ship.png"))
    ship1=pygame.image.load(os.path.join("assets/store", "ship1.png"))
    ship2 = pygame.image.load(os.path.join("assets/store", "ship2.png"))
    ship3 = pygame.image.load(os.path.join("assets/store", "ship3.png"))
    ship4 = pygame.image.load(os.path.join("assets/store", "ship4.png"))
    ship5 = pygame.image.load(os.path.join("assets/store", "ship5.png"))
    ship6 = pygame.image.load(os.path.join("assets/store", "ship6.png"))
    ship7 = pygame.image.load(os.path.join("assets/store", "ship7.png"))
    arrow_left=pygame.image.load(os.path.join("assets/store", "arl.png"))
    arrow_right=pygame.image.load(os.path.join("assets/store", "arr.png"))
    uncheck=pygame.image.load(os.path.join("assets/store", "uncheck.png"))
    check = pygame.image.load(os.path.join("assets/store", "check.png"))
    buy = pygame.image.load(os.path.join("assets/store", "buy.png"))
    gray_buy=pygame.image.load(os.path.join("assets/store", "gray_buy.png"))
    images=[def_ship,ship1,ship2,ship3,ship4,ship5,ship6,ship7]
    prices=[0,5,15,20,25,30,35,40]
    clock = pygame.time.Clock()
    back_button=0
    buy_button=0
    select_button=0

    i=0
    c_no=n

    while run:
        clock.tick(FPS)
        if state[i]==0:
            WIN.blit(BG, (0, 0))
            lives_label = game_font.render("Store", 1, (255, 255, 255))
            coin_number = game_font.render(f"{c_no}", 1, (255, 255, 255))
            WIN.blit(lives_label, (0, 0))
            WIN.blit(coin, (600, -10))
            WIN.blit(coin_number, (655, -3))
            WIN.blit(back, (10, 675))
            WIN.blit(arrow_left, (100, 350))
            WIN.blit(arrow_right, (590, 350))
            WIN.blit(images[i], (250, 250))
            WIN.blit(check, (362, 550))
        elif state[i]==1:
            WIN.blit(BG, (0, 0))
            lives_label = game_font.render("Store", 1, (255, 255, 255))
            coin_number = game_font.render(f"{c_no}", 1, (255, 255, 255))
            price = game_font.render(f"{prices[i]}", 1, (255, 255, 255))
            WIN.blit(lives_label, (0, 0))
            WIN.blit(coin, (600, -10))
            WIN.blit(coin_number, (655, -3))
            WIN.blit(back, (10, 675))
            WIN.blit(arrow_left, (100, 350))
            WIN.blit(arrow_right, (590, 350))
            WIN.blit(coin, (300, 164))
            WIN.blit(images[i], (250, 250))
            WIN.blit(price, (360, 170))
            WIN.blit(uncheck, (362, 550))
            WIN.blit(gray_buy, (348, 590))
        elif state[i]==2:
            WIN.blit(BG, (0, 0))
            lives_label = game_font.render("Store", 1, (255, 255, 255))
            coin_number = game_font.render(f"{c_no}", 1, (255, 255, 255))
            price = game_font.render(f"{prices[i]}", 1, (255, 255, 255))
            WIN.blit(lives_label, (0, 0))
            WIN.blit(coin, (600, -10))
            WIN.blit(coin_number, (655, -3))
            WIN.blit(back, (10, 675))
            WIN.blit(arrow_left, (100, 350))
            WIN.blit(arrow_right, (590, 350))
            WIN.blit(coin, (300, 164))
            WIN.blit(images[i], (250, 250))
            WIN.blit(price, (360, 170))
            WIN.blit(uncheck, (362, 550))
            WIN.blit(buy, (348, 590))
        elif state[i]==3:
            WIN.blit(BG, (0, 0))
            lives_label = game_font.render("Store", 1, (255, 255, 255))
            coin_number = game_font.render(f"{c_no}", 1, (255, 255, 255))
            WIN.blit(lives_label, (0, 0))
            WIN.blit(coin, (600, -10))
            WIN.blit(coin_number, (655, -3))
            WIN.blit(back, (10, 675))
            WIN.blit(arrow_left, (100, 350))
            WIN.blit(arrow_right, (590, 350))
            WIN.blit(images[i], (250, 250))
            WIN.blit(uncheck, (362, 550))

        if buy_button==1 and c_no>=prices[i]:
            c_no=c_no-prices[i]
            l=0

            for p in prices:
                if c_no<=p and buyed[l]!=1 :
                    state[l]=1
                l=l+1
            state[i] = 3
            buyed[i] = 1
            buy_button = 0

        if select_button==1 and buyed[i]==1:
            k = 0
            for j in state:
                if j==0 :
                    state[k]=3
                k=k+1

            state[i]=0
            s=i
            select_button=0

        if back_button==1:
            main_menu(c_no, state, buyed,s)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y=event.pos
                if x>=590 and x<=650 and y>=350 and y<=412:
                    if i>=0 and i<=6:
                        i = i + 1
                    else:
                        i=0
                elif x >= 100 and x <= 163 and y >= 350 and y <= 412:
                    if i >=1 and i<= 7:
                        i = i - 1
                    else:
                        i = 7
                elif x >= 15 and x <= 70 and y >= 680 and y <= 730 :
                    back_button=1
                elif x>=350 and x<=411 and y>=603 and y<=640 and c_no>=prices[i]:
                    buy_button=1
                elif x>=362 and x<=393 and y>=550 and y<=580:
                    select_button=1



def main_menu(n, state, buyed,s):

    run = True


    # white color
    color = (255, 255, 255)

    # light shade of the button
    color_light = (170, 170, 170)

    # dark shade of the button
    color_dark = (100, 100, 100)


    # defining a font
    smallfont = pygame.font.SysFont('Corbel', 35)

    # rendering a text written in
    # this font
    start = smallfont.render('START', True, color)
    title = smallfont.render('Space Invaders', True, color)
    store = smallfont.render('STORE', True, color)
    quit = smallfont.render('QUIT', True, color)

    while run:
        WIN.blit(BG, (0, 0))
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH / 2 -start.get_width()/2 -33<= mouse[0] <= WIDTH / 2 -start.get_width()/2 + 107 and 245 <= mouse[1] <= 285:
                    game(n,s)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH / 2 - store.get_width() / 2 - 21 <= mouse[0] <= WIDTH / 2 - store.get_width() / 2 + 107 and 300 <= mouse[1] <= 340:
                    store_game(n, state, buyed,s)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH / 2 - quit.get_width() / 2<= mouse[0] <= WIDTH / 2 - quit.get_width() / 2 + 107 and 355 <= mouse[1] <= 395:
                    pygame.quit()

                # fills the screen with a color


                # stores the (x,y) coordinates into
                # the variable as a tuple


                # if mouse is hovered on a button it
                # changes to lighter shade

        if WIDTH / 2 -start.get_width()/2 -23<= mouse[0] <= WIDTH / 2 -start.get_width()/2 + 117 and 245 <= mouse[1] <= 285:
            pygame.draw.rect(WIN, color_light, [WIDTH / 2 -start.get_width()/2-23, 245, 140, 40])
        else:
            pygame.draw.rect(WIN, color_dark, [WIDTH / 2-start.get_width()/2-23, 245, 140, 40])

        if WIDTH / 2 - store.get_width() / 2 - 21 <= mouse[0] <= WIDTH / 2 - store.get_width() / 2 + 107 and 300 <= mouse[1] <= 340:
            pygame.draw.rect(WIN, color_light, [WIDTH / 2 - store.get_width() / 2 - 21, 300, 140, 40])
        else:
            pygame.draw.rect(WIN, color_dark, [WIDTH / 2 - store.get_width() / 2 - 21, 300, 140, 40])

        if WIDTH / 2 - quit.get_width() / 2 - 33 <= mouse[0] <= WIDTH / 2 - quit.get_width() / 2 + 107 and 355 <= mouse[1] <= 395:
            pygame.draw.rect(WIN, color_light, [WIDTH / 2 - quit.get_width() / 2 - 33, 355, 140, 40])
        else:
            pygame.draw.rect(WIN, color_dark, [WIDTH / 2 - quit.get_width() / 2 - 33, 355, 140, 40])


                # superimposing the text onto our button
        WIN.blit(title, (WIDTH / 2 - title.get_width() / 2, 100))
        WIN.blit(start, (WIDTH / 2 - start.get_width()/2, 250))
        WIN.blit(store, (WIDTH / 2 - store.get_width() / 2, 305))
        WIN.blit(quit, (WIDTH / 2 - quit.get_width() / 2, 360))
        pygame.display.update()

x=0
buyed=[1,0,0,0,0,0,0,0]
state=[0,1,1,1,1,1,1,1]
s=0
main_menu(x, state, buyed,s)