# By Alberto Caro S.
# Ing. Civil en Computacion
# Doctor(c) Cs. de la Computacion
# Pontificia Universidad Catolica de Chile
# Programacion de Robot -> INFO1139
#---------------------------------------------------------------------
#__________      ___.           __  .__
#\______   \ ____\_ |__   _____/  |_|__| ____ _____
# |       _//  _ \| __ \ /  _ \   __\  |/ ___\\__  \
# |    |   (  <_> ) \_\ (  <_> )  | |  \  \___ / __ \_
# |____|_  /\____/|___  /\____/|__| |__|\___  >____  /
#        \/           \/                    \/     \/
#---------------------------------------------------------------------
import pygame, time, random as RA, ctypes as ct
from pygame.locals import *

#---------------------------------------------------------------------
# Definicion de Constantes Globales
#---------------------------------------------------------------------
nRES = (1200,700) ; nMAX_ROBOTS  = 100 ;nMAX_NAVES = 2  ; xd = 0
nMIN_X = 0 ; nMAX_X = 2640 ; nMIN_Y = 0 ; nMAX_Y = 1760 ; yd = 0
nTRUE  = 1 ; nTIME1 = 400 ; nTIME2 = 400 ; lOK = True
nTILE_WX = 44 ; nTILE_HY = 44 ; nX0 = 232 ; nY0 = 14 ; nBTN_LEFT = 1

#---------------------------------------------------------------------
# Definicion de Estructura de Datos.-
#
# nF : Identifica al Robot (Sprite a usar o tipo de robot)
# nX : Coordenada X del Robot
# nY : Coordenada Y del Robot
# nR : Rango a mover del robot -> Cuantos pixeles intentara moverse
# dX : Direccion en Eje X ->
#                           0 : No se mueve
#                          +1 : Se Mueve un pixel a la Derecha
#                          -1 : Se Mueve un pixel a la Izquierda
# dY :
#                           0 : No se mueve
#                          +1 : Se Mueve un pixel hacia Abajo
#                          -1 : Se Mueve un pixel hacia Arriba
# nV : Velocidad del robot -> (0,1,2,3, ...etc) Aleatoria

#---------------------------------------------------------------------
class eRobot(ct.Structure):
 _fields_ = [
             ('nF',ct.c_short),('nX',ct.c_short),('nY',ct.c_short),
	         ('nR',ct.c_short),('dX',ct.c_short),('dY',ct.c_short),
	         ('nV',ct.c_short)
            ]

#---------------------------------------------------------------------
# Definicion de Estructura de Datos.-
#
# Identica a la estructura de los robots, pero es para las Naves.-
#---------------------------------------------------------------------
class eNaves(ct.Structure):
 _fields_ = [
             ('nF',ct.c_short),('nX',ct.c_short),('nY',ct.c_short),
	         ('nR',ct.c_short),('dX',ct.c_short),('dY',ct.c_short),
	         ('nV',ct.c_short)
            ]

#---------------------------------------------------------------------
# Carga imagenes y convierte formato PyGame
#---------------------------------------------------------------------
def Load_Image(sFile,transp = False):
    try: image = pygame.image.load(sFile)
    except pygame.error,message:
           raise SystemExit,message
    image = image.convert()
    if transp:
       color = image.get_at((0,0))
       image.set_colorkey(color,RLEACCEL)
    return image

#---------------------------------------------------------------------
# Inicializa PyGames.-
# Inicializa el Engine de PyGame
# Define 2 Timers (contadores/relojes) a los cuales se les puede
# asignar cualquier SCRIPTS a ejecutar de manera independiente de
# la logica o secuencia del SCRIPT principal
#---------------------------------------------------------------------
def PyGame_Init():
    pygame.init()
    #el evento USEREVENT+1 va a aparecer en la lista de eventos cada 400ms
    pygame.time.set_timer(USEREVENT+1,nTIME1)
    pygame.time.set_timer(USEREVENT+2,nTIME2)
    pygame.mouse.set_visible(False) # Hacemos invisible el cursos del Mouse
    pygame.display.set_caption('Demo Robot Mapa2D - By Alberto Caro')
    return pygame.display.set_mode(nRES) # Retornamos la Surface principal
                                         # de 1.200 x 700 RGB

