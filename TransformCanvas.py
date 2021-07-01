from Shapes import *
from Screen import *

class TrCanvas:
    def __init__(self,size,transform):
        self.canvas=Canvas(size)
        self.offset=Vi(size)/2
        assert isinstance(transform,Transform)
        self.transform = transform
    def DrawCircle(self,transform,color):
        tr=transform.attach(self.transform)
        self.canvas.DrawCircle(tr.pos+self.offset,color,abs(tr.rot))
    def DrawLine(self,transform,color):
        tr=transform.attach(self.transform)
        self.canvas.DrawLine(tr.pos+self.offset,tr.pos+tr.rot+self.offset,color,abs(tr.rot)/10)
    def InverseTransformPos(self,pos:cv):
        tr=Transform(pos-self.offset,V(1,0),self.transform)
        return tr
    def GetSurface(self):
        return self.canvas.surface
    def Fill(self,color):
        self.canvas.Fill(color)
        pass
    def Blit(self,source,destTransform):
        self.canvas.Blit(source,destTransform.attach(self.transform).pos)

class MoveCamera(GameObject):
    def Update(self):
        scene=self.scene
        tr=scene.canvas.transform
        if scene.inputs.IsKeyPressed(pygame.K_a):
            tr.pos+=tr.rot*V(-10,0)
        elif scene.inputs.IsKeyPressed(pygame.K_d):
            tr.pos+=tr.rot*V(10,0)
        if scene.inputs.IsKeyPressed(pygame.K_w):
            tr.pos+=tr.rot*V(0,-10)
        elif scene.inputs.IsKeyPressed(pygame.K_s):
            tr.pos+=tr.rot*V(0,10)
        if scene.inputs.IsKeyPressed(pygame.K_q):
            tr.rot*=V(1,0.1)
        elif scene.inputs.IsKeyPressed(pygame.K_e):
            tr.rot*=1/V(1,0.1)
        if scene.inputs.IsKeyPressed(pygame.K_r):
            tr.rot*=1.1
        elif scene.inputs.IsKeyPressed(pygame.K_f):
            tr.rot/=1.1