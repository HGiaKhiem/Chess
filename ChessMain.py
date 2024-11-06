import pygame as p
import ChessEngine 
import random
<<<<<<< HEAD
#thông tin về bàn cờ
WIDTH = HEIGHT = 512 # kích thước 
DIMENSION = 8 # số ô cờ
SQ_SIZE = HEIGHT // DIMENSION # kích thước các ô cờ
MAX_FPS = 20 #  tốc độ khung hình khi di chuyển chuột
IMAGES = {} # 1 dict để lưu các quân cờ
#Hàm  load các hình ảnh quân cờ
=======

WIDTH = HEIGHT = 512
DIMENSION = 8 
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 20
IMAGES = {}

>>>>>>> 595b1e9b0c537e24d442e53e99c8b383bbf65f10
def loadImages():
    pieces = ['wp','wR','wN','wB','wK', 'wQ','bp','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

<<<<<<< HEAD
=======
""" def main(): 
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade =False
    animate = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        # Kiểm tra lượt chơi trước khi thực hiện nước đi
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade =True
                                animate = True
                                sqSelected = ()  # reset lựa chọn
                                playerClicks = []
                                print(move.getChessInfo() + " vi tri: " + move.getChessNotation())
                        if not moveMade: 
                            playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Nhấn z để undo move
                    gs.undoMove()
                    animate = False
                    moveMade =True
                if e.key == p.K_r: # nhan r resset game
                    gs =ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False


        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board,clock)
            validMoves = gs.getValidMoves()
            moveMade =False

        drawGameState(screen, gs, validMoves, sqSelected)  

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawEndGameText(screen,"Vua Trang Da Bi Chieu")
            else:
                drawEndGameText(screen,"Vua Den Da Bi Chieu")
        if gs.staleMate:
            gameOver = True
            drawEndGameText("Hoa")

        clock.tick(MAX_FPS)
        p.display.flip()
"""

>>>>>>> 595b1e9b0c537e24d442e53e99c8b383bbf65f10
def main_menu():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chess Game - Choose Mode")
    font = p.font.SysFont("Arial", 32)
    clock = p.time.Clock()

    while True:
        screen.fill(p.Color("white"))

        # Hiển thị hai tùy chọn
        pvp_text = font.render("1. Player vs Player", True, p.Color("black"))
        pvai_text = font.render("2. Player vs AI", True, p.Color("black"))

        screen.blit(pvp_text, (WIDTH // 2 - pvp_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(pvai_text, (WIDTH // 2 - pvai_text.get_width() // 2, HEIGHT // 2 + 20))

        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                return None
            elif e.type == p.KEYDOWN:
                if e.key == p.K_1: 
                    return "PvP"
                elif e.key == p.K_2:  
                    return "PvAI"

        p.display.flip()
        clock.tick(MAX_FPS)


def start_pvp():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
<<<<<<< HEAD
                                if move.isPawnPromotion:
                                    chosenPiece = choosePromotionPiece(screen, move.pieceMoved[0])
                                    gs.board[move.endRow][move.endCol] = chosenPiece
=======

                                if move.isPawnPromotion:
                                    chosenPiece = choosePromotionPiece(screen, move.pieceMoved[0])
                                    gs.board[move.endRow][move.endCol] = chosenPiece

                                    
>>>>>>> 595b1e9b0c537e24d442e53e99c8b383bbf65f10
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade: 
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    animate = False
                    moveMade = True
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board,clock)
            validMoves = gs.getValidMoves()
            moveMade =False

        drawGameState(screen, gs, validMoves, sqSelected)  

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawEndGameText(screen,"Vua Trang Da Bi Chieu")
            else:
                drawEndGameText(screen,"Vua Den Da Bi Chieu")
        if gs.staleMate:
            gameOver = True
            drawEndGameText("Hoa")

        clock.tick(MAX_FPS)
        p.display.flip()

def start_pvai():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and gs.whiteToMove:  
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade: 
                            playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    animate = False
                    moveMade = True
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False

        if not gs.whiteToMove and not gameOver: 
            ai_move = findBestMove(gs, validMoves)  
            if ai_move:
                gs.makeMove(ai_move)
                moveMade = True
                animate = True

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawEndGameText(screen,"Vua Trang Da Bi Chieu")
            else:
                drawEndGameText(screen,"Vua Den Da Bi Chieu")
        if gs.staleMate:
            gameOver = True
            drawEndGameText("Hoa")

        clock.tick(MAX_FPS)
        p.display.flip()

<<<<<<< HEAD
def findBestMove(gs, validMoves):
    if validMoves:
        return random.choice(validMoves)
    return None




=======
# ------------------------------------------Game--------------------------------------------
>>>>>>> 595b1e9b0c537e24d442e53e99c8b383bbf65f10
def highlightMoves(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        piece = gs.board[r][c]
        if piece[0] == ('w' if gs.whiteToMove else 'b'): 
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))

            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    if gs.board[move.endRow][move.endCol] != "--":  
                        s.fill(p.Color('red'))  
                    else:
                        s.fill(p.Color('lightgreen')) 
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))



