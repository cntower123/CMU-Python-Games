#===============================================================================================================
#=========================================== T3TR1S - L1AM.M ===================================================
#===============================================================================================================

from cmu_graphics import *
import random

def onAppStart(app):
    app.rows = 15
    app.cols = 10
    app.boardLeft = 50
    app.boardTop = 70
    app.boardWidth = 250
    app.boardHeight = 325
    app.cellBorderWidth = 2
    app.stepsPerSecond = 4
    loadTetrisPieces(app)
    resetGame(app)
    
def resetGame(app):
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.score = 0
    app.lines = 0 # FEATRUE: Lines counter
    app.level = 1 # FEATURE: Level system
    app.gameOver = False
    app.paused = False
    app.nextPieceIndex = random.randrange(len(app.tetrisPieces))
    loadNextPiece(app)

def loadTetrisPieces(app):
    iPiece = [[ True, True, True, True ]]
    jPiece = [[ True, False, False ],
                [True, True, True ]]
    lPiece = [[ False, False, True ],
                [ True, True, True ]]
    oPiece = [[ True, True ], 
                [ True, True ]]
    sPiece = [[ False, True, True ],
                [ True, True, False] ]
    tPiece = [[ False, True, False ],
                [ True, True, True ]]
    zPiece = [[ True, True, False ],
                [ False, True, True]]
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [ 'red', 'yellow', 'magenta', 'pink', 'cyan', 'green', 'orange' ]
    
# FEATURE: Random pieces + next piece tracking
def loadPiece(app, pieceIndex):
    app.piece = app.tetrisPieces[pieceIndex]
    app.pieceColor = app.tetrisPieceColors[pieceIndex]
    app.pieceTopRow = 0
    pieceCols = len(app.piece[0])
    app.pieceLeftCol = (app.cols - pieceCols) // 2

def loadNextPiece(app):
    pieceIndex = app.nextPieceIndex
    app.nextPieceIndex = random.randrange(len(app.tetrisPieces))
    loadPiece(app, pieceIndex)
    if not pieceIsLegal(app):
        app.gameOver = True
    
def onKeyPress(app, key):
    # FEATURE: Game over restart
    if app.gameOver:
        resetGame(app)
        return
    # FEATRUE: Pause
    if key == 'p':
        app.paused = not app.paused
    if app.paused:
        return
    if key == 'left':
        movePiece(app, 0, -1)
    elif key == 'right':
        movePiece(app, 0, +1)
    elif key == 'down':
        movePiece(app, +1, 0)
    elif key == 'space':
        hardDropPiece(app)
    elif key == 'up':
        rotatePieceClockwise(app)
    elif key == 's':
        takeStep(app)

# FEATURE: Automatic stepping
def onStep(app):
    if not app.gameOver and not app.paused:
        takeStep(app)
        
def takeStep(app):
    if not movePiece(app, +1, 0):
        placePieceOnBoard(app)
        numCleared = removeFullRows(app)
        app.lines += numCleared
        app.level = 1 + app.lines // 5 # FEATURE: Level increases every 5 lines
        app.stepsPerSecond = 4 + app.level # FEATURE: Speed increases with level
        loadNextPiece(app)

def movePiece(app, drow, dcol):
    app.pieceTopRow += drow
    app.pieceLeftCol += dcol
    if pieceIsLegal(app):
        return True
    else:
        app.pieceTopRow -= drow
        app.pieceLeftCol -= dcol
        return False
        
def pieceIsLegal(app):
    for row in range(len(app.piece)):
        for col in range(len(app.piece[0])):
            if app.piece[row][col]:
                boardRow = app.pieceTopRow + row
                boardCol = app.pieceLeftCol + col
                if boardRow < 0 or boardRow >= app.rows:
                    return False
                if boardCol < 0 or boardCol >= app.cols:
                    return False
                if app.board[boardRow][boardCol] != None:
                    return False
    return True

def drawPiece(app):
    for row in range(len(app.piece)):
        for col in range(len(app.piece[0])):
            if app.piece[row][col]:
                boardRow = app.pieceTopRow + row
                boardCol = app.pieceLeftCol + col
                drawCell(app, boardRow, boardCol, app.pieceColor)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def rotate2dListClockwise(L):
    oldRows = len(L)
    oldCols = len(L[0])
    newRows = oldCols
    newCols = oldRows
    M = [([None] * newCols) for row in range(newRows)]
    for oldRow in range(oldRows):
        for oldCol in range(oldCols):
            newRow = oldCol
            newCol = oldRows - 1 - oldRow
            M[newRow][newCol] = L[oldRow][oldCol]
    return M

def rotatePieceClockwise(app):
    oldPiece = app.piece
    oldTopRow = app.pieceTopRow
    oldLeftCol = app.pieceLeftCol
    oldRows = len(oldPiece)
    oldCols = len(oldPiece[0])
    centerRow = oldTopRow + oldRows // 2 
    centerCol = oldLeftCol + oldCols // 2
    app.piece = rotate2dListClockwise(app.piece)
    newRows = len(app.piece)
    newCols = len(app.piece[0])
    app.pieceTopRow = centerRow - newRows // 2
    app.pieceLeftCol = centerCol - newCols // 2
    if not pieceIsLegal(app):
        app.piece = oldPiece
        app.pieceTopRow = oldTopRow
        app.pieceLeftCol = oldLeftCol

