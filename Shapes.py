from Screen import *
import math
def sign(x):
    return math.copysign(1,x)
class Shape:
    def Intersect(self,other):
        pass
    pass

'''
TODO:
Circle
basic rectangle
line
ray
line segment
combining shapes with | and &
finding intersections with &
rotation
world-local coordinate, scale and rotation transformation, like in Unity
arbitrary polygons

change all position vectors to transforms
fold line's direction vector and circle's radius into their transform's rotation

'''

class Rect(Shape):
    def __init__(self,x1,y1,x2,y2):
        self.x1,self.x2=sorted(x1,x2)
        self.y1,self.y2=sorted(y1,y2)
        self.edges=self.x1,self.y1,self.x2,self.y2
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
    @staticmethod
    def FromVectorPair(a,b):
        return Rect(a.x,a.y,b.x,b.y)
        

class Line(Shape):
    def __init__(self,origin,vector):
        self.origin=origin
        self.vector=vector
    @staticmethod
    def FromPointPair(a,b):
        return Line(a,b-a)        
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
    def IntersectCircleRelative(self,difference,radius,behind=True):
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
    def IntersectCircle(self,circle,behind=False):
        out = self.IntersectCircleRelative(circle.center-self.origin,circle.radius,behind)
        if out:
            return map(lambda x: x+self.origin,out)
        else:
            return None
    def IntersectRect(self,rect:Rect):
        x1,y1,x2,y2 = map(lambda x: x-self.origin,rect.edges)
        l=[]
        vx,vy=self.vector
        if x1*abs(vy)<y1*vx*sign(vy)<=x2*abs(vy):
            l.append(y1*V(vx/vy,1))
            pass
        if x1*abs(vy)<=y2*vx*sign(vy)<x2*abs(vy):
            l.append(y2*V(vx/vy,1))
            pass
        if y1*abs(vx)<=x1*vy*sign(vx)<y2*abs(vx):
            l.append(x1*V(1,vy/vx))
        if y1*abs(vx)<x2*vy*sign(vx)<=y2*abs(vx):
            l.append(x2*V(1,vy/vx))

        if len(l)==2:
            return LineSegment(l[0]+self.origin,l[1]+self.origin)
        else:
            return None
class Ray(Line):
    def __init__(self,origin,vector):
        super().__init__(origin,vector)
class LineSegment(Line):
    def __init__(self, pointA, pointB):
        super().__init__(pointA, pointB-pointA)
        self.rect=Rect.FromVectorPair(pointA,pointB)

class Circle(Shape):
    def __init__(self,transform,radius):
        self.center=transform
        self.radius=radius
    def IntersectLine(self,line):
        line.IntersectCircle(self.center,self.radius,True)
    def IsInside(self,transform):
        return self.radius <= self.center.distance(transform)
    pass

class Transform:
    def __init__(self,pos:cv,rot:cv,parent=None):
        self.parent=parent
        self.pos=pos
        self.rot=rot
    def detachOnce(self):
        return Transform(self.parent.pos+self.pos*self.parent.rot,self.rot*self.parent.rot,self.parent.parent)
    def detach(self,until=None): #probably needs optimization idk
        c = self
        while c.parent!=until:
            #assert c.parent!=None
            c = c.detachOnce()
        return c
    def Become(self,other):
        self.__dict__=other.__dict__
    def copy(self):
        return Transform(self.pos,self.rot,self.parent)
    def distance(self,other,ancestor=None):
        return abs(other.attach(self).pos)
    def attach(self,other,ancestor=None):
        'changes parent to other without changing the world coordinates'
        unattached=self.detach(ancestor)
        parent=other.detach(ancestor)
        # unattached.pos = parent.pos+self.pos*parent.rot
        # unattached.rot = self.rot*parent.rot
        # unattached.parent = parent.parent
        return Transform(
        (unattached.pos - parent.pos)/parent.rot,
        unattached.rot/parent.rot,
        other)
    def commonAncestor(self,other,until=None):
        sFT=self.familyTree(until)
        oFT=other.familyTree(until)
        for i in len(sFT):
            if sFT[i] in oFT:
                #oFT.index(sFT[i])
                return sFT[i]
    def familyTree(self,until=None):
        l=[self.parent]
        while l[-1]!=until:
            #assert c.parent!=None
            l.append(l[-1].parent)
        return l


class Combination:
    def __init__(self):
        pass
    def IsInside(self,transform) -> bool:
        return 
class C_union(Combination):
    def __init__(self,shapes):
        self.shapes=shapes