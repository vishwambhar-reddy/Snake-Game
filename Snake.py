import pygame
import random
import time

#initialise pygame
pygame.init()
#screen dimensions
x=757
y=635
#velocity of snake, initially snake moves to the right
vx_snake=10
vy_snake=0

#Display Settings
Window= pygame.display.set_mode((x,y))
bg=pygame.image.load('Background.jpg')
pygame.display.set_caption("Snake")
#clock variable to set fps
clock=pygame.time.Clock()

#Sound Settings
GameOver_Sound=pygame.mixer.Sound('sounds_dead.wav')
Eat_Sound=pygame.mixer.Sound('sounds_eat.wav')
bgm=pygame.mixer.music.load('Background music.mp3')
pygame.mixer.music.play(-1,0.0)

#initialise snake as a list
snake_pos=[300,300]
snake_body=[[290,300],[280,300],[270,300],[260,300]]

#Variables to store the score and current direction, initial direction is RIGHT
score=0
direction='RIGHT'

#Function to spawn food
def Spawn_food(snake_body):
    pos=[random.randrange(5,70)*10,random.randrange(5,57)*10]
    #Makes sure that the food is not spawned on top of the snake
    if pos in snake_body:
        Spawn_food(snake_body)
    else:
        return pos

#Initialise food
food_pos=Spawn_food(snake_body)
food_spawned=True

def write_message(font,size,message,color,coordinates,var=''):
    msg_font=pygame.font.SysFont(font,size)
    if var!='':
        msg=msg_font.render(str(message)+' : '+str(var),True,color)
    else:
        msg=msg_font.render(str(message),True,color)
    msg_surface=msg.get_rect()
    if coordinates!=(0,0):
        msg_surface.midtop=coordinates
    Window.blit(msg,msg_surface)


#Game Over function, called when the game over conditions are reached
def game_over():
    pygame.mixer.music.stop()
    GameOver_Sound.play()
    write_message('Comic Sans MS',50,'Game Over!!!',pygame.Color(0,0,0),(x//2,y//4))
    write_message('Comic Sans MS',30,'Score',pygame.Color(0,0,0),(x//2,y//2),score)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit()

#variable to keep the loop running
loop=True

#Main Game loop
while loop:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            loop=False
        if event.type == pygame.KEYDOWN:
            #The if conditions make sure that a 180 degree turn does not happen
            if event.key==pygame.K_UP and direction!='DOWN':
                direction='UP'
                vy_snake=-10
                vx_snake=0
            elif event.key==pygame.K_DOWN and direction!='UP':
                direction='DOWN'
                vy_snake=10
                vx_snake=0
            elif event.key==pygame.K_RIGHT and direction!='LEFT':
                direction='RIGHT'
                vx_snake=10
                vy_snake=0
            elif event.key==pygame.K_LEFT and direction!='RIGHT':
                direction='LEFT'
                vx_snake=-10
                vy_snake=0
    
    #Update the position of snake head
    snake_pos[0]+=vx_snake
    snake_pos[1]+=vy_snake
    
    #Logic for snake movement and increase in length when it eats
    snake_body.insert(0, list(snake_pos))
    if abs(snake_pos[0]-food_pos[0])<=10 and abs(snake_pos[1]-food_pos[1])<=10:
        Eat_Sound.play()
        score += 10
        food_spawned = False
    else:
        snake_body.pop()

    #Spawning food once the current food is eaten    
    if not food_spawned:
        food_pos = Spawn_food(snake_body)
        food_spawned = True
    
    #Drawing screen, snake and food
    Window.blit(bg,(0,0))  
    for body in snake_body:
        pygame.draw.rect(Window, pygame.Color(75,0,130),pygame.Rect(body[0], body[1], 10, 10))
    pygame.draw.circle(Window, pygame.Color(255,0,0), food_pos, 5)

    #Game Over Conditions  
    if snake_pos[0] < 40 or snake_pos[0] > 710:
        game_over()
    if snake_pos[1] < 40 or snake_pos[1] > 590:
        game_over()
    if snake_pos in snake_body[1:]:
        game_over()
    
    #display score
    write_message('Comic Sans MS',20,'Score',pygame.Color(255,255,255),(0,0),score)
    #Update screen
    pygame.display.update()
    clock.tick(15)
    
pygame.quit()