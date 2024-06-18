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
import pygame as PG, time as Ti, random as RA, ctypes as ct
from pygame.locals import *

#---------------------------------------------------------------------
# Definicion de Constantes Globales
#---------------------------------------------------------------------
nRES = (960,640); nTW_X = nTH_Y = 32 ; nMx = nMy = 0 ; lOK = True 

#---------------------------------------------------------------------
# Definicion de Structura
#---------------------------------------------------------------------
class eRobots(ct.Structure):
 _fields_ = [
             ('nF',ct.c_short),
             ('nX',ct.c_short),
             ('nY',ct.c_short),
             ('nR',ct.c_short),
             ('dX',ct.c_short),
             ('dY',ct.c_short),
	   ('nV',ct.c_short)
            ]

#---------------------------------------------------------------------
# Carga imagenes y convierte formato PG
#---------------------------------------------------------------------
def Load_Image(sFile,transp = False):
    try: image = PG.image.load(sFile)
    except PG.error,message:
           raise SystemExit,message
    image = image.convert()
    if transp:
       color = image.get_at((0,0))
       image.set_colorkey(color,RLEACCEL)
    return image

#---------------------------------------------------------------------
# Inicializa PGs.-
#---------------------------------------------------------------------
def PyGame_Init():
    PG.init()
    PG.mouse.set_visible(False) 
    PG.display.set_caption('Dynamic Big Map 2D - By Alberto Caro')
    return PG.display.set_mode(nRES) 

#---------------------------------------------------------------------
# Inicilaiza parametros de los Robots
#---------------------------------------------------------------------
def Init_Robots():
    return

#---------------------------------------------------------------------
# Pinta los Robots en el Super Extra Mega Mapa.-
# Se pintan los Robots en Surface -> sMapa (6400 x 480)
#---------------------------------------------------------------------
def Pinta_Robots():
    return

#---------------------------------------------------------------------
# Actualiza la estructura de datos de cada uno de los robots dentro del
# Mapa sMapa.
#---------------------------------------------------------------------
def Mueve_Robots():
    return
    
#---------------------------------------------------------------------
# Inicializa las Baldozas = Tiles del Super Extra Mega Mapa.-
#---------------------------------------------------------------------
def Get_Tiles(nMW_X,nMH_Y,tRng):      
    return [[ RA.randint(tRng[0],tRng[1]) for i in range(0,nMW_X/nTW_X)] for i in range(0,nMH_Y/nTH_Y)]
 
#---------------------------------------------------------------------
# Inicializa Superficie del Super Extra Mega Mapa.-
#---------------------------------------------------------------------
def Get_Surface(nAncho_X,nAlto_Y):
    return PG.Surface((nAncho_X,nAlto_Y))

#---------------------------------------------------------------------
# Inicializa Array de Sprites.-
#---------------------------------------------------------------------
def Img_Init():
    aImg = []
    aImg.append(Load_Image('T00.png',False )) # Tierra
    aImg.append(Load_Image('T01.png',False )) # Tierra + Piedras
    aImg.append(Load_Image('T02.png',False )) # Rocas
    aImg.append(Load_Image('T03.png',False )) # Marmol Celeste    
    aImg.append(Load_Image('T04.png',False )) # Marmol Star Yellow
    aImg.append(Load_Image('T05.png',False )) # Marmol Star Blue
    aImg.append(Load_Image('T06.png',False )) # Marmol Star Red
    aImg.append(Load_Image('T07.png',False )) # Marmol Gris Claro
    aImg.append(Load_Image('T08.png',False )) # Marmol Cafe
    aImg.append(Load_Image('T09.png',True  )) # Mouse
    aImg.append(Load_Image('bkg.png',False )) # Bkg
    aImg.append(Load_Image('video.png',False )) # Video
    return aImg

#---------------------------------------------------------------------
# Make Mapa 
#---------------------------------------------------------------------
def Make_Mapa(sMem,aTiles,tCF):
    nPx = nPy = 0
    for f in range(0,tCF[1]/nTH_Y):
     for c in range(0,tCF[0]/nTW_X):
      if aTiles[f][c] == 0: 
         sMem.blit(aSprt[0],(nPx,nPy)); nPx += nTW_X
      if aTiles[f][c] == 1: 
         sMem.blit(aSprt[1],(nPx,nPy)); nPx += nTW_X
      if aTiles[f][c] == 2: 
         sMem.blit(aSprt[2],(nPx,nPy)); nPx += nTW_X
      if aTiles[f][c] == 3: 
         sMem.blit(aSprt[3],(nPx,nPy)); nPx += nTW_X
      if aTiles[f][c] == 4: 
         sMem.blit(aSprt[4],(nPx,nPy)); nPx += nTW_X
      if aTiles[f][c] == 5: 
         sMem.blit(aSprt[5],(nPx,nPy)); nPx += nTW_X
      if aTiles[f][c] == 6: 
         sMem.blit(aSprt[6],(nPx,nPy)); nPx += nTW_X
      if aTiles[f][c] == 7: 
         sMem.blit(aSprt[7],(nPx,nPy)); nPx += nTW_X
      if aTiles[f][c] == 8: 
         sMem.blit(aSprt[8],(nPx,nPy)); nPx += nTW_X
     nPx = 0; nPy += nTH_Y
    return

#---------------------------------------------------------------------
# Pinta Mouse
#---------------------------------------------------------------------
def Pinta_Mouse():
    sPanta.blit(aSprt[9],(nMx,nMy))
    return 

