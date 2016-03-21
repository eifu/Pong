## Ping Pong
## by eifu -- april 15. Updated april 29 2015.


## This is a single-player game. One can play this game based on the
## difficulty they choose just before they start playing the game.
## Players use the right and left keys to move the bar at the 
## bottom of the window. Players win when they get 5 points and 
## lose when the computer gets 5 points.
## the ball will be acceralated when human or computer players' bars
## hit the ball at the quarter from the both of edges.


## REFERENCE
## 1. the visiting professor Rhys Price Jones 
## 2. "Making Games with Python and Pygame."
####################################################################
####################################################################
import random, pygame, sys
from pygame.locals import *

BOARDWIDTH = 480
BOARDHEIGHT = 640
RACKETWIDTH = 160
RACKETHEIGHT = 3
BALLSIZE = 5
RACKETMOVE = 5
FPS = 90

## In this 3-line part, inspired by Dr Jones.
EASY  = [(3,1),(2,2),(1,3),(3,2),(2,3)]
NOMAL = [(2,4),(3,3),(4,2),(2,5),(3,4),(4,3),(5,2)]
HARD  = [(2,6),(3,5),(4,4),(5,3),(6,2),(3,6),(4,5),(5,4),(6,3)]

#             R   G   B
BLUE =      (  0,  0,200)
LIGHTBLUE = (  0,153,255)
DARKBLUE  = ( 20, 20,100)
GRAY =      (128,128,128)
WHITE =     (225,225,225)

TEXTCOLOR = BLUE
BGCOLOR = GRAY
RACKETCOLOR = DARKBLUE
COMPUTERRACKETCOLOR = LIGHTBLUE
BALLCOLOR = WHITE
BLANK = "."

#####################################################################
#####################################################################
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT,BIGFONT, acc
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((BOARDWIDTH,BOARDHEIGHT))
    BASICFONT = pygame.font.Font("freesansbold.ttf",18)
    BIGFONT = pygame.font.Font("freesansbold.ttf",60)
    pygame.display.set_caption('Pong!')    
    ## TITLE SCREEN ##
    DISPLAYSURF.fill(BGCOLOR)
    firstScreen()

    while True: ## MAIN LOOP ##
        DISPLAYSURF.fill(BGCOLOR)
        difficulty = secondScreen()
        acc = [0,0]
        print ("_"*21)
        while max(acc) < 5:gameScreen(difficulty)
        checkIfContinue(acc)

