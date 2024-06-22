import pygame as pg, time as ti, random as ra, ctypes as ct, serial as sl, re
from pygame.locals import * 

nRes = (837,142); nt_WX = nt_HY = 32; lGo = True
nMIN_X = 0 ; nMAX_X = 6400 ; nMIN_Y = 0 ; nMAX_Y = 480; nMAX_ROBOTS = 100
nMx = nMy = 0; nMAX_ROBOTSsicensa = 10; cantidadyrecurso = []
nX0 = 19 ; nY0 = 405 ; yd = 0; xd = 0

class eReg(ct.Structure):
    fields = [
                ('nB',ct.c_ushort), # ID Robot
                ('nF',ct.c_ushort), # Fila de Mapa
                ('nC',ct.c_ushort), # Columna de Mapa
                ('nR',ct.c_ushort), # Recursos 
                ('nQ',ct.c_ushort), # Qty
            ]

# Inicializar el puerto serial
ser = sl.Serial(port='COM3',baudrate= 9600, timeout=1)  # Usa el otro puerto que creaste

def recibir_datos_serial():
    with open('Recursos Proyecto #3\Problema 1\data.dat', 'a') as file:
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                file.write(data + '\n')
                print(data)
                match = re.match(r'idrobot:(\d+), recurso:(\d+), cantidad:(\d+), fila:\d+, columna:\d+', data)
                if match:
                    #id = int(match.group(1))
                    recurso = int(match.group(2))
                    cantidad = int(match.group(3))
                    
                    #print('recurso'+str(recurso))
                    #print('id'+str(id))
                    #print('cantidad'+str(cantidad))
                    #print(cantidadyrecurso)
                    cantidadyrecurso.append((recurso, cantidad))
                else:
                        print("Datos recibidos en formato incorrecto: {data}")

def pinta_lineas():
    colores = {1 : (237, 28, 36), #rojo
    2 : (0, 162, 232), #celeste
    3 : (34, 177, 76), #verde
    4 : (63, 72, 204), #azul
    5 : (255, 201, 14)} #amarillo
    
    for recurso, cantidad in cantidadyrecurso:
            color = colores.get(recurso)  # Blanco por defecto si no se encuentra el recurso
            altura = (cantidad - 10) * (50 - 10) / (50 - 10) + 10  # Escalar de 10 a 50 pixeles
            start_pos = (100, 100)
            end_pos = (400, 300)
            pg.draw.line(sWin, color, start_pos, end_pos, width=5)
    pg.display.flip()
# Lanzar la recepcion de datos en un hilo separado
import threading
thread = threading.Thread(target=recibir_datos_serial)
thread.setDaemon(True)
thread.start()

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
    pg.display.set_caption('Panel recursos | Proyecto P.R #3.1')
    return pg.display.set_mode(nRes)

def Init_Fig():         
    aImg = []
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\cara.png',True  ))   # Mouse     id = 0
    aImg.append(Load_Image('Recursos Proyecto #3\Problema 1\panel.png',True  ))   # panel censo recursos id = 1 
    return aImg    

def Pinta_Mouse():
    sWin.blit(aFig[0],(nMx,nMy))
    return 

def Pinta_panel():
    sWin.blit(aFig[1],(0,0))
    return

def Pausa():
    while 1:
        e = pg.event.wait()
        if e.type in (pg.QUIT, pg.KEYDOWN):
            return

sWin = init_Pygame() 
aFig = Init_Fig() 
aClk = [pg.time.Clock(), pg.time.Clock()] 

while lGo:
    cKey = pg.key.get_pressed()
    if cKey[pg.K_ESCAPE] : lGo = ('A' > 'B')
 
    if cKey[pg.K_p]  : Pausa() 
    if cKey[pg.K_s]  : pg.image.save(sWin,'mapinte.png') 
     
    ev = pg.event.get()
    for e in ev:
        if e.type == QUIT           : lGo = (2 > 3)
        if e.type == pg.MOUSEMOTION : nMx,nMy = e.pos

    Pinta_panel()
    Pinta_Mouse()
    pinta_lineas()
    pg.display.flip()
    aClk[0].tick(1000)

pg.quit