#---------------------------------------------------------------------
# Pinta Display Main
#---------------------------------------------------------------------
def Pinta_Panta():
    sPanta.blit(aSprt[10],(0,0))#fondo
    sPanta.blit(aSprt[11],(5,5))#video
    return 

#---------------------------------------------------------------------
# Pinta Mapas
#---------------------------------------------------------------------
def Pinta_Mapas():
    sPanta.blit(sMap_1.subsurface((nXd,0,597,304)),(357,5)) #esquina superior derecha
    sPanta.blit(sMap_2.subsurface((0,0,345,393)),(5,241)) #esquina inferior izquierda
    sPanta.blit(sMap_3.subsurface((0,0,597,319)),(357,315)) #esquina inferior derecha
    return

#---------------------------------------------------------------------
# Pinta Reglas
#---------------------------------------------------------------------
def Pinta_Regla():
    if nMx >= 357 and nMx <= 953: #si pasa mouse por mapa1
       if nMy >= 5 and nMy <= 308:
          PG.draw.line(sPanta,(255,255,255),(357,nMy),(953,nMy),2) 
          #PG.draw.line(donde,color,punto inicio, punto fin,ancho)
          PG.draw.line(sPanta,(255,255,255),(nMx,5),(nMx,308),2)
    return

#---------------------------------------------------------------------
# Handle Mapa ==> no se usa en este codigo
#---------------------------------------------------------------------
def Handle_Mapa():
    global nXp,nYp
    sMem.blit(sMap,(0,0))
    Mueve_Robots()
    Pinta_Robots()    
    sWin.blit(sMem.subsurface((nXp,nYp,800,480)),(0,0))
    sWin.blit(aSprt[9],(300,440)) 
    Pinta_Sonda()
    if lFlag:
       sWin.blit(aSprt[7],(220,10)) 
    nXp += 1
    if nXp == (5600 - 1): 
       nXp = 0
    return

#--------------------------------------------------------------
# Handle de Pause.-
##--------------------------------------------------------------
def Pausa():
    while 1:
     e = PG.event.wait()
     if e.type in (PG.QUIT, PG.KEYDOWN):
        return

#--------------------------------------------------------------
# Mueve
##--------------------------------------------------------------
def Mueve(cKey):
    global nXd
    if cKey == 'D':
       nXd += 1
       if nXd >= 3243: nXd = 3243 #3840-597=3243 (ancho mapa - ancho visible mapa)
    if cKey == 'I':
       nXd -= 1
       if nXd <= 0: nXd = 0
    return     

#---------------------------------------------------------------------
# While Principal del Demo.-
#---------------------------------------------------------------------
    
# Display Main
sPanta = PyGame_Init(); 

# Tiles/Sprites
aSprt = Img_Init() 

# Mapas....
sInfo  = Get_Surface(345,230); #equivalente a video
sMap_1 = Get_Surface(3840,1920); #3840-597=(3243)
sMap_2 = Get_Surface(1920,3200); 
sMap_3 = Get_Surface(1920,1920); 

#Get_Tiles(ancho,alto,rangodetiles)    #Make_Mapa(mapa/surface,distribuciontiles,resolucion)
aMapTi_1 = Get_Tiles(3840,1920,(0,2)); Make_Mapa(sMap_1,aMapTi_1,(3840,1920)) #rectangulo horizontal 
aMapTi_2 = Get_Tiles(1920,3200,(3,5)); Make_Mapa(sMap_2,aMapTi_2,(1920,3200)) #rectangulo vertical
aMapTi_3 = Get_Tiles(1920,1920,(6,8)); Make_Mapa(sMap_3,aMapTi_3,(1920,1920)) #cuadrado

aClk = [PG.time.Clock(),PG.time.Clock()] # Init Array de Cloks

nXd = nYd = 0 #coordenada desde donde se obtiene el mapa mas grande para poner en pantalla (mapa1).

#print PG.Surface.get_size(sMap_1) #obtener tamano de un surface en tupla

while lOK:
 cKey = PG.key.get_pressed()
 if cKey[PG.K_ESCAPE] : lOK = False
 if cKey[PG.K_p]      : Pausa() 
 if cKey[PG.K_c]      : PG.image.save(sPanta,'foto.png') 
 if cKey[PG.K_a]      : Mueve('D')
 if cKey[PG.K_s]      : Mueve('I')

 ev = PG.event.get()
 for e in ev:
  if e.type == QUIT           : lOK = False
  if e.type == PG.MOUSEMOTION : nMx,nMy = e.pos  
  
 Pinta_Panta()
 Pinta_Mapas()
 Pinta_Regla()
 Pinta_Mouse()
 PG.display.flip()
 aClk[0].tick(100)

PG.quit

#1.- modifique el codigo de manera que la funcionalidad de la tecla a y s se inviertan
#2.- haga que el mapa sMap_2 se recorra automaticamente de arriba hacia abajo de manera automatica, volviendo arriba cuando se acaba el mapa (como ejemplo inicial de mover mapa, pero vertical). recuerde que en pintaMapas se saca el pedazo de mapa que se ve en pantalla.
#3.- ponga un robot en sMap_3 que se mueva al azar, pero que comience siempre su recorrido en la coordenada (0,0).
#4.- piense y aplique: como generaria el codigo para que la camara siga al robot mientras se mueve? Empiece pensando que informacion requiere conocer y mantener accesible y cuales serian los pasos para utilizar esta informacion para mover y mostrar la camara de manera correcta y consistente (sin salir del mapa).





