from Screen import *
import numpy as np

class PixelGrid(GameObject):
    def __init__(self,size,dimensions,pos):
        self.size=iV(size)
        self.grid= np.ndarray(size,int)
        self.grid.fill(0)
        self.pos=pos
        self.dim=dimensions
        self.surface=None
        pass
    def Remove(self):
        pass
    def Init(self,scene):
        pass
    def Draw(self,canvas:ScaledCanvas):
        if self.surface:
            canvas.Blit(self.surface,self.pos,(self.dim))
    def Update(self,scene):
        pass
    def UpdateSurface(self):
        self.surface=pygame.Surface(self.size)
        self.surface.lock()
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.surface.set_at((x,y),(0,0,100*self.getPoint((x,y))))
        self.surface.unlock()
        
    def getPoint(self,pos):
        x,y = self.WarpInside(pos)
        a= self.grid[x,y]
        return a
    def setPoint(self,pos,value):
        x,y = self.WarpInside(pos)
        self.grid[x,y]=value
    def TransformPos(self,pos):
        x,y=(pos-self.pos)
        return V(x/self.dim.x*self.size[0],y/self.dim.y*self.size[1])
    def IsInside(self,pos):
        return (0<=pos[0]<self.size[0]) and (0<=pos[0]<self.size[0])
    def WarpInside(self,pos):
        return pos[0]%self.size[0],pos[1]%self.size[1]
    def FillGrid(self,value):
        self.grid.fill(value)
class Conway(PixelGrid):
    def Init(self,scene:Scene):
        self.run=True
    def Update(self,scene:Scene):
        u=False
        oldGrid =self.grid.copy()
        if self.run:
            u=True
            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    if True:
                        s=0
                        for p in (1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1):
                            ax,ay=self.WarpInside((x+p[0],y+p[1]))
                            if oldGrid[ax,ay]==True:
                                s+=1
                        if s==3:
                            self.setPoint((x,y),True)
                        elif s!=2:
                            self.setPoint((x,y),False)
                    else:
                        s=0
                        for p in (1,1),(-1,2),(0,1),(0,-1):
                            ax,ay=self.WarpInside((x+p[0],y+p[1]))
                            if oldGrid[ax,ay]==True:
                                s+=1
                        if s==1:
                            self.setPoint((x,y),True)
                        elif s==0:
                            self.setPoint((x,y),False)
        if scene.inputs.IsMousePressed(1):
            u=True
            pos=self.TransformPos(scene.inputs.GetMousePos())
            if self.IsInside(pos):
                self.setPoint(iV(pos),True)
        if scene.inputs.IsKeyDown(pygame.K_e):
            self.run = not self.run
        if scene.inputs.IsKeyDown(pygame.K_w):
            u=True
            self.FillGrid(0)
        if u:
            self.UpdateSurface()
        pass

a=Scene()
b=Display(V(800,800))
a.AddObject(Conway((64,64),V(8,8),V(-4,-4)))

b.Loop(a.ScreenUpdate)