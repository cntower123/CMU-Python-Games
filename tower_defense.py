# ========================================================================================================================================================
# TOWER DEFENSE - ICS4U Summative Capstone Project
# By: Liam M
# This was a grind :) Hope you like it! 
##========================================================================================================================================================
from cmu_graphics import *
import math
import random

# Model Classes - Custom OOP blueprints for game entities 
class Enemy:
    """
    Represents an enemy unit that follows a predefined path.
    Manages its own health, movement, and death state.
    """
    def __init__(self, enemyType, path, waveNum):
        self.path = path
        self.pathIndex = 0
        self.x, self.y = path[0]
        self.alive = True
        self.reachedEnd = False
        self.rewarded = False
        self.enemyType = enemyType
        if enemyType == 'normal':
            self.maxHp = 50 + waveNum * 12
            self.speed = 1.5
            self.reward = 10
            self.colour = 'crimson'
            self.radius = 8
        elif enemyType == 'fast':
            self.maxHp = 30 + waveNum * 6
            self.speed = 3.0
            self.reward = 15
            self.colour = 'orange'
            self.radius = 6
        elif enemyType == 'tank':
            self.maxHp = 120 + waveNum * 30
            self.speed = 0.8
            self.reward = 25
            self.colour = 'purple'
            self.radius = 12
        self.hp = self.maxHp
        
    def __repr__(self):
        return f'Enemy({self.enemyType}, hp={self.hp}/{self.maxHp})'
    
    def update(self):
        """Move this enemy along the path toward the next waypoint."""
        if not self.alive or self.reachedEnd:
            return
        if self.pathIndex >= len(self.path) - 1:
            self.reachedEnd = True
            return
        targetX, targetY = self.path[self.pathIndex + 1]
        dx = targetX - self.x
        dy = targetY - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < self.speed:
            self.pathIndex += 1 
            if self.pathIndex >= len(self.path) - 1:
                self.reachedEnd = True
                return
            self.x, self.y = self.path[self.pathIndex]
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed    
    
    def takeDamage(self, damage):
        """Apply damage and check for death."""
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0 
            self.alive = False

class Tower:
    """
    Represents a defensive tower placed on the grid.
    Tracks cooldown, finds targes, and fires prokectiles.
    """
    TYPES = {  
        'arrow': {'cost': 50, 'damage': 15, 'range': 80,
                'cooldown': 15, 'colour': 'dodgerBlue',
                'projcolour': 'lightBlue', 'projSpeed': 5,
                'splash': 0, 'name': 'Arrow'},
         
        'cannon': {'cost': 100, 'damage': 40, 'range': 65,
                'cooldown': 30, 'colour': 'forestGreen',
                'projcolour': 'lime', 'projSpeed': 3,
                'splash': 30, 'name': 'Cannon'},
                      
        'sniper': {'cost': 150, 'damage': 80, 'range': 150,
                    'cooldown': 50, 'colour': 'gold', 
                    'projcolour': 'yellow', 'projSpeed': 8,
                    'splash': 0, 'name': 'Sniper'},
    }
        
    def __init__(self, gridRow, gridCol, towerType, cellW, cellH, boardLeft, boardTop):
        self.gridRow = gridRow
        self.gridCol = gridCol
        self.towerType = towerType
        stats = Tower.TYPES[towerType]
        self.damage = stats['damage']
        self.range = stats['range']
        self.maxCooldown = stats['cooldown']
        self.cooldown = 0
        self.colour = stats['colour']
        self.projcolour = stats['projcolour']
        self.splash = stats['splash']
        self.projSpeed = stats['projSpeed']
        self.level = 1
        self.x = boardLeft + gridCol * cellW + cellW / 2
        self.y = boardTop + gridRow * cellH + cellH / 2
        
    def __repr__(self):
        return f'Tower({self.towerType}, level={self.level})'
    
    def update(self, enemies, projectiles):
        """Tick cooldown and fire at the closet enemy in range."""
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        target = self.findTarget(enemies)
        if target is not None:
            proj = Projectile(self.x, self.y, target, self.damage, self.projcolour, self.projSpeed, self.splash)
            projectiles.append(proj)
            self.cooldown = self.maxCooldown
    
    def findTarget(self, enemies):
        """Return the closest alive enemy within firing range."""
        bestEnemy = None
        bestDist = self.range + 1
        for enemy in enemies:
            if enemy.alive and not enemy.reachedEnd:
                dist = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
                if dist <= self.range and dist < bestDist:
                    bestDist = dist
                    bestEnemy = enemy
        return bestEnemy
    
    def getUpgradeCost(self):
        """calculate cost to upgrage this tower."""
        baseCost = Tower.TYPES[self.towerType]['cost']
        return baseCost // 2 * self.level
    
    def upgrade(self):
        """Increase this tower's stats."""
        self.level += 1
        self.damage = int(self.damage * 1.5)
        self.range = int(self.range * 1.15)
        self.maxCooldown = max(5, self.maxCooldown - 3)
        
