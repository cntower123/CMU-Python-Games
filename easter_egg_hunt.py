from cmu_graphics import *
#                                                  ===================================================
#                                                  == Easter Egg Hunt - A Bunny Pac-Man if you will ==
#                                                  ==             - Creative Project -               ==     
#                                                  ==================================================

#   P.S I did go a bit ahead into unti and included Parallel Lists - List multiplication - Indexing - Looping with Index and Mutation) Hope this is okay :)

#Helper function - Circle Overlap Check (Same concept as intersections from animations unit)
def circlesOverlap(x1, y1, r1, x2, y2, r2):
    dist = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
    return dist < r1 + r2
#String Unit - Caesar Cipher Decoder
def decodeCaesar(text, shift):
    result = ''
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result += chr((ord(ch) - base - shift) % 26 + base)
        else:
            result += ch
    return result
#Model - onAppStart
def onAppStart(app):
    resetGame(app)
#Reset
def resetGame(app):
    #Screen Size
    app.width = 600
    app.height = 600
    #Game state 
    app.state = 'start'
    #Bunny (the player)
    app.bx = 300
    app.by = 300
    app.br = 18 
    app.bdx = 0 
    app.bdy = 0 
    app.bSpeed = 3
    #rotation and angle of chomping mouth arc and arc gap
    app.facing = 0 
    app.mouth = 30
    app.mouthDir = 1
    #Scores and lives
    app.score = 0 
    app.lives = 3
    #Power mode (golden carrot!!!)
    app.powered = False
    app.powerTimer = 0
    #Respawn flicker
    app.respawning = False
    app.respawnTimer = 0
    #EASTER EGGS (18 eggs around the garden border) - (egg data is stored in parallel lists, one list per property)
    app.eggX = [ 
        80, 180, 300, 420, 520, 
        80, 520, 
        80, 520, 
        80, 520, 
        80, 180, 300, 420, 520, 
        200, 400,
    ]
    app.eggY = [ 
        80, 80, 80, 80, 80,
        200, 200, 
        300, 300, 
        420, 420, 
        520, 520, 520, 520, 520, 
        300, 300, 
    ]
    app.eggColors = [ 
        'pink', 'lightBlue', 'lightGreen', 'lavender', 'peachPuff',
        'lightCyan', 'lightYellow',
        'mistyRose', 'honeydew',
        'lightPink', 'paleTurquoise', 
        'lightGoldenrodYellow', 'lavenderBlush', "aliceBlue",
        'mintCream', "seashell", 
        'lemonChiffon', 'thistle'
    ]
    app.eggVisible = [True] * 18 
    app.eggCount = 18
    app.eggR = 9 
    #GOLDEN carrot
    app.carrotX = 150 
    app.carrotY = 450
    app.carrotR = 13
    app.carrotVisible = True
    #Foxes
    app.foxX = [100, 500, 300]
    app.foxY = [120, 480, 100]
    app.foxDX = [2.0, -1.8, 1.5]
    app.foxDY = [1.5, 2.0, -2.0]
    app.foxR = 16
    #Sounds
    #app.andCollect = Sound ("collect.mp3")
    #app.andPower = Sound ("power.mp3")
    #app.andOuch = Sound ("ouch.mp3")
    #app.andWin = Sound ("win.mp3")
#View - redrawAll
def redrawAll(app): 
    if app.state == 'start':
        drawStartScreen(app)
    elif app.state == 'playing':
        drawGame(app)
    elif app.state == 'gameover':
        drawGameOver(app)
    elif app.state == 'win':
        drawWinScreen(app)
