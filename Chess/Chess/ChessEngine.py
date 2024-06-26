"""Storing all data annd info about current state of the Chess Game
also will responsible for detemining the valid moves also move LOG"""
class GameState():
    def __init__(self):
        #8*8 board made by multidimensional list
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.moveFunctions = {'p':self.getPawnMoves,'R':self.getRookMoves,'N': self.getKnightMoves,
                              'B':self.getBishopMoves,'Q':self.getQueenMoves,'K':self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
    def makeMove(self,move):
        self.board[move.startRow][move.startCol]= "--"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo or history
        self.whiteToMove= not self.whiteToMove #Swapping

    def undoMove(self):
        if len(self.moveLog)!= 0 :        #we need to know that here we can undo something
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol]= move.pieceMoved
            self.board[move.endRow][move.endCol]= move.pieceCaptured
            self.whiteToMove= not self.whiteToMove #switch back

    def getValidMoves(self):
        return self.getAllpossibleMoves()


    def getAllpossibleMoves(self):
        moves=[]
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #numbers of cols in given row
                turn = self.board[r][c][0]
                if (turn=='w' and self.whiteToMove) or (turn=='b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) #move based on piece
        return moves

    #All poss moves for pawn
    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=="--": #2 square pawn advance
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1>=0: #captures to the left
                if self.board[r-1][c-1][0]=='b':
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 <= 7: #captures to the right
                if self.board[r-1][c+1][0]=='b':
                    moves.append((Move((r,c),(r-1,c+1), self.board)))
        else: #black moves

            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 6 and self.board[r + 2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))

            if c - 1 >= 0:  # captures to the left
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # captures to the right
                if self.board[r - 1][c + 1][0] == 'w':
                    moves.append((Move((r, c), (r + 1, c + 1), self.board)))
            #pawn promotions
            #en patane tipo
    def getRookMoves(self,r,c,moves):
        directions= ((-1,0),(0,-1),(1,0),(0,1))

        if self.whiteToMove:
            enemyColor='b'
        else: enemyColor='w'

        for d in directions:
            for i in range(1,8):
                endRow = r+d[0]* i
                endCol = c+d[1]*i
                if 0 <= endRow <8 and 0 <= endCol <8: #board
                    endPiece = self.board[endRow][endCol]
                    if endPiece=="--": #empty space
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else:
                        break
                else:
                    break
    def getKnightMoves(self,r,c,moves):
        knightMoves= ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        if self.whiteToMove:
            allyColor='w'
        else: allyColor='b'

        for m in knightMoves:
            endRow = r+ m[0]
            endCol = c+ m[1]
            if 0 <= endRow<8 and 0 <= endCol <8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0]!= allyColor:
                    moves.append(Move((r,c), (endRow,endCol), self.board))
    def getKingMoves(self,r,c,moves):
        pass

    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    def getBishopMoves(self,r,c,moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))

        if self.whiteToMove:
            enemyColor = 'b'
        else:
            enemyColor = 'w'

        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
class Move():
    #maps keys to value
    #key : value
    ranksToRows = {'1':7,'2':6,'3':5,'4':4,'5':3,'6':2,'7':1,'8':0}
    rowsToRanks = {v: k for k,v in ranksToRows.items()}
    filesToCols= {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7,}
    colsToFiles = {v: k for k,v in filesToCols.items()}
    def __init__(self, startSq,endSq,board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol*100 + self.endRow*10 + self.endCol
        print(self.moveID)

        #overriding the equals method
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveID==other.moveID
        return False


    def getChessNotation(self):
        #as a real chess notation
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)
    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]