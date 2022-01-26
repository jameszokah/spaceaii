import pygame 
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WHITE = (255,255,255)
BLACK = (0,0,0)

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("spaceAII")


HEALTH_FONT = pygame.font.SysFont(name="comicsans",size=40)
WINNER_FONT = pygame.font.SysFont(name="comicsans",size=100)


FTP = 60
VEL = 5
BULLET_VEL = 7  
MAX_BULLETS = 3
clock = pygame.time.Clock
PLAYER_WIDTH = 90
PLAYER_HEIGHT = 120

BULLET_WIDTH = 60
BULLET_HEIGHT = 20

PLAYER1_HITS = pygame.USEREVENT + 1
PLAYER2_HITS = pygame.USEREVENT + 2

GAME_LOGO = pygame.image.load(os.path.join("Assets","spaceaii.png"))

pygame.display.set_icon(GAME_LOGO)

PLAYER1_IMAGE = pygame.image.load(os.path.join("Assets","player1.png"))
PLAYER2_IMAGE = pygame.image.load(os.path.join("Assets","player2.png"))

PLAYER1_BULLET = pygame.image.load(os.path.join("Assets","player1-bullet.png"))
PLAYER2_BULLET = pygame.image.load(os.path.join("Assets","player2-bullet.png"))

SPACEBG = pygame.image.load(os.path.join("Assets","space-bg.gif"))

EXPLOSION = pygame.mixer.Sound(os.path.join("Assets","explosion.mp3"))
SPACE_SOUND = pygame.mixer.Sound(os.path.join("Assets","space_sound.mp3"))
WIN_SOUND = pygame.mixer.Sound(os.path.join("Assets","win-sound.mp3"))
PLAYER1_GUNSHOT = pygame.mixer.Sound(os.path.join("Assets","player1-gunshot.mp3"))
PLAYER2_GUNSHOT = pygame.mixer.Sound(os.path.join("Assets","player2-gunshot.mp3"))



PLAYER1 = pygame.transform.rotate(pygame.transform.scale(PLAYER1_IMAGE,(PLAYER_WIDTH,PLAYER_HEIGHT)),115)
PLAYER2 = pygame.transform.rotate(pygame.transform.scale(PLAYER2_IMAGE,(PLAYER_WIDTH,PLAYER_HEIGHT)),300)

BULLET1 = pygame.transform.rotate(pygame.transform.scale(PLAYER1_BULLET,(BULLET_HEIGHT,BULLET_WIDTH)),270)
BULLET2 = pygame.transform.rotate(pygame.transform.scale(PLAYER2_BULLET,(BULLET_WIDTH,BULLET_HEIGHT)),0)


SPACE = pygame.transform.rotate(pygame.transform.scale(SPACEBG,(WIDTH,HEIGHT)),0)


BORDER = pygame.Rect((WIDTH//2) - 5,0,8,HEIGHT)

def draw_winner(text):
    draw_winner_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_winner_text,(WIDTH /2 - draw_winner_text.get_width() / 2, HEIGHT / 2 - draw_winner_text.get_height() /2))
    
    pygame.display.update()
    pygame.time.delay(5000)

def draw_window(player1,player2,player1_bullets,player2_bullets,player1_health,player2_health):
   
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,BLACK, BORDER)
    WIN.blit(PLAYER1,(player1.x,player1.y))
    WIN.blit(PLAYER2,(player2.x,player2.y))

    player1_health_text = HEALTH_FONT.render("Health: " + str(player1_health),1, WHITE)
    player2_health_text = HEALTH_FONT.render("Health: " + str(player2_health),1, WHITE)

    WIN.blit(player1_health_text,(10,10))
    WIN.blit(player2_health_text,(WIDTH - player2_health_text.get_width() - 10,10))

    for bullet in player1_bullets:
        WIN.blit(BULLET1,(bullet.x,bullet.y))
        


    for bullet in player2_bullets:
        WIN.blit(BULLET2,(bullet.x,bullet.y))
        


    pygame.display.update()


def player_handle_movements(key_pressed,player,player_type):
    if(player_type == "player1"):
        if key_pressed[pygame.K_a] and player.x - VEL > 0:
            player.x -= VEL

        elif key_pressed[pygame.K_d] and player.x + VEL + player.width  + 46 < BORDER.x:
            player.x += VEL

        elif key_pressed[pygame.K_w] and player.y - VEL > 0:
            player.y -= VEL

        elif key_pressed[pygame.K_s] and player.y + VEL + player.height < HEIGHT :
            player.y += VEL

    elif(player_type == "player2"):
        if key_pressed[pygame.K_LEFT] and player.x - VEL > BORDER.x + BORDER.width:
            player.x -= VEL

        elif key_pressed[pygame.K_RIGHT] and player.x + VEL + player.width + 30 < WIDTH:
            player.x += VEL

        elif key_pressed[pygame.K_UP] and player.y - VEL > 0:
            player.y -= VEL

        elif key_pressed[pygame.K_DOWN] and player.y + VEL + player.height < HEIGHT:
            player.y += VEL


def handle_bullets(player1_bullets,player2_bullets,player1,player2):
    for bullet in player1_bullets:
        bullet.x += BULLET_VEL
        if player2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYER1_HITS))
            player1_bullets.remove(bullet)

        elif bullet.x > WIDTH: 
            player1_bullets.remove(bullet)

    for bullet in player2_bullets:
        bullet.x -= BULLET_VEL
        if player1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYER2_HITS))
            player2_bullets.remove(bullet)


        elif bullet.x < 0: 
            player2_bullets.remove(bullet)

def main():
    player1 = pygame.Rect(100,100,PLAYER_WIDTH,PLAYER_HEIGHT)
    player2 = pygame.Rect(700,100,PLAYER_WIDTH,PLAYER_HEIGHT)

    player1_bullets = []
    player2_bullets = []

    player1_health = 15
    player2_health = 15
    
    # clock.tick(FTP)
    run = True
    SPACE_SOUND.play()
    while run:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
                pygame.quit()

            if(event.type == pygame.KEYDOWN):
                if event.key == pygame.K_LCTRL and len(player1_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(player1.x + player1.width,player1.y + player1.height // 2 -2,BULLET_WIDTH,BULLET_WIDTH)
                    player1_bullets.append(bullet)
                    PLAYER1_GUNSHOT.play()
                    

                elif event.key == pygame.K_RCTRL and len(player2_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(player2.x ,player2.y + player2.height // 2 -2,BULLET_WIDTH,BULLET_HEIGHT)
                    player2_bullets.append(bullet)
                    PLAYER2_GUNSHOT.play()

            
            if event.type == PLAYER1_HITS:
                player2_health -= 1


            if event.type == PLAYER2_HITS:
                player1_health -= 1

        winner_text = "" 
        if player1_health <= 0:
            winner_text = "PLAYER 2 WINS"
            WIN_SOUND.play()

        if player2_health <= 0:
            winner_text = "PLAYER 1 WINS"
            WIN_SOUND.play()

        if winner_text != "":
            draw_winner(winner_text)
            # WIN_SOUND.play()
            break
            
        
        

        # print(player2_bullets,player2_bullets)

        draw_window(player1,player2,player1_bullets,player2_bullets,player1_health,player2_health)
        handle_bullets(player1_bullets,player2_bullets,player1,player2)
        key_pressed = pygame.key.get_pressed()
        player_handle_movements(key_pressed,player1,"player1")
        player_handle_movements(key_pressed,player2,"player2")


    main()



if __name__ == "__main__":
    main()