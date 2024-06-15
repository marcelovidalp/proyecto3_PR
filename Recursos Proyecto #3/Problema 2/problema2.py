import pygame as pg, time as ti, random as ra, ctypes as ct
from pygame.locals import *

#---------------------------------------------------------------------
# Definicion de Constantes y Variables
#---------------------------------------------------------------------
nRes = (640,640); nt_WX = nt_HY = 32; nMAX_ROBOTS = 1; lGo = True
nMx = nMy = 0; nR_1 = 610 ; nR_2 = 32 
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
    
#----------------------------------------------------
#       Funcion Carga de Imagenes
#---------------------------------------------------- 
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
        aBoe[i].nX = 0    # (RA.randint(0,nRES[0] - nT_WX) / nT_WX) * nT_WX 
        aBoe[i].nY = 0    # (RA.randint(0,nRES[1] - nT_HY) / nT_HY) * nT_HY
        aBoe[i].nR = nR_1 # (RA.randint(0,nRES[0] - nT_WX) / nT_WX) * nT_WX
        aBoe[i].nS = 1    # Switch por defecto
        aBoe[i].dX = 0   # Por defecto robot Direccion Este.-
        aBoe[i].dY = 1
        aBoe[i].nV = 1 
        aBoe[i].nC = 1 
    return

def Init_Fig():         
    aImg = []
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\T01.png',  False )) # Tile Tierra, id = 0
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Bo1.png',  True ))   # fondo 1,   id = 1
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Bo2.png',  True ))   # fondo 1,   id = 2
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Bo3.png',  True ))   # fondo 1,   id = 3
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Bo4.png',  True ))   # fondo 1,   id = 4
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Bo5.png',  True ))   # fondo 1,   id = 5
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Bo6.png',  True ))   # fondo 1,   id = 6
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Bo7.png',  True ))   # fondo 1,   id = 7
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Bo8.png',  True ))   # fondo 1,   id = 8
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\b_01.png',False )) # fondo 1,   id = 9
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\b_02.png',False )) # fondo 2,   id = 10
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\b_03.png',False )) # fondo 3,   id = 11
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\b_04.png',False )) # fondo 4,   id = 12
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\b_05.png',False )) # fondo 5,   id = 13
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Rat.png',True  ))   # Mouse 9    id = 14

    return aImg

def Init_Mapa():
    for nF in range(0,nRes[1] / nt_HY):
        for nC in range(0,nRes[0] / nt_WX):  
            aMap[nF][nC].nT = 1 # inicializa el mapa con la tile sin recursos (0)
            aMap[nF][nC].nS = 0 # No se pinta por Defecto
            aMap[nF][nC].nF = nF # Fila de la Celda
            aMap[nF][nC].nC = nC # Colu de la Celda
    return 

def Pinta_Robot():
    for i in range(0,nMAX_ROBOTS): # Iteramos las 8 Figuras del Robot
        if aBoe[i].nF == 1: sWin.blit(aFig[1] ,(aBoe[i].nX,aBoe[i].nY))
        if aBoe[i].nF == 2: sWin.blit(aFig[2] ,(aBoe[i].nX,aBoe[i].nY))
        if aBoe[i].nF == 3: sWin.blit(aFig[3] ,(aBoe[i].nX,aBoe[i].nY))
        if aBoe[i].nF == 4: sWin.blit(aFig[4] ,(aBoe[i].nX,aBoe[i].nY))     
        if aBoe[i].nF == 5: sWin.blit(aFig[5] ,(aBoe[i].nX,aBoe[i].nY))
        if aBoe[i].nF == 6: sWin.blit(aFig[6] ,(aBoe[i].nX,aBoe[i].nY))
        if aBoe[i].nF == 7: sWin.blit(aFig[7] ,(aBoe[i].nX,aBoe[i].nY))
        if aBoe[i].nF == 8: sWin.blit(aFig[8] ,(aBoe[i].nX,aBoe[i].nY))
    return

