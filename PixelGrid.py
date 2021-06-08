from Screen import *
import numpy as np

class PixelGrid(GameObject):
    def __init__(self,size):
        self.size=size
        self.grid= np.ndarray(size,bool)
        self.grid.fill(False)
        print(self.grid)
        pass
    def Remove(self):
        pass
    def Init(self,scene):
        pass
    def Draw(self,canvas:ScaledCanvas):
        surf=pygame.Surface(self.size)
        surf.lock()
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                surf.set_at((x,y),(0,0,100*self.getPoint((x,y))))
        surf.unlock()
        canvas.Blit(surf,V(-3,-3),V(5,5))
    def Update(self,scene):
        pass
    def getPoint(self,pos):
        a= self.grid[pos[0]%self.size[0],pos[1]%self.size[1]]
        return a
    def setPoint(self,pos,value):
        self.grid[pos[0]%self.size[0],pos[1]%self.size[1]]=value
class Conway(PixelGrid):
    def Init(self,scene:Scene):
        self.setPoint((5,5),1)
        self.setPoint((5,6),1)
        self.setPoint((4,5),1)
        self.setPoint((6,5),1)
    def Update(self,scene:Scene):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                s=0
                for p in (1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1):
                    if self.getPoint((x+p[0],y+p[1]))==True:
                        s+=1
                if s==3:
                    self.setPoint((x,y),True)
                elif s!=2:
                    self.setPoint((x,y),False)
        pass

a=Scene()
b=Display(V(800,800))
a.AddObject(Conway((10,10)))

b.Loop(a.ScreenUpdate)