def hardDropPiece(app):
    while movePiece(app, +1, 0):
        pass

def placePieceOnBoard(app):
    for row in range(len(app.piece)):
        for col in range(len(app.piece[0])):
            if app.piece[row][col]:
                boardRow = app.pieceTopRow + row
                boardCol = app.pieceLeftCol + col
                app.board[boardRow][boardCol] = app.pieceColor

# FEATURE: Score system (More rows = exponentially more points, multiplied by level) *** Im pretty proud of this feature!
def removeFullRows(app):
    numFullRows = 0
    row = app.rows - 1 
    while row >= 0:
        if None not in app.board[row]:
            app.board.pop(row)
            numFullRows += 1 
        row -= 1
    for i in range(numFullRows):
        app.board.insert(0, [None] * app.cols)
    if numFullRows == 1: app.score+= 100 * app.level
    elif numFullRows == 2: app.score+= 300 * app.level
    elif numFullRows == 3: app.score+= 500 * app.level
    elif numFullRows == 4: app.score+= 800 * app.level
    return numFullRows

# FEATURE: Goast piece (Calculates where piece would land) 
def getGhostTopRow(app):
    ghostRow = app.pieceTopRow
    while True:
        ghostRow += 1 
        for row in range(len(app.piece)):
            for col in range(len(app.piece[0])):
                if app.piece[row][col]:
                    boardRow = ghostRow + row
                    boardCol = app.pieceLeftCol + col
                    if (boardRow >= app.rows or 
                        boardCol < 0 or boardCol >= app.cols or
                        app.board[boardRow][boardCol] != None):
                        return ghostRow - 1
       
def redrawAll(app):
    drawRect(0, 0, 400, 400, fill='darkSlateGray') # FEATURE: Dark theme
    drawLabel('Tetris', 175, 20, size=20, bold=True, fill='white')
    drawLabel(f'Score: {app.score} Level: {app.level} Lines: {app.lines}', # FEATURE: Score, level, lines display
                175, 42, size=12, fill='lightGray')
    drawLabel('P=pause Up=rotate Space=drop', # FEATURE: Controls help text
                175, 57, size=12, fill='yellow')
    drawBoard(app)
    if not app.gameOver: # FEATURE: Ghost piece
        drawGhostPiece(app) 
        drawPiece(app)
    drawBoardBorder(app)
    drawNextPiecePreview(app) # FEATURE: Next piece preview
    # FEATURE: Game over overlay
    if app.gameOver:
        drawRect(app.boardLeft, 180, app.boardWidth, 70,
                fill='black', opacity=85)
        drawLabel('GAME OVER', app.boardLeft + app.boardWidth/2, 205,
                    size=22, bold=True, fill='red')
        drawLabel('Press any key to restart', app.boardLeft + app.boardWidth/2, 230,
                    size=12, fill='white')
    # FEATURE: Pause overlay
    if app.paused:
        drawRect(app.boardLeft, 200, app.boardWidth, 40, 
                fill='black', opacity=85)
        drawLabel('PAUSED', app.boardLeft + app.boardWidth/2, 220,
                    size=18, bold=True, fill='yellow')
                    
# FEATURE: Dark theme cells
def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    if color == None:
        drawRect(cellLeft, cellTop, cellWidth, cellHeight, 
                    fill='darkSlateGray', border='slateGray',
                        borderWidth=app.cellBorderWidth)
    else:
        drawRect(cellLeft, cellTop, cellWidth, cellHeight,
                fill=color, border='black', 
                borderWidth=app.cellBorderWidth)
# FEATURE: Ghost piece drawing - outlined preview of landing position *** My favourite feature :)
def drawGhostPiece(app):
    ghostRow = getGhostTopRow(app)
    for row in range(len(app.piece)):
        for col in range(len(app.piece[0])):
            if app.piece[row][col]:
                boardRow = ghostRow + row
                boardCol = app.pieceLeftCol + col
                cellLeft, cellTop = getCellLeftTop(app, boardRow, boardCol)
                cellWidth, cellHeight = getCellSize(app)
                drawRect(cellLeft, cellTop, cellWidth, cellHeight,
                        fill=None, border=app.pieceColor,
                        borderWidth=2, opacity=50)
# FEATURE: Next piece preview
def drawNextPiecePreview(app):
    drawLabel('Next:', 345, 80, size=14, fill='white')
    nextPiece = app.tetrisPieces[app.nextPieceIndex]
    nextColor = app.tetrisPieceColors[app.nextPieceIndex]
    for row in range(len(nextPiece)):
        for col in range(len(nextPiece[0])):
            if nextPiece[row][col]:
                x = 325 + col * 18
                y = 95 + row * 18
                drawRect(x, y, 16, 16, fill=nextColor,
                        border='black', borderWidth=1)
                        
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            color = app.board[row][col]
            drawCell(app, row, col, color)

def drawBoardBorder(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight, 
                fill=None, border='white', borderWidth=2*app.cellBorderWidth)
                
def main():
    runApp()
    
main()