#---------------------------------------------------------------------
# Inicializa las Baldozas = Tiles del Super Extra Mega Mapa.-
# Las Baldosas = Tiles miden : X -> 44 px, Y -> 44 px
# Se crea y llena de manera aleatoria un SUPER Mapa de 2.640x1.760 px
# Asi en:
#            2.640 / 44 = 60 Tiles en Eje X
#            1.760 / 44 = 40 Tiles en Eje Y
#
#         << nTILE_WX = 44 , nTILE_HY = 44 >>
# Se retorna un Array de 2D (matriz) con 60 Columnas y 40 Filas con valores
# Aleatorios entre [0,1,2,3,4,5,6,7,8,9]
#(es decir, consideraremos 10 distintos tipos de tiles posibles)
#---------------------------------------------------------------------
def Tiles_Init():
    return [[RA.randint(0,9) for i in range(0,nMAX_X/nTILE_WX)] \
                             for i in range(0,nMAX_Y/nTILE_HY)]

#---------------------------------------------------------------------
# Inicializa Superficie del Super Extra Mega Mapa.-
# Se crea y retorna el Super Mapa de 2.640 x 1.760 px
# Es decir, retorna una Surface de este tamano donde se almacenara el
# Mapa mediante los Tiles/Baldosas
#---------------------------------------------------------------------
def Mapa_Init(nAncho_X,nAlto_Y):
    return pygame.Surface((nAncho_X,nAlto_Y))

#---------------------------------------------------------------------
# Inicializa Array de Sprites.-
# aImg es un Array donde sus celdas contienen las Baldosas (0...9)
# las 2 Naves (0,1) y Los 3 Tipos de Robots (0,1,2)
# 2 Cursores, Panel Main (Bkg)  y un MiniMapa
# Retorna el contenido de las Superficies anteriores dentro del Array
#---------------------------------------------------------------------
def Fig_Init():
    aImg = []
    aImg.append(Load_Image('f0.png',False )) # Baldosa 0               0
    aImg.append(Load_Image('f1.png',False )) # Baldosa 1               1
    aImg.append(Load_Image('f2.png',False )) # Baldosa 2               2
    aImg.append(Load_Image('f3.png',False )) # Baldosa 3               3
    aImg.append(Load_Image('f4.png',False )) # Baldosa 4               4
    aImg.append(Load_Image('f5.png',False )) # Baldosa 5               5
    aImg.append(Load_Image('f6.png',False )) # Baldosa 6               6
    aImg.append(Load_Image('f7.png',False )) # Baldosa 7               7
    aImg.append(Load_Image('f8.png',False )) # Baldosa 8               8
    aImg.append(Load_Image('f9.png',False )) # Baldosa 9               9
    aImg.append(Load_Image('fa.png',True  )) # Nave 1                 10
    aImg.append(Load_Image('fb.png',True  )) # Nave 2                 11
    aImg.append(Load_Image('fc.png',True  )) # Robot 1 Led R-V        12
    aImg.append(Load_Image('fd.png',True  )) # Robot 2 Led V-R        13
    aImg.append(Load_Image('fe.png',True  )) # Robot 3 Timer          14
    aImg.append(Load_Image('ff.png',True  )) # Cursor Mouse 1 Normal  15
    aImg.append(Load_Image('pm.png',True  )) # Cursor Mouse 2 Mini    16
    aImg.append(Load_Image('bg.png',True  )) # Panel Main             17
    aImg.append(Load_Image('mm.png',False )) # Mini Mapa              18
    return aImg

#---------------------------------------------------------------------
# Inicilaiza parametros de los Robots
#---------------------------------------------------------------------
def Robots_Init():
    for i in range(0,nMAX_ROBOTS):
     aBoes[i].nF = RA.randint(1,3)    # Identifica al Robot (tipo de robot)
     aBoes[i].nX = RA.randint(0,2639) # nMAX_X-nTILE_WX)  # Pos. X Robot Mapa
     aBoes[i].nY = RA.randint(0,1759) # nMAX_Y-nTILE_HY)  # Pos. Y Robot Mapa
     aBoes[i].nR = RA.randint(0,500)  # Rango de Desplazamiento.-
     aBoes[i].dX = 0 # Sin movimiento por eje X
     aBoes[i].dY = 0 # Sin movimiento por eje Y
     aBoes[i].nV = RA.randint(1,3) # Velocidad Aleatoria entre [1,2,3]
    return

#---------------------------------------------------------------------
# Incializa parametros de las Naves.-
#---------------------------------------------------------------------
def Naves_Init():
    for i in range(0,nMAX_NAVES):
     aNave[i].nF = i   # Identifica a la Nave
     aNave[i].nX = RA.randint(100,200) # Pos. X Robot Mapa
     aNave[i].nY = 600 # Pos. Y Robot Mapa
     aNave[i].nR = RA.randint(0,100)# Rango de Desplazamiento.-
     aNave[i].dX = 0  # Sin movimiento por eje X
     aNave[i].dY = -1 # Se movera hacia Arriba al inicio
     aNave[i].nV = RA.randint(1,2) # Velocidad entre [1,2]
    return

