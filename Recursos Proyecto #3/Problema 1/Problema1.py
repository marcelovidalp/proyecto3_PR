import pygame as pg, time as ti, random as ra, ctypes as ct, serial as sl
from pygame.locals import * 

nRes = (960,480); nt_WX = nt_HY = 32; lGo = True
nMIN_X = 0 ; nMAX_X = 6400 ; nMIN_Y = 0 ; nMAX_Y = 480; nMAX_ROBOTS = 100
nMx = nMy = 0; nMAX_ROBOTSsicensa = 10
nX0 = 19 ; nY0 = 405 ; yd = 0; xd = 0

conn = sl.Serial(port='COM2', baudrate=9600, timeout=1)  #abrimos el puerto serial con sus caracteristicas

def enviar_datos_serial(robot_id, recurso, cantidad,fila,columna): #funcion para el envio de datos por serial
    data = [robot_id, recurso, cantidad, fila, columna] #definimos data como un arreglo de INT con la informacion
    data = bytearray(data) #convertimos data a un arreglo de bytes
    conn.write(data) # escribimos/enviamos data a traves de serial

class eRobot(ct.Structure):
    __fields__ = [
        ('nF',ct.c_ushort), #Figura
        ('nX',ct.c_ushort), #Pos X
        ('nY',ct.c_ushort), #Pos Y
        ('nR',ct.c_ushort), #Rango (pasos)
        ('dX',ct.c_ushort), #direccion X
        ('dY',ct.c_ushort), #direccion Y
        ('nV',ct.c_ushort), #Velocidad
        ('Recursostiles'), # arreglo para guardar recursos y cantidad
        ('Tilescensados') # arreglo para guardar los tiles censados
]
    
