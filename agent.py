import pygame
import numpy as np
import random
import math
pygame.init()

COLORS = {
    "RED":  (255, 50, 50),
    "ORANGE": (200, 100, 50),
    "GREEN": (0, 255, 50),
    "CYAN": (0, 255, 255),
    "MAGENTA": (255, 0, 255),
    "BLUE": (50, 50, 255),
    "GREY": (200, 200, 200),
    "LIGHTGREY": (100, 100, 100),
    "YELLOW": (255, 255, 0),
    "TRANS": (1, 1, 1),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
}

class Agent(object):
    def  __init__(self,position):
        self.position = np.array(position, dtype=float)
        self.origin = np.array(position)
        self.size = 15

        self.color = (random.random() * 128, random.random() * 128, random.random() * 128)
        self.velocity = np.array((random.random()*2 -1,random.random()*2 -1))
        self.acceleration = np.zeros(2)

        self.maxforce = 1
        self.maxvelocity= 4

        self.cohesion_radius = self.size *10
        self.separation_radius = self.size *2
        self.alignment_radius = self.size *2
        self.clear_proximity_list()

    def clear_proximity_list(self):
        self.proximity_list = []

    def proximity(self, agents):
        '''
        calculates the distance to the given list of other agents. If distance isbelow the maximum sensing range,
        the other agent is added to the own proximity list
        '''
        for other_agent in agents:
            distance = np.linalg.norm(other_agent.position - self.position)
            if distance < max(self.cohesion_radius, self.alignment_radius,self.separation_radius):
                self.proximity_list.append(other_agent)
                other_agent.proximity_list.append(self)

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

    def separate(self, agents):
        separation_radius = self.size * 2
        steer = np.zeros(2)
        desired = np.zeros(2)
        proximity = 0
        for other in agents:
            distance = np.linalg.norm(other.position - self.position)
            if distance < separation_radius and distance > 0:
                difference = self.position - other.position
                difference = self.normalizeto(difference, 1)
                difference /= distance
                difference *= other.size
                desired += difference
                proximity += 1
        if proximity > 0:
            desired /= proximity
            desired = self.normalizeto(desired, self.maxvelocity)
            steer = desired - self.velocity
        if np.linalg.norm(steer) > self.maxforce:
            steer = self.normalizeto(steer, self.maxforce)
        return steer

    def align(self, agents):
        alignment_radius = self.size * 2
        steer = np.zeros(2)
        desired = np.zeros(2)
        alignwith = 0
        alignmentspeed = 0
        for other in agents:
            distance = np.linalg.norm(other.position - self.position)
            if distance < alignment_radius:
                alignwith += 1
                alignmentspeed += np.linalg.norm(other.velocity)
                desired += other.velocity
        if alignwith > 0:
            alignmentspeed /= alignwith
            desired /= alignwith
            desired = self.normalizeto(desired, self.maxvelocity)
            # desired = self.normalizeto(desired, alignmentspeed)
            steer = desired - self.velocity
        if np.linalg.norm(steer) > self.maxforce:
            steer = self.normalizeto(steer, self.maxforce)
        return steer

    def clear_view(self, agents):
        '''still in experimental mode'''
        front_pos = self.position + (self.velocity * self.size//self.maxvelocity)
        #self_distance = np.linalg.norm(self.position - front_pos)
        steer = np.zeros(2)
        desired = np.zeros(2)
        is_in_front = 0

        right = (self.position[0] + self.velocity[1] * -1, self.position[1] + self.velocity[0] * 1)
        left = (self.position[0] + self.velocity[1] * 1, self.position[1] + self.velocity[0] * -1)

        for other in agents:
            distance = np.linalg.norm(other.position - front_pos)
            print(distance)
            if distance < self.size*2:
                is_in_front += 1

        if is_in_front > 1:
            print("isinfront")
            desired = left if random.random()>0.5 else right
            desired = self.normalizeto(desired, self.maxvelocity)
            steer = desired - self.velocity
        if np.linalg.norm(steer) > self.maxforce:
            steer = self.normalizeto(steer, self.maxforce)
        return steer

    def flock(self, agents):
        '''
        combines
        * cohesionn
        * alignment
        * separation

        goal was to have a single function instead of having to check distances between all agents three times.
        '''
        c_steer = np.zeros(2)
        c_desired = np.zeros(2)
        c_pos_sum = np.zeros(2)
        c_proximity = 0
        s_steer = np.zeros(2)
        s_desired = np.zeros(2)
        s_difference = (0,0)
        s_proximity = 0
        a_steer = np.zeros(2)
        a_desired = np.zeros(2)
        a_alignmentspeed = 0
        a_proximity = 0
        #check all agents in proximity list (when calculated beforehand) or simply in full agent list
        #for other_agent in self.proximity_list:
        for other_agent in agents:
            distance = np.linalg.norm(other_agent.position - self.position)
            if distance < self.cohesion_radius:
                c_pos_sum += other_agent.position
                c_proximity += 1
            if distance < self.separation_radius and distance > 0:
                s_difference = self.position - other_agent.position
                s_difference = self.normalizeto(s_difference, 1)
                s_difference /= distance
                s_difference *= self.size ###!!
                s_desired += s_difference
                s_proximity += 1
            if distance < self.alignment_radius:
                a_alignmentspeed += np.linalg.norm(other_agent.velocity)
                a_desired += other_agent.velocity
                a_proximity += 1
        #check of cohesion, or separation or alignment are to be applied
        if c_proximity:
            c_pos_sum /= c_proximity
            c_desired =  c_pos_sum - self.position
            c_desired = self.normalizeto(c_desired, self.maxvelocity)
            c_steer = c_desired - self.velocity
            if np.linalg.norm(c_steer) > self.maxforce:
                c_steer = self.normalizeto(c_steer, self.maxforce)
        if s_proximity:
            s_desired /= s_proximity
            s_desired = self.normalizeto(s_desired, self.maxvelocity)
            s_steer = s_desired - self.velocity
            if np.linalg.norm(s_steer) > self.maxforce:
                s_steer = self.normalizeto(s_steer, self.maxforce)
        if a_proximity:
            a_alignmentspeed /= a_proximity
            a_desired /= a_proximity
            a_desired = self.normalizeto(a_desired, self.maxvelocity)
            # a_desired = self.normalizeto(desired, alignmentspeed)
            a_steer = a_desired - self.velocity
            if np.linalg.norm(a_steer) > self.maxforce:
                a_steer = self.normalizeto(a_steer, self.maxforce)
        return c_steer, s_steer, a_steer


    def applyForce(self, force):
        '''
        function to apply a force to an agent
        '''
        self.forces.append(force)
        self.acceleration += force


    def update(self, agents, weights=(100,70,40)):
        '''
        function that handles an agents behavior
        :param agents: list
            list of all agents
        :param weights: list
            list or tuple of the three weights for cohesion, separation and alignment
        '''
        fleeforce=np.zeros(2)
        arriveforce=np.zeros(2)
        seekforce=np.zeros(2)
        alignmentforce=np.zeros(2)
        separationforce=np.zeros(2)
        cohesionforce=np.zeros(2)
        self.forces = []

        alignment_weight = weights[0]/100
        separation_weight = weights[1]/100
        cohesion_weight = weights[2]/100

        #calculate forces
        fleeforce = self.flee(pygame.mouse.get_pos())
        #alignmentforce = self.align(agents)
        #separationforce = self.separate(agents)
        #cohesionforce = self.cohesion(agents)
        cohesionforce, separationforce, alignmentforce = self.flock(agents)

        #weigh and apply forces
        self.applyForce(fleeforce)
        self.applyForce(alignmentforce*alignment_weight)
        self.applyForce(separationforce*separation_weight)
        self.applyForce(cohesionforce*cohesion_weight)


        #get new velocity
        self.velocity += self.acceleration
        if np.linalg.norm(self.velocity) > self.maxvelocity:
            self.velocity = self.normalizeto(self.velocity,self.maxvelocity)

        #get new position
        self.position += self.velocity
        self.acceleration *= 0

        #HANDLE THE EDGE
        #1. overflow (
        #self.position[0] = self.position[0]% 1200
        #self.position[1] = self.position[1] % 800
        #2. hard fence (reset position)
        #self.position[0] = max(0,min(self.position[0],1200))
        #self.position[1] = max(0,min(self.position[1],800))
        #3. soft fence (seek center when leaving bounds)
        if self.position[0] < 0 or self.position[1] < 0 or self.position[0] > 1200 or self.position[1] > 800:
            correction_force = (self.seek((600,400)) * (abs(self.position[0])%1200) * (abs(self.position[1])%800)) *0.5
            self.applyForce(correction_force)

    def draw_forces(self, window):
        '''
        function to plot all apllied forces vectors
        '''
        for force, color in zip(self.forces, list(COLORS.items())[:-len(self.forces)]):
            force_end =  self.position+(50*force)
            pygame.draw.line(window, color[1], self.position, force_end, 1)


    def draw_velocity(self, window):
        pygame.draw.line(window, self.multiply_color(self.color,0.5), self.position, self.position+(self.velocity*self.size//self.maxvelocity), 1)


    def draw(self, window):
        '''
        function that draws the agent
        '''
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

        pygame.draw.line(window, self.color, angleLineR, tiplineEnd,
                         max(1, int((self.size * self.size) / 100)))
        pygame.draw.line(window, self.color, angleLineL, tiplineEnd,
                         max(1, int((self.size * self.size) / 100)))
        pygame.draw.line(window, self.color, self.position, angleLineR,
                         max(1, int((self.size * self.size) / 100)))
        pygame.draw.line(window, self.color, self.position, angleLineL,
                         max(1, int((self.size * self.size) / 100)))

    def normalizeto(self, vector, max):
        if np.linalg.norm(vector) > 0:
            return (vector/np.linalg.norm(vector)) * max
        else:
            return np.zeros(2)

    def multiply_color(self, color, value):
        return (color[0]*value, color[1]*value, color[2]*value)