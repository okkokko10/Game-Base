from ComplexVector import CompVec
from Shapes import *
from Screen import *
class TrCanvas:
    def __init__(self,size,transform,surface=None):
        self.canvas=Canvas(size,surface)
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
    def DrawSurface(self,source,transform:Transform):
        '''center is NYI'''
        tr=transform.attach(self.transform)
        angle=pygame.Vector2(tr.rot.x,tr.rot.y).angle_to(pygame.Vector2(1,0))
        out=pygame.transform.rotozoom(source,angle,abs(tr.rot))
        self.canvas.Blit(out,tr.pos+Vi(self.canvas.surface.get_size())/2-Vi(out.get_size())/2)
        pass
    def SetSurface(self,surface):
        self.canvas.surface=surface
class C_inputMove(Component):
    def O_OnUpdate(self):
        super().O_OnUpdate()
        tr=self.gameObject.GetComponent(C_Position).transform
        scene=self.gameObject.scene
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

class C_Camera(Component):
    def __init__(self,transform,size) -> None:
        self.transform=transform
        self.size=size
        super().__init__()
    def O_OnInit(self):
        trCanvas=TrCanvas(self.size,self.transform.detach())
        #trCanvas.canvas.surface=self.gameObject.scene.display.canvas
        self.gameObject.scene.canvas=trCanvas
        return super().O_OnInit()
    def O_OnUpdate(self):
        self.gameObject.scene.canvas.transform.Become(self.transform.detach())
        return super().O_OnUpdate()