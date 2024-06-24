import pygame as pg, time as ti, random as ra, ctypes as ct, serial as sl
from pygame.locals import * 

nRes = (837,142); nt_WX = nt_HY = 32; lGo = True
nMIN_X = 0 ; nMAX_X = 6400 ; nMIN_Y = 0 ; nMAX_Y = 480; nMAX_ROBOTS = 10
nMx = nMy = 0; nMAX_ROBOTSsicensa = 10; cantidadyrecurso = []
nX0 = 19 ; nY0 = 405 ; yd = 0; xd = 0

class eReg(ct.Structure):
    fields = [
                ('nB',ct.c_ushort), # ID Robot
                ('nPos',ct.c_ushort), # pos en el panel
                ('nAltura',ct.c_ushort), # Altura de la linea en el panel
                ('nR',ct.c_ushort), # Recursos 
                ('nQ',ct.c_ushort), # Qty
            ]
def init_eReg():
    for i in range(0,nMAX_ROBOTS):
        aRegs[i].nB = i    
        aRegs[i].nPos = (13+(83*i),130)
        aRegs[i].nAltura = (13+(83*i),130)
        aRegs[i].nR = 0 
        aRegs[i].nQ = 0 

# Inicializar el puerto serial
conn = sl.Serial(port='COM3',baudrate= 9600, timeout=1) 

def recibir_datos_serial():
    global nMx,nMy,lGo #llamamos variables globales
    with open('Recursos Proyecto #3\Problema 1\data.dat', 'a') as file: #abrimos el archivo data.dat
        while lGo:
            if conn.in_waiting > 0:
                data = conn.read(5)
                data = [ord(dato) for dato in data] #ciclo para recorrer la data y formatear los datos a caracteres con ord()
                id = data[0]
                recurso = data[1]
                cantidad = data[2]
                fila = data[3]
                columna = data[4]
                datos = 'idrobot:{}, recurso:{}, cantidad:{}, fila:{}, columna:{}\n'.format(id, recurso, cantidad,fila,columna)
                file.write(datos + '\n')
                init_lineas(id, recurso, cantidad)

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
            aClk[0].tick(100)

def init_lineas(id, recurso, cantidad):
    colores = {1 : (237, 28, 36), #rojo
    2 : (0, 162, 232), #celeste
    3 : (34, 177, 76), #verde
    4 : (63, 72, 204), #azul
    5 : (255, 201, 14)} #amarillo
    aRegs[id].nAltura = (13+(83*id), (130-(cantidad)))
    aRegs[id].nR = colores.get(recurso)
    aRegs[id].nQ = cantidad
    
def pinta_lineas():
    for i in range(0,nMAX_ROBOTS):
        pg.draw.line(sWin, aRegs[i].nR, aRegs[i].nAltura, aRegs[i].nPos, width=10)

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

aRegs = [ eReg() for i in range(0,nMAX_ROBOTS) ]
init_eReg()
sWin = init_Pygame() 
aFig = Init_Fig() 
aClk = [pg.time.Clock(), pg.time.Clock()] 

recibir_datos_serial()

