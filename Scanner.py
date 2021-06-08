from Screen import *


class Ray:
    def __init__(self,origin,direction):
        self.origin=origin
        self.vector=direction
    def IntersectNormal(self,center):
        return self.IntersectNormalRelative(center - self.origin)+self.origin
    def IntersectNormalRelative(self,difference):
        #x=\frac{v.x\cdot v.y}{v.y^2+v.x^2}\cdot \left(c.y-o.y\right)+c.x+\frac{v.y^2}{v.y^2+v.x^2}\cdot \left(o.x-c.x\right)
            #y=\frac{v.y}{v.x}\left(x-o.x\right)+o.y
            #x-o.x=\frac{v.x\cdot v.y}{v.y^2+v.x^2}\cdot d.y+\frac{v.x^2}{v.y^2+v.x^2}\cdot d.x
            #y-o.y=\frac{v.y}{v.x}\left(x-o.x\right)
        vx,vy=self.vector
        mul = vx/(vy*vy+vx*vx)
        x = mul *(vy*difference.y+vx*difference.x)
        y= x*vy/vx
        return x,y
    def IntersectCircleRelative(self,difference,radius):
        #y=\frac{v.y}{v.x}x
            #\frac{x=c.x+c.y\frac{v.y}{v.x}\pm \sqrt{\left(c.x+c.y\frac{v.y}{v.x}\right)^2-\left(\left(\frac{v.y}{v.x}\right)^2+1\right)\cdot \left(-R^2+c.y^2+c.x^2\right)}}{\left(\frac{v.y}{v.x}\right)^2+1}
        vx,vy=self.vector
        cx,cy=difference
        k = vy/vx
        a=k**2 +1
        b=cx+cy*k
        # c=cx**2+cy**2-radius**2
        # D=b**2 -a*c
        D=radius**2 *a -(cy-cx*k)**2
        if D>=0:
            sqrtD=D**0.5
            x1 = (b + sqrtD)/a
            x2 = (b - sqrtD)/a
            y1 = k*x1
            y2 = k*x2
            return (x1,y1),(x2,y2)
        else:
            return None
    def IntersectCircle(self,center,radius):
        return self.IntersectCircleRelative(center-self.origin,radius)+self.origin


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
    def Draw(self,canvas:ScaledCanvas):
        canvas.DrawCircle(self.pos,self.color,self.radius)
        canvas.DrawLine(self.pos,self.pos+self.direction,self.color,self.radius)
    def Update(self, scene:Scene):
        
        if pygame.K_d in scene.keysDown:
            self.pos+=V(1,0)

a=Scene()
b=Display(V(900,800))
#c=Obstacle(pos=V(1,-2),radius=1/2,color=(100,0,50))
#a.AddObject(c)
a.AddObject(Turtle(V(-1,-2),V(0,1)))
for i in range(8):
    o=Obstacle(
        V(i/4-1,0),
        1/8
    )
    a.AddObject(o)

b.Loop(a.ScreenUpdate)