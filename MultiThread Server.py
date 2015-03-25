#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      killer rin
#
# Created:     18/07/2012
# Copyright:   (c) killer rin 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pickle
import socket
import threading
import os
import random

# Our thread class:
class ClientThread ( threading.Thread ):

   # Override Thread's __init__ method to accept the parameters needed:
    def __init__ (self, channel, details):
        self.channel = channel # Socket Details
        self.details = details # ('Address', Port)

        self.debug_mode = False
        self.status = [True,'']
        self.username = None

        self.motd = database.get_motd()
        threading.Thread.__init__ ( self )
        print ('Received connection:', self.details [ 0 ])

    def run (self):
        data = ['']
        while self.status[0] == True:
            data = self.recv_packets(10000)
            if self.debug_mode == True: print (data)
            if data[0] == 'LOGIN':
                self.server_enterance ('login', [data[1], data[2]])
            elif data[0] == 'REGISTER':
                self.server_enterance ("register", [data[1], data[2]])
            elif data[0] == 'Lobby':
                self.server_lobby ([data[1], data[2], data[3]])
            elif data[0] == 'Game':
                self.server_game ([data[1]])
            elif data[0] == 'Pause':
                database.go_offline(self.username)
            elif data[0] == 'Logout':
                database.go_offline(self.username)
        self.channel.close()
        print ('Closed connection:', self.details [ 0 ])

    def server_enterance(self, logReg, data):
        if logReg == 'login':
            try:
                load_player_info = open (os.path.join('Server','Players',data[0],'Login.zs'), 'rb')
                load_player_stats = open (os.path.join('Server','Players',data[0],'Stats.zs'),'rb')
                player_info = pickle.load(load_player_info)
                player_stats = pickle.load(load_player_stats)
                load_player_info.close()
                load_player_stats.close()
                if data == player_info:
                    self.send_packets([[True, '', ''],player_stats, self.motd])
                    self.username = data[0]
                    self.stats = player_stats
                player_info = None

            except:
                if not os.path.exists (os.path.join('Server', 'Players', data[0])):
                    self.send_packets([[False,'That account does not exist', ''],[1,1,1,0]])
                else: self.send_packets([[False,'There was an error retrieving player information', ''],[1,1,1,0]])

        elif logReg == 'register':
            ctr = 0
            #--   Check to see if the account already exists  --#
            if ctr < 1:
                if not os.path.exists (os.path.join('Server', 'Players', data[0])):
                    os.makedirs(os.path.join('Server', 'Players', data[0]))
                    foldCheck = True
                    ctr += 1
                else:
                    self.send_packets([[False,'An account with that name already exists', ''],[1,1,1,0]])
                    foldCheck = False
                    ctr += 1

            #--  If the account does not exist, continue  --#
            if foldCheck == True:
                try:
                    player_info = open (os.path.join('Server','Players',data[0],'Login.zs'), 'wb')
                    player_stats = open (os.path.join('Server','Players',data[0],'Stats.zs'),'wb')
                    pickle.dump(data,player_info)
                    pickle.dump([1,1,1,5],player_stats)
                    player_info.close()
                    player_stats.close()
                    player_info = None

                    self.send_packets([[True, '', ''],[1,1,1,5], self.motd])
                    self.username = data[0]
                    self.stats = [1,1,1,5]
                except: self.send_packets([[False,'There was an error registering your account', 'Please Try Again Later'],[1,1,1,0]])

    def server_lobby(self, data):
        for i in data[0]: #Stats
            if i == 0: # Inc Strength
                if self.stats[3] > 0:
                    self.stats[0] += 1
                    self.stats[3] -= 1
            elif i == 1: # Inc Health
                if self.stats[3] > 0:
                    self.stats[1] += 1
                    self.stats[3] -= 1
            elif i == 2: # Inc Speed
                if self.stats[3] > 0:
                    self.stats[2] += 1
                    self.stats[3] -= 1
            elif i == 7: # Dec Strength
                if self.stats[0] > 1:
                    self.stats[0] -= 1
                    self.stats[3] += 1
            elif i == 8: # Dec Health
                if self.stats[1] > 1:
                    self.stats[1] -= 1
                    self.stats[3] += 1
            elif i == 9: # Dec Speed
                if self.stats[2] > 1:
                    self.stats[2] -= 1
                    self.stats[3] += 1

        #data[1] = Messages
        if data[2] == True:
            # Make a call to the master server memory to grab player location. Call the master server memory and move the player
            # to the online list. Send back online list
            self.players = database.go_online(self.username)
        self.send_packets([self.stats,[],data[2]])

    def server_game(self, data):
        """ The Error Is that it will not enter into the database. Check the Database code to ensure it works."""
        players = database.get_players()

        ctr = -1
        for i in players:
            ctr += 1
            if i[0] == self.username:
                i[1].set_stats(self.stats)
                break
        for i in data[0]: # Movements
            if i == 'w': players[ctr][1].update('w')
            if i == 's': players[ctr][1].update('s')
            if i == 'a': players[ctr][1].update('a')
            if i == 'd': players[ctr][1].update('d')
        database.update_player(players[ctr])
        self.send_packets(players)

    def send_packets(self, data):
        try:
            packets = pickle.dumps(data)
            self.channel.send(packets)
        except:
            self.status = [False,"There Was An Issue Sending Data", ""]

    def recv_packets(self, buffer):
        try:
            data = pickle.loads (self.channel.recv(buffer))
            return data
        except:
            self.status = [False, "There Was An Issue Recieveing Data", ""]
            return 'connectionfailure'

    def __exit__(self):
        import sys
        pygame.quit()
        sys.exit(0)

