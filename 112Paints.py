from cmu_graphics import *
import random
import math
import copy


def onAppStart(app):
    app.drawRect = False
    app.drawCircle = False
    app.drawLine = False
    app.drawPoly = False
    app.drawFree = False
    app.width = 700
    app.height = 450
    app.currColor = 'red'
    app.currShape = None
    app.red = fillButtons(5, 290, 'red')
    app.red.border = 'limeGreen'
    app.orange = fillButtons(40, 290, 'orange')
    app.yellow = fillButtons(5, 330, 'yellow')
    app.green = fillButtons(40, 330, 'green')
    app.blue = fillButtons(5, 370, 'blue')
    app.purple = fillButtons(40, 370, 'purple')
    app.black = fillButtons(5, 410, 'black')
    app.gray = fillButtons(40, 410, 'gray')
    app.fillColors = [app.red, app.orange, app.yellow, app.green, app.blue, app.purple, app.black, app.gray]
    app.rect = rect(5,60)
    app.circle = circle(40, 60)
    app.line = line(5, 100)
    app.poly = poly(40, 100)
    app.freeDrawing = freeDrawing(5, 140)
    app.shapeButtons = [app.rect, app.circle, app.line, app.poly, app.freeDrawing]
    app.allShapes = []
    app.allPoly = []
    app.rw= app.rh = 0
    app.rl = app.rt = app.cx = app.cy = app.cr = 0
    app.align = 'left-top'
    app.x1 = app.y1 = app.x2 = app.y2 = 0
    app.drawSingleLine = []
    app.polyDots = []
    app.drawMyPoly = False
    app.lines = []
    app.allRect = []
    app.allCircle = []
    app.lastValue = []
    app.drawingPoints = []
    app.remove = deleteAndUndo(5, 180, 'remove')
    app.undo = deleteAndUndo(40, 180, 'undo')
    app.processButtons = [app.remove, app.undo]
    app.allLines = []
    app.linestemp = []
    app.polyColorIndex = []
    app.freeLineIndex = []
    app.polyPop = []
    app.freePop = []
    
#Helper buildings
def distance(x1,y1, x2, y2):
    return ((x2-x1)**2+(y2-y1)**2)**.5
    
    
class fillButtons:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.border = 'black'
    def getColor(self):
        return self.color

class shapeButtons:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.border = 'black'
        
class rect(shapeButtons):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.shape = 'rect'

class circle(shapeButtons):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.shape = 'circle'

class line(shapeButtons):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.shape = 'line'

class poly(shapeButtons):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.shape = 'polygon'
        self.dots = []
    def addDots(self, x,y):
        self.dots.append((x,y))

class freeDrawing(shapeButtons):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.shape = 'freeDrawing'

class deleteAndUndo:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label


def redrawAll(app):
    drawUI(app)
    drawFillButtons(app)
    drawShapeButtons(app)
    drawActualShapes(app)
    drawInBoard(app)
def drawRect1(app):
    for (left, top, width, height, align2, color) in app.allRect:
        drawRect(left, top, width, height, align = align2, fill = color)
def drawCircle1(app):
    for (cx, cy, r, color) in app.allCircle:
        drawCircle(cx, cy, r, fill = color)
def drawLine1(app):
     for (x1, y1, x2, y2, color) in app.drawSingleLine:
        drawLine(x1,y1,x2,y2, fill = color)
def drawPoly1(app):

    if app.drawMyPoly:
        q = 0 
        for poly in app.allPoly:
            drawPolygon(*poly, fill = app.polyColorIndex[i])
            q += 1
def drawFree1(app):
    j = 0
    for line1 in app.allLines:
        for i in range(len(line1) -1):
            x1, y1 = line1[i]
            x2, y2 = line1[i+1]
            drawLine(x1,y1,x2,y2, fill =app.freeLineIndex[j])
        j += 1
    
