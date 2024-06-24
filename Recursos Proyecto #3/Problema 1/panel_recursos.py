import pygame as pg, time as ti, random as ra, ctypes as ct, serial as sl
from pygame.locals import * 

nRes = (837,142); lGo = True; cantidadyrecurso = []
nMx = nMy = 0; nMAX_ROBOTSsicensa = 10 
class eReg(ct.Structure):
    fields = [
                ('nB',ct.c_ushort), # ID Robot
                ('nPos',ct.c_ushort), # pos en el panel
                ('nAltura',ct.c_ushort), # Altura de la linea en el panel
                ('nR',ct.c_ushort), # Recursos 
                ('nQ',ct.c_ushort), # Qty
            ]
def init_eReg():
    for i in range(0,nMAX_ROBOTSsicensa): #recorremos los robots censadores
        aRegs[i].nB = i # iniciamos que el id sea el mismo que el numero de ciclo (el 0 sera el 0, el 1 sera el 1, y asi)
        aRegs[i].nPos = (13+(83*i),130) # iniciamos la posicion con valores de pixeles calculados como una tupla para X e Y en el panel de las barras
        #multiplicando por el id robot(cada ciclo) X  para desplazarlas hacia la derecha 
        aRegs[i].nAltura = (13+(83*i),130) #iniciamos la altura con valores de pixeles calculados como una tupla para X e Y en el panel de las barras
        # multiplicando por el id robot(cada ciclo) a X para desplazarlas hacia la derecha
        aRegs[i].nR = 0 #iniciamos el tipo de recurso
        aRegs[i].nQ = 0 # iniciamos la cantidad del recurso

conn = sl.Serial(port='COM3',baudrate= 9600, timeout=1) # abrimos el puerto serial con sus caracteristicas

def recibir_datos_serial(): #creamos la funcion para recibir datos y que funcionara como ciclo principal
    global nMx,nMy,lGo #llamamos variables globales
    with open('Recursos Proyecto #3\Problema 1\data.dat', 'a') as file: #abrimos el archivo data.dat para escribir sobre el
        while lGo: # creamos nuestro ciclo principal
            if conn.in_waiting > 0: # esto es basicamente otro while true, pero es mientras la conexion este abierta
                data = conn.read(5) # leemos el arreglo de bytes con una longitud de 5 bytes
                data = [ord(dato) for dato in data] #ciclo para recorrer la data y formatear los datos de hexadecimal a caracteres con ord()
                id = data[0] # rescatamos el primer elemento del arreglo
                recurso = data[1] # rescatamos el segundo elemento del arreglo
                cantidad = data[2] # rescatamos el tercer elemento del arreglo
                fila = data[3] # rescatamos el cuarto elemento del arreglo
                columna = data[4] # rescatamos el quinto elemento del arreglo
                datos = 'idrobot:{}, recurso:{}, cantidad:{}, fila:{}, columna:{}\n'.format(id, recurso, cantidad,fila,columna) # definimos datos como
                # un linea de texto con las variables rescatad utilizando la estructura de python 2.7
                file.write(datos + '\n') #escribimos datos sobre el archivo con un salto de linea al final
                init_lineas(id, recurso, cantidad) #llamamos a la inicializacion de las lineas entregandole los valores necesarios

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
            pinta_lineas() #llamamos a la funcion para pintar las lineas
            pg.display.flip()
            aClk[0].tick(100)

def init_lineas(id, recurso, cantidad): # iniciamos las lineas en base al id, recurso y cantidad
    #creamos un diccionario con los colores a usar
    colores = {1 : (237, 28, 36), #1 rojo   
    2 : (0, 162, 232), #2 celeste
    3 : (34, 177, 76), #3 verde
    4 : (63, 72, 204), #4 azul
    5 : (255, 201, 14)} #5 amarillo
    aRegs[id].nAltura = (13+(83*id), (130-(cantidad))) #calculamos la altura de la linea con valores calulados de pixeles
    aRegs[id].nR = colores.get(recurso)
    aRegs[id].nQ = cantidad
    
def pinta_lineas():
    for i in range(0,nMAX_ROBOTSsicensa): #recorremos los robots 
        pg.draw.line(sWin, aRegs[i].nR, aRegs[i].nAltura, aRegs[i].nPos, width=10) #dibujamos la linea en la pantalla principal en base a
        # la cantidad de recurso, la altura que tendra, la posicion y con un grosor de 10 pixeles

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

aRegs = [ eReg() for i in range(0,nMAX_ROBOTSsicensa) ]
init_eReg()
sWin = init_Pygame() 
aFig = Init_Fig() 
aClk = [pg.time.Clock(), pg.time.Clock()] 

recibir_datos_serial() #llamamos a la funcion