class ServerDatabase():
    def __init__ (self):
        self.motd = ['',\
                     '',\
                     '',\
                     '',\
                     '',\
                     '',\
                     '']
        self.online = []
        self.motd_update()
        print (self.motd)

    def motd_update(self):
        #---   Set up the MOTD   ---#
        lines = [[0, False],[0, False],[0, False],[0, False], [0, False],\
                [0, False],[0, False]]
        motdloop = True
        while motdloop == True:
            try:
                motd_file = open (os.path.join('Server','MOTD.txt'),'rU')
                motd_split = motd_file.read()
                motd_split = list(motd_split)
                motd_file.close()
                motdloop = False
            except:
                motd_file = open (os.path.join('Server','MOTD.txt'),'w')
                motd_file.write('')
                motd_file.close()
        for i in motd_split:
            if lines[0][1] != True:
                if len(self.motd[0]) < 39:
                    self.motd[0] += i
                else: lines[0][1] = True
            elif lines[1][1] != True:
                if len(self.motd[1]) < 39:
                    self.motd[1] += i
                else: lines[1][1] = True
            elif lines[2][1] != True:
                if len(self.motd[2]) < 39:
                    self.motd[2] += i
                else: lines[2][1] = True
            elif lines[3][1] != True:
                if len(self.motd[3]) < 39:
                    self.motd[3] += i
                else: lines[3][1] = True
            elif lines[4][1] != True:
                if len(self.motd[4]) < 39:
                    self.motd[4] += i
                else: lines[4][1] = True
            elif lines[5][1] != True:
                if len(self.motd[5]) < 39:
                    self.motd[5] += i
                else: lines[5][1] = True
            elif lines[6][1] != True:
                if len(self.motd[6]) < 39:
                    self.motd[6] += i
                else: lines[6][1]  = True

    def go_online (self, username):
        try:
            character_file = open (os.path.join('Server','Players',username,'Character.zs'), 'rb')
            character = pickle.load(character_file)
            character_file.close()
        except:
            character_file = open (os.path.join('Server','Players',username,'Character.zs'),'wb')
            character = Player ([random.randint(0,1000),random.randint(0,800),'s'],[1000,800], (0,255,0))
            pickle.dump(character,character_file)
            character_file.close()
        self.online.append([username,character])
        return self.online

    def go_offline (self, username):
        ctr = -1
        for i in self.online:
            ctr += 1
            if i[0] == username:
                character_file = open (os.path.join('Server','Players',username,'Character.zs'),'wb')
                pickle.dump(i[1],character_file)
                character_file.close()
                    #--- ---#
                self.online.pop(ctr)
                break

    def update_player (self,player):
        ctr = -1
        for i in self.online:
            ctr += 1
            if i[0] == player[0]:
                i[1] = player[1]
                break


    def get_motd (self):
        return self.motd

    def get_players (self):
        return self.online

    def set_motd (self,l1='',l2='',l3='',l4='',l5='',l6='',l7=''):
        self.motd = [l1,\
                     l2,\
                     l3,\
                     l4,\
                     l5,\
                     l6,\
                     l7]

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
        if change == 'w': move = [0,-(0.1+self.stats[2]),'w']
        if change == 's': move = [0,(0.1+self.stats[2]),'s']
        if change == 'a': move = [-(0.1+self.stats[2]),0,'a']
        if change == 'd': move = [(0.1+self.stats[2]),0,'d']

        self.oldxyd = self.xyd
        self.xyd = [self.xyd[0]+move[0], self.xyd[1]+move[1], move[2]]

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
    def get_stats (self):
        return self.stats
    def set_pos(self, pos):
        self.xyd = pos
    def set_clr(self, clr):
        self.clr = clr
    def set_stats(self,stats):
        self.stats = stats

#-- Ensure Directories Exist, If Not Create Them. --#
if not os.path.exists (os.path.join('Server', 'Players')):
    os.makedirs(os.path.join('Server', 'Players'))
#--  Make the Server Database  --#
database = ServerDatabase()

#--  Set up the server:  --#
server = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )

server.bind ( ( 'localhost',28637 ) ) #'localhost''192.168.0.100'
server.listen ( 5 )
# Have the server serve "forever":
while True:
   channel, details = server.accept()
   ClientThread ( channel, details ).start()