#---------------------------------------------------------------------
# Pinta los Robots en el Super Extra Mega Mapa.-
# Se pintan los Robots en Surface -> sMapa (2.640 x 1.760)
#---------------------------------------------------------------------
def Pinta_Robots():
    for i in range(0,nMAX_ROBOTS):
     if aBoes[i].nF == 1: #  Robot tipo 1?
        sMapa.blit(aSprt[12],(aBoes[i].nX,aBoes[i].nY))
     if aBoes[i].nF == 2: #  Robot tipo 2?
        sMapa.blit(aSprt[13],(aBoes[i].nX,aBoes[i].nY))
     if aBoes[i].nF == 3: #  Robot tipo 3?
        sMapa.blit(aSprt[14],(aBoes[i].nX,aBoes[i].nY))
    return

#---------------------------------------------------------------------
# Pinta las Naves en el Panel Izquierdo
# Utiliza la Surface -> Panta (Principal) 1.200 x 700 px
#---------------------------------------------------------------------
def Pinta_Naves():
    Panta.blit(aSprt[10],(aNave[0].nX,aNave[0].nY))
    Panta.blit(aSprt[11],(aNave[1].nX,aNave[1].nY))
    return

#---------------------------------------------------------------------
# Pinta la Pantalla Principal de PyGames.-
# Pinta el BackGround en Panta(Surface tipo Display Main)
#---------------------------------------------------------------------
def Pinta_Panel():
    Panta.blit(aSprt[17],(0,0))
    return

#---------------------------------------------------------------------
# Pinta el Super Extra Mega Mapa a Panta de PyGames.-
# Saca una copia del Mapa Ppal sMapa del tamano de 952 px de Ancho
# por 670 px de Alto, a partir de las coordenadas de inicio de
# (nX0,nY0) las cuales pueden ir variando de acuerdo a la posicion del
# Cursor del Mouse al apretar en el mini mapa.
#---------------------------------------------------------------------
def Pinta_Mapa():
    Panta.blit(sMapa.subsurface((xd,yd,952,670)),(nX0,nY0))
    return

#---------------------------------------------------------------------
# Pinta el Mini Mapa a Panta de PyGames.-
# Sobre este MiniMapa que se superpone a Panta, se pintan los robots
# de manera simbolica (unos cuadraditos pequenos).
# Para ello se realiza una InterPolacion (Escala) del Mini Mapa al Mapa
# Grande
#---------------------------------------------------------------------
def Pinta_MMapa():
    xp = 0; xy = 0
    Panta.blit(aSprt[18],(1013,20))
    for i in range(0,nMAX_ROBOTS):
     xp = int(159/float(2640)*aBoes[i].nX) + 1017 #la suma es para estar dentro
     xy = int(112/float(1760)*aBoes[i].nY) + 27 #del borde rojo
     Panta.blit(aSprt[16],(xp,xy))
    return
# respecto a la interpolacion/escala:
# para hacer el calculo se multiplica la dimension del mini mapa en x (sin el
# borde rojo) por la posicion en x del robot dividido por la dimension del mapa
# grande sumando luego un desface para empezar a imprimir en donde se posiciona
# el mini mapa.

#---------------------------------------------------------------------
# Pinta la Posicion de la Mouse en Panta de PyGame.-
#---------------------------------------------------------------------
def Pinta_Mouse():
    Panta.blit(aSprt[15],(nMx,nMy))
    return

#---------------------------------------------------------------------
# Acualiza Coordenadas Scroll Super Extra Mega Mapa.-
# Se realiza un Scroll del Mapa segun las coordenadas del mouse pero
# dentro del Mini Mapa.-
#---------------------------------------------------------------------
def UpDate_Scroll_Mapa(nMx,nMy):
    xd = 0 ; yd = 0
    if nMx in range(1018,1177):
       if nMy in range(25,137): #si esta en el mini mapa
          xd = int(2640*(nMx-1018)/float(159)) #deshace la interpolacion
          yd = int(1760*(nMy-25)/float(112)) #para obtener coordenadas en mapa grande
          pygame.display.set_caption('[Coord Mapa]-> X: %d - Y: %d' %(xd,yd))
          if xd >= 1687: xd = 1687 #si nos pasamos de la coordenada en que
          if yd >= 1090: yd = 1090 #mostrara el pedazo de mapa grande esperado
    return xd,yd
    
