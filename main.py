import math
import numpy as np
import random as rn
import sys
import pygame
from bodyclass import body


def ranfloat(tup):
    return rn.uniform(tup[0], tup[1])




# random seed set CONST_SEED to zero

CONST_SEED = 0

if CONST_SEED == 0:
    CONST_SEED = rn.randint(0,100000000000)


rn.seed(CONST_SEED)


START_AMOUNTBODIES = 100


# Printing all constants
print("[Internal] Const G: " + str(body.CONST_G))   # you can change const G in bodyclass.py
print("[Internal] Const Seed: " + str(CONST_SEED))
print("[Internal] Start Amount Of Bodies: " + str(START_AMOUNTBODIES))



bodylist = []   # MAIN LIST

# body settings

posxrange = (-1000,1000)
posyrange = (-1000,1000)
velxrange = (-1,1)
velyrange = (-1,1)
massrange = (10**5, 10**10)

for _ in range(START_AMOUNTBODIES):
    b = body((ranfloat(posxrange), ranfloat(posyrange)), (ranfloat(velxrange), ranfloat(velyrange)), ranfloat(massrange))
    bodylist.append(b)

# camera settings
cameraPos = np.zeros(2)
camerSize = 2
cameraSpeed = 10

# pygame settings

displaySize = [1080,720]

pygame.init()
display = pygame.display.set_mode((displaySize[0], displaySize[1]))

# MAIN EVENTS
def userInput(keys):
    tempcampos = cameraPos
    tempcamsize = camerSize

    if keys[pygame.K_x]:
        tempcamsize*=.9
    if keys[pygame.K_z]:
        tempcamsize/=.9

    if keys[pygame.K_w]:
        tempcampos[1]+=cameraSpeed*tempcamsize

    if keys[pygame.K_s]:
        tempcampos[1]-=cameraSpeed*tempcamsize

    if keys[pygame.K_d]:
        tempcampos[0]-=cameraSpeed*tempcamsize

    if keys[pygame.K_a]:
        tempcampos[0]+=cameraSpeed*tempcamsize

    return (tempcampos, tempcamsize)


# MAIN LOOP
while True:
    # pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clearin screen
    display.fill((20,20,20))


    # User input
    keys = pygame.key.get_pressed()
    cameraPos, camerSize = userInput(keys)

    #Physics
    tempbodylist= bodylist.copy()

    for i in range(len(bodylist)):
        for j in range(i+1, len(bodylist)):
            dist = body.calculateForce(bodylist[i], bodylist[j])

            radius = (bodylist[i].radius + bodylist[j].radius)
            if radius >= dist:
                if bodylist[i] in tempbodylist and bodylist[j] in tempbodylist:
                    av = body.average(bodylist[i], bodylist[j])
                    tempbodylist.append(body(av[0],av[1],av[2]))

                    tempbodylist.remove(bodylist[i])

                    tempbodylist.remove(bodylist[j])

    bodylist = tempbodylist.copy()

    # update bodies/draw
    for i in bodylist:
        i.update()
        i.drawpoint(cameraPos, camerSize, display)

    #update display
    pygame.display.flip()