#Start Screen
def drawStartScreen(app):
    drawRect(0, 0, app.width, app.height, fill='lightCyan')
    drawRect(0, app.height // 2, app.width, app.height // 2,
            fill='mediumSeaGreen')
    drawCircle(520, 70, 45, fill='gold', opacity=80)
    drawCircle(520, 70, 35, fill='yellow')
    drawRect(60, 140, 480, 100, fill='white', opacity=85,
            border='saddleBrown', borderWidth=3)
    drawLabel('EASTER EGG HUNT', 300, 175, size=36, bold=True,
             fill='saddleBrown', font='monospace')
    drawLabel('A Bunny Pac-Man Adventure', 300, 215, size=16, 
             fill='peru', font='monospace')
    drawBunny(300, 330, 24, 30, 0, False)
    drawLabel('Arrow Keys to move', 300, 398, size=14, fill='darkGreen')
    drawLabel('Collect all the eggs! Avoid the foxex!', 300, 420, size=14, fill='darkGreen')
    drawLabel('Grab the golden carrot for power!', 300, 442, size=14, fill='peru')
    drawRect(175, 446, 250, 38, fill='saddleBrown')
    drawLabel('Press SPACE to start', 300, 485, size=15, 
              bold=True, fill='white', font='monospace')
#Main game screen
def drawGame(app):
    drawRect(0, 0, app.width, app.height, fill='darkSeaGreen')
    drawRect(0, 270, app.width, 60, fill='tan', opacity=40)
    drawRect(270, 0, 60, app.height, fill='tan', opacity=40)
    drawRect(0, 0, app.width, app.height, 
             fill=None, border='saddlebrown', borderWidth=6)
    for row in range(6): 
        for col in range(6):
            drawCircle(50 + col * 100, 50 + row * 100,
                       3, fill='seaGreen', opacity=40)
    drawEggs(app)
    drawCarrot(app)
    drawFoxes(app)
    #Cool Touch
    if not app.respawning or (app.respawnTimer % 16 < 10):
        drawBunny(app.bx, app.by, app.br, 
                  app.mouth, app.facing, app.powered)
    drawHUD(app)
#Draw eggs
def drawEggs(app):
    for i in range(app.eggCount):
        if app.eggVisible[i]:
            ex = app.eggX[i]
            ey = app.eggY[i]
            er = app.eggR
            drawOval(ex, ey, er * 1.4, er * 1.8, 
                    fill=app.eggColors[i], border='white',
                    borderWidth=1)
            drawLine(ex - er * 0.5, ey, ex + er * 0.5, ey, 
                    fill='white', opacity=60, lineWidth=1)
#Draw Golden Carrot
def drawCarrot(app):
    if not app.carrotVisible:
        return 
    px = app.carrotX
    py = app.carrotY
    pr = app.carrotR
    drawCircle(px, py, pr + 5, fill='gold', opacity=40)
    drawOval(px, py + 2, pr * 0.65, pr * 1.2,
             fill='darkorange', border='orangeRed', borderWidth=1)
    drawArc(px, py + pr, pr * 0.65, pr * 0.55, 180, 180, 
        fill = 'darkorange')
    drawLine(px, py - pr * 0.5, px, py - pr * 1.4, 
        fill ='green', lineWidth=2)
    drawLine(px - 5, py - pr * 0.3, px - 10, py - pr * 1.2, 
        fill='green', lineWidth=2)
    drawLine(px + 5, py - pr * 0.3, px + 10, py - pr * 1.2,
        fill = 'green', lineWidth=2)
#Draw Bunny
def drawBunny(bx, by, br, mouth, facing, powered):
    drawOval(bx - br * 0.45, by - br * 1.5,
        br * 0.32, br * 0.85, fill='white', border = 'pink', borderWidth=1)
    drawOval(bx + br * 0.45, by - br * 1.5,
             br * 0.32, br * 0.85, fill='white', border='pink', borderWidth=1)
    drawOval(bx - br * 0.45, by - br * 1.5, 
             br * 0.16, br * 0.5, fill='lightPink')
    drawOval(bx + br * 0.45, by - br * 1.5, 
              br * 0.16, br * 0.5, fill='lightPink')
    bodyColor = 'lightGoldenrodYellow' if powered else 'white'
    drawCircle(bx, by + br * 0.3, br * 1.1, fill=bodyColor, border='lightGray', borderWidth=1)
    drawArc(bx, by, br * 2, br * 2, 
            facing + mouth // 2, 360 - mouth,
            fill=bodyColor, border='lightGray', borderWidth=1)
    if facing == 0: eyeX = bx + br * 0.5; eyeY = by - br * 0.4
    elif facing == 180: eyeX = bx - br * 0.5; eyeY = by - br * 0.4
    elif facing == 90: eyeX = bx + br * 0.4; eyeY = by + br * 0.5
    else: eyeX = bx - br * 0.4; eyeY = by - br * 0.5
    drawCircle(eyeX, eyeY, 2.5, fill='saddlebrown')
    if facing == 0: noseX = bx + br * 0.85; noseY = by
    elif facing == 180: noseX = bx - br * 0.85; noseY = by
    elif facing==90: noseX = bx; noseY = by + br * 0.85
    else: noseX = bx; noseY = by - br * 0.85
    drawOval(noseX, noseY, 4, 3, fill='pink')
