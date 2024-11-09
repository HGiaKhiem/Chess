import pygame as p
import ChessEngine 
import random
#thông tin về bàn cờ
WIDTH = HEIGHT = 512 # kích thước 
DIMENSION = 8 # số ô cờ
SQ_SIZE = HEIGHT // DIMENSION # kích thước các ô cờ
MAX_FPS = 20 #  tốc độ khung hình khi di chuyển chuột
IMAGES = {} # 1 dict để lưu các quân cờ
#Hàm  load các hình ảnh quân cờ
def loadImages():
    pieces = ['wp','wR','wN','wB','wK', 'wQ','bp','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main_menu():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT)) # tạo kích thước cửa sổ 
    p.display.set_caption("Chess Game - Choose Mode") # tiêu đề
    font = p.font.SysFont("Arial", 32)
    clock = p.time.Clock() # khởi tạo  clock để điều khiể fps

    while True:
        screen.fill(p.Color("white")) # làm sạch màn hình = màu trắng 

        # Hiển thị hai tùy chọn
        pvp_text = font.render("1. Player vs Player", True, p.Color("black"))
        pvai_text = font.render("2. Player vs AI", True, p.Color("black"))
        # vẽ văn bản lên màn hình 
        screen.blit(pvp_text, (WIDTH // 2 - pvp_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(pvai_text, (WIDTH // 2 - pvai_text.get_width() // 2, HEIGHT // 2 + 20))

        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                return None
            elif e.type == p.KEYDOWN: # nhấn phím để lựa chọn chế độ chơi
                if e.key == p.K_1:  # nhấn phím 1 để người vs người
                    return "PvP"
                elif e.key == p.K_2:   # nhấn 2 để người và máy
                    return "PvAI"

        p.display.flip()
        clock.tick(MAX_FPS)


def start_pvp():
    screen = p.display.set_mode((WIDTH, HEIGHT))  # Tạo cửa sổ trò chơi
    clock = p.time.Clock()  # Tạo đối tượng clock để điều khiển tốc độ khung hình
    screen.fill(p.Color("white"))  # Làm sạch màn hình với màu trắng
    gs = ChessEngine.GameState()  # Khởi tạo trạng thái trò chơi
    validMoves = gs.getValidMoves()  # Lấy danh sách các nước đi hợp lệ
    moveMade = False  # Biến theo dõi xem đã có nước đi nào được thực hiện hay chưa
    animate = False  # Biến theo dõi xem có cần hiệu ứng chuyển động không
    loadImages()  # Tải ảnh quân cờ
    running = True  # Biến điều khiển vòng lặp trò chơi
    sqSelected = ()  # Biến lưu vị trí ô được chọn
    playerClicks = []  # Danh sách các lần nhấp chuột của người chơi
    gameOver = False  # Biến xác định liệu trò chơi đã kết thúc chưa

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:  # Nếu người chơi đóng cửa sổ
                running = False  # Thoát khỏi vòng lặp
            elif e.type == p.MOUSEBUTTONDOWN:  # Nếu người chơi nhấp chuột
                if not gameOver:
                    location = p.mouse.get_pos()  # Lấy vị trí chuột
                    col = location[0] // SQ_SIZE  # Tính cột
                    row = location[1] // SQ_SIZE  # Tính hàng
                    if sqSelected == (row, col):  # Nếu ô đã chọn giống ô vừa nhấp
                        sqSelected = ()  # Deselect ô
                        playerClicks = []  # Xóa danh sách các lần nhấp chuột
                    else:
                        sqSelected = (row, col)  # Chọn ô mới
                        playerClicks.append(sqSelected)  # Thêm ô vào danh sách nhấp chuột

                    if len(playerClicks) == 2:  # Nếu đã chọn 2 ô
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)  # Tạo nước đi từ 2 ô
                        for i in range(len(validMoves)):  # Kiểm tra xem nước đi có hợp lệ không
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])  # Thực hiện nước đi
                                if move.isPawnPromotion:  # Nếu quân tốt lên hàng cuối
                                    chosenPiece = choosePromotionPiece(screen, move.pieceMoved[0])  # Chọn quân mới
                                    gs.board[move.endRow][move.endCol] = chosenPiece  # Phong quân tốt thành quân mới
                                moveMade = True  # Đánh dấu đã có nước đi
                                animate = True  # Kích hoạt hiệu ứng di chuyển
                                sqSelected = ()  # Reset ô đã chọn
                                playerClicks = []  # Reset danh sách các lần nhấp chuột
                        if not moveMade:  # Nếu không có nước đi hợp lệ
                            playerClicks = [sqSelected]  # Lưu lại ô đã chọn để tiếp tục di chuyển

            elif e.type == p.KEYDOWN:  # Nếu nhấn phím
                if e.key == p.K_z:  # Phím 'z' để hoàn tác
                    gs.undoMove()  # Hoàn tác nước đi
                    animate = False  # Tắt hiệu ứng
                    moveMade = True  # Đánh dấu đã có nước đi
                if e.key == p.K_r:  # Phím 'r' để làm lại trò chơi
                    gs = ChessEngine.GameState()  # Khởi tạo lại trạng thái trò chơi
                    validMoves = gs.getValidMoves()  # Lấy danh sách các nước đi hợp lệ
                    sqSelected = ()  # Reset ô đã chọn
                    playerClicks = []  # Reset danh sách nhấp chuột
                    moveMade = False  # Reset trạng thái nước đi
                    animate = False  # Tắt hiệu ứng

        if moveMade:  # Nếu đã có nước đi
            if animate:  # Nếu cần hiệu ứng di chuyển
                animateMove(gs.moveLog[-1], screen, gs.board, clock)  # Hiển thị hiệu ứng di chuyển
            validMoves = gs.getValidMoves()  # Lấy lại danh sách nước đi hợp lệ
            moveMade = False  # Reset trạng thái nước đi

        drawGameState(screen, gs, validMoves, sqSelected)  # Vẽ trạng thái trò chơi lên màn hình

        if gs.checkMate:  # Nếu ván cờ kết thúc bằng chiếu hết
            gameOver = True  # Đánh dấu trò chơi kết thúc
            if gs.whiteToMove:
                drawEndGameText(screen, "Vua Trang Da Bi Chieu")  # Hiển thị thông báo vua trắng bị chiếu
            else:
                drawEndGameText(screen, "Vua Den Da Bi Chieu")  # Hiển thị thông báo vua đen bị chiếu
        if gs.staleMate:  # Nếu ván cờ kết thúc bằng hòa do bí
            gameOver = True  # Đánh dấu trò chơi kết thúc
            drawEndGameText(screen, "Hoa")  # Hiển thị thông báo hòa

        clock.tick(MAX_FPS)  # Giới hạn tốc độ khung hình
        p.display.flip()  # Cập nhật màn hình