def drawActualShapes(app):
    i = j = x = y = z = 0
    w = 0
    for elements in app.allShapes:
        if elements in app.allRect:
            left, top, width, height, align2, color = app.allRect[i]
            drawRect(left, top, width, height, align = align2, fill = color)
            i += 1
        elif elements in app.allCircle:
            cx, cy, r, color = app.allCircle[j]
            drawCircle(cx, cy, r, fill = color)
            j += 1
        elif elements in app.drawSingleLine:
             x1, y1, x2, y2, color = app.drawSingleLine[x]
             drawLine(x1,y1,x2,y2, fill = color)
             x += 1
        elif elements in app.allPoly:
            poly = app.allPoly[y]
            drawPolygon(*poly, fill = app.polyColorIndex[y])
            y += 1
        elif elements in app.allLines:
            for q in range(len(app.allLines[z]) -1):
                x1, y1 = app.allLines[z][q]
                x2, y2 = app.allLines[z][q+1]
                drawLine(x1,y1,x2,y2, fill = app.freeLineIndex[w])
            z += 1
            w += 1
    
    
def drawInBoard(app):
    if app.drawRect:
        if app.rw != 0 and app.rh != 0 and app.rl != 0 and app.rt != 0:
            drawRect(app.rl, app.rt, app.rw, app.rh, fill = None, border = app.currColor, align = app.align)
    elif app.drawCircle:
        if app.cx != 0 and app.cy != 0 and app.cr != 0:
            drawCircle(app.cx, app.cy, app.cr, fill = None, border = app.currColor)
    elif app.drawLine:
        if app.x1 != 0 and app.x2 != 0 and app.y1 != 0 and app.y2 != 0:
            drawLine(app.x1, app.y1, app.x2, app.y2, fill = app.currColor)
    elif app.drawPoly:
        if app.poly.dots != []:
            for i in range(len(app.poly.dots)):
                x, y = app.poly.dots[i]
                if i == 0:
                    color = 'darkGreen'
                else:
                    color = 'red'
                drawLabel('x', x, y, fill = color)
    elif app.drawFree:
        for i in range(len(app.linestemp) -1):
                    x1, y1 = app.linestemp[i]
                    x2, y2 = app.linestemp[i+1]
                    drawLine(x1,y1,x2,y2, fill = app.currColor)

def drawFillButtons(app):
    drawRect(app.red.x,app.red.y, 30, 30, fill = app.red.color, border = app.red.border)
    drawRect(app.orange.x,app.orange.y, 30, 30, fill = app.orange.color, border = app.orange.border)
    drawRect(app.yellow.x,app.yellow.y, 30, 30, fill = app.yellow.color, border = app.yellow.border)
    drawRect(app.green.x,app.green.y, 30, 30, fill = app.green.color, border = app.green.border)
    drawRect(app.blue.x,app.blue.y, 30, 30, fill = app.blue.color, border = app.blue.border)
    drawRect(app.purple.x,app.purple.y, 30, 30, fill = app.purple.color, border = app.purple.border)
    drawRect(app.black.x,app.black.y, 30, 30, fill = app.black.color, border = app.black.border)
    drawRect(app.gray.x,app.gray.y, 30, 30, fill = app.gray.color, border = app.gray.border)

def drawShapeButtons(app):
    drawRect(app.rect.x, app.rect.y, 30, 30, fill = None, border = app.rect.border)
    drawRect(10,65, 20, 20, fill = 'darkGray', border = 'dimGray')
    drawRect(app.circle.x, app.circle.y, 30, 30, fill = None, border = app.circle.border)
    drawCircle(55, 75, 10, fill = 'darkGray', border = 'dimGray')
    drawRect(app.line.x, app.line.y, 30, 30, fill = None, border = app.line.border)
    drawLine(12, 123, 28, 107, fill = 'dimGray')
    drawRect(app.poly.x, app.poly.y, 30, 30, fill = None, border = app.poly.border)
    drawPolygon(45, 110, 62, 105, 59, 125,50, 120, fill = 'darkGray', border = 'dimGray')
    drawRect(app.freeDrawing.x, app.freeDrawing.y, 30, 30, fill = None, border = app.freeDrawing.border)

