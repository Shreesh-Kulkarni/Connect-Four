#connect four game
#importing modules
import random
import pygame
import sys
import os
import copy
from pygame.locals import *
#specifying height and width of the board
bwidth=7#how many spaces tall board is
bheight=6
assert bwidth>=4 and bheight>=4#board must be atleast 4x4 to play the game
diff=2#asserting difficulty
ssize=50#asserting space size for tokens
fps=30#frames per second
#seeting height and width of the window
wwidth=480
wheight=640
xmargin=int((wwidth-bwidth*ssize)/2)
ymargin=int((wheight-bheight*ssize)/2)
bg=os.path.join("C:\\Users\Shreesh Kulkarni\OneDrive\Desktop\Shreesh\Images1\\bg.jpg")
bg1=pygame.image.load(bg)
BRIGHTBLUE = (0, 50, 255)
WHITE = (255, 255, 255)
BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE
RED = 'red'
BLACK = 'black'
EMPTY = None
HUMAN = 'human'
COMPUTER = 'computer'
#main function
def main():
    global FPSCLOCK, Dsurf,Rpilerect,Bpilerect,Rtoken
    global Btoken,Bimg,Hwinnerimg,ARROWIMG, ARROWRECT
    global compwinnerimg,winnerect,tiewinnerimg
    #specifying different images
    pygame.init()
    FPSCLOCK=pygame.time.Clock()
    Dsurf=pygame.display.set_mode((wwidth,wheight))
    pygame.display.set_caption("connect four")
    Rpilerect=pygame.Rect(int(ssize/2),wheight-int(3*ssize/2),ssize,ssize)
    Bpilerect=pygame.Rect(int(ssize/2),wwidth-int(3*ssize/2),ssize,ssize)
    Rtoken1=os.path.join("C:\\Users\Shreesh Kulkarni\OneDrive\Desktop\Shreesh\Images1\\rtoken.png")
    Rtoken=pygame.image.load(Rtoken1)
    Rtoken=pygame.transform.smoothscale(Rtoken,(ssize,ssize))
    Btoken1=os.path.join("C:\\Users\Shreesh Kulkarni\OneDrive\Desktop\Shreesh\Images1\\btoken.png")
    Btoken=pygame.image.load(Btoken1)
    Btoken=pygame.transform.smoothscale(Btoken,(ssize,ssize))
    Bimg1=os.path.join("C:\\Users\Shreesh Kulkarni\OneDrive\Desktop\Shreesh\Images1\\board.png")
    Bimg=pygame.image.load(Bimg1)
    Bimg=pygame.transform.smoothscale(Bimg,(ssize,ssize))
    hwinner1=os.path.join("C:\\Users\Shreesh Kulkarni\OneDrive\Desktop\Shreesh\Images1\\human.jpg")
    Hwinnerimg= pygame.image.load(hwinner1)
    cwinner1=os.path.join("C:\\Users\Shreesh Kulkarni\OneDrive\Desktop\Shreesh\Images1\\comp.jpg")
    compwinnerimg=pygame.image.load(cwinner1)
    twinner1=os.path.join("C:\\Users\Shreesh Kulkarni\OneDrive\Desktop\Shreesh\Images1\\tie.png")
    tiewinnerimg=pygame.image.load(twinner1)
    winnerect=Hwinnerimg.get_rect()
    winnerect.center = (int(wwidth / 2), int(wheight / 2))
    ARROWIMG = pygame.image.load("C:\\Users\Shreesh Kulkarni\OneDrive\Desktop\Shreesh\Images1\\arrow.png")
    ARROWRECT = ARROWIMG.get_rect()
    ARROWRECT.left = Rpilerect.right + 10
    ARROWRECT.centery = Rpilerect.centery
    isFirstGame=True
    while True:
        rungame(isFirstGame)
        isFirstGame=False
