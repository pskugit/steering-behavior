import pygame
import sys
import numpy as np
from agent import *
from interaction import *

pygame.init()
pygame.font.init()
sys_font = pygame.font.SysFont('lucidasanstypewriterfett', 12)

win_width=1200
win_height=800
bg_color = (250,250,250)
window = pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption("Steering bahavior")
window.fill(bg_color)

clock = pygame.time.Clock()
run = True

#screen elements
align = Slider("Alignment", 70, 0, 100, 20, 20)
sepa = Slider("Separation", 100, 0, 100, 20, 65)
cohe = Slider("Cohesion", 40, 0, 100, 20, 110)
sliders = [align, sepa, cohe]

#initial agents
agents = []
for i in range(20):
    agents.append(Agent((int(random.random()*1600),int(random.random()*900))))

while(run):
    window.fill(bg_color)
    # Event handler
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            agents.append(Agent(mouse_pos))
            # slider
            for s in sliders:
                if s.button_rect.collidepoint(mouse_pos):
                    s.hit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            for s in sliders:
                s.hit = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                agents = agents[:-1]

    #weights and slider settings
    weights = [s.val for s in sliders]
    # Move sliders
    for s in sliders:
        if s.hit:
            s.move()
        s.draw(window)

    #for i, agent in enumerate(agents):
    #   #agent.proximity(agents[i:])
    #   agent.proximity(agents[i+1:])

    # iterate over all agents to calculate the behavior
    for agent in agents:
        agent.update(agents, weights)
        agent.draw(window)
        # agent.clear_proximity_list()

    # draw instruction
    #instr1 = sys_font.render("Instructions:" , 0, (0, 0, 0))
    instr2 = sys_font.render("click to spawn new agent" , 0, (0, 0, 0))
    instr3 = sys_font.render("press R to remove agent" , 0, (0, 0, 0))
    #window.blit(instr1, (1000, 30))
    window.blit(instr2, (1000, 30))
    window.blit(instr3, (1000, 50))

    pygame.display.update()
    clock.tick(90)

pygame.quit()
quit()