def drawUI(app):
    drawRect(0,0,app.width,app.height, fill = 'gainsboro')
    drawRect(75,50,605,380, fill = 'white', )
    drawLabel('112 Paints', 350, 25, font = 'caveat', size = 30)
    drawLabel('Fill Options', 37, 275, size = 13, italic = True)
    drawLine(0,50, 750, 50)
    drawLine(75, 50, 75, 450)
    drawLine(75, 430, 680, 430)
    drawLine(680,50, 680, 430)
    drawRect(app.remove.x, app.remove.y, 30, 30, border = 'black', fill = None)
    drawLabel('z', 11, 204, fill = 'dimGray', size = 10)
    drawRect(app.undo.x, app.undo.y, 30, 30, border = 'black', fill = None)
    drawLabel('y', 46, 204, fill = 'dimGray', size = 10)
    drawLabel(chr(0x1f589),20,155, font= 'symbols', fill = 'dimGray', size = 20)
    drawLabel(chr(0x21e6),20,195, font= 'symbols', fill = 'dimGray', size = 20)
    drawLabel(chr(0x21e8),55,195, font= 'symbols', fill = 'dimGray', size = 20)

def onMousePress(app, mouseX, mouseY):
    selectingLogic(app, mouseX, mouseY)
    drawingLogic(app,mouseX,mouseY)
    deleteAndUndoLogic(app,mouseX, mouseY)
    
def deleteAndUndoLogic(app,mouseX, mouseY):
    for button in app.processButtons:
        left, top, width, height = button.x, button.y, 30, 30
        if mouseX >= left and mouseX <= left + width and mouseY >= top and mouseY <= top+height:
            if button.label == 'remove':
                doRemoveAction(app)
            if button.label == 'undo':
                doUndoAction(app)

def doRemoveAction(app):
    if app.allShapes != []:
        lastItem = app.allShapes[-1]
        if lastItem in app.allRect:
            app.allRect.remove(lastItem)
        if lastItem in app.allCircle:
            app.allCircle.remove(lastItem)
        if lastItem in app.drawSingleLine:
            app.drawSingleLine.remove(lastItem)
        if lastItem in app.allPoly:
            app.allPoly.remove(lastItem)
            app.polyPop.append(app.polyColorIndex.pop())
        if lastItem in app.allLines:
            app.allLines.remove(lastItem)
            app.freePop.append(app.freeLineIndex.pop())
        app.lastValue.append(app.allShapes.pop())
        
def doUndoAction(app):
    if app.lastValue != []:
        undoShape = app.lastValue.pop()
        check = True
        for x in undoShape:
            if not isinstance(x, int):
                check = False
        if check:
            app.allPoly.append(undoShape)
            app.allShapes.append(undoShape)
            app.polyColorIndex.append(app.polyPop.pop())
            return
        if isinstance(undoShape, list):
            app.allLines.append(undoShape)
            app.freeLineIndex.append(app.freePop.pop())
        elif len(undoShape) == 6:
            app.allRect.append(undoShape)
        elif len(undoShape) == 5:
            app.drawSingleLine.append(undoShape)
        elif len(undoShape) == 4:
            app.allCircle.append(undoShape)
        app.allShapes.append(undoShape)

def onKeyPress(app, key):
    if key == 'z':
        doRemoveAction(app)
    if key == 'y':
        doUndoAction(app)
        
def drawingLogic(app, mouseX, mouseY):
    if mouseX > 75:
        if app.currShape == 'rect':
            app.drawRect = True
            app.rl = mouseX
            app.rt = mouseY
            app.lastValue = []
        if app.currShape == 'circle':
            app.drawCircle = True
            app.cx = mouseX
            app.cy = mouseY
            app.lastValue = []
        if app.currShape == 'line':
            app.drawLine = True
            app.x1 = mouseX
            app.y1 = mouseY
            app.lastValue = []
        if app.currShape == 'polygon':
            app.drawPoly = True
            app.lastValue = []
            if mouseX > 75 and mouseX < 680 and mouseY > 50 and mouseY < 430:
                makePoly(app, mouseX, mouseY)
                if app.drawPoly == True:
                    doPolyAction(app, mouseX, mouseY)
        if app.currShape == 'freeDrawing':
            app.drawFree = True
            app.lastValue = []


def makePoly(app, mouseX, mouseY):
    if app.poly.dots != []:
        x, y = app.poly.dots[0]
        if distance(x,y, mouseX, mouseY) <=5:
            app.drawMyPoly = True
            app.allPoly.append(app.polyDots)
            app.allShapes.append(app.polyDots)
            app.polyColorIndex.append(app.currColor)
            app.poly.dots = []
            app.polyDots = []
            app.drawPoly = False
            return
        
