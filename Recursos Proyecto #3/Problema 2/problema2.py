import pygame as pg, time as ti, random as ra, ctypes as ct
from pygame.locals import *

nRes = (640,640); nt_WX = nt_HY = 32; nMAX_ROBOTS = 1; lGo = True
nMx = nMy = 0; nR_1 = 610 ; nR_2 = 32 

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
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\T01.png',  False )) # Tile acero, id = 0
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Bo1.png',  True ))   # figura robot 1,   id = 1
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Bo2.png',  True ))   # figura robot 2,   id = 2
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Bo3.png',  True ))   # figura robot 3,   id = 3
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Bo4.png',  True ))   # figura robot 4,   id = 4
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Bo5.png',  True ))   # figura robot 5   id = 5
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Bo6.png',  True ))   # figura robot 6,   id = 6
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Bo7.png',  True ))   # figura robot 7,   id = 7
    aImg.append(Load_Image('Recursos Proyecto #3\\Problema 2\\Bo8.png',  True ))   # figura robot 8,   id = 8
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
            aMap[nF][nC].nT = 1 # inicializa el mapa con la tilede acero
            aMap[nF][nC].nS = 0 # la tile aparece por defecto
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
        for nC in range(0,nRes[0] / nt_WX): #recorremos filas y columnas
            if  nC == (aBoe[0].nX+1)/nR_2 and nF == (aBoe[0].nY+1)/nR_2: #detectamos lacelda en la que esta el robot
                if aMap[nF][nC].nT == 1: #si la celda es de tipo 1
                    aMap[nF][nC].nS = 1 #cambiamos el switch a 1 para despintar la celda y que se vea el fondo
            if aMap[nF][nC].nS == 1: #si cualquier tile es switch 1 (despintada)
                fondopantalla = (nC * nt_WX, nF * nt_HY, nt_WX, nt_HY) # definimos fondopantalla que es una tupla que contiene 
                #por orden (pos  en X, pos en Y, Ancho, Alto)
                sWin.blit(fondo,fondopantalla, fondopantalla) #en nuestra pantalla cargamos alguna imagen de fondo del arreglo luego
                # le entregamos los valores de X,Y,Ancho,Alto para especificar en donde se colocara la imagen para despues
                # entregarle los mismos valores para que sepa los valores de la imagen que colocaremos
            else: sWin.blit(aFig[0],(aMap[nF][nC].nC*nt_HY,aMap[nF][nC].nF*nt_WX)) #Pinta las tiles de acero para que el robot las vaya despintando

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
                
        newX = aBoe[i].nX + aBoe[i].dX * aBoe[i].nV
        newY = aBoe[i].nY + aBoe[i].dY * aBoe[i].nV

        if 0 <= newX < nRes[0] - nt_WX and 0 <= newY < nRes[1] - nt_HY:
            if newX == 607 and newY == 32: #si el robot llega al final
                Reiniciar_Mapa() #llamamos a la funcion para reiniciar el mapa
            
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
    global fondo #llamamos a el arreglo que contiene los fondos
    fondo = aFig[ra.randint(9,13)] # definimos fondo    
    init_Robot() # reiniciamois los parametros del robot
    Init_Mapa() # reiniciamos los parametros del mapa con otro fondo del arreglo fondo

def Pinta_Mouse():
    sWin.blit(aFig[14],(nMx,nMy))
    return 

def Pausa():
    while 1:
        e = pg.event.wait()
        if e.type in (pg.QUIT, pg.KEYDOWN):
            return

sWin = init_Pygame() ; aFig = Init_Fig() 
fondo = aFig[ra.randint(9,13)] # arreglo con los 5 posibles fondos
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
