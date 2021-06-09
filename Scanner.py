from Screen import *

from Shapes import *

class Obstacle(GameObject):
    def __init__(self,pos,radius):
        self.pos=pos
        self.radius=radius
        self.color=(100,0,50)
    def Draw(self,canvas:ScaledCanvas):
        canvas.DrawCircle(self.pos,self.color,self.radius)
    def Update(self,scene:Scene):
        pass
    def IntersectRay(self,ray):
        return ray.IntersectCircle(self.pos,self.radius)

class Turtle(GameObject):
    def __init__(self,pos,direction):
        self.pos=pos
        self.direction=direction
        self.color=(0,100,100)
        self.radius=1/4
        self.hits=[]
    def Draw(self,canvas:ScaledCanvas):
        canvas.DrawCircle(self.pos,self.color,self.radius)
        canvas.DrawLine(self.pos,self.pos+self.direction,self.color,self.radius/2)
        for h in self.hits:
            canvas.DrawCircle(h,self.color,1/16)
    def Update(self, scene:Scene):
        if scene.inputs.IsKeyPressed(pygame.K_d):
            self.pos+=(scene.inputs.GetMousePos()-self.pos).normalize()*scene.deltaTime/1000
        if scene.inputs.IsKeyPressed(pygame.K_a):
            self.direction+=(scene.inputs.GetMousePos()-self.pos-self.direction)*scene.deltaTime/500
        if scene.inputs.IsKeyPressed(pygame.K_s):
            possibleHits=[]
            for o in scene.objects:
                if isinstance(o,Obstacle):
                    hit=o.IntersectRay(Ray(self.pos,self.direction))
                    if hit:
                        possibleHits.extend(hit)
            if possibleHits:
                m=possibleHits[0]
                for h in possibleHits:
                    if self.direction.x==0:
                        if (m.y<h.y) == (self.direction.y<0):
                            m=h
                    else:
                        if (m.x<h.x) == (self.direction.x<0):
                            m=h
                self.hits.append(m)
        if scene.inputs.IsKeyPressed(pygame.K_w):
            self.hits.clear()

a=Scene()
b=Display(V(800,800))
#c=Obstacle(pos=V(1,-2),radius=1/2,color=(100,0,50))
#a.AddObject(c)
for i in range(16):
    o=Obstacle(
        V(i/4-1,0),
        1/8
    )
    a.AddObject(o)
a.AddObject(Turtle(V(-1,-2),V(0,1)))

# from PixelGrid import *

# a.AddObject(Conway((64,64),V(4,4),V(0,0)))

b.Loop(a.ScreenUpdate)