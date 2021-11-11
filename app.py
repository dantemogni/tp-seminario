import pygame, random

from pygame.constants import KEYDOWN
from pygame.key import start_text_input

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.image.load("assets/fondo.png").convert()
        self.pause_background = pygame.image.load("assets/fondo-pausa.png").convert()
        self.game_background = pygame.image.load("assets/fondo-juego.png").convert()
        self.ship_background = pygame.image.load("assets/fondo-nave.png").convert()
        self.explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
        self.sonidos_img_verde = pygame.image.load("assets/boton_sonidos_verde.png")
        self.sonidos_img_rojo = pygame.image.load("assets/boton_sonidos_rojo.png")
        self.musica_img_verde = pygame.image.load("assets/boton_musica_verde.png")
        self.musica_img_rojo = pygame.image.load("assets/boton_musica_rojo.png")
        self.explosion_sound.set_volume(0.2)
        self.game_over = True 
        self.running = True
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.bullets = pygame.sprite.Group()
        self.paused = False
        self.sound_on = True
        self.music_on = True

    #Pantalla de inicio
    def show_go_screen(self):
        self.screen.blit(self.background, [0,0])
        self.draw_logo(self.screen, "SHOOTER", WIDTH // 2, HEIGHT // 3)
        self.draw_text_general(self.screen, "Presione 'ENTER' para iniciar", WIDTH // 2, HEIGHT / 1.3)
        self.draw_text_general(self.screen, "Presione 'ESC' para salir", WIDTH // 2, HEIGHT / 1.2)
        pygame.display.flip()

        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pygame.event.get():
                # Si el usuario cierra el programa
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # Si el usuario presiona "Enter"
                if event.type == pygame.KEYUP: 
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        waiting = False
        
                # Si el usuario presiona "ESC"    
                if event.type == pygame.KEYUP: 
                    if event.key == pygame.K_ESCAPE:      
                        pygame.quit()
                        quit()

    # Pantalla para elegir la dificultad
    def choose_difficulty(self):
        self.screen.blit(self.ship_background, [0,0])

        self.draw_text_titles(self.screen, "Elige la dificultad", WIDTH // 2, HEIGHT / 2.7)

        self.draw_text_general(self.screen, "1 - Muy Facil", WIDTH * 4/30, HEIGHT * 6/10)
        self.draw_text_general(self.screen, "2 - Facil", WIDTH / 3.15, HEIGHT * 6/10)
        self.draw_text_general(self.screen, "3 - Normal", WIDTH / 2, HEIGHT * 6/10)
        self.draw_text_general(self.screen, "4 - Dificil", WIDTH / 1.48, HEIGHT * 6/10)
        self.draw_text_general(self.screen, "5 - Extremo ;)", WIDTH / 1.15, HEIGHT * 6/10)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP: 
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        waiting = False 
                        return 1 
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        waiting = False 
                        return 2
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        waiting = False 
                        return 3
                    if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        waiting = False 
                        return 4
                    if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        waiting = False 
                        return 5


    #Pantalla para elegir nave
    def choose_ship(self):
        self.screen.blit(self.ship_background, [0,0])
        self.draw_text_titles(self.screen, "Elige la nave", WIDTH // 2, HEIGHT / 7)

        self.image = pygame.image.load("assets/avion2-costado.png")
        self.screen.blit(self.image, [WIDTH * 2/20, HEIGHT * 4/10])
        self.draw_text_general(self.screen, "1 - Boeing 747", WIDTH * 4/20, HEIGHT * 6/10)
        
        self.image = pygame.image.load("assets/halconM.png").convert()
        self.image.set_colorkey(BLACK)
        self.screen.blit(self.image, [WIDTH * 8/20, HEIGHT * 4/10])
        self.draw_text_general(self.screen, "2 - Halcon Milenario", WIDTH // 2, HEIGHT * 6/10)

        self.image = pygame.image.load("assets/elmo.png")
        self.screen.blit(self.image, [WIDTH * 14/20, HEIGHT * 2.3/10])
        self.draw_text_general(self.screen, "3 - Elmo", WIDTH * 16/20, HEIGHT * 6/10)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP: 
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        waiting = False 
                        return "avion2" #   aca iria el nombre del png
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        waiting = False 
                        return "halcon"
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        waiting = False 
                        return "nave3"
        
    def game_over_screen(self):
        self.screen.blit(self.game_background, [0,0])
        self.draw_logo(self.screen, "SHOOTER", WIDTH // 2, HEIGHT // 4)
        self.draw_text_titles(self.screen, "FIN DEL JUEGO", WIDTH // 2, HEIGHT / 2)
        self.draw_text_general(self.screen, "Puntaje total: " + str(self.score), WIDTH // 2, HEIGHT / 1.6)
        self.draw_text_general(self.screen, "Presione 'ENTER' para volver a jugar", WIDTH // 2, HEIGHT / 1.3)
        self.draw_text_general(self.screen, "Presione 'ESC' para salir", WIDTH // 2, HEIGHT / 1.2)
        pygame.display.flip()

        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pygame.event.get():
                # Si el usuario cierra el programa
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # Si el usuario presiona "Enter"
                if event.type == pygame.KEYUP: 
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:      
                        waiting = False 
                        return       
                # Si el usuario presiona "ESC"    
                if event.type == pygame.KEYUP: 
                    if event.key == pygame.K_ESCAPE:      
                        pygame.quit()
                        quit()


    def pause_screen(self, player):
        self.paused = True

        #botones
        self.sonidos_verde = Button(WIDTH-160,25,self.sonidos_img_verde, 0.7)                
        self.sonidos_rojo = Button(WIDTH-160,25,self.sonidos_img_rojo, 0.7)
        self.musica_verde = Button(WIDTH-160,85,self.musica_img_verde, 0.7)
        self.musica_rojo = Button(WIDTH-160,85,self.musica_img_rojo, 0.7)
        
        while self.paused:
            self.running = False
            self.draw_text_titles(self.pause_background, "PAUSA", WIDTH // 2, HEIGHT / 2)
            self.draw_text_general(self.pause_background, "Presione 'P' o 'Esc' para continuar",  WIDTH // 2, HEIGHT / 1.3)
            self.draw_text_general(self.pause_background, "Presione 'Q' para salir", WIDTH // 2, HEIGHT / 1.2)
            self.screen.blit(self.pause_background, [0, 0])

            if game.sound_on:
                if self.sonidos_verde.draw():
                    game.sound_on = False
                    game.explosion_sound.set_volume(0)
                    player.laser_sound.set_volume(0)
            elif self.sonidos_rojo.draw():
                    game.sound_on = True
                    game.explosion_sound.set_volume(0.2)
                    player.laser_sound.set_volume(1)    

            if game.music_on:
                if self.musica_verde.draw():
                    game.music_on = False
                    pygame.mixer.music.pause()   
            elif self.musica_rojo.draw():
                    game.music_on = True
                    pygame.mixer.music.unpause()   

            pygame.display.update()
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.paused = False
                        self.running = True
                        return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
#--------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------Comienzo del loop juego--------------------------------------------
    def main_loop(self):
        self.show_go_screen() #pantalla de inicio
        
        while self.running:
            if self.game_over:
                self.game_over = False

                difficulty = self.choose_difficulty()
                ship_image = self.choose_ship() #pantalla para elegir nave (solo hay 1 por ahora)

                self.all_sprites = pygame.sprite.Group()
                meteor_list = pygame.sprite.Group()
                self.bullets = pygame.sprite.Group()
                
                #Jugador
                player = Player(ship_image)
                self.all_sprites.add(player)

                # Variables de tiempo
                start_timer = pygame.time.get_ticks()
                pause_msg_timer = pygame.time.get_ticks()
                retore_health_timer = pygame.time.get_ticks()

                self.score = 0

                if game.sound_on == False:
                    game.explosion_sound.set_volume(0)
                    player.laser_sound.set_volume(0)

                if(difficulty == 1):
                    for i in range(3):
                        meteor = Meteor()
                        self.all_sprites.add(meteor)
                        meteor_list.add(meteor)
                elif (difficulty == 2):
                     for i in range(5):
                        meteor = Meteor()
                        self.all_sprites.add(meteor)
                        meteor_list.add(meteor)
                elif (difficulty == 3):
                     for i in range(9):
                        meteor = Meteor()
                        self.all_sprites.add(meteor)
                        meteor_list.add(meteor)
                elif (difficulty == 4):
                     for i in range(14):
                        meteor = Meteor()
                        self.all_sprites.add(meteor)
                        meteor_list.add(meteor)
                else:
                    for i in range(24):
                        meteor = Meteor()
                        self.all_sprites.add(meteor)
                        meteor_list.add(meteor)    
        
            self.clock.tick(60)   #Velocidad del juego

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.shoot()
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.pause_screen(player)
        
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

            # Colisiones - jugador - meteoro
            hits = pygame.sprite.spritecollide(player, meteor_list, True, pygame.sprite.collide_mask)
            for hit in hits:
                player.shield -= 25 # Al ser chocado, disminuye en 25 su salud
                meteor = Meteor()
                self.explosion_sound.play()
                explosion = Explosion(hit.rect.center)
                self.all_sprites.add(meteor)
                self.all_sprites.add(explosion)
                meteor_list.add(meteor)
                if player.shield <= 0: # si el jugador se queda sin puntos pierde
                    self.game_over_screen()
                    self.game_over = True


            self.screen.blit(self.game_background, [0, 0])

            self.all_sprites.draw(self.screen)

            #Marcador
            self.draw_text_general(self.screen, str(self.score), WIDTH * 33/35, 10)
            self.draw_text_general(self.screen, "Puntaje:", WIDTH * 30/35, 10)

            # Escudo.
            self.draw_shield_bar(self.screen, 5, 5, player.shield)
            self.draw_text_general(self.screen, "Salud",  WIDTH * 3/35, HEIGHT * 1/35)

            # Muestro mensaje de pausa en los primeros 4 segundos
            if pygame.time.get_ticks() - pause_msg_timer < 4000:
                self.draw_text_general(self.screen, "Presione 'P' o 'ESC' para pausar el juego", WIDTH // 2, HEIGHT * 6/10)

            # Aumenta la salud del jugador cada 4 segundos 
            if pygame.time.get_ticks() - retore_health_timer > 4000:
                if player.shield < 100:
                    player.shield += 5
                retore_health_timer = pygame.time.get_ticks() # reinicia el contador

            pygame.display.flip()

        pygame.quit()
    
    def draw_logo(self, surface, text, x, y):
        text_surface = font_logo.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    #Escribir texto en pantalla
    def draw_text_general(self, surface, text, x, y):
        text_surface = font_general.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)
    
    def draw_text_titles(self, surface, text, x, y):
        text_surface = font_titles.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    #Barra de vida
    def draw_shield_bar(self, surface, x, y, percentage):
        BAR_LENGHT = 100
        BAR_HEIGHT = 10
        fill = (percentage / 100) * BAR_LENGHT
        border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
        fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surface, GREEN, fill)
        pygame.draw.rect(surface, WHITE, border, 2)


#-----------------------------------------------------Fin del loop juego---------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        """Creamos los atributos del jugador"""
        super().__init__()
        self.laser_sound = pygame.mixer.Sound("assets/sounds/laser5.wav")
        self.image = pygame.image.load("assets/" + image + ".png").convert()
        self.image.set_colorkey(BLACK)  
        self.rect = self.image.get_rect()
        #mascara
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.shield = 100 # Salud

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

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True               
            else:
                if self.clicked == True:
                    action = True
                    self.clicked = False

        game.pause_background.blit(self.image, (self.rect.x, self.rect.y))

        return action

if __name__ == '__main__':
    """Esto es lo primero que se ejecuta cuando se llama a app.py"""
    pygame.init()

    font_logo    = pygame.font.Font("./assets/fonts/Quicksilver Italic.ttf", 90)
    font_general = pygame.font.Font("./assets/fonts/8-bit-hud.ttf", 10)
    font_titles  = pygame.font.Font("./assets/fonts/8-bit-hud.ttf", 20)

    pygame.mixer.init()
    pygame.display.set_caption("Shooter")
    pygame.mixer.music.load("assets/sounds/music.wav")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1)
    pygame.font.SysFont("arial", 14)
    
    game = Game()
    game.main_loop()

# TODO: Seleccion de naves mediante las flechas del teclado