#notar que respecto a deshacer la interpolacion el calculo es para x:
#ancho_mapagigante*(posicion_mouseX-posx_minimapa)/ancho_minimapa_sin bordes

#---------------------------------------------------------------------
# Acualiza el Super Extra Mega Mapa.-
# Pinta el Mapa Completo de sMapa segun los tiles asociados en el array.
#---------------------------------------------------------------------
def UpDate_Mapa():
    nPx = nPy = 0
    for f in range(0,nMAX_Y/nTILE_HY):
     for c in range(0,nMAX_X/nTILE_WX):
      if aTile[f][c] == 0: # Tile 0
         sMapa.blit(aSprt[0],(nPx,nPy)); nPx += nTILE_WX
      if aTile[f][c] == 1: # Tile 1
         sMapa.blit(aSprt[1],(nPx,nPy)); nPx += nTILE_WX
      if aTile[f][c] == 2: # Tile 2
         sMapa.blit(aSprt[1],(nPx,nPy)); nPx += nTILE_WX
      if aTile[f][c] == 3: # Tile 3
         sMapa.blit(aSprt[3],(nPx,nPy)); nPx += nTILE_WX
      if aTile[f][c] == 4: # Tile 4
         sMapa.blit(aSprt[4],(nPx,nPy)); nPx += nTILE_WX
      if aTile[f][c] == 5: # Tile 5
         sMapa.blit(aSprt[1],(nPx,nPy)); nPx += nTILE_WX
      if aTile[f][c] == 6: # Tile 6
         sMapa.blit(aSprt[1],(nPx,nPy)); nPx += nTILE_WX
      if aTile[f][c] == 7: # Tile 7
         sMapa.blit(aSprt[1],(nPx,nPy)); nPx += nTILE_WX
      if aTile[f][c] == 8: # Tile 8
         sMapa.blit(aSprt[1],(nPx,nPy)); nPx += nTILE_WX
      if aTile[f][c] == 9: # Tile 9
         sMapa.blit(aSprt[4],(nPx,nPy)); nPx += nTILE_WX
     nPx = 0; nPy += nTILE_HY
    return

#---------------------------------------------------------------------
# Actualiza la estructura de datos de cada uno de los robots dentro del
# Mapa sMapa.
#---------------------------------------------------------------------
def UpDate_Robots():
    for i in range(0,nMAX_ROBOTS): # Recorrimos todos los Robots
     aBoes[i].nR -= 1    # Decrementamos en 1 el Rango del Robot
     if aBoes[i].nR < 0: # Si es negativo ->
        aBoes[i].nR = RA.randint(0,500) # Asignamos otro Rango aleatorio
        aBoes[i].nV = RA.randint(1,3)   # Asignamos otra velocidad
        nDir = RA.randint(1,9)  # Generamos una Direccion de Movimiento Aleat.
        if nDir == 1: # Norte ?
           aBoes[i].dX = +0 ; aBoes[i].dY = -1
        if nDir == 2: # Este ?
           aBoes[i].dX = +1 ; aBoes[i].dY = 0
        if nDir == 3: # Sur ?
           aBoes[i].dX = +0 ; aBoes[i].dY = +1
        if nDir == 4: # Oeste ?
           aBoes[i].dX = -1 ; aBoes[i].dY = +0
        if nDir == 5: # Detenido ?
	       aBoes[i].dX = +0 ; aBoes[i].dY = +0
        if nDir == 6: # NorEste
	       aBoes[i].dX = +1 ; aBoes[i].dY = -1
        if nDir == 7: # NorWeste
	       aBoes[i].dX = -1 ; aBoes[i].dY = -1
        if nDir == 8: # SurEste
	       aBoes[i].dX = +1 ; aBoes[i].dY = +1
        if nDir == 9: # SurWeste
	       aBoes[i].dX = -1 ; aBoes[i].dY = +1

     #Actualizamos (Xs,Ys) de los Sprites en el Mapa 2D
     #--------------------------------------------------

     aBoes[i].nX += aBoes[i].dX*aBoes[i].nV # Posicion Robot[i] en eje X
     aBoes[i].nY += aBoes[i].dY*aBoes[i].nV # Posicion Robot[i] en eje Y

     if aBoes[i].nX < nMIN_X: # Check los bordes o limites
        aBoes[i].nX = nMIN_X ; aBoes[i].nR = 0 # Flag

     if aBoes[i].nX > (nMAX_X - nTILE_WX): # Check los bordes o limites
        aBoes[i].nX = nMAX_X - nTILE_WX ; aBoes[i].nR = 0 # Flag

     if aBoes[i].nY < nMIN_Y: # Check los bordes o limites
        aBoes[i].nY = nMIN_Y ; aBoes[i].nR = 0 # Flag

     if aBoes[i].nY > (nMAX_Y - nTILE_HY): # Check los bordes o limites
        aBoes[i].nY = nMAX_Y - nTILE_HY ; aBoes[i].nR = 0 # Flag

    return

