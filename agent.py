import pygame
import numpy as np
import random
import math

pygame.init()

class Agent(object):
    def  __init__(self,position):
        self.position = np.array(position, dtype=float)
        self.origin = np.array(position)
        self.size = 10

        self.color = (random.random() * 155, random.random() * 155, random.random() * 155)
        self.velocity = np.array((random.random()*2 -1,random.random()*2 -1))
        self.acceleration = np.zeros(2)


        self.maxforce = 1
        self.maxvelocity= 4


    def seek(self,target_pos):
        steer = np.zeros(2)
        #difference to target
        desired = np.array(target_pos) - self.position

        #normalization
        if np.linalg.norm(desired) > 0:
            desired = desired/np.linalg.norm(desired)
            #magnitude is maxvelocity
            desired = desired*self.maxvelocity
            #calculate steering force
            steer = desired - self.velocity
            # limit force
            if np.linalg.norm(steer) > self.maxforce:
                steer = self.normalizeto(steer, self.maxforce)

        return steer

    def flee(self, target_pos):
        steer = np.zeros(2)
        # difference to target
        difference = np.array(target_pos) - self.position
        #distance
        distance = np.linalg.norm(difference)
        # normalization
        if distance < 50 and distance > 0:
            desired = difference / np.linalg.norm(difference)
            # magnitude is maxvelocity
            desired_speed = self.maxvelocity
            desired = desired * desired_speed
            # calculate steering force
            steer = desired - self.velocity
            # limit force
            if np.linalg.norm(steer) > self.maxforce:
                steer = self.normalizeto(steer, self.maxforce)
        return steer*-1

    def arrive(self,target_pos):
        steer = np.zeros(2)
        #difference to target
        difference = np.array(target_pos) - self.position
        #normalization
        distance = np.linalg.norm(difference)
        print("distance", distance)
        if distance > 0:
            desired = difference/np.linalg.norm(difference)
            #magnitude is dependant on distance to target
            desired_speed = np.interp(distance,[0,50],[0,self.maxvelocity])
            print("des speed", desired_speed)
            desired = desired*desired_speed
            #calculate steering force
            steer = desired - self.velocity
            #limit force
            if np.linalg.norm(steer) > self.maxforce:
                steer = self.normalizeto(steer,self.maxforce)
        return steer


    def align(self,agents):
        alignment_radius = self.size*2
        steer = np.zeros(2)
        desired = np.zeros(2)
        alignwith = 0
        alignmentspeed = 0
        for other in agents:
            distance = np.linalg.norm(other.position-self.position)
            if distance<alignment_radius:
                alignwith += 1
                alignmentspeed += np.linalg.norm(other.velocity)
                desired += other.velocity
        if alignwith >0:
            alignmentspeed /= alignwith
            desired /= alignwith
            desired = self.normalizeto(desired,self.maxvelocity)
            #desired = self.normalizeto(desired, alignmentspeed)
            steer = desired - self.velocity
        if np.linalg.norm(steer) > self.maxforce:
            steer = self.normalizeto(steer, self.maxforce)
        return steer


    def separate(self,agents):
        separation_radius = self.size*2
        steer = np.zeros(2)
        desired = np.zeros(2)
        proximity = 0
        for other in agents:
            distance = np.linalg.norm(other.position - self.position)
            if distance < separation_radius and distance > 0:
                difference = self.position - other.position
                difference = self.normalizeto(difference,1)
                difference /= distance
                difference *= other.size
                desired += difference
                proximity += 1
        if proximity >0:
            desired /= proximity
            desired = self.normalizeto(desired, self.maxvelocity)
            steer = desired - self.velocity
        if np.linalg.norm(steer) > self.maxforce:
            steer = self.normalizeto(steer, self.maxforce)
        return steer

    def cohesion(self, agents):
        cohesion_radius = self.size * 10
        steer = np.zeros(2)
        desired = np.zeros(2)
        proximity = 0
        pos_sum = np.zeros(2)
        for other in agents:
            distance = np.linalg.norm(other.position - self.position)
            if distance < cohesion_radius:
                pos_sum += other.position
                proximity += 1
        if proximity > 0:
            pos_sum /= proximity
            desired =  pos_sum - self.position
            desired = self.normalizeto(desired, self.maxvelocity)
            steer = desired - self.velocity
        if np.linalg.norm(steer) > self.maxforce:
            steer = self.normalizeto(steer, self.maxforce)
        return steer


    def applyForce(self, force):
        self.acceleration += force


    def update(self, agents, weights=[100,70,40]):
        fleeforce=np.zeros(2)
        arriveforce=np.zeros(2)
        seekforce=np.zeros(2)
        alignmentforce=np.zeros(2)

        alignment_weight = weights[0]/100
        separation_weight = weights[1]/100
        cohesion_weight = weights[2]/100


        fleeforce = self.flee(pygame.mouse.get_pos())
        #arriveforce = self.arrive(self.origin)
        alignmentforce = self.align(agents)
        separationforce = self.separate(agents)
        cohesionforce = self.cohesion(agents)

        self.applyForce(alignmentforce*alignment_weight)
        self.applyForce(separationforce*separation_weight)
        self.applyForce(cohesionforce*cohesion_weight)
        self.applyForce(fleeforce)


        self.velocity += self.acceleration
        if np.linalg.norm(self.velocity) > self.maxvelocity:
            self.velocity = self.normalizeto(self.velocity,self.maxvelocity)


        self.position += self.velocity
        self.acceleration *= 0


        self.position[0] = self.position[0]% 1200
        self.position[1] = self.position[1] % 800


    def draw(self, window):
        # draw character blob

        #pygame.draw.circle(window, self.color, (int(self.position[0]),int(self.position[1])), int(self.size),2)
        #pygame.draw.circle(window, self.color, self.origin, int(self.size/3), 2)

        tip = self.normalizeto(self.velocity, self.size)
        tiplineEnd = (self.position[0] + tip[0],
                   self.position[1] + tip[1])
        #pygame.draw.line(window, (0, 0, 0), self.position, lineEnd,1)

        #perplineEndr = (self.position[0] + self.velocity[1] * 10,
        #               self.position[1] + self.velocity[0] * -10)
        #perplineEndl = (self.position[0] + self.velocity[1] * -10,
        #                self.position[1] + self.velocity[0] * 10)

        angle = math.atan2(self.velocity[0], self.velocity[1]) + (math.pi*0.85)
        angle2 = math.atan2(self.velocity[0], self.velocity[1]) - (math.pi*0.85)
        angleLineR = (self.position[0] + math.sin(angle) * self.size,
                    self.position[1] + math.cos(angle) * self.size)
        angleLineL = (self.position[0] + math.sin(angle2) * self.size,
                      self.position[1] + math.cos(angle2) * self.size)

        pygame.draw.line(window, (0, 0, 0), angleLineR, tiplineEnd,
                         max(1, int((self.size * self.size) / 100)))
        pygame.draw.line(window, (0, 0, 0), angleLineL, tiplineEnd,
                         max(1, int((self.size * self.size) / 100)))
        pygame.draw.line(window, (0, 0, 0), self.position, angleLineR,
                         max(1, int((self.size * self.size) / 100)))
        pygame.draw.line(window, (0, 0, 0), self.position, angleLineL,
                         max(1, int((self.size * self.size) / 100)))



    def normalizeto(self, vector, max):
        if np.linalg.norm(vector) > 0:
            return (vector/np.linalg.norm(vector)) * max
        else:
            return np.zeros(2)