def rungame(isFirstGame):
    if isFirstGame:
        #COMPUTER TURN FIRST
        turn= COMPUTER
        showhelp= True
    else:
        #choosing who goes first
        a=random.randint(0,1)
        if a==0:
            turn=COMPUTER
        else:
            turn=HUMAN
            showhelp=False
    #setting main board
    mainboard= getNewBoard()
    #main game loop
    while True:
        if turn==HUMAN:
            #HUMAN TURN
            gethumanmove(mainboard,showhelp)
            if showhelp:
                showhelp=False
            if iswinner(mainboard,RED):
                winnerimg=Hwinnerimg
                break
            turn=COMPUTER
        else:
            column=getcompmove(mainboard)
            animateCompmoving(mainboard,column)
            makemove(mainboard,BLACK,column)
            if iswinner(mainboard,BLACK):
                winnerimg= compwinnerimg
                break
            turn=HUMAN
        if isboardfull(mainboard):
            #filled board means a tie
            winnerimg=tiewinnerimg
            break
    while True:
        #keep looping until player quits or stops
        drawboard(mainboard)
        Dsurf.blit(winnerimg, winnerect)
        pygame.display.update()
        FPSCLOCK.tick()
        for event in pygame.event.get():
            if event.type==QUIT or (event.type== KEYUP and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type== MOUSEBUTTONUP:
                return
def makemove(board,player,column):
    lowest=getlowestemptyspace(board,column)
    if lowest!=-1:
        board[column][lowest]= player
def drawboard(board,extratoken=None):
    Dsurf.fill(BGCOLOR)
    Dsurf.blit(bg1,(0,0))
    #drawing tokens
    spacerect=pygame.Rect(0,0,ssize,ssize)
    for x in range(bwidth):
        for y in range(bheight):
            spacerect.topleft=(xmargin+(x*ssize),ymargin+(y*ssize))
            if board[x][y]==RED:
                Dsurf.blit(Rtoken,spacerect)
            elif board[x][y]==BLACK:
                Dsurf.blit(Btoken,spacerect)
    if extratoken!=None:
        if extratoken['color']==RED:
            Dsurf.blit(Rtoken,(extratoken['x'],extratoken['y'],ssize,ssize))
        elif extratoken['color']==BLACK:
            Dsurf.blit(Btoken,(extratoken['x'],extratoken['y'],ssize,ssize))

    #drawing board over tokens
    for x in range(bwidth):
        for y in range(bheight):
            spacerect.topleft=(xmargin+(x*ssize),ymargin+(y*ssize))
            Dsurf.blit(Bimg,spacerect)
    #drawing tokens on the side
    Dsurf.blit(Rtoken,Rpilerect)
    Dsurf.blit(Btoken,Bpilerect)
def getNewBoard():
    board=[]
    for x in range(bwidth):
        board.append([EMPTY]*bheight)
    return board
#specifying different function for human to move
def gethumanmove(board,isFirstMove):
    #token which is choosed by player
    dtoken=False
    tokenx,tokeny=None,None
    #event handling loop
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and not dtoken and Rpilerect.collidepoint(event.pos):
                #start of dragging the red token by the player
                tokenx,tokeny=event.pos
                dtoken=True
            elif event.type==MOUSEMOTION and dtoken:
                #update position of the token being dragged
                tokenx,tokeny= event.pos
            elif event.type==MOUSEBUTTONUP and dtoken:
                #let go of token being dragged and leave it inside the grid
                if tokeny<ymargin and tokenx>xmargin and tokenx<wwidth-xmargin:
                    #let go at top of the screen
                    column=int((tokenx-xmargin)/ssize)
                    if isValidMove(board,column):
                        animatedroppingtoken(board,column,RED)
                        board[column][getlowestemptyspace(board,column)]=RED
                        drawboard(board)
                        pygame.display.update()
                        return
                    tokenx,tokeny=None,None
                    dtoken=False
                if tokenx!=None and tokeny!=None:
                    drawboard(board,{'x':tokenx-int(ssize/2),'y':tokeny-int(ssize/2),'color':RED})
                else:
                    drawboard(board)
                if isFirstMove:
                    Dsurf.blit(ARROWIMG,ARROWRECT)
                pygame.display.update()
                FPSCLOCK.tick()
def animatedroppingtoken(board,column,color):
    x=xmargin +column*ssize
    y=ymargin - ssize
    dspeed=1.0
    lowestemptyspace=getlowestemptyspace(board,column)

    while True:
        y+=int(dspeed)
        dspeed+=0.5
        if int((y-ymargin)/ssize)>=lowestemptyspace:
            return
        drawboard(board,{'x':x,'y':y,'color':color})
        pygame.display.update()
        FPSCLOCK.tick()
def animateCompmoving(board,column):
    x= Bpilerect.left
    y= Bpilerect.top
    speed=1.0
    #getting the computer to move the black token
    while y>(ymargin-ssize):
        y-=int(speed)
        speed+=0.5
        drawboard(board,{'x':x,'y':y,'color':BLACK})
        pygame.display.update()
        FPSCLOCK.tick()
        #moving black tile over
    y=ymargin-ssize
    speed=1.0
    while x>(xmargin+column*ssize):
        x-=int(speed)
        speed+=0.5
        drawboard(board,{'x':x,'y':y,'color':BLACK})
        pygame.display.update()
        FPSCLOCK.tick()
    #dropping black tile
    animatedroppingtoken(board,column,BLACK)

def getcompmove(board):
    potentialMoves = getPotentialMoves(board, BLACK, diff)
    # get the best fitness from the potential moves
    bestMoveFitness = -1
    for i in range(bwidth):
        if potentialMoves[i] > bestMoveFitness and isValidMove(board, i):
            bestMoveFitness = potentialMoves[i]
      # find all potential moves that have this best fitness

    bestMoves = []
    for i in range(len(potentialMoves)):
        if potentialMoves[i] == bestMoveFitness and isValidMove(board, i):
            bestMoves.append(i)
    return random.choice(bestMoves)
def getPotentialMoves(board,tile,lookahead):
    if lookahead==0 and isboardfull(board):
        return[0]*bwidth
    if tile==RED:
        enemytile=BLACK
    else:
        enemytile=RED
    #figuring out best move to make
    potentialMoves=[0]*bwidth
    for i in range(bwidth):
        dboard=copy.deepcopy(board)
        if not isValidMove(dboard,i):
            continue
        makemove(dboard,tile,i)
        if iswinner(dboard,tile):
            #winning move gets good fitness
            potentialMoves[i]=1
            break
        else:
            #do other player counter moves and thus determine the best one
            if isboardfull(dboard):
                potentialMoves[i]=0
            else:
                for j in range(bwidth):
                    dboard2 = copy.deepcopy(dboard)
                if not isValidMove(dboard2, j):
                    continue
                makemove(dboard2, enemytile, j)
                if iswinner(dboard2,enemytile):
                    #alosing move gets bad fitness
                    potentialMoves[i]=-1
                    break
                else:
                    #do something to get the next move right
                    results=getPotentialMoves(dboard2,tile,lookahead-1)
                    potentialMoves[i]+=(sum(results)/bwidth)/bwidth
    return potentialMoves

def getlowestemptyspace(board,column):
    #return row number of lowest row empty in the column
    for y in range(bheight-1,-1,-1):
        if board[column][y]==EMPTY:
            return y
    return -1
def isValidMove(board,column):
    #returns true if there is empty space otherwise false
    if column < 0 or column >= (bwidth) or board[column][0] != EMPTY:
        return False
    return True

def isboardfull(board):
    #returns true if board is full
    for x in range(bwidth):
        for y in range(bheight):
            if board[x][y]==EMPTY:
                return False
    return True

def iswinner(board,tile):
    #check for horizontal spaces
    for x in range(bwidth - 3):
        for y in range(bheight):
            if board[x][y] == tile and board[x + 1][y] == tile and board[x + 2][y] == tile and board[x + 3][y] == tile:
                return True
    #check for vertical spaces
    for x in range(bwidth):
        for y in range(bheight-3):
            if board[x][y] == tile and board[x][y + 1] == tile and board[x][y + 2] == tile and board[x][y + 3] == tile:
                return True
    #check for diagonal spaces
    for x in range(bwidth-3):
        for y in range(3,bheight):
            if board[x][y] == tile and board[x + 1][y - 1] == tile and board[x + 2][y - 2] == tile and board[x + 3][y - 3] == tile:
                return True
    #check for diagonal spaces the other side
    for x in range(bwidth-3):
        for y in range(bheight-3):
            if board[x][y] == tile and board[x + 1][y + 1] == tile and board[x + 2][y + 2] == tile and board[x + 3][y + 3] == tile:
                return True
    return False
if __name__ == '__main__':
    main()



