def Pinta_Mapa():
    
    for nF in range(0,nRes[1] / nt_HY):
        for nC in range(0,nRes[0] / nt_WX): #Recorre columnas y filas # pregunta si la baldosa no tiene recursos
             #Muestra la tile 0 (sin recursos)

            if  nC == (aBoe[0].nX+1)/nR_2 and nF == (aBoe[0].nY+1)/nR_2:    #Aqui preguntamos y calculamos la tile actual 
                if aMap[nF][nC].nT == 1:
                    aMap[nF][nC].nS = 1 # Cambiamos el valor de la baldosa para pintarla
            if aMap[nF][nC].nS == 1: # Preguntamos si la tile es acero 
                fondopantalla = (nC * nt_WX, nF * nt_HY, nt_WX, nt_HY)
                sWin.blit(fondo, fondopantalla, fondopantalla) # Mostramos la tile de acero
            else: sWin.blit(aFig[0],(aMap[nF][nC].nC*nt_HY,aMap[nF][nC].nF*nt_WX)) #Si no mostramos tile vacia 

#---------------------------------------------------------------------
# Actualiza la estructura de datos de cada uno de los robots dentro del
# Mapa sMapa.
#---------------------------------------------------------------------
def Mueve_Robot():
    for i in range(0,nMAX_ROBOTS): # Recorrimos todos los Robots
        aBoe[i].nR -= 1      # Decrementamos en 1 el Rango del Robot
        if aBoe[i].nR <= 0:   # Robot termino sus pasos? 
            if aBoe[i].nS == 1:
                aBoe[i].nS = 2  # Cambio de estado
                aBoe[i].nR = nR_2 # Robot ESTE nR_2 pasos
                aBoe[i].dX = 1 ; aBoe[i].dY = 0
            elif aBoe[i].nS == 2:
                aBoe[i].nS = 3  # Cambio de estado
                aBoe[i].nR = nR_1 # Robot SUBE nR_1 pasos
                aBoe[i].dX = 0 ; aBoe[i].dY = -1
            elif aBoe[i].nS == 3:
                aBoe[i].nS = 4  # Cambio de estado
                aBoe[i].nR = nR_2 # Robot ESTE nR_2 pasos
                aBoe[i].dX = 1 ; aBoe[i].dY = 0
            else:
                aBoe[i].nS = 1  # Cambio de estado
                aBoe[i].nR = nR_1 # Robot BAJA nR_1 pasos
                aBoe[i].dX = 0 ; aBoe[i].dY = 1
     #Actualizamos (Xs,Ys) de los Sprites en el Mapa 2D
     #--------------------------------------------------
        newX = aBoe[i].nX + aBoe[i].dX * aBoe[i].nV
        newY = aBoe[i].nY + aBoe[i].dY * aBoe[i].nV

        if 0 <= newX < nRes[0] - nt_WX and 0 <= newY < nRes[1] - nt_HY:
            if newX == 607 and newY == 32:
                aBoe[i].nR = 0
                Reiniciar_Mapa() 
                #Final()#Llamamos a la funcion final cuando la tile esta en x:607 e y:32
            
            else:
                aBoe[i].nX = newX  
                aBoe[i].nY = newY

        aBoe[i].nC += 1
        if aBoe[i].nC >= 20:
            aBoe[i].nC = 1
            aBoe[i].nF += 1
            if aBoe[i].nF == 9:
                aBoe[i].nF = 1
    return

def Reiniciar_Mapa():
    global fondo
    fondo = aFig[ra.randint(9,13)]
    init_Robot()
    Init_Mapa()

def Pinta_Mouse():
    sWin.blit(aFig[14],(nMx,nMy))
    return 

def Final():

    #sWin.blit(aFig[11],(200,200)) #Muestra la bandera
    pg.display.flip()#Actualiza la pantalla para mostrar la bandera
    global lGo #Llama a la variable global lGo 
    while lGo:
        e = pg.event.wait()   #Pausa el juego hasta un evento quit
        if e.type in (pg.QUIT, pg.KEYDOWN):
            lGo = False

def Pausa():
    while 1:
        e = pg.event.wait()
        if e.type in (pg.QUIT, pg.KEYDOWN):
            return

sWin = init_Pygame() ; aFig = Init_Fig() 
fondo = aFig[ra.randint(9,13)]
aMap = [[eCelda() for nC in range(nRes[0]/nt_WX)] for nF in range(nRes[1]/nt_HY)]
aBoe = [ eRobot() for i in range(0,nMAX_ROBOTS) ] ; init_Robot(); Init_Mapa() 
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
    Pinta_Mapa()
    Pinta_Robot() 
    Mueve_Robot() 
    Pinta_Mouse()
    pg.display.flip()
    aClk[0].tick(10000)

pg.quit
