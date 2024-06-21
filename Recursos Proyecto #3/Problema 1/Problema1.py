import pygame as pg, time as ti, random as ra, ctypes as ct, serial as sl
from pygame.locals import * 
#askjdfhaskdfl
nRes = (960,480); nt_WX = nt_HY = 32; lGo = True
nMIN_X = 0 ; nMAX_X = 6400 ; nMIN_Y = 0 ; nMAX_Y = 480; nMAX_ROBOTS = 100
nMx = nMy = 0; nMAX_ROBOTSsicensa = 10
nX0 = 19 ; nY0 = 405 ; yd = 0; xd = 0
#200 columnas y 15 filas
#----------------------------------------------------
#       Estructura Robots
#----------------------------------------------------
class eRobot(ct.Structure):
    __fields__ = [
        ('nF',ct.c_ushort), #Figura
        ('nX',ct.c_ushort), #Pos X
        ('nY',ct.c_ushort), #Pos Y
        ('nR',ct.c_ushort), #Rango
        ('nS',ct.c_ushort), #
        ('dX',ct.c_ushort),
        ('dY',ct.c_ushort),
        ('nV',ct.c_ushort),
        ('nC',ct.c_ushort),
        ('Recursostiles'),
        ('Tilescensados')
]
#----------------------------------------------------
#       Estructura Celda Inteligente Mapa
#----------------------------------------------------
class eCelda(ct.Structure):
    _fields_ = [
        ('nT',ct.c_ubyte), # Tipo de Tile/Baldosa
        ('nS',ct.c_ubyte), # 0 : No se pinta - # 1 : Si se pinta
        ('nF',ct.c_ubyte), # Fila de Mapa
        ('nC',ct.c_ubyte), # Columna de Mapa 
        ('nR',ct.c_ubyte), # Tipo de recurso
        ('nQ',ct.c_ubyte), # cantidad de recurso
        ]  
     
def Load_Image(sFile,transp = False):
    try: image = pg.image.load(sFile)
    except pg.error as message:
        raise SystemExit(message)
    image = image.convert()
    if transp:
       color = image.get_at((0,0))
       image.set_colorkey(color,RLEACCEL)
    return image

def init_Pygame():
    pg.init()
    pg.mouse.set_visible(False) 
    pg.display.set_caption('Fondo robots | Proyecto P.R #3.2')
    return pg.display.set_mode(nRes)

#---------------------------------------------------------------------
# Inicilaiza parametros de los Robots
#---------------------------------------------------------------------
def init_Robot():
    for i in range(0,nMAX_ROBOTS):
        aBoe[i].nF = 1    # Robot Tipo 1
        aBoe[i].nX = (ra.randint(0,nMAX_X - nt_WX) / nt_WX) * nt_WX 
        aBoe[i].nY = (ra.randint(0,nMAX_Y - nt_HY) / nt_HY) * nt_HY
        aBoe[i].nR = 1 # (RA.randint(0,nRES[0] - nT_WX) / nT_WX) * nT_WX
        aBoe[i].nS = 1 # Switch por defecto
        aBoe[i].dX = 0 # Por defecto robot Direccion Este.-
        aBoe[i].dY = 1
        aBoe[i].nV = 1 
        aBoe[i].nC = 1 
        aBoe[i].Recursostiles = []
        aBoe[i].Tilescensados = []
    for i in range(0,nMAX_ROBOTSsicensa):
        aBoe[i].nF = 2
    return

def Init_Fig():         
    aImg = []
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\T00.png',  True )) # robot no censador id = 0
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\T02.png',  True ))   # robot censador   id = 1
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\T04.png',  False ))   # tile de tierra   id = 2
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\T05.png',  False ))   # tile de roca   id = 3
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\T06.png',  False ))   # tile de acero   id = 4
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\T08.png',  False ))   # fondo mini mapa  id = 5
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\T09.png',  True ))   # censador minimapa   id = 6
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\T10.png',  True ))   # no censador minimapa   id = 7
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\cara.png',True  ))   # Mouse     id = 8
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\panel.png',True  ))   # panel censo recursos id = 9    
    return aImg    

def Init_Mapa(nAncho_X,nAlto_Y):
    for nF in range(0,nMAX_Y / nt_HY):
        for nC in range(0,nMAX_X / nt_WX):  
            aMap[nF][nC].nT = ra.randint(1,3) # inicializa el mapa con la tile sin recursos (0)
            aMap[nF][nC].nS = 0 # la tile aparece por defecto
            aMap[nF][nC].nF = nF # Fila de la Celda
            aMap[nF][nC].nC = nC # Colu de la Celda
            aMap[nF][nC].nR = ra.randint(1,5) #1 agua, 2 acero, 3 carbon, 4 petroleo, 5 aluminio
            aMap[nF][nC].nQ = ra.randint(10,50)
    return pg.Surface((nAncho_X,nAlto_Y))

def Pinta_Robot():
    for i in range(0,nMAX_ROBOTS): 
        if aBoe[i].nF == 1:
            sWin.blit(aFig[0] ,(aBoe[i].nX-xd,aBoe[i].nY-yd))
        if aBoe[i].nF == 2: 
            sWin.blit(aFig[1] ,(aBoe[i].nX-xd,aBoe[i].nY-yd))
    return

def Pinta_subMapa():
    global xd,yd,nX0,nY0
    sWin.blit(mapa.subsurface((xd,yd,924,64)),(nX0,nY0))
    return

