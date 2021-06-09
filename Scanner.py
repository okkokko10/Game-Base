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
    def IntersectCircleRelative(self,difference,radius,behind=False):
        #y=\frac{v.y}{v.x}x
            #\frac{x=c.x+c.y\frac{v.y}{v.x}\pm \sqrt{\left(c.x+c.y\frac{v.y}{v.x}\right)^2-\left(\left(\frac{v.y}{v.x}\right)^2+1\right)\cdot \left(-R^2+c.y^2+c.x^2\right)}}{\left(\frac{v.y}{v.x}\right)^2+1}
        vx,vy=self.vector
        cx,cy=difference
        if vx == 0:
            D=radius**2-cx**2
            if D>=0:
                sqrtD=D**0.5
                y1=cy+sqrtD
                y2=cy-sqrtD
                out=[]
                if y1*vy>=0 or behind:
                    out.append(V(0,y1))
                if y2*vy>=0 or behind:
                    out.append(V(0,y2))
                if vy<0:
                    return out
                else:
                    return reversed(out)
            else:
                return None
                
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
            out=[]
            if x1*vx>=0 or behind:
                out.append(V(x1,y1))
            if x2*vx>=0 or behind:
                out.append(V(x2,y2))
            if vx>0:
                return out
            else:
                return reversed(out)
        else:
            return None
    def IntersectCircle(self,center,radius,behind=False):
        out = self.IntersectCircleRelative(center-self.origin,radius,behind)
        if out:
            return map(lambda x: x+self.origin,out)
        else:
            return None


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
            self.pos+=(scene.mousePos-self.pos).normalize()*scene.deltaTime/1000
        if scene.inputs.IsKeyPressed(pygame.K_a):
            self.direction+=(scene.mousePos-self.pos-self.direction)*scene.deltaTime/500
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
b=Display(V(900,800))
#c=Obstacle(pos=V(1,-2),radius=1/2,color=(100,0,50))
#a.AddObject(c)
for i in range(16):
    o=Obstacle(
        V(i/4-1,0),
        1/8
    )
    a.AddObject(o)
a.AddObject(Turtle(V(-1,-2),V(0,1)))

b.Loop(a.ScreenUpdate)