#Draw foxes
def drawFoxes(app):
    for i in range(3):
        fx = app.foxX[i]
        fy = app.foxY[i]
        fr = app.foxR
        color = 'steelBlue' if app.powered else 'darkorange'
        drawCircle(fx, fy, fr, fill=color, border='peru', 
            borderWidth=2)
        drawOval(fx, fy + fr * 0.2, fr * 0.55, fr * 0.65,
                 fill='bisque')
        if app.powered:
            drawLabel('?', fx, fy, size=fr, bold=True, fill='white')
        else: 
            drawArc(fx - fr * 0.5, fy - fr * 0.8, fr * 0.7, fr * 0.7, 
                    200, 140, fill='darkorange', border='peru', borderWidth=1)
            drawArc(fx + fr *  0.5, fy - fr * 0.8, fr * 0.7, fr * 0.7, 
                    200, 140, fill='darkorange', borderWidth=1)
            drawCircle(fx - fr * 0.32, fy - fr * 0.18, 3, fill='black')
            drawCircle(fx + fr * 0.32, fy - fr * 0.18, 3, fill='black')
            drawOval(fx, fy + fr * 0.18, fr * 0.38, fr * 0.28, fill='bisque')
            drawCircle(fx, fy + fr * 0.1, 2.5, fill='saddleBrown')
#Hud
def drawHUD(app):
    drawRect(0, 0, app.width, 42, fill='black', opacity =55)
    drawLabel(f'Eggs: {app.score}/{app.eggCount}', 80, 21, size = 15, 
            bold=True, fill='lightGreen', font='monospace')
    drawLabel('Lives:', 270, 21, size=14, fill='white', font='monospace')
    for i in range(app.lives):
        drawCircle(330 + i * 28, 21, 9, fill='white', border='lightGray', borderWidth=1)
        drawOval(325 + i * 28, 13, 4, 7, fill='white', border='pink', borderWidth=1)
        drawOval(335 + i * 28, 13, 3, 7, fill='white', border='pink', borderWidth=1)
    if app.powered:
        secs = app.powerTimer // 60 
        drawLabel(f'POWER! {secs}s', 490, 21, size=14, bold=True, fill='gold', font='monospace')
#Game over screen
def drawGameOver(app):
    drawRect(0, 0, app.width, app.height, fill='black')
    drawLabel('GAME OVER', 300, 200, size=48, bold=True, fill='crimson', font='monospace')
    drawLabel(f'You collected {app.score} eggs.', 300, 280, size=20, fill='white', font='monospace')
    drawLabel('better luck next Easter!', 300, 315, size=16, fill='gray', font='monospace')
    drawRect(175, 360, 250, 42, fill='crimson')
    drawLabel('Press SPACE to Retry', 300, 381, size=14, bold=True, fill='white', font='monospace')
