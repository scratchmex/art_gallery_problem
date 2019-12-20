import pygame
import main

def drawVertex(c, r, w, h, color=(0,0,0)):
    radius=int(min((w, h))/2)

    screen=pygame.display.get_surface()
    pygame.draw.circle(screen,
                        color, 
                        (c,r),
                        radius
                    )

def drawEdge(v1, v2, thickness=1, color=(0,0,0)):
    screen=pygame.display.get_surface()
    pygame.draw.line(screen, color, v1, v2, thickness)

class Window:
    def __init__(self,
                 SCREEN_WIDTH = 800,
                 SCREEN_HEIGHT = 800):

        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        self.cols=SCREEN_WIDTH//6
        self.rows=SCREEN_HEIGHT//6

        self.w=self.SCREEN_WIDTH/self.cols
        self.h=self.SCREEN_HEIGHT/self.rows

        self.grid = [[0 for c in range(self.cols)] 
                        for r in range(self.rows)]

        self.vertices=[]

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Seleccione los vértices de un polígono simple COUNTER-CLOCKWISE!!")
        self.screen.fill((230,230,230))

        pygame.display.flip()

    def xy_to_grid(self, x, y):
        c = int(x // self.w)
        r = int(y // self.h)

        return (c,r)

    def xy_to_cr(self, x, y):
        c = int(x // self.w)
        r = int(y // self.h)

        return (int(c*self.w+self.w/2), int(r*self.h+self.h/2))

    def onClick(self, pos):
        x,y=pos
        c = int(x // self.w)
        r = int(y // self.h)
        # print(f'({y,x})->{r,c}')

        color=(0,0,0)
        thickness=2

        if len(self.vertices)==0:
            color=(255,0,0)
        elif self.xy_to_grid(*self.vertices[0])==(c,r):
            #the polygon is closed
            v1=self.xy_to_cr(*self.vertices[-1])
            v2=self.xy_to_cr(*self.vertices[0])
            drawEdge(v1, v2, thickness=thickness)
            pygame.display.set_caption('Poligono cerrado! Triangulando y viendo guardias...')
            
            #call main algorithm
            edges,guards,min_color=main.main(self.vertices)

            for edge in edges:
                v1, v2=self.xy_to_cr(*edge[0]), self.xy_to_cr(*edge[1])
                drawEdge(v1, v2, color=(0,0,255))

                pygame.display.update()
                pygame.time.wait(200)

            for color,guard in guards:
                v=self.xy_to_cr(*guard)
                drawVertex(*v, 10, 10, color=color)
            pygame.display.update()
            pygame.display.set_caption(f'El color de los guardias óptimos es {min_color}')

            return 1

        if self.grid[r][c] != 0:
            return 0

        drawVertex(*self.xy_to_cr(x,y), self.w, self.h, color=color)
        self.grid[r][c]=1

        if len(self.vertices)>=1:
            v2=self.xy_to_cr(*self.vertices[-1])
            drawEdge(self.xy_to_cr(x,y), v2, thickness=thickness)

        self.vertices.append((x,y))

        return 0
        
    def mainloop(self):#main loop
        running=True
        drawing=True
        while running:
            # Posibles entradas del teclado y mouse
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False
                    break

                if pygame.mouse.get_pressed()[0] and drawing:
                    try:
                        pos = pygame.mouse.get_pos()
                        stat=self.onClick(pos)
                        if stat==1:
                            drawing=False

                    except AttributeError:
                        pass

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    w=Window()
    w.mainloop()