#---------------------------------------------------------------------
# Actualiza las Naves en el Panel Izquierdo.-
#---------------------------------------------------------------------
def UpDate_Naves():
    for i in range(0,nMAX_NAVES):
     aNave[i].nR -= 1
     if aNave[i].nR < 0:
        aNave[i].nR = RA.randint(0,100)
        aNave[i].nV = RA.randint(1,2)
        nDir = RA.randint(1,5)
        if nDir == 1: # Norte ?
           aNave[i].dX = +0 ; aNave[i].dY = -1
        if nDir == 2: # Este ?
           aNave[i].dX = +1 ; aNave[i].dY = 0
        if nDir == 3: # Sur ?
           aNave[i].dX = +0 ; aNave[i].dY = +1
        if nDir == 4: # Oeste ?
           aNave[i].dX = -1 ; aNave[i].dY = +0
        if nDir == 5: # Detenido ?
	       aNave[i].dX = +0 ; aNave[i].dY = +0

     #Actualizamos (Xs,Ys) de los Sprites en el Mapa 2D
     #--------------------------------------------------

     aNave[i].nX += aNave[i].dX*aNave[i].nV # Posicion en Eje X de Nave[i]
     aNave[i].nY += aNave[i].dY*aNave[i].nV # Posicion en Eje X de Nave[i]

     # Check bordes o limites de las naves en su sector
     if aNave[i].nX < 17 : aNave[i].nX = 17 ; aNave[i].nR = 0 # Flag
     if aNave[i].nX > 156 : aNave[i].nX = 156 ; aNave[i].nR = 0
     if aNave[i].nY < 52 : aNave[i].nY = 52 ; aNave[i].nR = 0
     if aNave[i].nY > 600 : aNave[i].nY = 600 ; aNave[i].nR = 0

    return

#--------------------------------------------------------------
# Handle de Pause.-
# Pausamos la ejecucion de la aplicacion
#--------------------------------------------------------------
def Pausa():
    while 1:
     e = pygame.event.wait()
     if e.type in (pygame.QUIT, pygame.KEYDOWN):
        return

#---------------------------------------------------------------------
# While Principal del Demo.-
#---------------------------------------------------------------------
Panta = PyGame_Init() # Surface tipo Surface Display principal
aSprt = Fig_Init()    # Cargamos los graficos al Array aSprt
aTile = Tiles_Init(); # Inicializamos el Array de Tiles
sMapa = Mapa_Init(2640,1760) # Creamos el Super Mapa -> sMapa (Surface)
aBoes = [ eRobot() for i in range(0,nMAX_ROBOTS) ] # Array de Robots
aNave = [ eNaves() for i in range(0,nMAX_NAVES)  ] # Array de Naves
Clok  = pygame.time.Clock(); nMx = 0; nMy = 0 # Clock para Syncronize

Robots_Init() # Inicializamos todas las Estructuras de Datos de los Robots
Naves_Init()  # Inicializamos todas las Estructuras de Datos de las Naves

# While principal y logica de llamadas y salida del programa
while lOK:
 cKey = pygame.key.get_pressed() # Se presiono alguna tecla?
 if cKey[pygame.K_ESCAPE] : lOK = False
 if cKey[pygame.K_p]      : Pausa() # Tecla 'P' -> Pausa
 if cKey[pygame.K_s]      : pygame.image.save(Panta,'Capture.png') # Captura
 ev = pygame.event.get()
 for e in ev:
  if e.type == QUIT               : lOK = False
  if e.type == pygame.MOUSEMOTION : nMx,nMy = e.pos # Coordenada Mouse
  if e.type == pygame.MOUSEBUTTONDOWN and e.button == nBTN_LEFT:
               xd,yd = UpDate_Scroll_Mapa(nMx,nMy) # Scroll Mapa
 Pinta_Panel()
 UpDate_Mapa()
 UpDate_Robots()
 UpDate_Naves()
 Pinta_Robots()
 Pinta_Mapa()
 Pinta_Naves()
 Pinta_MMapa()
 Pinta_Mouse()
 pygame.display.flip()

pygame.quit






