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


agents = []

for i in range(1):
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

    weigths = [s.val for s in sliders]


    for agent in agents:
        agent.update(agents, weigths)
        agent.draw(window)



    # Move sliders
    for s in sliders:
        if s.hit:
            s.move()
        s.draw(window)


    pygame.display.update()
    clock.tick(90)


pygame.quit()
quit()