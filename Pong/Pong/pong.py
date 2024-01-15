import pygame
pygame.init()

# Window Settings
WIDTH, HEIGHT = 700, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) # setting window up
pygame.display.set_caption("Atari's Pong!") # display title
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100  # drawing height & width of paddles

fps = 60 # frame per second

BallRadius = 7 # moving ball radius
ScoreFont = pygame.font.SysFont("comicsans", 50) # font of game font
WinnerScore = 10 # score

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)



##### Defining Paddles #####
class Paddles:
    COLOR = WHITE
    VELOCITY = 4  # velocity of paddles moving
    
    ## attributes of the paddles
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
    
    ## drawing the paddles itself
    def draw(self, WINDOW):
        pygame.draw.rect(WINDOW, self.COLOR, (self.x, self.y, self.width, self.height))

    ## paddles moving
    def move(self, up = True):
        if up:
           self.y -= self.VELOCITY
        else:
           self.y += self.VELOCITY
           
    # reset
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y



#### Ball Class ####
class MovingBall:
    MaxVelocity = 5
    COLOR = WHITE
    
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MaxVelocity
        self.y_vel = 0
        
    # drawing the ball on the window
    def draw(self, WINDOW):
        pygame.draw.circle(WINDOW, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
    # resetting the ball
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1
        


##### Drawing Function #####
def drawing(WINDOW, paddles, ball, LeftPlayerScore, RightPlayerScore):
    WINDOW.fill(BLACK)
    
    LeftPlayerScore = ScoreFont.render(f"{LeftPlayerScore}", 1, WHITE) # rendering LEFT player score
    RightPlayerScore = ScoreFont.render(f"{RightPlayerScore}", 1 , WHITE) # rendering right player score
    
    WINDOW.blit(LeftPlayerScore, (WIDTH//4 - LeftPlayerScore.get_width()//2, 20)) # positioning LEFT player score [Note: 20 ~ mean 20 pixels]
    WINDOW.blit(RightPlayerScore, (WIDTH * (3/4) - RightPlayerScore.get_width()//2, 20)) # positioning RIGHT player score
    
    for paddle in paddles:
        paddle.draw(WINDOW)
    
    ## draws middle line
    for line in range(10, HEIGHT, HEIGHT//20):
        if line % 2 == 1:
            continue
        pygame.draw.rect(WINDOW, WHITE, (WIDTH//2 - 5, line, 10, HEIGHT//20))
    
    ball.draw(WINDOW)
    pygame.display.update() # updates display



##### Handling Collisions #####
def HandleCollision(ball, LeftPaddle, RightPaddle):
    
    # collision in LEFT paddle
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
        
    if ball.x_vel < 0:
        if ball.y >= LeftPaddle.y and ball.y <= LeftPaddle.y + LeftPaddle.height:
            if ball.x - ball.radius <= LeftPaddle.x + LeftPaddle.width:
                ball.x_vel *= -1
                
                # bouncing the ball off the middle of the LEFT paddle
                middleY = LeftPaddle.y + LeftPaddle.height / 2
                difference_inY = middleY - ball.y
                ReductionFactor = (LeftPaddle.height / 2) / ball.MaxVelocity
                y_vel = difference_inY / ReductionFactor
                ball.y_vel = -1 * y_vel # allows it to bounce off in the right direction
                    
    # collision in RIGHT paddle
    else:
        if ball.y >= RightPaddle.y and ball.y <= RightPaddle.y + RightPaddle.height:
            if ball.x + ball.radius >= RightPaddle.x:
                ball.x_vel *= -1

                # bouncing the ball off the middle of the RIGHT paddle
                middleY = RightPaddle.y + RightPaddle.height / 2
                difference_inY = middleY - ball.y
                ReductionFactor = (RightPaddle.height / 2) / ball.MaxVelocity
                y_vel = difference_inY / ReductionFactor
                ball.y_vel = -1 * y_vel # allows it to bounce off in the right direction



##### Paddle Movements #####
def HandlePaddleMovement(keys, LeftPaddle, RightPaddle):
    # left paddle
    if keys[pygame.K_w] and LeftPaddle.y - LeftPaddle.VELOCITY >= 0:  
        LeftPaddle.move(up = True)
    if keys[pygame.K_s] and LeftPaddle.y + LeftPaddle.VELOCITY + LeftPaddle.height <= HEIGHT:
        LeftPaddle.move(up = False)

    # notes: [pygame.K_w] = W Keys; The 'and LeftPaddle.y - LeftPaddle.VELOCITY >= 0' limits paddles on window
    
    # right paddle
    if keys[pygame.K_UP] and RightPaddle.y - RightPaddle.VELOCITY >= 0:
        RightPaddle.move(up = True)
    if keys[pygame.K_DOWN] and RightPaddle.y + RightPaddle.VELOCITY + RightPaddle.height <= HEIGHT:
        RightPaddle.move(up = False)



### Event Loop ###
def main():
    run = True
    clk = pygame.time.Clock()
    
    ## initializing paddles
    LeftPaddle = Paddles(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    RightPaddle = Paddles(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
      
    ## initializing ball
    ball  = MovingBall(WIDTH//2, HEIGHT//2, BallRadius)
        
    # left & right player
    LeftPlayerScore = 0
    RightPlayerScore = 0
        
    # running window
    while run:
        clk.tick(fps)
        drawing(WINDOW, [LeftPaddle, RightPaddle], ball, LeftPlayerScore, RightPlayerScore) # drawing onto window funct (draw funct)
        
        # user-interface event
        for event in pygame.event.get(): 
            
            # checking if user quits
            if event.type == pygame.QUIT: 
                run = False
                break
            
        # paddles moving
        keys = pygame.key.get_pressed()
        HandlePaddleMovement(keys, LeftPaddle, RightPaddle)
        
        # ball moving
        ball.move()
        HandleCollision(ball, LeftPaddle, RightPaddle)
        
        
        # checking of scoring
        if ball.x < 0:
            RightPlayerScore += 1
            ball.reset() # resetting the ball
            
        elif ball.x > WIDTH:
            LeftPlayerScore += 1
            ball.reset() # resetting the ball
            
        # checking winning score
        PlayerWon = False
        
        if LeftPlayerScore >= WinnerScore:
           PlayerWon = True
           WinningText = "Left Player Won!"
            
        elif RightPlayerScore >= WinnerScore:
           PlayerWon = True
           WinningText = "Right Player Won!"
            
        if PlayerWon:
            # display winning text 
            text = ScoreFont.render(WinningText, 1, GREEN)
            WINDOW.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update() # updating display
            pygame.time.delay(5000) # 5000 ms
            
            # reset everything after each win
            ball.reset()
            LeftPaddle.reset()
            RightPaddle.reset()
            
            LeftPlayerScore = 0
            RightPlayerScore = 0
             
    pygame.quit()

    
# checks if 'main' func if it matches the files 'main' func
if __name__ == '__main__':
    main()