#Win Screen
def drawWinScreen(app):
    drawRect(0, 0, app.width, app.height, fill='lightCyan')
    drawRect(0, app.height // 2, app.width, app.height // 2, fill='mediumSeaGreen')
    drawLabel('YOU WIN!', 300, 120, size=52, bold=True, fill='saddleBrown', font='monospace')
    drawLabel(f'ALL {app.score} eggs collected!', 300, 185, size = 20, fill='darkgreen', font='monospace')
    secret = 'Kdssb Hdvwhu!'
    decoded = decodeCaesar(secret, 3)
    drawRect(80, 225, 440, 80, fill='white', opacity=80, 
        border='saddleBrown', borderWidth=2)
    drawLabel('Secret message ( Caeser cipher, shift 3):', 300, 250, size=12, fill='gray', font='monospace')
    drawLabel(decoded, 300, 278, size=24, bold=True, fill='saddleBrown', font='monospace')
    drawRect(175, 330, 250, 42, fill='saddleBrown')
    drawLabel('Press SPACE to Play Again', 300, 351, size=13, bold=True, fill='white', font='monospace')
#Controlls
def onKeyPress(app,key):
    if app.state == 'start' and key == 'space':
        app.state = 'playing'
        return
    if app.state in ('gameover', 'win') and key == 'space': 
        resetGame(app)
        app.state = 'playing'
        return
    if app.state != 'playing':
        return
    if key=='right':
        app.bdx = app.bSpeed; app.bdy = 0; app.facing = 0
    elif key == 'left': app.bdx = -app.bSpeed; app.bdy = 0; app.facing = 180
    elif key == 'down': app.bdx = 0; app.bdy = app.bSpeed; app.facing = 90
    elif key == 'up': app.bdx = 0; app.bdy = -app.bSpeed; app.facing = 270
#Game logic
def onStep(app):
    if app.state != 'playing':
        return
    if app.respawning:
        app.respawnTimer -= 1
        if app.respawnTimer <= 0:
            app.respawning = False
        return
    #Bunny movement 
    app.bx += app.bdx
    app.by += app.bdy
    if app.bx < 0: app.bx = app.width
    if app.bx > app.width: app.bx = 0
    if app.by < 0: app.by = app.height
    if app.by > app.height: app.by = 0
    #Mouth Chomp
    app.mouth += app.mouthDir * 4 
    if app.mouth >= 55: app.mouthDir = -1
    if app.mouth <= 5: app.mouthDir = 1
    #Fox movement 
    for i in range(3):
        moveFox(app, i)
    if app.powered: 
        app.powerTimer -= 1 
        if app.powerTimer <= 0:
            app.powered = False
            app.powerTimer = 0
    #Egg collection
    for i in range(app.eggCount):
        if app.eggVisible[i]:
            if circlesOverlap(app.bx, app.by, app.br, app.eggX[i], app.eggY[i], app.eggR + 2):
                app.eggVisible[i] = False
                app.score += 1 
    #Carrot collection        
    if app.carrotVisible: 
        if circlesOverlap(app.bx, app.by, app.br, app.carrotX, app.carrotY, app.carrotR):
            app.carrotVisible = False
            app.powered = True
            app.powerTimer = 360
    #Fox collision
    foxHit = False
    for i in range(3):
        if circlesOverlap(app.bx, app.by, app.br, app.foxX[i], app.foxY[i], app.foxR):
            foxHit = True
    if foxHit: 
        if app.powered:
            app.foxX = [100, 500, 300]
            app.foxY = [120, 480, 100]
            app.score += 3
        else: 
            app.lives -= 1
            if app.lives <= 0:
                app.state = 'gameover'
            else: 
                app.bx = 300
                app.by = 300
                app.bdx = 0 
                app.bdy = 0
                app.respawning = True
                app.respawnTimer = 120
    #Win condition
    if app.score >= app.eggCount: 
        app.state = 'win'
def moveFox(app,i):
    fx = app.foxX[i]
    fy= app.foxY[i]
    fdx = app.foxDX[i]
    fdy = app.foxDY[i]
    fr = app.foxR
    if not app.powered: 
        if app.bx > fx: fdx = abs(fdx)
        else: fdx = -abs(fdx)
        if app.by > fy: fdy = abs(fdy)
        else: fdy = -abs(fdy)
    #Bounce of walls 
    fx += fdx
    fy += fdy
    if fx - fr < 0 or fx + fr > app.width:
        fdx *= -1 
        fx = max(fr, min(app.width - fr, fx))
    if fy - fr < 0 or fy + fr > app.height:
        fdy *= -1
        fy = max(fr, min(app.height - fr, fy))
    app.foxX[i] = fx
    app.foxY[i] = fy
    app.foxDX[i] = fdx
    app.foxDY[i] = fdy
    
def main():
    runApp(width=600, height=600)
    
main()
