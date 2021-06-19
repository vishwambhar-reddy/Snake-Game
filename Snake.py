import pygame
import random
import time

#initialise pygame
pygame.init()
#screen dimensions, set so that the background image fits perfectly
x=757
y=635

#Color Settings
white=pygame.Color(255,255,255)
black=pygame.Color(0,0,0)
red=pygame.Color(255,0,0)
indigo=pygame.Color(75,0,130)

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

#Function to spawn food
def Spawn_food(snake_body):
    pos=[random.randrange(5,70)*10,random.randrange(5,57)*10]
    #Makes sure that the food is not spawned on top of the snake
    if pos in snake_body:
        Spawn_food(snake_body)
    else:
        return pos


#Function to display custom messages on the screen
#Here we use parameters 'coordinates' and 'var' for custom made messages
#If we specify non zero coordinates, the message will be printed with center allignment with center as the 
#coordinates, else if the coordinates are zero, the message will be printed with left allignment
#var is used to print any variable along with the message if it is mentioned
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

#Function for game rules and instuctions screen
def game_intro():
    #Game rules and instructions
    msg1="Use keyboard arrowkeys to move the snake"
    msg2="Everytime the snake eats the food, 10 points will be added to score"
    msg3="The snake dies when it crosses the green boundary or hits its own body"
    #Prompts the player to start the game
    msg4="Press 'Enter' to start"
    loop=True
    
    while loop:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                loop=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    loop=False
                    game_loop()
        
        Window.blit(bg,(0,0))
        write_message('Comic Sans MS',20,msg1,black,(x//2,y//3))
        write_message('Comic Sans MS',20,msg2,black,(x//2,y//3 + 20))
        write_message('Comic Sans MS',20,msg3,black,(x//2, y//3 + 40))
        write_message('Comic Sans MS',20,msg4,black,(x//2, y//3 + 60))
        pygame.display.update()
        clock.tick(15)


#Game Over function, takes final score as a parameter
def game_over(score):
    #Plays game over sound and stops the background music
    pygame.mixer.music.stop()
    GameOver_Sound.play()
    #Displays Game Over message
    write_message('Comic Sans MS',50,'Game Over!!!',black,(x//2,y//4))
    #Displays final score
    write_message('Comic Sans MS',30,'Score',black,(x//2,y//2),score)
    pygame.display.update()
    #Screen freezes for 2 seconds so the player can see his score
    time.sleep(2)
    pygame.quit()
    quit()

#variable to keep the loop running

#Main Game loop
def game_loop():
    #Initialise snake head
    snake_pos=[300,300]
    #Initialise snake body as a list
    snake_body=[[300,300],[290,300],[280,300],[270,300]]
    #Initialise velocity and direction of the snake, the snake will start moving towards the right
    vx_snake=10
    vy_snake=0
    direction='RIGHT'
    #Initialise score to zero
    score=0
    #Initialise food position using Spawn food function and set food_spawned to true
    food_pos=Spawn_food(snake_body)
    food_spawned=True
    #Boolean variable to keep the while loop running
    loop=True
    while loop:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                #If the player quits the game, the boolean variable becomes false and exits out of the while loop
                loop=False
            #Checking for which arrow-key the player pressed
            if event.type==pygame.KEYDOWN:
                #Updates the velocity according to the direction the snake is going
                #Using the direction variable, we can make sure that a 180 degree turn does not happen
                if event.key==pygame.K_UP and direction!='DOWN':
                    direction='UP'
                    vx_snake=0
                    vy_snake=-10
                elif event.key==pygame.K_DOWN and direction!='UP':
                    direction='DOWN'
                    vx_snake=0
                    vy_snake=10
                elif event.key==pygame.K_RIGHT and direction!='LEFT':
                    direction='RIGHT'
                    vx_snake=10
                    vy_snake=0
                elif event.key==pygame.K_LEFT and direction!='RIGHT':
                    direction='LEFT'
                    vx_snake=-10
                    vy_snake=0
        
        #Updates the snake head coordinates according to the velocity
        snake_pos[0] += vx_snake
        snake_pos[1] += vy_snake

        #Logic for movement of snake and increase in length
        #As long as the snake does not eat the food, we simultaneously insert the new head position into the list
        #and pop the tail, at a high spped this creates the illusion of the snake movement
        #When the snake eats the food, the pop function is ignored, hence a new block is added to list, increasing
        #length
        snake_body.insert(0,list(snake_pos))
        #Checking for a collision between the snake head and food, since the snake is a rectangle and the food a
        #circle, we are checking with respect to the difference between both the centres, so as not to create
        #overlap
        if abs(snake_pos[0]-food_pos[0])<=10 and abs(snake_pos[1]-food_pos[1])<=10:
            Eat_Sound.play()
            score = score + 10
            food_spawned=False
        else:
            snake_body.pop()
        
        #Once the food is eaten, a new one gets created
        if not food_spawned:
            food_pos = Spawn_food(snake_body)
            food_spawned=True
        
        #Drawing the screen, snake and food using pygame functions
        Window.blit(bg,(0,0))
        for body in snake_body:
            pygame.draw.rect(Window,indigo,pygame.Rect(body[0],body[1],10,10))
        pygame.draw.circle(Window,red,food_pos,5)

        #Game Over Conditions
        #Game ends when the snake goes out of boundary or hits itself
        #Here 40 and 710 are the x-coordinates of the play ground boundary
        if snake_pos[0]<40 or snake_pos[0]>710:
            game_over(score)
        #Here 40 and 590 are the y-coordinates of the play ground boundary
        if snake_pos[1]<40 or snake_pos[1]>590:
            game_over(score)
        #Essentially checks whether the snake head is colliding with its body
        if snake_pos in snake_body[1:]:
            game_over(score)
        
        #Displays score on top-left corner
        write_message('Comic Sans MS',20,'Score',white,(0,0),score)
        #Updates display at 15 fps
        pygame.display.update()
        clock.tick(15)

game_intro()    
pygame.quit()