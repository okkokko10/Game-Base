import pygame

def V(x,y):
    return pygame.Vector2(x,y)
def Vi(v):
    return pygame.Vector2(v)
def iV(v):
    return int(v[0]),int(v[1])
    

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
    def Blit(self,source,dest):
        self.surface.blit(source,iV(dest))

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
    def Blit(self,source,dest,size):
        self.canvas.Blit(pygame.transform.scale(source,iV(size*self.zoom)),self.TransformPos(dest))
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
    def __init__(self,canvas=None):
        if canvas:
            self.canvas=canvas
        else:
            self.canvas=ScaledCanvas(V(800,800),V(0,0),100)
        self.objects=set()
        self.deltaTime=0
        self.globalMethods=set()
        self.events=[]
        self.inputs=Inputs()
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
        self.inputs.Update(self)
        pass
class Inputs:
    def __init__(self):
        self.keysDown={}
        self.mousePosScreen=V(0,0)
        self.mousePos=V(0,0)
        self.mouseButtonsDown={}
    def Update(self,scene):
        self._UpdateKeys()
        self._UpdateMouse()
        for e in scene.events:
            if e.type == pygame.KEYDOWN:
                self._KeyDown(e.__dict__['key'])
            elif e.type == pygame.KEYUP:
                self._KeyUp(e.__dict__['key'])
            elif e.type in (pygame.MOUSEMOTION,pygame.MOUSEBUTTONUP,pygame.MOUSEBUTTONDOWN):
                x,y=e.__dict__['pos']
                self.mousePosScreen=V(x,y)
                self.mousePos=scene.canvas.InverseTransformPos(self.mousePosScreen)
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self._MouseDown(e.__dict__['button'])
                elif e.type == pygame.MOUSEBUTTONUP:
                    self._MouseUp(e.__dict__['button'])
    def IsKeyPressed(self,key):
        if key in self.keysDown:
            if self.keysDown[key]&4:
                return True
        return False
    def IsKeyDown(self,key):
        if key in self.keysDown:
            if self.keysDown[key]&1:
                return True
        return False
    def IsKeyUp(self,key):
        if key in self.keysDown:
            if self.keysDown[key]&2:
                return True
        return False
    def _KeyUp(self,key):
        self.keysDown[key]|=2 #x1x
    def _KeyDown(self,key):
        self.keysDown[key]=5 #101
    def _UpdateKeys(self):
        remove=[]
        for k in self.keysDown:
            self.keysDown[k] &= 6 #110
            if self.keysDown[k]&2:
                self.keysDown[k] &= 3 #011
                remove.append(k)
        for k in remove:
            del self.keysDown[k]
    def IsMousePressed(self,key):
        if key in self.mouseButtonsDown:
            if self.mouseButtonsDown[key]&4:
                return True
        return False
    def IsMouseDown(self,key):
        if key in self.mouseButtonsDown:
            if self.mouseButtonsDown[key]&1:
                return True
        return False
    def IsMouseUp(self,key):
        if key in self.mouseButtonsDown:
            if self.mouseButtonsDown[key]&2:
                return True
        return False
    def _MouseUp(self,key):
        self.mouseButtonsDown[key]|=2
    def _MouseDown(self,key):
        self.mouseButtonsDown[key]=5
    def _UpdateMouse(self):
        remove=[]
        for k in self.mouseButtonsDown:
            self.mouseButtonsDown[k]&=6
            if self.mouseButtonsDown[k]&2:
                self.mouseButtonsDown[k] &= 3
                remove.append(k)
        for k in remove:
            del self.mouseButtonsDown[k]
    def GetMousePos(self):
        return self.mousePos
    def GetTrueMousePos(self):
        return self.mousePosScreen

