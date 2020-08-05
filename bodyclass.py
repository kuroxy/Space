import numpy as np
import math
import pygame

class body(object):
    """docstring for body."""
    CONST_G = 6.674*10**-9

    def __init__(self, pos, vel, mass):
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.acc = np.zeros(2)
        self.mass = mass
        self.radius = math.sqrt(mass/math.pi)*.0001

    def applyForce(self, force):
        force = np.divide(force, self.mass)
        self.acc = np.add(self.acc, force)

    def update(self):
        self.vel = np.add(self.vel, self.acc)
        self.pos = np.add(self.pos, self.vel)
        self.acc = np.multiply(self.acc, 0)

    def drawpoint(self, CAMERAPOS, CAMERASIZE, surface):

        r_pos_x = int((self.pos[0] + CAMERAPOS[0] + (surface.get_size()[0]*CAMERASIZE)/2) * 1 / CAMERASIZE)
        r_pos_y = int((self.pos[1] + CAMERAPOS[1] + (surface.get_size()[1]*CAMERASIZE)/2) * 1 / CAMERASIZE)

        r_size = math.ceil(self.radius / CAMERASIZE)

        pygame.draw.circle(surface, (255, 255, 255), [r_pos_x,r_pos_y], r_size)


    @staticmethod
    def calcdist(b1, b2):
        temp = np.subtract(b1.pos, b2.pos)
        return np.hypot(temp[0],temp[1])


    @staticmethod
    def calculateForce(b1, b2):
        distancevec = np.subtract(b1.pos, b2.pos)
        distance = body.calcdist(b1, b2)


        if distance != 0:
            normalized = np.divide(distancevec, distance)
            force = np.multiply(np.multiply(normalized, -1), (body.CONST_G*b1.mass*b2.mass)/(distance*distance))
        else:
            force = np.zeros(2)

        b1.applyForce(force)
        b2.applyForce(np.multiply(force,-1))

        return distance
        # a bit counterintuitive but it makes it easier to do collision without calculating distance again

    @staticmethod
    def average(b1, b2):
        b3mass = b1.mass + b2.mass
        b3pos = b1.pos/b3mass*b1.mass + b2.pos/b3mass*b2.mass
        b3vel = b1.vel/b3mass*b1.mass + b2.vel/b3mass*b2.mass
        return (b3pos, b3vel, b3mass)