def doPolyAction(app, mouseX, mouseY):
    app.polyDots.append(mouseX)
    app.polyDots.append(mouseY)
    app.poly.addDots(mouseX,mouseY)
            
def selectingLogic(app, mouseX, mouseY):
    #selectColors
    for fillButton in app.fillColors:
        left, top, width, height = fillButton.x, fillButton.y, 30, 30
        if mouseX >= left and mouseX <= left + width and mouseY >= top and mouseY <= top+height:
            if fillButton.border == 'black':
                fillButton.border = 'limeGreen'
                app.currColor = fillButton.color
                fixHighLight(app, mouseX, mouseY)
            else:
                fillButton.border = 'black'
                app.currColor = None
    #select Shapes
    for shape in app.shapeButtons:
        left, top, width, height = shape.x, shape.y, 30, 30
        if mouseX >= left and mouseX <= left + width and mouseY >= top and mouseY <= top+height:
            app.polyDots = []
            app.drawPoly = False
            app.poly.dots = []
            if shape.border == 'black':
                shape.border = 'limeGreen'
                app.currShape = shape.shape
                fixHighLight(app, mouseX, mouseY)
            else:
                shape.border = 'black'
                app.currShape = None
    
def fixHighLight(app, mouseX, mouseY):
    for fillButton in app.fillColors:
        if app.currColor != fillButton.color:
            fillButton.border = 'black'
    for shape in app.shapeButtons:
        if shape.shape != app.currShape:
            shape.border = 'black'
            
def onMouseDrag(app, mouseX, mouseY):
    if app.drawRect:
        if mouseX > 75 and mouseX < 680  and mouseY > 50 and mouseY < 430:
            if mouseY < app.rt and mouseX > app.rl:
                app.align = 'left-bottom'
            if mouseY < app.rt and mouseX < app.rl:
                app.align = 'right-bottom'
            if mouseY > app.rt and mouseX > app.rl:
                app.align = 'left-top'
            if mouseY > app.rt and mouseX < app.rl:
                app.align = 'top-right'
            app.rw = abs(app.rl -mouseX) 
            app.rh = abs(app.rt -mouseY)
    if app.drawCircle:
        app.cr = distance(app.cx, app.cy, mouseX, mouseY)
        maxRadius = min(app.cx -75, 680 - app.cx, app.cy - 50, 430 - app.cy)
        app.cr = min(maxRadius, app.cr)
    if app.drawLine:
        if mouseX > 75 and mouseX < 680  and mouseY > 50 and mouseY < 430:
            app.x2 = mouseX
            app.y2 = mouseY
    if app.drawFree:
        if mouseX > 75 and mouseX < 680  and mouseY > 50 and mouseY < 430:
            app.lines.append((mouseX, mouseY))
            app.linestemp.append((mouseX, mouseY))

def onMouseRelease(app,mouseX,mouseY):
    app.drawRect = False
    app.drawCircle = False
    app.drawLine = False
    align = app.align
    color = app.currColor
    if app.drawFree:
        app.linestemp = []
        app.drawFree = False
        app.freeLineIndex.append(color)
        app.lines.append((mouseX,mouseY))
        app.allLines.append(app.lines)
        app.allShapes.append(app.lines)
        app.lines = []
    if app.rw != 0 and app.rh != 0 and app.rl != 0 and app.rt != 0:
        app.allRect.append((app.rl, app.rt, app.rw, app.rh, align, color))
        app.allShapes.append((app.rl, app.rt, app.rw, app.rh, align, color))
    if app.cx != 0 and app.cy != 0 and app.cr != 0:
        app.allCircle.append((app.cx, app.cy, app.cr, color))
        app.allShapes.append((app.cx, app.cy, app.cr, color))
    if app.x1 != 0 and app.x2 != 0 and app.y1 != 0 and app.y2 !=0:
        app.drawSingleLine.append((app.x1, app.y1, app.x2, app.y2, color))
        app.allShapes.append((app.x1, app.y1, app.x2, app.y2, color))
    app.x1 = app.x2 = app.y1 = app.y2 = 0
    app.cx = app.cy = app.cr = 0
    app.rw = app.rh = app.rl = app.rt = 0
            
def main():
    runApp()

main()