def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)  
    drawPieces(screen, gs.board)
    highlightMoves(screen, gs, validMoves, sqSelected)

def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # Nếu ô không trống
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
 

def animateMove(move, screen, board , clock):
    global colors
    # tinh toan khoang cach 
    dR = move.endRow - move.startRow 
    dC = move.endCol - move.startCol
    # toc do khung hinh (sqeed tang thi khung hinh giam)
    frameSpeed  = 5
    frameCount = (abs(dR) + abs(dC)) * frameSpeed

    for frame in range (frameCount + 1):
        r ,c  =(move.startRow + dR*frame/frameCount, move.startCol +dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquares = p.Rect(move.endCol* SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen, color, endSquares)

        if move.pieceCaptured != '--':
            screen.blit (IMAGES[move.pieceCaptured], endSquares)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawEndGameText (screen, text):
    font = p.font.SysFont("Arial", 32, True, False)
    textObject =font.render(text, 0, p.Color("Black"))
    textLocation = p .Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2,
                                                    HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject,textLocation)


def choosePromotionPiece(screen, color):
    promotionPieces = ['Q', 'R', 'B', 'N']  
    pieceImages = {}
    for piece in promotionPieces:
        pieceImages[piece] = p.transform.scale(p.image.load(f"images/{color + piece}.png"), (SQ_SIZE, SQ_SIZE)) 
    
    choiceRect = [p.Rect((WIDTH - (len(promotionPieces) * SQ_SIZE)) // 2 + i * SQ_SIZE, HEIGHT // 2 - SQ_SIZE // 2, SQ_SIZE, SQ_SIZE) for i in range(len(promotionPieces))]


    while True:
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN:
                mouseX, mouseY = p.mouse.get_pos()
                for i, rect in enumerate(choiceRect):
                    if rect.collidepoint(mouseX,mouseY):
                        return color + promotionPieces[i]
        
        for i, rect in enumerate(choiceRect):
            screen.blit(pieceImages[promotionPieces[i]], rect)
            p.draw.rect(screen,p.Color("black"), rect,1)
        
        p.display.flip()
            
<<<<<<< HEAD

=======
#------------------------------------------------------------------------------------------------------------

#-------------------------------------------------AI-------------------------------------------------------
def findBestMove(gs, validMoves):
    if validMoves:
        return random.choice(validMoves)
    return None

#----------------------------------------------------------------------------------------------------------
>>>>>>> 595b1e9b0c537e24d442e53e99c8b383bbf65f10
if __name__ == "__main__":
    mode = main_menu()
    if mode == "PvP":
        start_pvp()
    elif mode == "PvAI":
<<<<<<< HEAD
        start_pvai()
=======
        start_pvai()
>>>>>>> 595b1e9b0c537e24d442e53e99c8b383bbf65f10
