import math
import numpy as np
import random as rn
import pygame

CONST_G = 1


# random seed set CONST_SEED to zero

CONST_SEED = 0
if CONST_SEED == 0:
    CONST_SEED = rn.randrange(0, 1000000)


rn.seed(CONST_SEED)

# amount of point that are going to be created
CONST_AMOUNTPOINTS = 70

# Printing all constants that can define the outcome
print("[Internal] Const G: " + str(CONST_G))
print("[Internal] Const Seed: " + str(CONST_SEED))
print("[Internal] Const Amount Of Points: " + str(CONST_AMOUNTPOINTS))


class idclass():
    def __init__(self):
        self.id = 0

    def returnid(self):
        self.id += 1

        return self.id


main = idclass()


class point():
    def __init__(self, loc, vel, mass, pid):
        self.location = np.array([loc[0], loc[1]])
        self.velocity = np.array([vel[0], vel[1]])
        self.acceleration = np.array([0, 0])
        self.mass = mass
        self.id = pid
        self.radius = math.sqrt(mass/math.pi)

    def applyForce(self, force):
        force = np.divide(force, self.mass)
        self.acceleration = np.add(self.acceleration, force)

    def update(self):
        self.velocity = np.add(self.velocity, self.acceleration)
        self.location = np.add(self.location, self.velocity)
        self.acceleration = np.multiply(self.acceleration, 0)

    def drawpoint(self, surface):
        pygame.draw.circle(surface, (0, 0, 0), [int(
            self.location[0]), int(self.location[1])], int(self.radius))

    def removewithid(self):
        self.id = 0


def calculateDistance(loc1, loc2):
    distancevec = np.absolute(np.subtract(loc1, loc2))
    distance = math.sqrt(
        distancevec[0]*distancevec[0]+distancevec[1]*distancevec[1])
    return distance


def calculateForce(loc1, loc2, m1, m2):
    distancevec = (np.subtract(loc1, loc2))
    distance = calculateDistance(loc1, loc2)
    normalized = np.divide(distancevec, distance)

    force = np.multiply(np.multiply(normalized, -1),
                        (CONST_G*m1*m2)/(distance*distance))
    return force


# plist the list with objects, loc location, vel velocity, mass mass,
# idclss the object with the idclass
def createpoint(plist, loc, vel, mass, idclss):
    id
    plist.append(point(loc, vel, mass, idclss.returnid()))
    print("[info] Point " + str(idclss.id) + " created.")

# suffix m smallest int, suffix r biggest the int can be


def randcreatepoint(plist, locm, locr, velm, velr, massm, massr, idclss):
    loc = [rn.randint(locm[0], locr[0]), rn.randint(locm[1], locr[1])]
    vel = [rn.randint(velm[0], velr[0]), rn.randint(velm[1], velr[1])]
    mass = rn.randint(massm, massr)
    createpoint(plist, loc, vel, mass, idclss)


def returnlistid(prlist):
    printtxt = "[ "
    for i in prlist:
        printtxt += str(i.id) + " "

    printtxt += "]"
    return printtxt


screenSize = np.array([1080, 720])

listofpoints = []  # list with all points objects


for i in range(CONST_AMOUNTPOINTS):
    randcreatepoint(listofpoints, [0, 0], [screenSize[0], screenSize[1]], [
                    0, 0], [0, 0], 5, 50, main)


pygame.init()
display = pygame.display.set_mode((screenSize[0], screenSize[1]))
run = True

print("Starting")
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pointsremoved = False

    # clear screen

    display.fill((255, 255, 255))

    # draw point on screen

    for i in listofpoints:
        i.drawpoint(display)

    # calculations

    for i in listofpoints:
        for j in listofpoints:
            if i.id != j.id:
                calc = calculateForce(i.location, j.location, i.mass, j.mass)
                i.applyForce(calc)

    # update points

    for i in listofpoints:
        i.update()

    # collision dection
    for i in listofpoints:
        if i.id != 0:
            for j in listofpoints:
                if i.id != j.id and i.id != 0 and j.id != 0:
                    rad = i.radius + j.radius
                    if calculateDistance(i.location, j.location) <= rad:
                        # if colliding create new mass
                        # new location for the new created point
                        # by averaging by the mass of the 2 points

                        newmass = i.mass + j.mass

                        newloc = i.location/newmass*i.mass + \
                            j.location/newmass*j.mass

                        newvel = i.velocity/newmass*i.mass + \
                            j.velocity/newmass*j.mass

                        createpoint(listofpoints, newloc,
                                    newvel, newmass, main)

                        i.removewithid()
                        j.removewithid()
                        pointsremoved = True

                        
 
    # update screen

    pygame.display.flip()

    # removing collided points
    # but only if we know if points are removed for performance
    if pointsremoved:
        copiedlist = listofpoints.copy()
        for i in copiedlist:
            if i.id == 0:
                listofpoints.remove(i)
        print("[Debug] List " + returnlistid(listofpoints))
    pygame.time.wait(10)

pygame.quit()
