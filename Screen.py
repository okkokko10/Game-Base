import pygame

def V(x,y):
    return pygame.Vector2(x,y)
def iV(v):
    return int(v.x),int(v.y)

class Display:
    def __init__(self,size):
        self.canvas = pygame.display.set_mode(iV(size))
    def Update(self,surface):
        self.canvas.blit(surface,V(0,0))
        pygame.display.update()
    def Loop(self,function,speed=50):
        """function(events,deltaTime) -> surface"""
        while True:
            d=pygame.time.wait(speed)
            if pygame.event.get(pygame.QUIT):
                return
            events = pygame.event.get()
            out = function(events,d)
            self.Update(out)
        
class Canvas:
    def __init__(self,size):
        self.surface=pygame.Surface(size)
    def DrawCircle(self,pos,color,radius):
        pygame.draw.circle(self.surface,color,iV(pos),int(radius))
    def DrawLine(self,posA,posB,color,width):
        pygame.draw.line(self.surface,color,iV(posA),iV(posB),int(width))
    def Fill(self,color):
        self.surface.fill(color)

class ScaledCanvas:
    def __init__(self,size,center,zoom):
        self.canvas=Canvas(size)
        self.size=size
        self.center=center
        self.zoom=zoom
    def GetSurface(self):
        return self.canvas.surface
    def TransformPos(self,pos):
        return self.zoom*(pos-self.center)+self.size/2
    def TransformScale(self,length):
        return self.zoom*length
    def InverseTransformPos(self,pos):
        return self.center+(pos-self.size/2)/self.zoom
    def InverseTransformScale(self,length):
        return length/self.zoom
    def DrawCircle(self,pos,color,radius):
        self.canvas.DrawCircle(self.TransformPos(pos),color,self.TransformScale(radius))
        pass
    def DrawLine(self,posA,posB,color,width):
        self.canvas.DrawLine(self.TransformPos(posA),self.TransformPos(posB),color,self.TransformScale(width))
    def Fill(self,color):
        self.canvas.Fill(color)
    def SetCenter(self,pos):
        self.center=pos
    def SetZoom(self,zoom):
        self.zoom=zoom
    def GetCenter(self):
        return self.center
    def GetZoom(self):
        return self.zoom

class GameObject:
    active:bool
    def __init__(self,*args):
        pass
    def Remove(self):
        pass
    def Init(self,scene):
        pass
    def Draw(self,canvas:ScaledCanvas):
        pass
    def Update(self,scene):
        pass

class Scene:
    def __init__(self):
        self.canvas=ScaledCanvas(V(800,800),V(0,0),100)
        self.objects=set()
        self.deltaTime=0
        self.globalMethods=set()
        self.events=[]
        self.keysDown=set()
        self.mousePosScreen=V(0,0)
        self.mousePos=V(0,0)
        self.mouseButtonsDown=set()
        pass
    def AddObject(self,gameObject):
        gameObject.active=True
        self.objects.add(gameObject)
        gameObject.Init(self)
    def ScreenUpdate(self,events,deltaTime):
        self.events=events
        self.deltaTime=deltaTime
        self.UpdateInputs()
        self.canvas.Fill((0,100,0))
        for f in self.globalMethods:
            f(self)
        for o in self.objects:
            o.Update(self)
            o.Draw(self.canvas)

        return self.canvas.GetSurface()
    def UpdateInputs(self):
        for e in self.events:
            if e.type == pygame.KEYDOWN:
                self.keysDown.add(e.__dict__['key'])
            elif e.type == pygame.KEYUP:
                self.keysDown.discard(e.__dict__['key'])
            elif e.type in (pygame.MOUSEMOTION,pygame.MOUSEBUTTONUP,pygame.MOUSEBUTTONDOWN):
                x,y=e.__dict__['pos']
                self.mousePosScreen=V(x,y)
                self.mousePos=self.canvas.InverseTransformPos(self.mousePosScreen)
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.mouseButtonsDown.add(e.__dict__['button'])
                elif e.type == pygame.MOUSEBUTTONUP:
                    self.mouseButtonsDown.discard(e.__dict__['button'])
