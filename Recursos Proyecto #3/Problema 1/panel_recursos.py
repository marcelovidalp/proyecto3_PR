import pygame as pg, time as ti, random as ra, ctypes as ct, serial as sl
from pygame.locals import * 

nRes = (837,142); nt_WX = nt_HY = 32; lGo = True
nMIN_X = 0 ; nMAX_X = 6400 ; nMIN_Y = 0 ; nMAX_Y = 480; nMAX_ROBOTS = 100
nMx = nMy = 0; nMAX_ROBOTSsicensa = 10
nX0 = 19 ; nY0 = 405 ; yd = 0; xd = 0

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

def Pinta_linea():
    white = (255, 255, 255)
    red = (255, 0, 0)
    line_width = 1
    start_pos = (0, 0)
    end_pos = (500, 100)
    pg.draw.line(sWin,red,start_pos,end_pos,line_width)
    pg.display.flip()
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
    Pinta_linea()
    pg.display.flip()
    aClk[0].tick(1000)

pg.quit
