from Screen import *


class Shape:
    def Intersect(self,other):
        pass
    pass

class Rect:
    def __init__(self,x1,y1,x2,y2):
        self.x1,self.x2=sorted(x1,x2)
        self.y1,self.y2=sorted(y1,y2)
        self.corner1=V(self.x1,self.y1)
        self.corner2=V(self.x2,self.y2)
        pass
    def IntersectRect(self,rect,getResult=True):
        if self.x1<rect.x2 and rect.x1<self.x2 and self.y1<rect.y2 and rect.y1<self.y2:
            if getResult:
                return Rect(max(self.x1,rect.x1),max(self.y1,rect.y1),min(self.x2,rect.x2),min(self.y2,rect.y2))
            else:
                return True
        else:
            return None
    def __and__(self,other):
        return self.IntersectRect(other,True)
        


class Ray(Shape):
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

class Circle(Shape):
    def __init__(self,center,radius):
        self.center=center
        self.radius=radius
    def IntersectRay(self,ray:Ray):
        ray.IntersectCircle(self.center,self.radius,True)
    pass