class eCelda(ct.Structure):
    _fields_ = [
        ('nT',ct.c_ubyte), # Tipo de Tile/Baldosa
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
    pg.display.set_caption('Robots censadores | Proyecto P.R #3.1')
    return pg.display.set_mode(nRes)

def init_Robot():
    for i in range(0,nMAX_ROBOTS):
        aBoe[i].nF = 1    # Robot Tipo 1 (no censa)
        aBoe[i].nX = (ra.randint(0,nMAX_X - nt_WX) / nt_WX) * nt_WX # iniciamos X en posicion aleatoria
        aBoe[i].nY = (ra.randint(0,nMAX_Y - nt_HY) / nt_HY) * nt_HY # iniciamos Y en posicion aleatoria
        aBoe[i].nR = 0 # iniciamos con 1 paso (rango)
        aBoe[i].dX = 0 # iniciamos direccion en X en 0
        aBoe[i].dY = 0 # iniciamos direccion en Y en 0
        aBoe[i].nV = 0 # iniciamos velocidad en 0 
        aBoe[i].Recursostiles = [] # iniciamos un arreglo vacio para guardar los recursos y cantidad
        aBoe[i].Tilescensados = [] # iniciamos un arreglo vacio para guardar las filas y columnas censadas
    for i in range(0,nMAX_ROBOTSsicensa): # Para la cantidad de robots que si censen
        aBoe[i].nF = 2 # los definimos como tipo 2 para identificarlos
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
    for nF in range(0,nMAX_Y / nt_HY): #recorre  las filas y columnas del mapa
        for nC in range(0,nMAX_X / nt_WX):  
            aMap[nF][nC].nT = ra.randint(1,3) # inicializa el mapa al azar entre las tres tiles (tierra,roca,acero)
            aMap[nF][nC].nF = nF # Fila de la Celda
            aMap[nF][nC].nC = nC # Colu de la Celda
            aMap[nF][nC].nR = ra.randint(1,5) #iniciamos recursos al azar; 1 agua, 2 acero, 3 carbon, 4 petroleo, 5 aluminio
            aMap[nF][nC].nQ = ra.randint(10,50) #cantidad de recursos
    return pg.Surface((nAncho_X,nAlto_Y)) #creamos una surface de pygame en 6400,480 (mapa gigante)

def Pinta_Robot():
    for i in range(0,nMAX_ROBOTS): #recorre todos los robots
        if aBoe[i].nF == 1:        #para no censadores
            sWin.blit(aFig[0] ,(aBoe[i].nX-xd,aBoe[i].nY-yd)) #muestra su figura
        if aBoe[i].nF == 2:        #para censadores
            sWin.blit(aFig[1] ,(aBoe[i].nX-xd,aBoe[i].nY-yd)) #muestra su figura
    return

def Pinta_subMapa():
    global xd,yd,nX0,nY0 #llamamos a las variables globales
    sWin.blit(mapa.subsurface((xd,yd,924,64)),(nX0,nY0)) # Superficie que se usara para el scroll
    return

def Pinta_MiniMapa():
    xp = 0; xy = 0
    sWin.blit(aFig[5],(15,400))         #muestra la figura del minimapa
    for i in range(0,nMAX_ROBOTS):      #recorre todos los robots
        xp = int(923/float(6400)*aBoe[i].nX) + 20 #calculamos la posicion actual del robot en X para mostrarla en el mini mapa
        xy = int(65/float(480)*aBoe[i].nY) + 404  #calculamos la posicion actual del robot en Y para mostrarla en el mini mapa
        if aBoe[i].nF == 1: #si el robot no censa
            sWin.blit(aFig[7],(xp,xy)) #muestra su figura en el mini mapa
        if aBoe[i].nF == 2: #si el robot censa
            sWin.blit(aFig[6],(xp,xy))#muestra su figura en el mini mapa
    return

def UpDate_Scroll_Mapa(nMx,nMy):
    global xd, yd #llamamos a la variables globales
    if 20 <= nMx <= 40 and 400 <= nMy <= 469: #verifica si el mouse esta en los limites del minimapa
        xd = int((nMx - 20) / 923.0 * (nMAX_X - nRes[0])) #deshace interpolacion en x
        yd = int((nMy - 404) / 65.0 * (nMAX_Y - nRes[1])) #deshace interpolacion en y
        pg.display.set_caption('[Coord Mapa]-> X: %d - Y: %d' % (xd, yd)) #muestra las cordenadas en la ventana
    return xd,yd #retorna la interpolacion

def Pinta_Mapa():
    for nF in range(nMAX_Y // nt_HY): #recorre  las filas y columnas del mapa
        for nC in range(nMAX_X // nt_WX):
            if aMap[nF][nC].nT == 1: #si el tile es 1
                sWin.blit(aFig[2], (aMap[nF][nC].nC * nt_WX, aMap[nF][nC].nF * nt_HY)) #mostramos su tile (tierra)
            if aMap[nF][nC].nT == 2: #si el tile es 2
                sWin.blit(aFig[3], (aMap[nF][nC].nC * nt_WX, aMap[nF][nC].nF * nt_HY)) #mostramos su tile (roca)
            if aMap[nF][nC].nT == 3: #si el tile es 3
                sWin.blit(aFig[4], (aMap[nF][nC].nC * nt_WX, aMap[nF][nC].nF * nt_HY)) #mostramos su tile (acero)

def Mueve_Robot():
    for i in range(0,nMAX_ROBOTS): # Recorremos todos los Robots
        aBoe[i].nR -= 1    # Decrementamos en 1 el Rango (pasos) del Robot
        if aBoe[i].nR < 0: # Si es negativo ->
            aBoe[i].nR = ra.randint(0,480) # Asignamos otro Rango aleatorio
            aBoe[i].nV = ra.randint(1,3)   # Asignamos otra velocidad alatoria
            nDir = ra.randint(1,5)  # Generamos una Direccion de Movimiento Aleatoria
            if nDir == 1: # Norte 
                aBoe[i].dX = +0 ; aBoe[i].dY = -1
            if nDir == 2: # Este 
                aBoe[i].dX = +1 ; aBoe[i].dY = 0
            if nDir == 3: # Sur 
                aBoe[i].dX = +0 ; aBoe[i].dY = +1
            if nDir == 4: # Oeste 
                aBoe[i].dX = -1 ; aBoe[i].dY = +0
            if nDir == 5: # Detenido 
	            aBoe[i].dX = +0 ; aBoe[i].dY = +0
        #calculamos las posiciones actuales de cada robot
        newX = aBoe[i].nX + aBoe[i].dX * aBoe[i].nV
        newY = aBoe[i].nY + aBoe[i].dY * aBoe[i].nV

        if 0 <= newX < nMAX_X - nt_WX and 0 <= newY < nMAX_Y - nt_HY:  # verifica si el robot esta en los limites de la surface
            aBoe[i].nX = newX # actualiza la posicion del robot
            aBoe[i].nY = newY
            if aBoe[i].nF == 2: # si el robot censa
                nF = aBoe[i].nY // nt_HY # obtenemos la fila censada
                nC = aBoe[i].nX // nt_WX # obtenemos la columna censada
                tile_actual = aMap[nF][nC] # definimos que tile_actual sera la misma tile del mapa
                if (nF,nC) not in aBoe[i].Tilescensados: # si la fila y columna no esta en el arreglo de tiles censadas del robot
                    aBoe[i].Recursostiles.append({ # agregamos al arreglo de recursos el recurso y cantidad de la tile_actual
                    'recurso': tile_actual.nR,
                    'cantidad': tile_actual.nQ
                    })
                    aBoe[i].Tilescensados.append((nF, nC)) # agregamos la fila y columna de la tile actual al arreglo de tiles censados del robot
                    enviar_datos_serial(i, tile_actual.nR,tile_actual.nQ,nF,nC)
                    # llamamos a la funcion para enviar los datos por serial y le entregamos los datos del robot que censo y los datos de la tile actual
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
aMap = [[eCelda() for nC in range(nMAX_X/nt_WX)] for nF in range(nMAX_Y/nt_HY)]
aBoe = [ eRobot() for i in range(0,nMAX_ROBOTS) ]
init_Robot()
mapa = Init_Mapa(6400,480) #llamamos a init_mapa y le entregamos las dimensiones de la surface 
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
    aClk[0].tick(100)

pg.quit
