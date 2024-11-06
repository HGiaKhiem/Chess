class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.moveFunction = {'p': self.getPawnMoves, 'R':self.getRookMoves, 'N':self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves,'K': self.getKingMoves}

        self.whiteToMove =True
        self.moveLog=[]

        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enPassantPossible = () # bat tot qua duong
        self.in_check = False       
        self.pins = [] #quan chan
        self.checks= [] # quan chieu

        self.current_Castling_Rights = CastleRights (True,True,True,True)# quyền nhập thành
        self.castleRightLog = [CastleRights(self.current_Castling_Rights.wK_Side, self.current_Castling_Rights.bK_Side, 
                                            self.current_Castling_Rights.wQ_Side, self.current_Castling_Rights.bQ_Side)] #Log quyền nhập thành

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"  # Xóa quân tại vị trí bắt đầu
        self.board[move.endRow][move.endCol] = move.pieceMoved  # Đặt quân tại vị trí kết thúc
        self.moveLog.append(move)  
        self.whiteToMove = not self.whiteToMove  # Đổi lượt chơi

        # Cập nhật vị trí của quân Vua
        if move.pieceMoved == "wK":  # Nếu quân di chuyển là Vua trắng
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":  # Nếu quân di chuyển là Vua đen
            self.blackKingLocation = (move.endRow, move.endCol) 
        #Phong Tốt
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # bat tot qua duong
        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = "--"
        
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enPassantPossible = ()

        #kiem tra nhap thanh
        if move.isCastleMove:
            if move.endCol - move.startCol  == 2:
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1] #di chuyen quan xe 
                self.board[move.endRow][move.endCol + 1] = '--'
            else:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'

        #Quyền Nhập thành -Khi vua hoặc xe di chuyển
        self.updateCastleRights(move)
        self.castleRightLog.append(CastleRights(self.current_Castling_Rights.wK_Side, self.current_Castling_Rights.bK_Side, 
                                                self.current_Castling_Rights.wQ_Side, self.current_Castling_Rights.bQ_Side))
        
    def undoMove(self):
        if len(self.moveLog) != 0: 
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]= move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved  == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            
            #undo bat tot qua duong
            if move.isEnPassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enPassantPossible = (move.endRow, move.endCol)
            #undo tot di 2 o 
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enPassantPossible = ()
            #undo nhap thanh
            self.castleRightLog.pop()
            self.current_Castling_Rights = self.castleRightLog[-1]

            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'


    def updateCastleRights(self, move):
        #neu con xe da bi an mat
        if move.pieceCaptured == "wR":
            if move.endCol  == 0 :
                self.current_Castling_Rights.wQ_Side = False
            elif move.endCol == 7:
                self.current_Castling_Rights.wK_Side = False
        elif move.pieceCaptured == "bR":
            if move.endCol == 0 :
                self.current_Castling_Rights.bQ_Side = False
            elif move.endCol == 7:
                self.current_Castling_Rights.bK_Side = False
        #neu con vua di chuyen
        if move.pieceMoved == 'wK':
            self.current_Castling_Rights.wK_Side = False
            self.current_Castling_Rights.wQ_Side = False
        elif move.pieceMoved == 'bK':
            self.current_Castling_Rights.bK_Side = False
            self.current_Castling_Rights.bQ_Side = False
        # neu con xe di chuyen
        if move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:
                    self.current_Castling_Rights.wK_Side = False
                if move.startCol  == 7:
                    self.current_Castling_Rights.wQ_Side = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0 :
                if move.startCol == 0:
                    self.current_Castling_Rights.bQ_Side = False
                if move.startCol == 7 :
                    self.current_Castling_Rights.bK_Side = False
    

    def getValidMoves(self):
        tempCastleRights = CastleRights(self.current_Castling_Rights.wK_Side, self.current_Castling_Rights.bK_Side, 
                                        self.current_Castling_Rights.wQ_Side, self.current_Castling_Rights.bQ_Side)
        
        moves = []
        self.in_Check, self.pins, self.checks = self.checkForPinsAndChecks()

        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        if self.in_Check:
            if len(self.checks) == 1:  # Chỉ bị chiếu bởi một quân
                moves = self.getAllPossibleMoves()
                checkInfo = self.checks[0]  # Lấy thông tin về quân đang chiếu vua
                checkRow = checkInfo[0]
                checkCol = checkInfo[1]
                pieceChecking = self.board[checkRow][checkCol] # Lấy thông tin quân cờ 
                valid_Squares = [] # Danh sach quan cờ có thể đi
                
                if pieceChecking[1] == 'N':  # Nếu quân mã chiếu vua, chỉ có thể ăn quân mã hoặc chạy vua
                    valid_Squares = [(checkRow, checkCol)]
                else:  # Nếu là quân khác, tìm các ô vua có thể trốn
                    for i in range(1, 8):
                        validSquare = (kingRow + checkInfo[2] * i, kingCol + checkInfo[3] * i)
                        valid_Squares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                # Loại bỏ các nước đi không hợp lệ
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':  # Không phải là vua di chuyển
                        if not (moves[i].endRow, moves[i].endCol)  in valid_Squares:  # Nếu không nằm trong ô trốn
                            moves.remove(moves[i])
            else:  # Bị chiếu đôi (double check)
                self.getKingMoves(kingRow, kingCol, moves)  # Chỉ quân vua mới có thể di chuyển
        else:
            moves = self.getAllPossibleMoves()  # Nếu không bị chiếu, lấy tất cả các nước đi
            if self.whiteToMove:
                self.getCastleMoves(self.whiteKingLocation[0],self.whiteKingLocation[1], moves)
            else: 
                self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkmate = False
            self.stalemate = False
        self.current_Castling_Rights = tempCastleRights

        return moves

    def inCheck(self): # Kiểm tra chiếu
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])  # ktra tra quân Vua trắng
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])  # ktra tra quân Vua đen

    def squareUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove
        oppMoves =self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        # Kiểm tra xem ô (r, c) có nằm trong nước đi của quân đối phương không
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True  # Ô bị tấn công
        return False  # Ô không bị tấn công
    
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]   
                if (turn == 'w' and self.whiteToMove) or (turn== 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunction[piece](r,c,moves)
        return moves
    
    def checkForPinsAndChecks(self):
        pins = []  # Quân cờ bị khóa
        checks = []  # Quân đang chiếu
        in_check = False       
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1),  # Các hướng theo hàng và cột
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Các hướng theo đường chéo

        for j in range(len(directions)):
            direction = directions[j]
            possiblePin = ()  # Lưu vị trí quân có thể bị khóa
            for i in range(1, 8):
                endRow = startRow + direction[0] * i
                endCol = startCol + direction[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Đảm bảo không ra ngoài bàn cờ
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':  # Nếu gặp quân đồng minh
                        if possiblePin == ():  # Quân cờ đồng minh đầu tiên
                            possiblePin = (endRow, endCol, direction[0], direction[1])
                        else:  # Nếu đã có một quân bị khóa, dừng lại
                            break
                    elif endPiece[0] == enemyColor:
                        pieceType = endPiece[1]
                            # Kiểm tra nếu có quân địch đang chiếu vua
                        if (0 <= j <= 3 and pieceType == 'R') or \
                            (4 <= j <= 7 and pieceType == 'B') or \
                            (i == 1 and pieceType == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                            (pieceType == 'Q') or (i == 1 and pieceType == 'K'):
                                if possiblePin == ():  # Không có quân bị khóa, vua bị chiếu
                                    in_check = True
                                    checks.append((endRow, endCol, direction[0], direction[1]))
                                    break
                                else:  # Có quân bị khóa
                                    pins.append(possiblePin)
                                    break
                        else:  # Quân địch không chiếu vua, dừng lại
                            break
                else:
                    break  # Nếu ra khỏi bàn cờ, dừng lại
        # Kiểm tra nước đi của quân mã
        knightMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # Kiểm tra không ra khỏi bàn cờ
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':  # Nếu là quân mã địch
                    in_check = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return in_check, pins, checks

    def getPawnMoves(self, r, c, moves):
        piecePinned = False  # Quân cờ có đang khóa không
        pinDirection = ()  # Hướng mà quân cờ bị khóa có thể di chuyển
        # Kiểm tra xem quân cờ có bị khóa hay không
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])  # Xóa quân bị khóa khỏi danh sách
                break

        if self.whiteToMove:  # Nước đi của quân trắng
            moveAmount = -1
            startRow = 6
            enemyColor = 'b'
        else:
            moveAmount = 1
            startRow = 1
            enemyColor = 'w'           
            # Các nước ăn chéo

        if self.board[r + moveAmount][c] == "--":  # 1 square pawn advance
            if not piecePinned or pinDirection == (moveAmount, 0):
                moves.append(Move((r, c), (r + moveAmount, c), self.board))
                if r == startRow and self.board[r + 2 * moveAmount][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2 * moveAmount, c), self.board))

        if c - 1 >= 0 : 
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c  - 1][0] == enemyColor:  # Kiểm tra ăn chéo phải
                    moves.append(Move((r,c),(r+moveAmount, c-1), self.board))
                if (r + moveAmount,c - 1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r + moveAmount, c-1),self.board, isEnPassantMove = True ))
        if c + 1 <= 7 :
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r + moveAmount][c + 1][0] == enemyColor:  # Kiểm tra ăn chéo phải
                    moves.append(Move((r,c), (r + moveAmount, c+1), self.board))
                if (r+moveAmount, c+1) == self.enPassantPossible:
                    moves.append(Move((r,c),(r + moveAmount, c+1), self.board, isEnPassantMove =  True))

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()  # Hướng quân bị khóa có thể di chuyển
        # Kiểm tra xem quân cờ có bị khóa hay không
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':  # Chỉ loại bỏ quân bị khóa nếu không phải là Hậu
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # Các hướng di chuyển của quân Xe
        enemyColor = 'b' if self.whiteToMove else 'w'  # Màu quân địch

        for direction in directions:
            for i in range(1, 8):  # Di chuyển tối đa 7 ô theo hướng
                endRow = r + direction[0] * i
                endCol = c + direction[1] * i
                
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # Kiểm tra xem có nằm trong bàn cờ
                    if not piecePinned or pinDirection == direction or pinDirection == (-direction[0], -direction[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # Nếu ô đó trống
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:  # Nếu có quân địch
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break  # Quân Xe không thể tiếp tục sau khi ăn quân địch
                        else:
                            break  # Nếu gặp quân cùng màu
                else:
                    break  # Dừng lại nếu quân bị khóa

    def getKnightMoves(self, r, c, moves):
        piecePinned = False  # Quân cờ có đang khóa không (di chuyển vua sẽ bị chiếu)
        # Kiểm tra xem quân cờ có bị khóa hay không
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break  # Không cần xóa quân khóa, chỉ cần đánh dấu là bị khóa

        knightMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        allyColor ='w' if self.whiteToMove else 'b' # Xác định quan cung mau
        
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # Kiểm tra nước đi có trong bàn cờ không
                if not piecePinned:  # Nếu quân không bị khóa
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: # Nếu ô đó trống hoặc có quân cùng màu
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        piecePinned = False  # quân cờ có đang khóa ko (di chuyển vua sẽ bị chiếu)
        pinDirection = ()  # hướng mà quân cờ bị khóa có thế di chuyển dễ vua k bị chiếu
         # Kiểm tra xem quân cờ có bị khóa hay không
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break        
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        enemyColor = "b" if self.whiteToMove else "w"
        for direction in directions: 
            for i in range(1,8):
                endRow = r + direction[0] * i
                endCol = c + direction[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == direction or pinDirection == (-direction[0], -direction[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c), (endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c), (endRow,endCol),self.board))
                            break
                        else:
                            break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1,  0,  0,  1,  1, 1) 
        colMoves = ( 1,  0,  1, -1,  1, -1 , 0, 1)    
        allyColor = 'w' if self.whiteToMove else 'b'  # Xác định màu quân địch
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # Kiểm tra nước đi có trong bàn cờ không
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  #nếu không phải quân cùng màu
                    if allyColor == "w":
                       self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow,endCol)
                    in_check, pins, checks =self.checkForPinsAndChecks()
                    if not in_check:
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                    if allyColor == "w":
                        self.whiteKingLocation = (r,c)
                    else:
                        self.blackKingLocation = (r,c)
                
    def getCastleMoves (self ,r , c, moves):
        if self.squareUnderAttack (r,c):
            return
        if (self.whiteToMove and self.current_Castling_Rights.wK_Side) or (not self.whiteToMove and self.current_Castling_Rights.bK_Side):
            self.getKingSideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.current_Castling_Rights.wQ_Side) or (not self.whiteToMove and self.current_Castling_Rights.bQ_Side):
            self.getQueenSideCastleMoves(r, c, moves)

    def getKingSideCastleMoves (self, r, c, moves):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove = True))
    
    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove = True))

class CastleRights():
    def __init__(self,wK_Side, bK_Side, wQ_Side, bQ_Side):
        #Nhap thanh ben phia vua
        self.wK_Side = wK_Side 
        self.bK_Side = bK_Side
        #nhap thanh ben phia hau
        self.wQ_Side = wQ_Side
        self.bQ_Side = bQ_Side

class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k , v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles =  {v: k for k , v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnPassantMove=False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7)
        #Enpassant bat tot qua duong
        self.isEnPassantMove = isEnPassantMove
        if self.isEnPassantMove:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"
        #CastleMove : nhap thanh
        self.isCastleMove = isCastleMove


        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol

    def __eq__(self, other) :
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):# Lấy ký hiệu cờ vua từ vị trí bắt đầu và kết thúc
        return self.getRankFile(self.startRow,self.startCol) + "->"+ self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self, r,c): # chuyen doi vi tri theo quy tat co vua
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
    def getChessInfo (self):
        pieceInfo = self.pieceMoved
        return pieceInfo