class Projectile:
    """
    Represents a projectile fired from a tower toward an enemy. Handles movement, hit detection,
    and splash damage.
    """
    def __init__(self, x, y, target, damage, colour, speed, splash):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.colour = colour
        self.speed = speed
        self.splash = splash
        self.alive = True
        self.radius = 4
    
    def update(self, enemies):
        """Move toward the target and check for collision."""
        if not self.target.alive:
            self.alive = False
            return
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < self.speed + self.target.radius:
            self.hitTarget(enemies)
            self.alive = False
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
    
    def hitTarget(self, enemies):
        """Deal damage on impact. Apply splash if applicable."""
        self.target.takeDamage(self.damage)
        if self.splash > 0:
            for enemy in enemies:
                if enemy is not self.target and enemy.alive:
                    dist = math.sqrt((self.target.x - enemy.x) ** 2 + (self.target.y - enemy.y) ** 2)
                    if dist <= self.splash:
                        enemy.takeDamage(self.damage // 2)
class Wave:
    """
    manages spawning a sequence of enemies for a single wave. Difficulty scales automatically with wave number.
    """
    def __init__(self, waveNum, path):
        self.waveNum = waveNum
        self.path = path
        self.spawnQueue = self.buildSpawnQueue()
        self.spawnIndex = 0
        self.spawnTimer = 0
        self.spawnDelay = 20
        self.complete = False
    
    def buildSpawnQueue(self):
        """Generate the enemy type sequence for this wave."""
        queue = []
        numEnemies = 5 + self.waveNum * 2
        for i in range(numEnemies):
            if i % 5 == 4 and self.waveNum >= 3:
                queue.append('tank')
            elif i % 3 == 2 and self.waveNum >= 2:
                queue.append('fast')
            else:  
                queue.append('normal')
        return queue
    
    def update(self):
        """Spawn the next enemy when the timer allows."""
        if self.spawnIndex >= len(self.spawnQueue):
            self.complete = True
            return None
        self.spawnTimer -= 1
        if self.spawnTimer <= 0:
            enemyType = self.spawnQueue[self.spawnIndex]
            self.spawnIndex += 1 
            self.spawnTimer = self.spawnDelay
            return Enemy(enemyType, self.path, self.waveNum)
        return None

#CONTROLLER - Game state management and input handling

def onAppStart(app):
    """Initialize the application and all persistent game state."""
    app.rows = 8
    app.cols = 12
    app.boardLeft = 10
    app.boardTop = 55
    app.boardWidth = 380
    app.boardHeight = 280
    app.cellWidth = app.boardWidth / app.cols
    app.cellHeight = app.boardHeight / app.rows
    app.pathCells = buildPathCells(app)
    app.pathPixels = gridPathToPixels(app, app.pathCells)
    app.stepsPerSecond = 30
    resetGame(app)

def resetGame(app):
    """Reset all mutable game state for a new game."""
    app.state = 'start'
    app.money = 200
    app.lives = 20
    app.score = 0
    app.waveNum = 0
    app.maxWaves = 10
    app.towers = []
    app.enemies = []
    app.projectiles = []
    app.currentWave = None
    app.waveActive = False
    app.betweenWaves = True
    app.selectedTowerType = 'arrow'
    app.hoveredCell = None
    app.grid = [[None] * app.cols for row in range(app.rows)]
    for row, col in app.pathCells:
        app.grid[row][col] = 'path'

def buildPathCells(app):
    """Define the enemy path as a list of (row, col) gril cells."""
    path = []
    for col in range(app.cols):
        path.append((1, col))
    for row in range(2, 5):
        path.append((row, app.cols - 1))
    for col in range(app.cols - 1, -1, -1):
        path.append((4, col))
    for row in range(5, 8):
        path.append((row, 0))
    for col in range(app.cols):
        path.append((7, col))
    cleaned = [path[0]]
    for i in range(1, len(path)):
        if path[i] != path[i - 1]:
            cleaned.append(path[i])
    return cleaned

def gridPathToPixels(app, pathCells):
    """Convery gril-cells path to pixel-coordinate waypoints."""
    waypoints = [pathCells[0]]
    for i in range(1, len(pathCells) - 1):
        prevR, prevC = pathCells[i - 1]
        currR, currC = pathCells[i]
        nextR, nextC = pathCells[i + 1]
        dr1, dc1 = currR - prevR, currC - prevC
        dr2, dc2 = nextR - currR, nextC - currC
        if (dr1, dc1) != (dr2, dc2):
            waypoints.append(pathCells[i])
    waypoints.append(pathCells[-1])
    pixels = []
    for row, col in waypoints:
        px = app.boardLeft + col * app.cellWidth + app.cellWidth / 2
        py = app.boardTop + row * app.cellHeight + app.cellHeight / 2
        pixels.append((px, py))
    return pixels
    
def onKeyPress(app, key):
    """Handle all keyboard inpput based on current game state."""
    if app.state == 'start':
        if key == 'space':
            app.state = 'playing'
        return
    if app.state in ('gameover', 'won'):
        if key == 'r':
            resetGame(app)
            app.state = 'start'
        return
    if app.state == 'playing':
        if key == '1':
            app.selectedTowerType = 'arrow'
        elif key == '2':
            app.selectedTowerType = 'cannon'
        elif key == '3':
            app.selectedTowerType = 'sniper'
        elif key == 'space' and app.betweenWaves:
            startNextWave(app)
            
def onMouseMove(app, mouseX, mouseY):
    """Track which grid cell the mouse hovers over."""
    if app.state != 'playing':
        app.hoveredCell = None
        return
    col = int((mouseX - app.boardLeft) / app.cellWidth)
    row = int((mouseY - app.boardTop) / app.cellHeight)
    if 0 <= row < app.rows and 0 <= col < app.cols:
        app.hoveredCell = (row, col)
    else:
        app.hoveredCell = None
        
def onMousePress(app, mouseX, mouseY):
    """Handle clicks: place towers or upgrade existing ones."""
    if app.state != 'playing' or app.hoveredCell is None:
        return
    row, col = app.hoveredCell
    cell = app.grid[row][col]
    if isinstance(cell, Tower):
        tower = cell
        cost = tower.getUpgradeCost()
        if app.money >= cost and tower.level < 3:
            app.money -= cost
            tower.upgrade()
        return
    if cell is not None:
        return
    cost = Tower.TYPES[app.selectedTowerType]['cost']
    if app.money >= cost:
        tower = Tower(row, col, app.selectedTowerType, app.cellWidth, app.cellHeight, app.boardLeft, 
        app.boardTop)
        app.grid[row][col] = tower
        app.towers.append(tower)
        app.money -= cost

def startNextWave(app):
    """Initialize and begin the next enemy wave."""
    app.waveNum += 1
    app.currentWave = Wave(app.waveNum, app.pathPixels)
    app.waveActive = True
    app.betweenWaves = False

def onStep(app):
    """Main game loop - updates all game entities each frame."""
    if app.state != 'playing':
        return
    if app.waveActive and app.currentWave is not None:
        newEnemy = app.currentWave.update()
        if newEnemy is not None:
            app.enemies.append(newEnemy)
    for enemy in app.enemies:
        enemy.update()
    for enemy in app.enemies:
        if enemy.reachedEnd and not enemy.rewarded:
            app.lives -= 1
            enemy.rewarded = True
    for tower in app.towers:
        tower.update(app.enemies, app.projectiles)
    for proj in app.projectiles:
        proj.update(app.enemies)
    for enemy in app.enemies:
        if not enemy.alive and not enemy.rewarded:
            app.money += enemy.reward
            app.score += enemy.reward
            enemy.rewarded = True
    app.enemies = [e for e in app.enemies if e.alive and not e.reachedEnd]
    app.projectiles = [p for p in app.projectiles if p.alive]
    if (app.waveActive and app.currentWave is not None and app.currentWave.complete and len(app.enemies) == 0):
        app.waveActive = False
        app.betweenWaves = True
        if app.waveNum >= app.maxWaves:
            app.state = 'won'
    if app.lives <= 0:
        app.lives = 0
        app.state = 'gameover'
        
#VIEW - All drawing functions (purely read from model state)
def redrawAll(app):
    """Master draw dispatcher - renders the correct screen."""
    if app.state == 'start':
        drawStartScreen(app)
    elif app.state == 'playing':
        drawGameScreen(app)
    elif app.state == 'gameover':
        drawGameScreen(app)
        drawOverlay(app, 'GAME OVER', 'crimson', f'Final Score: {app.score}', f'Waves survived: {app.waveNum}')
    elif app.state == 'won':
        drawGameScreen(app)
        drawOverlay(app, 'VICTORY', 'gold', f'Final Score: {app.score}', f'Lives remaining: {app.lives}')

def drawStartScreen(app):
    """Render the title screen with instructions."""
    drawRect(0, 0, 400, 400, fill='darkSlateGray')
    drawLabel('TOWER DEFENSE', 200, 100, size=30, bold=True, fill='white')
    drawLabel('Defend your base from waves of enemies!', 200, 140, size=14, fill='lightGray')
    drawLabel('Press SPACE to start', 200, 280, size=16, fill='cyan')
    types = ['arrow', 'cannon', 'sniper']
    for i in range(len(types)):
        t = types[i]
        cx = 100 + i * 100
        drawCircle(cx, 200, 14, fill=Tower.TYPES[t]['colour'], border='white', borderWidth=1)
        drawLabel(Tower.TYPES[t]['name'], cx, 225, size=11, fill='lightGray')
    drawLabel('1/2/3 = Select tower - Click = Place/Upgrade', 200, 310, size=14, fill='orange')
    drawLabel('SPACE = send next wave', 200, 328, size=14, fill='orange')
        
def drawGameScreen(app):
    """Render the full in-game view."""
    drawRect(0, 0, 400, 400, fill='darkSlateGray')
    drawGrid(app)
    drawPath(app)
    drawTowerRanges(app)
    drawTowers(app)
    drawEnemies(app)
    drawProjectiles(app)
    drawHoverPreview(app)
    drawHUD(app)
    drawTowerPanel(app)
    
def drawGrid(app):
    """Draw the background grill cells."""
    for row in range(app.rows):
        for col in range(app.cols):
            x = app.boardLeft + col * app.cellWidth
            y = app.boardTop + row * app.cellHeight
            drawRect(x, y, app.cellWidth, app.cellHeight, fill='darkOliveGreen', border='olive', borderWidth=1)

def drawPath(app):
    """Draw path cells in a distinct colour."""
    for row, col in app.pathCells:
        x = app.boardLeft + col * app.cellWidth
        y = app.boardTop + row * app.cellHeight
        drawRect(x, y, app.cellWidth, app.cellHeight, fill='sandyBrown', border='peru', borderWidth=1)
        
def drawTowerRanges(app):
    """Show range circle when hovering over a tower."""
    if app.hoveredCell is None:
        return
    hRow, hCol = app.hoveredCell
    cell = app.grid[hRow][hCol]
    if isinstance(cell, Tower):
        drawCircle(cell.x, cell.y, cell.range, fill=None, border='white', borderWidth=1, opacity=25)
        
def drawTowers(app):
    """Draw all placed towers with level indicators."""
    for tower in app.towers:
        drawCircle(tower.x, tower.y, 13, fill=tower.colour, border='black', borderWidth=2)
        if tower.level > 1:
            drawLabel(str(tower.level), tower.x, tower.y, size=10, bold=True, fill='white')
            
def drawEnemies(app):
    """Draw all alive enemies with health bars."""
    for enemy in app.enemies:
        if not enemy.alive:
            continue
        drawCircle(enemy.x, enemy.y, enemy.radius, fill=enemy.colour, border='black', borderWidth=1)
        barW, barH = 20, 3
        barX = enemy.x - barW / 2
        barY = enemy.y - enemy.radius - 6
        drawRect(barX, barY, barW, barH, fill='darkRed')
        hpRatio = enemy.hp / enemy.maxHp
        drawRect(barX, barY, barW * hpRatio, barH, fill='lime')
        
def drawProjectiles(app):
    """Dra all active projectiles."""
    for proj in app.projectiles:
        if proj.alive:
            drawCircle(proj.x, proj.y, proj.radius, fill=proj.colour)

def drawHoverPreview(app):
    """Show ghoast tower and range on empty hovered cell."""
    if app.hoveredCell is None:
        return
    row, col = app.hoveredCell
    if app.grid[row][col] is not None:
        return 
    stats = Tower.TYPES[app.selectedTowerType]
    px = app.boardLeft + col * app.cellWidth + app.cellWidth / 2
    py = app.boardTop + row * app.cellHeight + app.cellHeight / 2
    canAfford = app.money >= stats['cost']
    c = stats['colour'] if canAfford else 'gray'
    drawCircle(px, py, stats['range'], fill=None, border=c, borderWidth=1, opacity=25)
    drawCircle(px, py, 13, fill=c, opacity=40)
 
def drawHUD(app):
    """Draw the HUD at the top."""
    drawRect(0, 0, 400, 50, fill='black',opacity=75)
    drawLabel(f'${app.money}', 45, 14, size=13, fill='gold', bold=True)
    drawLabel(f'Lives: {app.lives}',130, 14, size=13, fill='crimson', bold=True)
    drawLabel(f'Wave: {app.waveNum}/{app.maxWaves}', 240, 14, size=13, fill='white', bold=True)
    if app.betweenWaves:
        drawLabel('Press SPACE for next wave', 200, 38, size=11, fill='lime')
    elif app.waveActive:
        drawLabel(f'Enemies: {len(app.enemies)}', 200, 38, size=11, fill='lightGray')
        
def drawTowerPanel(app):
    """Draw the tower selection panel at the bottom."""
    panelY = 345
    drawRect(0, panelY, 400, 55, fill='black', opacity=75)
    towerKeys = ['arrow', 'cannon', 'sniper']
    labels = ['1: Arrow $50', '2: Cannon $100', '3: Sniper $150']
    for i in range(3):
        cx = 70 + i * 130
        tType = towerKeys[i]
        color = Tower.TYPES[tType]['colour']
        selected = (app.selectedTowerType == tType)
        bColor = 'white' if selected else 'gray'
        bWidth = 2 if selected else 1 
        drawRect(cx - 58, panelY + 5, 116, 40, fill=None, border=bColor, borderWidth=bWidth)
        drawCircle(cx - 38, panelY + 25, 9, fill=color, border='black', borderWidth=1)
        drawLabel(labels[i], cx + 12, panelY + 25, size=11, fill='white')
        
def drawOverlay(app, title, titleColor, line1, line2):
    """Draw a semi-transparent overlay with title and info."""
    drawRect(0, 0, 400, 400, fill='black', opacity=70)
    drawLabel(title, 200, 150, size=32, bold=True, fill=titleColor)
    drawLabel(line1, 200, 195, size=16, fill='white')
    drawLabel(line2, 200, 220, size=13, fill='lightGray')
    drawLabel('Press R to restart', 200, 270, size=16, fill='cyan')
    
    
    
def main():
    runApp()
    
main()