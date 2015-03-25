#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      killer rin
#
# Created:     09/09/2012
# Copyright:   (c) killer rin 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import pickle
import os
import random

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

character_file = open (os.path.join('Server','Players','kill','Character.zs'), 'rb')
character = pickle.load(character_file)
character_file.close()

##character_file = open (os.path.join('Server','Players','kill','Character.zs'),'wb')
##character = Player ([random.randint(0,1000),random.randint(0,800),'s'],[1000,800], (0,255,0))
##pickle.dump(character,character_file)
##character_file.close()

print(character)