#-------------------------------------------------------------------------------
# Name:        Main
# Purpose:
#
# Author:      killer rin
#
# Created:     17/07/2012
# Copyright:   (c) killer rin 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#===============================================================================
#============================== ESSENTIAL IMPORTS ==============================
#===============================================================================
import pygame
from pygame.locals import *
import os
import socket
import threading
import pickle
#===============================================================================
#=============================== CUSTOM IMPORTS ================================
#===============================================================================

#===============================================================================
#============================== DEFINE ESSENTIALS ==============================
#===============================================================================
BLACK = (0,0,0)
WHITE = (255,255,255)
#===============================================================================

class Main():
    def __init__(self, resolution):
        self.debug_mode = True
        self.resolution = resolution

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.screen = pygame.display.set_mode(resolution)
        self.screen.fill(BLACK)
        pygame.display.flip()

        self.MainServer = ('localhost',28637)#'localhost' 192.168.0.101
        self.status = [False, '', '']
        self.motd = ['The Sky Is Falling', '', '',\
         '', '', '', '']
        self.stats = [1,1,1,0]
        self.messages = ['','','','','','']

        self.singleplayerChar = Player([int(resolution[0]/2),int(resolution[1]/2), 's'], self.resolution, (0,255,0))

    def load_resources(self):
        self.zombexfont = os.path.join('Resources', 'Fonts', 'Futurex Apocalypse.ttf')
        self.titlescreen = pygame.image.load(os.path.join('Resources', 'Backgrounds', 'Title Screen.png'))
        self.titlescreen = pygame.transform.scale(self.titlescreen, self.resolution)

    def send_packets(self, data):
        try:
            packets = pickle.dumps(data)
            self.client.send(packets)
        except:
            self.status = [False,"There Was An Issue Sending Data", ""]

    def recv_packets(self, buffer):
        try:
            data = pickle.loads (self.client.recv(buffer))
            return data
        except:
            self.status = [False, "There Was An Issue Recieveing Data", ""]
            return 'connectionfailure'

    def titleLoop (self):
        self.loop = True
        self.tSelection = 0
        self.menumax = 3

        while self.loop == True:
            self.screen.fill(BLACK)

            if self.debug_mode == True:
                curX, curY = pygame.mouse.get_pos()
                drawtxt(self.screen,str(curX)+" | "+str(curY),self.zombexfont,40,BLACK,(0,25))

            #self.screen.blit(self.titlescreen, (0,0))
            drawtxt(self.screen, "ZOMBIE SURVIVAL: OG", self.zombexfont, int(105.79), (63,6,6), (self.resolution[0]/8.0, self.resolution[1]/24.0))
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.loop = False
                    self.__exit__()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if self.tSelection > 0: self.tSelection -=1
                        else: self.tSelection = self.menumax
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if self.tSelection < self.menumax: self.tSelection +=1
                        else: self.tSelection = 0
                    if event.key == pygame.K_SPACE:
                        if self.tSelection == 0: self.singleplayerLoop()
                        elif self.tSelection == 1: self.rinnet_login()
                        elif self.tSelection == 2: self.options()
                        elif self.tSelection == 3: self.__exit__()
                        if self.loop == False: self.loop = True
            if self.status[0] == True: self.rinnet_lobby()
            #------------------------------------------------------------------#
            if self.tSelection == 0: drawtxt(self.screen, "SINGLE PLAYER", self.zombexfont, int(105.79), (96,111,15), (self.resolution[0]/40.0,self.resolution[1]/3.2)) # (20,250)
            else: drawtxt(self.screen, "SINGLE PLAYER", self.zombexfont, int(105.79), (63,6,6), (0,self.resolution[1]/3.2)) # (0,250)
            if self.tSelection == 1: drawtxt(self.screen, "RIN-NET", self.zombexfont, int(105.79), (96,111,15), (self.resolution[0]/40.0,self.resolution[1]/2.2857142857142856)) # (20,350)
            else: drawtxt(self.screen, "RIN-NET", self.zombexfont, int(105.79), (63,6,6), (0,self.resolution[1]/2.2857142857142856)) # (0,350)
            if self.tSelection == 2: drawtxt(self.screen, "OPTIONS", self.zombexfont, int(105.79), (96,111,15), (self.resolution[0]/40.0,self.resolution[1]/1.7777777777777777)) # (20,450)
            else: drawtxt(self.screen, "OPTIONS", self.zombexfont, int(105.79), (63,6,6), (0,self.resolution[1]/1.7777777777777777)) # (0,450)
            if self.tSelection == 3: drawtxt(self.screen, "EXIT GAME", self.zombexfont, int(105.79), (96,111,15), (self.resolution[0]/40.0,self.resolution[1]/1.4545454545454546)) # (20,550)
            else: drawtxt(self.screen, "EXIT GAME", self.zombexfont, int(105.79), (63,6,6), (0,self.resolution[1]/1.4545454545454546)) # (0,550)

            drawtxt(self.screen,self.status[1],self.zombexfont,40,WHITE,(100,150), (True, 200, 50, BLACK))
            drawtxt(self.screen,self.status[2],self.zombexfont,40,WHITE,(100,180), (True, 200, 50, BLACK))

            pygame.display.update()

    def singleplayerLoop (self):
        self.loop = True
        while self.loop == True:
            self.screen.fill(BLACK)

            if self.debug_mode == True:
                curX, curY = pygame.mouse.get_pos()
                drawtxt(self.screen,str(curX)+" | "+str(curY),self.zombexfont,40,BLACK,(0,25))

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.loop = False
                    self.__exit__()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause = True

                        while pause == True:
                            self.screen.fill(BLACK)
                            drawtxt(self.screen, "GAME PAUSED", self.zombexfont, int(105.79), (63,6,6), (self.resolution[0]/8.0, self.resolution[1]/24.0))

                            if self.debug_mode == True:
                                curX, curY = pygame.mouse.get_pos()
                                drawtxt(self.screen,str(curX)+" | "+str(curY),self.zombexfont,40,BLACK,(0,25))
                            for event in pygame.event.get(): # User did something
                                if event.type == pygame.QUIT: # If user clicked close
                                    self.loop = False
                                    self.__exit__()

                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                                        self.loop = False
                                        pause = False
                                    if event.key == pygame.K_ESCAPE:
                                        pause = False
                            pygame.display.update()

            pygame.event.pump()
            key = pygame.key.get_pressed()
            if key[K_UP] or key[K_w]:
                self.singleplayerChar.update([0,-(0.1+self.stats[2]),'w'])
            if key[K_DOWN] or key[K_s]:
                self.singleplayerChar.update([0,(0.1+self.stats[2]),'s'])
            if key[K_LEFT] or key[K_a]:
                self.singleplayerChar.update([-(0.1+self.stats[2]),0,'a'])
            if key[K_RIGHT] or key[K_d]:
                self.singleplayerChar.update([(0.1+self.stats[2]),0,'d'])

            self.singleplayerChar.draw(self.screen)
            pygame.display.update()

    def rinnet_login (self):
        loop = True
        usernameselect, passwordselect = True, False
        loginselect, registerselect = True, False
        username, password = '', ''
        ctr = 19
        while loop == True:
            self.screen.fill(BLACK)

            if self.debug_mode == True:
                curX, curY = pygame.mouse.get_pos()
                drawtxt(self.screen,str(curX)+" | "+str(curY),self.zombexfont,40,BLACK,(0,25))

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.loop, loop = False, False
                    self.__exit__()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        ctr = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.loop, loop = False, False
                        return (99)
                    if event.key == pygame.K_UP:
                        if usernameselect == True:
                            usernameselect = False
                            passwordselect = True
                        else:
                            usernameselect = True
                            passwordselect = False
                    if event.key == pygame.K_DOWN:
                        if passwordselect == True:
                            usernameselect = True
                            passwordselect = False
                        else:
                            usernameselect = False
                            passwordselect = True
                    if event.key == pygame.K_LEFT:
                        if loginselect == True:
                            loginselect = False
                            registerselect = True
                        else:
                            loginselect = True
                            registerselect = False
                    if event.key == pygame.K_RIGHT:
                        if registerselect == True:
                            loginselect = True
                            registerselect = False
                        else:
                            loginselect = False
                            registerselect = True
                    if event.key == pygame.K_a:
                        if usernameselect == True: username+='a'
                        elif passwordselect == True: password+='a'
                    if event.key == pygame.K_b:
                        if usernameselect == True: username+='b'
                        elif passwordselect == True: password+='b'
                    if event.key == pygame.K_c:
                        if usernameselect == True: username+='c'
                        elif passwordselect == True: password+='c'
                    if event.key == pygame.K_d:
                        if usernameselect == True: username+='d'
                        elif passwordselect == True: password+='d'
                    if event.key == pygame.K_e:
                        if usernameselect == True: username+='e'
                        elif passwordselect == True: password+='e'
                    if event.key == pygame.K_f:
                        if usernameselect == True: username+='f'
                        elif passwordselect == True: password+='f'
                    if event.key == pygame.K_g:
                        if usernameselect == True: username+='g'
                        elif passwordselect == True: password+='g'
                    if event.key == pygame.K_h:
                        if usernameselect == True: username+='h'
                        elif passwordselect == True: password+='h'
                    if event.key == pygame.K_i:
                        if usernameselect == True: username+='i'
                        elif passwordselect == True: password+='i'
                    if event.key == pygame.K_j:
                        if usernameselect == True: username+='j'
                        elif passwordselect == True: password+='j'
                    if event.key == pygame.K_k:
                        if usernameselect == True: username+='k'
                        elif passwordselect == True: password+='k'
                    if event.key == pygame.K_l:
                        if usernameselect == True: username+='l'
                        elif passwordselect == True: password+='l'
                    if event.key == pygame.K_m:
                        if usernameselect == True: username+='m'
                        elif passwordselect == True: password+='m'
                    if event.key == pygame.K_n:
                        if usernameselect == True: username+='n'
                        elif passwordselect == True: password+='n'
                    if event.key == pygame.K_o:
                        if usernameselect == True: username+='o'
                        elif passwordselect == True: password+='o'
                    if event.key == pygame.K_p:
                        if usernameselect == True: username+='p'
                        elif passwordselect == True: password+='p'
                    if event.key == pygame.K_q:
                        if usernameselect == True: username+='q'
                        elif passwordselect == True: password+='q'
                    if event.key == pygame.K_r:
                        if usernameselect == True: username+='r'
                        elif passwordselect == True: password+='r'
                    if event.key == pygame.K_s:
                        if usernameselect == True: username+='s'
                        elif passwordselect == True: password+='s'
                    if event.key == pygame.K_t:
                        if usernameselect == True: username+='t'
                        elif passwordselect == True: password+='t'
                    if event.key == pygame.K_u:
                        if usernameselect == True: username+='u'
                        elif passwordselect == True: password+='u'
                    if event.key == pygame.K_v:
                        if usernameselect == True: username+='v'
                        elif passwordselect == True: password+='v'
                    if event.key == pygame.K_w:
                        if usernameselect == True: username+='w'
                        elif passwordselect == True: password+='w'
                    if event.key == pygame.K_x:
                        if usernameselect == True: username+='x'
                        elif passwordselect == True: password+='x'
                    if event.key == pygame.K_y:
                        if usernameselect == True: username+='y'
                        elif passwordselect == True: password+='y'
                    if event.key == pygame.K_z:
                        if usernameselect == True: username+='z'
                        elif passwordselect == True: password+='z'
                    if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                        if usernameselect == True: username+='0'
                        elif passwordselect == True: password+='0'
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        if usernameselect == True: username+='1'
                        elif passwordselect == True: password+='1'
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        if usernameselect == True: username+='2'
                        elif passwordselect == True: password+='2'
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        if usernameselect == True: username+='3'
                        elif passwordselect == True: password+='3'
                    if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        if usernameselect == True: username+='4'
                        elif passwordselect == True: password+='4'
                    if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        if usernameselect == True: username+='5'
                        elif passwordselect == True: password+='5'
                    if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        if usernameselect == True: username+='6'
                        elif passwordselect == True: password+='6'
                    if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        if usernameselect == True: username+='7'
                        elif passwordselect == True: password+='7'
                    if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        if usernameselect == True: username+='8'
                        elif passwordselect == True: password+='8'
                    if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        if usernameselect == True: username+='9'
                        elif passwordselect == True: password+='9'
                    if event.key == K_KP_ENTER or event.key == K_RETURN:
                        if loginselect == True:
                            ##logindata = pickle.dumps(['LOGIN', username, password], True)
                            try:
                                drawtxt(self.screen,"Connecting to Server ...",self.zombexfont,40,WHITE,(100,150), (True, 200, 50, BLACK))
                                pygame.display.update()
                                self.client = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
                                self.client.connect (self.MainServer)
                            except:
                                self.status = [False,"There Was An Issue Connecting To The Server", ""]
                                break
                            self.screen.fill(BLACK)
                            try:
                                drawtxt(self.screen,"Sending Data ...",self.zombexfont,40,WHITE,(100,150), (True, 200, 50, BLACK))
                                pygame.display.update()
                                self.send_packets(['LOGIN', username, password]) #self.client.send(logindata)
                            except:
                                self.status = [False,"There Was An Issue Sending Data", ""]
                                break
                            self.screen.fill(BLACK)
                            try:
                                drawtxt(self.screen,"Waiting on Server ...",self.zombexfont,40,WHITE,(100,150), (True, 200, 50, BLACK))
                                pygame.display.update()

                                info = self.recv_packets(10000) ##info = pickle.loads (self.client.recv(10000))
                                self.status = info[0]
                                self.stats = info[1]
                                self.motd = info[2]
                            except:
                                self.status = [False, "There Was An Issue Recieveing Data", ""]
                                break
                            self.screen.fill(BLACK)
                            try:
                                drawtxt(self.screen,status[1],self.zombexfont,40,WHITE,(100,150), (True, 200, 50, BLACK))
                                drawtxt(self.screen,status[2],self.zombexfont,40,WHITE,(100,150), (True, 200, 50, BLACK))

                                pygame.display.update()
                            except: pass
                        elif registerselect == True:
                            ##registerdata = pickle.dumps(['REGISTER', username, password], True)
                            try:
                                drawtxt(self.screen,"Connecting to Server ...",self.zombexfont,40,WHITE,(100,150), (True, 200, 50, BLACK))
                                pygame.display.update()
                                self.client = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
                                self.client.connect (self.MainServer)
                            except:
                                self.status = [False,"There Was An Issue Connecting To The Server", ""]
                                break
                            self.screen.fill(BLACK)
                            try:
                                drawtxt(self.screen,"Sending Data ...",self.zombexfont,40,WHITE,(100,150), (True, 200, 50, BLACK))
                                pygame.display.update()
                                self.send_packets(['REGISTER', username, password]) ##self.client.send(registerdata)
                            except:
                                self.status = [False,"There Was An Issue Sending Data", ""]
                                break
                            self.screen.fill(BLACK)
                            try:
                                drawtxt(self.screen,"Waiting on Server ...",self.zombexfont,40,WHITE,(100,150), (True, 200, 50, BLACK))
                                pygame.display.update()
                                info = self.recv_packets(10000) ##info = pickle.loads (self.client.recv(10000))
                                self.status = info[0]
                                self.stats = info[1]
                                self.motd = info[2]
                            except:
                                self.status = [False, "There Was An Issue Recieveing Data", ""]
                                break
                            self.screen.fill(BLACK)
                            try:
                                drawtxt(self.screen,self.status[1],self.zombexfont,40,WHITE,(100,150), (True, 200, 50, BLACK))
                                drawtxt(self.screen,self.status[2],self.zombexfont,40,WHITE,(100,180), (True, 200, 50, BLACK))

                                pygame.display.update()
                            except: pass
                        if self.status[0] == True:
                            loop = False
                            break

            pygame.event.pump()
            key = pygame.key.get_pressed()
            if key[K_BACKSPACE] or key[K_DELETE]:
                if ctr > 10:
                    if usernameselect == True:
                        try: username = username[:-1]
                        except: pass
                    elif passwordselect == True:
                        try: password = password[:-1]
                        except: pass
                    ctr = 0
                else: ctr = ctr+1


            if usernameselect == True: drawtxt(self.screen,"Username:",self.zombexfont,40,(96,111,15),(25,300))
            else: drawtxt(self.screen,"Username:",self.zombexfont,40,(63,6,6),(25,300))
            if passwordselect == True: drawtxt(self.screen,"Password:",self.zombexfont,40,(96,111,15),(25,400))
            else: drawtxt(self.screen,"Password:",self.zombexfont,40,(63,6,6),(25,400))

            if loginselect == True: drawtxt(self.screen,"LOGIN",self.zombexfont,40,(96,111,15),(400,475))
            else: drawtxt(self.screen,"LOGIN",self.zombexfont,40,(63,6,6),(400,475))
            if registerselect == True: drawtxt(self.screen,"REGISTER",self.zombexfont,40,(96,111,15),(500,475))
            else: drawtxt(self.screen,"REGISTER",self.zombexfont,40,(63,6,6),(500,475))

            drawtxt(self.screen,username,self.zombexfont,40,WHITE,(200,300))
            drawtxt(self.screen,password,self.zombexfont,40,WHITE,(200,400))

            drawtxt(self.screen,self.status[1],self.zombexfont,40,WHITE,(100,150), (True, 200, 50, BLACK))

            pygame.display.update()

    def rinnet_lobby(self):
        lobbysendqueue = ['Lobby',[],[],False]
        datarecieve = [self.stats,self.messages,False]
        loop = True
        while loop == True:
            self.screen.fill(BLACK)
            #--------------------Chat & Inventory------------------------------------
            pygame.draw.rect(self.screen,WHITE,(0,0,225,self.resolution[1]))         #
            pygame.draw.rect(self.screen,(63,6,6),(0,0,225,self.resolution[1]),5)    #
            pygame.draw.rect(self.screen,(63,6,6),(0,700,225,100),5)                 #
            pygame.draw.rect(self.screen,(63,6,6),(0,0,225,250),5)                   #
            #--------------------Stats Window---------------------------------------------------------------
            pygame.draw.rect(self.screen,WHITE,(700,0,300,220))                                             #
            pygame.draw.rect(self.screen,(63,6,6), (700,0,300,220),5)                                       #
            drawtxt(self.screen, "STATS",self.zombexfont, 40, BLACK,(800,4))                                #
            pygame.draw.line(self.screen,(63,6,6),(700,40),(self.resolution[0],40),5)                       #
            drawtxt(self.screen, "STRENGTH  "+str(self.stats[0]),self.zombexfont,40,BLACK,(710,50))         #
            drawtxt(self.screen, "HEALTH       "+str(self.stats[1]),self.zombexfont,40,BLACK,(710,90))      #
            drawtxt(self.screen, "SPEED        "+str(self.stats[2]),self.zombexfont,40,BLACK,(710,130))     #
            pygame.draw.line(self.screen,(63,6,6), (700,170),(self.resolution[0],170),5)                    #
            drawtxt(self.screen,"REMAINING: "+str(self.stats[3]),self.zombexfont,40,BLACK,(710,175))        #
            pygame.draw.rect(self.screen,BLACK,(925,50,30,30)) #PlusBox     Strength                        #
            pygame.draw.rect(self.screen,BLACK,(925,90,30,30)) #PlusBox     Health                          #
            pygame.draw.rect(self.screen,BLACK,(925,130,30,30)) #PlusBox    Speed                           #
            pygame.draw.rect(self.screen,BLACK,(960,50,30,30)) #MinusBox                                    #
            pygame.draw.rect(self.screen,BLACK,(960,90,30,30)) #MinusBox                                    #
            pygame.draw.rect(self.screen,BLACK,(960,130,30,30)) #MinusBox                                   #
            pygame.draw.rect(self.screen,(63,6,6),(960,130,30,30),2) #MinusOutline                          #
            pygame.draw.rect(self.screen,(63,6,6),(960,90,30,30),2) #MinusOutline                           #
            pygame.draw.rect(self.screen,(63,6,6),(960,50,30,30),2) #MinusOutline                           #
            pygame.draw.rect(self.screen,(63,6,6),(925,130,30,30),2) #PlusOutline                           #
            pygame.draw.rect(self.screen,(63,6,6),(925,90,30,30),2) #PlusOutline                            #
            pygame.draw.rect(self.screen,(63,6,6),(925,50,30,30),2) #PlusOutline                            #
            pygame.draw.line(self.screen,WHITE,(930,65),(950,65),3) #PlusHorizontal                         #
            pygame.draw.line(self.screen,WHITE,(965,65),(985,65),3) #Minus                                  #
            pygame.draw.line(self.screen,WHITE,(930,105),(950,105),3) #PlusHorizontal                       #
            pygame.draw.line(self.screen,WHITE,(965,105),(985,105),3) #Minus                                #
            pygame.draw.line(self.screen,WHITE,(930,145),(950,145),3) #PlusHorizontal                       #
            pygame.draw.line(self.screen,WHITE,(965,145),(985,145),3) #Minus                                #
            pygame.draw.line(self.screen,WHITE,(940,55),(940,75),3) #PlusVertical                           #
            pygame.draw.line(self.screen,WHITE,(940,95),(940,115),3) #PlusVertical                          #
            pygame.draw.line(self.screen,WHITE,(940,135),(940,155),3) #PlusVertical                         #
            #-----------------------------------------------------------------------------------------------
            pygame.draw.rect(self.screen, (96,111,16),(350,325,400,200))                                    #
            pygame.draw.rect(self.screen, (63,6,6),(350,325,400,200),5)                                     #
            drawtxt(self.screen, "ENTER WORLD",self.zombexfont, 80, BLACK,(355,400))                        #
            #-----------------------------------------------------------------------------------------------
            pygame.draw.rect(self.screen,(63,6,6), (225,0,477,220),5)                                       #
            drawtxt(self.screen,self.motd[0],self.zombexfont,30,WHITE,(235,6))                              #
            drawtxt(self.screen,self.motd[1],self.zombexfont,30,WHITE,(235,36))                             #
            drawtxt(self.screen,self.motd[2],self.zombexfont,30,WHITE,(235,66))                             #
            drawtxt(self.screen,self.motd[3],self.zombexfont,30,WHITE,(235,96))                             #
            drawtxt(self.screen,self.motd[4],self.zombexfont,30,WHITE,(235,126))                            #
            drawtxt(self.screen,self.motd[5],self.zombexfont,30,WHITE,(235,156))                            #
            drawtxt(self.screen,self.motd[5],self.zombexfont,30,WHITE,(235,186))                            #
            #-----------------------------------------------------------------------------------------------
            curX, curY = pygame.mouse.get_pos()
            if self.debug_mode == True: drawtxt(self.screen,str(curX)+" | "+str(curY),self.zombexfont,40,BLACK,(0,25))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                    self.__exit__()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if curX >= 925 and curX <= (925+30) and curY >=50 and curY <= (50+30):
                            if self.stats[3] > 0:
                                lobbysendqueue[1].append(0)
                                ##print("Increase Strength")
                            pass #Increase Strength
                        elif curX >= 925 and curX <= (925+30) and curY >=90 and curY <= (90+30):
                            if self.stats[3] > 0:
                                lobbysendqueue[1].append(1)
                                ##print("Increase Health")
                            pass #Increase Health
                        elif curX >= 925 and curX <= (925+30) and curY >=130 and curY <= (130+30):
                            if self.stats[3] > 0:
                                lobbysendqueue[1].append(2)
                                ##print("Increase Speed")
                            pass #Increase Speed
                        elif curX >= 960 and curX <= (960+30) and curY >=50 and curY <= (50+30):
                            if self.stats[0] > 1:
                                lobbysendqueue[1].append(7)
                                ##print("Decrease Strength")
                            pass #Decrease Strength
                        elif curX >= 960 and curX <= (960+30) and curY >=90 and curY <= (90+30):
                            if self.stats[1] > 1:
                                lobbysendqueue[1].append(8)
                                ##print("Decrease Health")
                            pass #Decrease Health
                        elif curX >= 960 and curX <= (960+30) and curY >=130 and curY <= (130+30):
                            if self.stats[2] > 1:
                                lobbysendqueue[1].append(9)
                                ##print("Decrease Speed")
                            pass #Decrease Speed
                        elif curX >= 350 and curX <=(350+400) and curY >=325 and curY <= (325+200):
                            lobbysendqueue[3] = True
                            ##print ("Enter Server")
            pygame.display.update()

            ##lobbydata = pickle.dumps(lobbysendqueue)
            try:
                self.send_packets(lobbysendqueue) #self.client.send(lobbydata)
                lobbysendqueue = ['Lobby',[],[],False]
            except: self.status = [True, 'There was an error sending to the server..', '']
            try:
                datarecieve = self.recv_packets(10000) #datarecieve = pickle.loads (self.client.recv(10000))
            except: pass
            self.stats = datarecieve[0]
            self.messages = datarecieve[1]
            if datarecieve[2]==True:
                lobbysendqueue[3] = False
                self.rinnet_game()
                datarecieve[2] = False

    def rinnet_game(self):
        loop, pause = True, False
        while loop == True:
            keypresses = []
            processedData = []
            self.screen.fill(BLACK)

            if self.debug_mode == True:
                curX, curY = pygame.mouse.get_pos()
                drawtxt(self.screen,str(curX)+" | "+str(curY),self.zombexfont,40,BLACK,(0,25))

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.send_packets(['Logout'])
                    self.loop = False
                    self.__exit__()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.send_packets(['Pause'])
                        loop, pause = False, True


            if pause != True:
                pygame.event.pump()
                key = pygame.key.get_pressed()
                if key[K_UP] or key[K_w]:
                    keypresses.append('w')
                if key[K_DOWN] or key[K_s]:
                    keypresses.append('s')
                if key[K_LEFT] or key[K_a]:
                    keypresses.append('a')
                if key[K_RIGHT] or key[K_d]:
                    keypresses.append('d')

                ##sendDump = ['Game',movements]
                self.send_packets(['Game',keypresses]) ##sendDump
                processedData = self.recv_packets (10000)

                #--   Draw The Players   --#
                try:
                    for i in processedData:
                        i[1].draw(self.screen)
                except: pass
                #--   Draw the Bullets   --#

            pygame.display.update()

    def options (self):
        loop = True
        self.tSelection = 0
        self.menumax = 3

        while loop == True:
            self.screen.fill(BLACK)

            if self.debug_mode == True:
                curX, curY = pygame.mouse.get_pos()
                drawtxt(self.screen,str(curX)+" | "+str(curY),self.zombexfont,40,BLACK,(0,25))

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    loop = False
                    self.__exit__()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if self.tSelection > 0: self.tSelection -=1
                        else: self.tSelection = self.menumax
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if self.tSelection < self.menumax: self.tSelection +=1
                        else: self.tSelection = 0

    def __exit__(self):
        import sys
        pygame.quit()
        sys.exit(0)

