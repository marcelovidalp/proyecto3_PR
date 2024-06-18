import pygame as pg, time as ti, random as ra, ctypes as ct
from pygame.locals import *

nRes = (6400,480); nt_WX = nt_HY = 32; nMAX_ROBOTSnocensa = 90; lGo = True
nMx = nMy = 0; nR_1 = 610 ; nR_2 = 32; nMAX_ROBOTSsicensa = 10; tiles = []
nX0 = 232 ; nY0 = 14 ; yd = 0; xd = 0
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
        ('nC',ct.c_ushort)
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
    for i in range(0,nMAX_ROBOTSnocensa):
        aBoe[i].nF = 1    # Robot Tipo 1
        aBoe[i].nX = (ra.randint(0,nRes[0] - nt_WX) / nt_WX) * nt_WX 
        aBoe[i].nY = (ra.randint(0,nRes[1] - nt_HY) / nt_HY) * nt_HY
        aBoe[i].nR = nR_1 # (RA.randint(0,nRES[0] - nT_WX) / nT_WX) * nT_WX
        aBoe[i].nS = 1    # Switch por defecto
        aBoe[i].dX = 0   # Por defecto robot Direccion Este.-
        aBoe[i].dY = 1
        aBoe[i].nV = 1 
        aBoe[i].nC = 1 
    return

def Init_Fig():         
    aImg = []
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\T00.png',  True )) # robot no censador id = 0
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\T02.png',  True ))   # robot censador   id = 1
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\T04.png',  False ))   # tile de tierra   id = 2
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\T05.png',  False ))   # tile de roca   id = 3
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\T06.png',  False ))   # tile de acero   id = 4
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\T08.png',  True ))   # fondo mini mapa  id = 5
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\T09.png',  True ))   # censador minimapa   id = 6
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\T10.png',  True ))   # no censador minimapa   id = 7
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\cara.png',True  ))   # Mouse     id = 8
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\panel.png',True  ))   # panel censo recursos id = 9    
    return aImg    

def Init_Mapa():
    for nF in range(0,nRes[1] / nt_HY):
        for nC in range(0,nRes[0] / nt_WX):  
            aMap[nF][nC].nT = ra.randint(1,3) # inicializa el mapa con la tile sin recursos (0)
            aMap[nF][nC].nS = 0 # la tile aparece por defecto
            aMap[nF][nC].nF = nF # Fila de la Celda
            aMap[nF][nC].nC = nC # Colu de la Celda
    return

def Mapa_Init(nAncho_X,nAlto_Y):
    return pg.Surface((nAncho_X,nAlto_Y))

def Pinta_Robot():
    for i in range(0,nMAX_ROBOTSnocensa): # Iteramos las 8 Figuras del Robot
        if aBoe[i].nF == 1: sWin.blit(aFig[0] ,(aBoe[i].nX,aBoe[i].nY))
    for i in range(0,nMAX_ROBOTSsicensa): # Iteramos las 8 Figuras del Robot
        if aBoe[i].nF == 1: sWin.blit(aFig[1] ,(aBoe[i].nX,aBoe[i].nY))
    return

def Pinta_MMapa():
    xp = 0; xy = 0
    sWin.blit(aFig[5],(1013,20))
    for i in range(0,nMAX_ROBOTSnocensa):
        xp = int(159/float(2640)*aBoe[i].nX) + 1017 #la suma es para estar dentro
        xy = int(112/float(1760)*aBoe[i].nY) + 27 #del borde rojo
        sWin.blit(aFig[7],(xp,xy))

    for i in range(0,nMAX_ROBOTSsicensa):
        xp = int(159/float(2640)*aBoe[i].nX) + 1017 #la suma es para estar dentro
        xy = int(112/float(1760)*aBoe[i].nY) + 27 #del borde rojo
        sWin.blit(aFig[6],(xp,xy))
    return

def UpDate_Scroll_Mapa(nMx,nMy):
    xd = 0 ; yd = 0
    if nMx in range(1018,1177):
       if nMy in range(25,137): #si esta en el mini mapa
          xd = int(2640*(nMx-1018)/float(159)) #deshace la interpolacion
          yd = int(1760*(nMy-25)/float(112)) #para obtener coordenadas en mapa grande
          pg.display.set_caption('[Coord Mapa]-> X: %d - Y: %d' %(xd,yd))
          if xd >= 1687: xd = 1687 #si nos pasamos de la coordenada en que
          if yd >= 1090: yd = 1090 #mostrara el pedazo de mapa grande esperado
    return xd,yd
    

def Pinta_Mapa():
    for nF in range(0,nRes[1] / nt_HY):
        for nC in range(0,nRes[0] / nt_WX): #Recorre columnas y filas # pregunta si la baldosa no tiene recursos
            if aMap[nF][nC].nT == 1:
                sWin.blit(aFig[2],(aMap[nF][nC].nC*nt_HY,aMap[nF][nC].nF*nt_WX))
            if aMap[nF][nC].nT == 2:
                sWin.blit(aFig[3],(aMap[nF][nC].nC*nt_HY,aMap[nF][nC].nF*nt_WX))
            if aMap[nF][nC].nT == 3:
                sWin.blit(aFig[4],(aMap[nF][nC].nC*nt_HY,aMap[nF][nC].nF*nt_WX)) #Muestra la tile 0 (sin recursos)

def Mapa_Init(nAncho_X,nAlto_Y):
    return pg.Surface((nAncho_X,nAlto_Y))

def Pinta_subMapa():
    global xd,yd,nX0,nY0
    global pico
    sWin.blit(pico.subsurface((xd,yd,952,300)),(nX0,nY0))
    return
 
def Mueve_Robot():
    for i in range(0,nMAX_ROBOTSnocensa): # Recorrimos todos los Robots
        aBoe[i].nR -= 1    # Decrementamos en 1 el Rango del Robot
        if aBoe[i].nR < 0: # Si es negativo ->
            aBoe[i].nR = ra.randint(0,500) # Asignamos otro Rango aleatorio
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

        if 0 <= newX < nRes[0] - nt_WX and 0 <= newY < nRes[1] - nt_HY:  
                aBoe[i].nX = newX  
                aBoe[i].nY = newY
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
aMap = [[eCelda() for nC in range(nRes[0]/nt_WX)] for nF in range(nRes[1]/nt_HY)]
aBoe = [ eRobot() for i in range(0,nMAX_ROBOTSnocensa) ]
init_Robot()
Init_Mapa() 
pico = Mapa_Init(6400,480)
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
        if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
            xd,yd = UpDate_Scroll_Mapa(nMx,nMy) # Scroll Mapa

    Pinta_Mapa()
    Pinta_Robot() 
    Mueve_Robot() 
    Pinta_Mouse()
    Pinta_MMapa()
    Pinta_subMapa()

    pg.display.flip()
    aClk[0].tick(10000)

pg.quit