def checkIfContinue(acc):
    if acc[0] ==5:titleSurf, titleRect = makeTextObjs("LOSE", BIGFONT, TEXTCOLOR)
    else:titleSurf, titleRect = makeTextObjs("WIN", BIGFONT, TEXTCOLOR)
    
    titleRect.center = (int(BOARDWIDTH // 2), int(BOARDHEIGHT//2))
    DISPLAYSURF.blit(titleSurf, titleRect)  

    messageSurf, messageRect = makeTextObjs("Pless Space Button to play again", BASICFONT, TEXTCOLOR)
    messageRect.center = (int(BOARDWIDTH // 2), int(BOARDHEIGHT//2)+50)
    DISPLAYSURF.blit(messageSurf, messageRect)
    

    while True:    
        checkForQuit()
        for event in pygame.event.get():
            if event.type ==KEYDOWN and event.key == K_SPACE:
                return True
        pygame.display.update()
        FPSCLOCK.tick()

## In this function, inspired by "Making games with Python and Pygame."
def checkForQuit():
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        pygame.event.post(event)
        

def generateBlankBoard():
    board = []
    for y in range(BOARDHEIGHT):
        board.append([BLANK] * BOARDWIDTH)
    
    for x in range(BOARDWIDTH//2-RACKETWIDTH//2,(BOARDWIDTH//2+RACKETWIDTH//2)+1):
        for y in range(BOARDHEIGHT-RACKETHEIGHT,BOARDHEIGHT):
            board[y][x] = RACKETCOLOR
             
    return board


def drawRacket(board, leftTopP, color,LR=0):
    
    pointX = leftTopP[0] + (BOARDWIDTH/2 - RACKETWIDTH/2)    ## CONVERT INTO XY COORDINATES ##
    pointY = leftTopP[1] + (BOARDHEIGHT - RACKETHEIGHT)
    
    pygame.draw.rect(DISPLAYSURF, color,
                     (pointX, pointY, RACKETWIDTH, RACKETHEIGHT))
    
    for xR in range(0,BOARDHEIGHT+1):
        for yR in range(pointY, pointY + RACKETHEIGHT):
            if xR == color:
                newX = pointX+LR
                board[yR][xR],board[yR][newX] = BLANK, RACKETCOLOR
            
def drawComputerRacket(board, startP, color):
    startP = (startP[0] + (BOARDWIDTH//2 - RACKETWIDTH//2),startP[1] ) 
    pygame.draw.rect(DISPLAYSURF, color,
                     (startP[0],startP[1], RACKETWIDTH, RACKETHEIGHT))
    for x in range(startP[0], startP[0] + RACKETWIDTH):
        for y in range(startP[1], startP[1] + RACKETHEIGHT):
            board[y][x] = color

def drawBall(board,oldCenter):
    pygame.draw.circle(DISPLAYSURF, BALLCOLOR, (oldCenter[0]+ xVelosity,oldCenter[1]+ yVelosity), BALLSIZE)

    for x in range(oldCenter[0]-BALLSIZE,oldCenter[0]+BALLSIZE+1):
        for y in range(oldCenter[1]-BALLSIZE,oldCenter[1]+BALLSIZE+1):
            if board[y][x] == BALLCOLOR:
                newX, newY = center[0] +xVelosity, center[1] +yVelosity
                board[y][x],board[newY][newX] = BLANK, BALLCOLOR

def firstScreen():
    titleSurf, titleRect = makeTextObjs("Pong", BIGFONT, TEXTCOLOR)
    titleRect.center = (BOARDWIDTH // 2, BOARDHEIGHT//2)
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    additionalSurf, additionalRect = makeTextObjs("Pressa a key to play", BASICFONT,TEXTCOLOR)
    additionalRect.center = (BOARDWIDTH//2, BOARDHEIGHT//2 + 200)
    DISPLAYSURF.blit(additionalSurf, additionalRect)
    
    while True:
        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYDOWN:return 
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def secondScreen():
    titleSurf, titleRect = makeTextObjs("Press h To Play Hard ", BASICFONT, TEXTCOLOR)
    titleRect.center = (BOARDWIDTH // 2, (BOARDHEIGHT//2 )-50)
    DISPLAYSURF.blit(titleSurf, titleRect)

    titleSurf, titleRect = makeTextObjs("Press n To Play Nomal", BASICFONT, TEXTCOLOR)
    titleRect.center = (BOARDWIDTH // 2, BOARDHEIGHT//2)
    DISPLAYSURF.blit(titleSurf, titleRect)

    titleSurf, titleRect = makeTextObjs("Press e To Play Easy ", BASICFONT, TEXTCOLOR)
    titleRect.center = (BOARDWIDTH // 2, (BOARDHEIGHT//2)+50)
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    while True:
        checkForQuit()
        for event in pygame.event.get(KEYUP):
            if event.key not in [K_h, K_n, K_e]:continue
            elif event.key == K_h:return HARD
            elif event.key == K_n:return NOMAL
            else:return EASY
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def makeTextObjs(text,font,color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

    
def gameScreen(difficulty):
    global xVelosity,yVelosity, center, collisionPoint
    mainBoard = generateBlankBoard()
    
    ## PLAYER RACKET ##
    racketCoords = []
    for j in range(RACKETHEIGHT):
        coords = [{"x":linex} for linex in range(RACKETWIDTH)]
        for i in range(RACKETWIDTH):
            coords[i]["y"] = j
        racketCoords += coords
    ## COMPUTER RACKET ##
    computerRacketCoords = []
    for j in range(RACKETHEIGHT):
        coords = [{"x":linex} for linex in range(RACKETWIDTH)]
        for i in range(RACKETWIDTH):
            coords[i]["y"] = j
        computerRacketCoords += coords
    ## BALL ##
    center = (BOARDWIDTH//2, BOARDHEIGHT//2)
    xVelosity,yVelosity = random.choice(difficulty)
    xVelosity *= random.choice([-1,1])
    
    collisionPoint = (0,0)
    move = 0
    accelerate = 2
    if difficulty == EASY:accelerate = 1
    elif difficulty == HARD:accelerate = 3
    

    ## MAIN LOOP ##
    while True:
        checkForQuit()
        
        ## BALL BOUNDING ON THE SIDE WALLS ##
        if center[0] +xVelosity <= BALLSIZE:xVelosity *= -1
        if center[0] +xVelosity >= BOARDWIDTH-BALLSIZE:xVelosity *= -1
        
        
        ## reaching the goal of the opponent ##
        if center[1] +yVelosity<=BALLSIZE:
            if computerRacketCoords[0]["x"]+ BOARDWIDTH//2 - RACKETWIDTH//2  <= center[0] and \
               computerRacketCoords[0]["x"]+ BOARDWIDTH//2 + RACKETWIDTH//2  >= center[0] :
                yVelosity *= -1
                ## ACCELERATE THE BALL SPEED ##
                if  (computerRacketCoords[0]["x"]+ BOARDWIDTH//2 - RACKETWIDTH//2 <= center[0]and \
                     computerRacketCoords[0]["x"]+ BOARDWIDTH//2 - RACKETWIDTH//4 >= center[0])or \
                    (computerRacketCoords[0]["x"]+ BOARDWIDTH//2 + RACKETWIDTH//4 <= center[0]and \
                     computerRacketCoords[0]["x"]+ BOARDWIDTH//2 + RACKETWIDTH//2 >= center[0]):
                    xVelosity += random.choice([1,-1])
                    yVelosity += accelerate
                    if xVelosity ==0: xVelosity = 1
                collisionPoint = (0,0)
                
            else:
                acc[1] += 1
                print ("Player:",acc[1],"Computer:",acc[0])
                return
            
        ## reaching the goal of the player ##
        if center[1] +yVelosity>=BOARDHEIGHT-BALLSIZE:
            if racketCoords[0]["x"]+ BOARDWIDTH//2 - RACKETWIDTH//2  <= center[0] and \
               racketCoords[0]["x"]+ BOARDWIDTH//2 + RACKETWIDTH//2  >= center[0] :
                yVelosity *= -1
                ## ACCELERATE THE BALL SPEED ##
                if  (racketCoords[0]["x"]+ BOARDWIDTH//2 - RACKETWIDTH//2 <= center[0]and \
                     racketCoords[0]["x"]+ BOARDWIDTH//2 - RACKETWIDTH//4 >= center[0])or \
                    (racketCoords[0]["x"]+ BOARDWIDTH//2 + RACKETWIDTH//4 <= center[0]and \
                     racketCoords[0]["x"]+ BOARDWIDTH//2 + RACKETWIDTH//2 >= center[0]):
                    xVelosity += random.choice([1,-1])
                    yVelosity -= accelerate
                    if xVelosity == 0: xVelosity = 1
                collisionPoint = (center[0],BOARDHEIGHT)

            else:
                acc[0] += 1
                print ("Player:",acc[1],"Computer:",acc[0])
                return 
            
        ## ASSIGNING THE BALL POSITION ##
        newX = center[0]+ xVelosity
        newY = center[1]+ yVelosity
        if newX > BOARDWIDTH: newX = BOARDWIDTH
        if newX < 0: newX = 0
        center = (newX,newY)
        
        ## MOVING THE PLAYER'S RACKET ##
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_LEFT  and racketCoords[0]["x"] -5 >= RACKETWIDTH/2 - BOARDWIDTH/2:move = -RACKETMOVE
                if event.key == K_RIGHT and racketCoords[0]["x"] +5 <= BOARDWIDTH/2 - RACKETWIDTH/2:move =  RACKETMOVE
            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT:
                    move =0        
        racketCoords[0]["x"] += move
        if racketCoords[0]["x"] < RACKETWIDTH//2 - BOARDWIDTH//2:racketCoords[0]["x"] = RACKETWIDTH//2 - BOARDWIDTH/2
        if BOARDWIDTH/2 - RACKETWIDTH//2 < racketCoords[0]["x"]:racketCoords[0]["x"] = BOARDWIDTH//2 - RACKETWIDTH/2 
         
        ## AI of computer ##
        if not collisionPoint == (0,0):
            if not computerRacketCoords[0]["x"] + BOARDWIDTH//2 - RACKETWIDTH//2 <= center[0] or \
                   computerRacketCoords[0]["x"] + BOARDWIDTH//2 + RACKETWIDTH//2 >= center[0]:
                computerRacketCoords[0]["x"] = center[0] - BOARDWIDTH//2                 
            if computerRacketCoords[0]["x"] < RACKETWIDTH//2 - BOARDWIDTH//2: computerRacketCoords[0]["x"] = RACKETWIDTH//2 - BOARDWIDTH//2
            if computerRacketCoords[0]["x"] > BOARDWIDTH//2 - RACKETWIDTH//2: computerRacketCoords[0]["x"] = BOARDWIDTH//2 - RACKETWIDTH//2
            

        DISPLAYSURF.fill(BGCOLOR)
        drawRacket(mainBoard,(racketCoords[0]["x"],racketCoords[0]["y"]),RACKETCOLOR)
        drawComputerRacket(mainBoard,(computerRacketCoords[0]["x"],computerRacketCoords[0]["y"]),COMPUTERRACKETCOLOR)
        drawBall(mainBoard,center)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    main()