def drawtxt(screen, txt,font,size,clr,coordinates,blackbox=[False]):
    """ Coordinates = (x,y)  |  Blackbox = [True/False, width, height, colour] """
    if blackbox[0] == True:
        pygame.draw.rect(screen, blackbox[3], (coordinates[0],coordinates[1],blackbox[1],blackbox[2]))
    font = pygame.font.Font(font,size)
    text = font.render(txt, False, clr)
    screen.blit(text, coordinates)


class Player ():
    def __init__(self, startzone, resolution, clr, radius=15):
        self.xyd, self.oldxyd = startzone, startzone
        self.radius = radius
        self.resolution = resolution
        self.clr = clr

    def update(self, change):
        """ 19/07/2012      TO DO
            Move the current items within the Player Update module into the
            Server Module. In replace, have the Player Update Module gather
            input commands as string and send off to the server for processing
        """

        self.oldxyd = self.xyd
        self.xyd = [self.xyd[0]+change[0], self.xyd[1]+change[1], change[2]]

        if self.xyd[0] > self.resolution[0]:
            self.xyd[0] = self.resolution[0]-25
        elif self.xyd[0] < 0:
            self.xyd[0] = 0

        if self.xyd[1] > self.resolution[1]:
            self.xyd[1] = self.resolution[1]-25
        elif self.xyd[1] < 0:
            self.xyd[1] = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.clr,(int(self.xyd[0]), int(self.xyd[1])), self.radius)
        #--Draw the Gun--#
        if self.xyd[2] == 'w': #Draw Gun Up
            pygame.draw.rect(screen, self.clr,((self.xyd[0]+self.radius-5), (self.xyd[1]+1), 5, -20))
        elif self.xyd[2] == 's': #Draw Gun Down
            pygame.draw.rect(screen, self.clr,((self.xyd[0]-16), (self.xyd[1]+self.radius-15), 5, 20))
        elif self.xyd[2] == 'a': #Draw Gun Left
            pygame.draw.rect(screen, self.clr,((self.xyd[0]+self.radius-15), (self.xyd[1]-15), -20, 5))
        elif self.xyd[2] == 'd': #Draw Gun Right
            pygame.draw.rect(screen, self.clr,((self.xyd[0]+self.radius-14), (self.xyd[1]+self.radius-4), 20, 5))

    def get_pos(self):
        return self.xyd
    def get_clr (self):
        return self.clr
    def set_pos(self, pos):
        self.xyd = pos
    def set_clr(self, clr):
        self.clr = clr

if __name__ == '__main__':
    main = Main([1000,800])
    main.load_resources()
    #main.rinnet_lobby()
    menusel = main.titleLoop()