#faehf;aefhhdsfh

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

def findBestMove(gs, validMoves): # bắt đầu viết ai cho nay
    if validMoves:
        return random.choice(validMoves)
    return None




def highlightMoves(screen, gs, validMoves, sqSelected): # tô màu các ô di chuyển
    # nếu đã chọn 1 ô
    if sqSelected != ():
        #lấy vị trí ô đó
        r, c = sqSelected
        piece = gs.board[r][c]
        #check màu 
        if piece[0] == ('w' if gs.whiteToMove else 'b'): 
            # tô màu cho ô cờ
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # tô màu  xanh cho ô cờ hợp lệ và đỏ cho ô cờ có quân địch đang đứng trên đó
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    if gs.board[move.endRow][move.endCol] != "--":  
                        s.fill(p.Color('red'))  
                    else:
                        s.fill(p.Color('lightgreen')) 
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))



def drawGameState(screen, gs, validMoves, sqSelected): # thực hiện vẽ
    drawBoard(screen)  
    drawPieces(screen, gs.board)
    highlightMoves(screen, gs, validMoves, sqSelected)

def drawBoard(screen): #vẽ bàn cờ và  các ô cờ trắng đen
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board): # vẽ các quân cờ lên bàn cờ
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # Nếu ô không trống
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
 

def animateMove(move, screen, board , clock): # hiệu ứng chuyển động  khi di chuyển 1 quân cờ
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


def drawEndGameText (screen, text): # in ra thông báo kết thúc
    font = p.font.SysFont("Arial", 32, True, False)
    textObject =font.render(text, 0, p.Color("Black"))
    textLocation = p .Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2,
                                                    HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject,textLocation)


def choosePromotionPiece(screen, color): # lựa chọn các quân khi phong tốt 
    promotionPieces = ['Q', 'R', 'B', 'N']  
    pieceImages = {}
    # duyệt qua các quân cờ và tải ảnh lên
    for piece in promotionPieces:
        pieceImages[piece] = p.transform.scale(p.image.load(f"images/{color + piece}.png"), (SQ_SIZE, SQ_SIZE)) 
    #tạo list ô lựa chọn để nhấp dô
    choiceRect = [p.Rect((WIDTH - (len(promotionPieces) * SQ_SIZE)) // 2 + i * SQ_SIZE, HEIGHT // 2 - SQ_SIZE // 2, SQ_SIZE, SQ_SIZE) for i in range(len(promotionPieces))]

    #vòng lặp kiểm tra khi nhấp chuột
    #vị trí nhấp chuột có đúng vào ô  list các quân có thể phong lên không
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
            
if __name__ == "__main__":
    mode = main_menu()
    if mode == "PvP":
        start_pvp()
    elif mode == "PvAI":
        start_pvai()