def Pinta_MiniMapa():
    xp = 0; xy = 0
    sWin.blit(aFig[5],(15,400))
    for i in range(0,nMAX_ROBOTS):
        xp = int(923/float(6400)*aBoe[i].nX) + 20 #mueve los limites
        xy = int(65/float(480)*aBoe[i].nY) + 404
        if aBoe[i].nF == 1:#en el minimapa del robot
            sWin.blit(aFig[7],(xp,xy))
        if aBoe[i].nF == 2:    
            sWin.blit(aFig[6],(xp,xy))
    return

def UpDate_Scroll_Mapa(nMx,nMy):
    global xd, yd
    if 20 <= nMx <= 943 and 400 <= nMy <= 469:
        xd = int((nMx - 20) / 923.0 * (nMAX_X - nRes[0]))
        yd = int((nMy - 404) / 65.0 * (nMAX_Y - nRes[1]))
        pg.display.set_caption('[Coord Mapa]-> X: %d - Y: %d' % (xd, yd))
    return xd,yd

def Pinta_Mapa():
    for nF in range(nMAX_Y // nt_HY):
        for nC in range(nMAX_X // nt_WX):
            if aMap[nF][nC].nT == 1:
                sWin.blit(aFig[2], (aMap[nF][nC].nC * nt_WX - xd, aMap[nF][nC].nF * nt_HY - yd))
            if aMap[nF][nC].nT == 2:
                sWin.blit(aFig[3], (aMap[nF][nC].nC * nt_WX - xd, aMap[nF][nC].nF * nt_HY - yd))
            if aMap[nF][nC].nT == 3:
                sWin.blit(aFig[4], (aMap[nF][nC].nC * nt_WX - xd, aMap[nF][nC].nF * nt_HY - yd))

def Mueve_Robot():
    for i in range(0,nMAX_ROBOTS): # Recorrimos todos los Robots
        aBoe[i].nR -= 1    # Decrementamos en 1 el Rango del Robot
        if aBoe[i].nR < 0: # Si es negativo ->
            aBoe[i].nR = ra.randint(0,480) # Asignamos otro Rango aleatorio
            aBoe[i].nV = ra.randint(1,3)   # Asignamos otra velocidad
            nDir = ra.randint(1,5)  # Generamos una Direccion de Movimiento Aleat.
            if nDir == 1: # Norte ?
                aBoe[i].dX = +0 ; aBoe[i].dY = -1
            if nDir == 2: # Este ?
                aBoe[i].dX = +1 ; aBoe[i].dY = 0
            if nDir == 3: # Sur ?
                aBoe[i].dX = +0 ; aBoe[i].dY = +1
            if nDir == 4: # Oeste ?
                aBoe[i].dX = -1 ; aBoe[i].dY = +0
            if nDir == 5: # Detenido ?
	            aBoe[i].dX = +0 ; aBoe[i].dY = +0
     #Actualizamos (Xs,Ys) de los Sprites en el Mapa 2D
     #--------------------------------------------------
        newX = aBoe[i].nX + aBoe[i].dX * aBoe[i].nV
        newY = aBoe[i].nY + aBoe[i].dY * aBoe[i].nV

        if 0 <= newX < nMAX_X - nt_WX and 0 <= newY < nMAX_Y - nt_HY:  
            aBoe[i].nX = newX  
            aBoe[i].nY = newY
            if aBoe[i].nF == 2:
                nF = aBoe[i].nY // nt_HY
                nC = aBoe[i].nX // nt_WX
                tile_actual = aMap[nF][nC]
                if (nF,nC) not in aBoe[i].Tilescensados:
                    aBoe[i].Recursostiles.append({
                    'recurso': tile_actual.nR,
                    'cantidad': tile_actual.nQ
                    })
                    aBoe[i].Tilescensados.append((nF, nC))
                    #print('idrobot:'+str([i])+'recurso:'+str(tile_actual.nR)+'cantidad:'+str(tile_actual.nQ))
                    print(aBoe[i].Recursostiles)
                    print(aBoe[i].Tilescensados)
    return

def Pinta_Mouse():
    sWin.blit(aFig[8],(nMx,nMy))
    return 

def Pausa():
    while 1:
        e = pg.event.wait()
        if e.type in (pg.QUIT, pg.KEYDOWN):
            return
        
sWin = init_Pygame() 
aFig = Init_Fig() 
fondo = aFig[ra.randint(2,5)]
aMap = [[eCelda() for nC in range(nMAX_X/nt_WX)] for nF in range(nMAX_Y/nt_HY)]
aBoe = [ eRobot() for i in range(0,nMAX_ROBOTS) ]
init_Robot()
mapa = Init_Mapa(6400,480) 
aClk = [pg.time.Clock(), pg.time.Clock()] ; eReg = eCelda() 

while lGo:
    cKey = pg.key.get_pressed()
    if cKey[pg.K_ESCAPE] : lGo = ('A' > 'B')
 
    if cKey[pg.K_p]  : Pausa() 
    if cKey[pg.K_s]  : pg.image.save(sWin,'mapinte.png') 
     
    ev = pg.event.get()
    for e in ev:
        if e.type == QUIT           : lGo = (2 > 3)
        if e.type == pg.MOUSEMOTION : nMx,nMy = e.pos
        if 20 <= nMx <= 943 and 400 <= nMy <= 469:
            if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                xd,yd = UpDate_Scroll_Mapa(nMx,nMy) # Scroll Mapa

    Pinta_Mapa()
    Pinta_Robot() 
    Mueve_Robot() 
    Pinta_subMapa()
    Pinta_MiniMapa()
    Pinta_Mouse()

    pg.display.flip()
    aClk[0].tick(10000)

pg.quit
