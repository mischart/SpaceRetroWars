import pygame, sys, pygame.locals#1
pygame.init()#2
window=pygame.display.set_mode((500, 400), 0, 32)#3
pygame.display.set_caption("Paint")#4
BLACK = (0, 0, 0)#5
WHITE = (255, 255, 255)#6
RED = (255, 0, 0)#7
GREEN = (0, 255, 0)#8
BLUE = (0, 0, 255)#9
pentagon=pygame.Surface((250, 265))#10
pentagon.fill((0, 0, 0))#11
pygame.draw.polygon(pentagon, BLUE, ((146, 0), (250, 100), (230, 265), (44, 250), (0,110)))#12
pentagon.set_colorkey((0, 0, 0))#13
triangle=pygame.Surface((150, 200))#14
triangle.fill((0, 0, 0))#15
pygame.draw.polygon(triangle, RED, ((70, 0), (150, 200), (0, 50)))#16
triangle.set_colorkey((0, 0, 0))#17
line=pygame.Surface((60, 8))#18
line.fill(BLACK)#19
circle=pygame.Surface((30, 30))#20
circle.fill((0, 0, 0))#21
pygame.draw.circle(circle, GREEN , (15, 15), 15, 0)#22
circle.set_colorkey((0, 0, 0))#23
rects={'pentagon': pentagon.get_rect(), 'triangle': triangle.get_rect(), 'line': line.get_rect(), 'circle': circle.get_rect()}#24
rects['line'].centery=60#25
rects['line'].left=60#26
rects['circle'].centerx=150#27
rects['circle'].centery=150#28
while True:#29
    for event in pygame.event.get():#30
        if event.type==pygame.locals.QUIT:#31
            pygame.quit()#32
            sys.exit()#33
    for rect in rects:#34
        rects[rect].right+=1#35
        if rects[rect].right>500:#36
            if rect=='line':#37
                rects['line'].centery=60#38
                rects['line'].left=60#39
            elif rect=='circle':#40
                rects['circle'].centerx=150#41
                rects['circle'].centery=150#42
            else:#43
                rects[rect].topleft=(0, 0)#44
    window.fill(WHITE)#45
    #window.blit(pentagon, rects['pentagon'])#46
    #window.blit(triangle, rects['triangle'])#47
    #window.blit(line, rects['line'])#48
    window.blit(circle, rects['circle'])#49
    pygame.time.Clock().tick(40)#50
    pygame.display.update()#51