import pygame, random

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.image.load("assets/fondo2.png").convert()
        self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
        self.game_over = True
        self.running = True
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.bullets = pygame.sprite.Group()


    def show_go_screen(self):
        self.screen.blit(self.background, [0,0])
        self.draw_text(self.screen, "SHOOTER", 65, WIDTH // 2, HEIGHT // 4)
        self.draw_text(self.screen, "Instruciones van aquí", 27, WIDTH // 2, HEIGHT // 2)
        self.draw_text(self.screen, "Press Key", 20, WIDTH // 2, HEIGHT * 3/4)
        pygame.display.flip()

        waiting = True
        while waiting:
            #self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False
    

    def main_loop(self):
        while self.running:
            if self.game_over:
                self.show_go_screen()
                self.game_over = False

                self.all_sprites = pygame.sprite.Group()
                meteor_list = pygame.sprite.Group()
                self.bullets = pygame.sprite.Group()
                
                player = Player()
                self.all_sprites.add(player)

                for i in range(8):
                    meteor = Meteor()
                    self.all_sprites.add(meteor)
                    meteor_list.add(meteor)
                self.score = 0

            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.shoot()

            self.all_sprites.update()

            #colisiones - meteoro - laser
            hits = pygame.sprite.groupcollide(meteor_list, self.bullets, True, True)
            for hit in hits:
                self.score += 10
                self.explosion_sound.play()
                explosion = Explosion(hit.rect.center)
                self.all_sprites.add(explosion)
                meteor = Meteor()
                self.all_sprites.add(meteor)
                meteor_list.add(meteor)

            # Checar colisiones - jugador - meteoro
            hits = pygame.sprite.spritecollide(player, meteor_list, True)
            for hit in hits:
                player.shield -= 25
                meteor = Meteor()
                self.all_sprites.add(meteor)
                meteor_list.add(meteor)
                if player.shield <= 0: # si el jugador se queda sin puntos pierde
                    self.game_over = True

            self.screen.blit(self.background, [0, 0])

            self.all_sprites.draw(self.screen)

            #Marcador
            self.draw_text(self.screen, str(self.score), 25, WIDTH // 2, 10)

            # Escudo.
            self.draw_shield_bar(self.screen, 5, 5, player.shield)

            pygame.display.flip()

        pygame.quit()

    def draw_text(self, surface, text, size, x, y):
        font = pygame.font.SysFont("serif", size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def draw_shield_bar(self, surface, x, y, percentage):
        BAR_LENGHT = 100
        BAR_HEIGHT = 10
        fill = (percentage / 100) * BAR_LENGHT
        border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
        fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surface, GREEN, fill)
        pygame.draw.rect(surface, WHITE, border, 2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        """Creamos los atributos del jugador"""
        super().__init__()
        self.laser_sound = pygame.mixer.Sound("assets/sounds/laser5.ogg")
        self.image = pygame.image.load("assets/nave.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.shield = 100

    def update(self):
        """Genera el movimiento"""
        speed = 8
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if keystate[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += speed 
        if keystate[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= speed
        if keystate[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        game.all_sprites.add(bullet)
        game.bullets.add(bullet)
        self.laser_sound.play()


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        """Imagenes de los meteoritos"""
        self.meteor_images = []
        self.meteor_list = ["assets/meteoro_big1.png", "assets/meteoro_big2.png", "assets/meteoro_big3.png", "assets/meteoro_big4.png",
			    "assets/meteoro_med1.png", "assets/meteoro_med2.png",]

        for img in self.meteor_list:
            self.meteor_images.append(pygame.image.load(img).convert())

        self.image = random.choice(self.meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)


    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, - 100)
            self.speedy = random.randrange(1, 10)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()

        self.explosion_anim = []
        for i in range(9):
            file = "assets/regularExplosion0{}.png".format(i)
            img = pygame.image.load(file).convert()
            img.set_colorkey(BLACK)
            img_scale = pygame.transform.scale(img, (70,70))
            self.explosion_anim.append(img_scale)

        self.image = self.explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # VELOCIDAD DE LA EXPLOSION

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


if __name__ == '__main__':
    """Esto es lo primero que se ejecuta cuando se llama a app.py"""
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Shooter")
    pygame.mixer.music.load("assets/sounds/music.ogg")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1)

    game = Game()
    game.main_loop()
