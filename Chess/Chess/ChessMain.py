#Main and response for input and display the currten GameState object
import pygame as p
from Chess import ChessEngine
p.init()
WIDTH = HEIGHT = 512
DIMENSION= 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS= 15
IMAGES={}


"""
Initialize a global dictionary of images. This will e called exactly one in the main"""

def loadImages():
    pieces=["wp","wR","wN","wB","wK","wQ","bp","bR","bN","bB","bK","bQ"]
    for piece in pieces:
        IMAGES[piece]= p.transform.scale(p.image.load("images/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))
    #Note we can acces an image by saying IMAGES["wp"]


def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()

    loadImages()
    running=True
    sqSelected=() #no square is selected, keep track of the last clicl of the user
    playerClicks= [] #player clicks two tupples
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running= False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # x and y coor of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE

                if sqSelected == (row,col): #the user clicked same square twice
                    sqSelected= () #deselect
                    playerClicks = [ ] #clear player clicks
                else:
                    sqSelected= (row, col)
                    playerClicks.append(sqSelected) #append for both clicks
                if len(playerClicks)== 2:
                    move=ChessEngine.Move(playerClicks[0],playerClicks[1], gs.board)
                    print(move.getChessNotation())


                    gs.makeMove(move)
                    sqSelected = () #reset user clicks
                    playerClicks=[]
            #key handlers
            elif e.type== p.KEYDOWN:
                if e.key == p.K_z:#bind
                    gs.undoMove()

        drawGameState(screen , gs)
        clock.tick(MAX_FPS)
        p.display.flip()



def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("white"),p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen , color , p.Rect(c*SQ_SIZE, r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))



if __name__ == "__main__":
    main()