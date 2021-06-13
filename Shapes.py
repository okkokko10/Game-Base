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
--fold line's direction vector and circle's radius into their transform's rotation

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
        

class LineOld(Shape):
    def __init__(self,transform):
        self.transform=transform
        self.origin
        self.vector
    @staticmethod
    def FromPointPair(a,b):
        return Line(Transform(a,b-a,None))

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

class Line(Shape):
    'a line going along the x-axis, transformed by its transform'
    def __init__(self,transform):
        assert isinstance(transform,Transform)
        self.transform=transform
    def IntersectNormal(self,transform):
        'basically just projects the input onto the line'
        assert isinstance(transform,Transform)
        tr=transform.attach(self.transform)
        tr.pos=V(tr.pos.x,0)
        return self.DoesIntersect([tr])
    def IntersectCircle(self,circle):
        'returns the points at which the circle intersects the line. returns None if it doesn\'t'
        assert isinstance(circle,Circle)
        tr=circle.transform.attach(self.transform)
        D=tr.rot.lengthSq()-tr.pos.y**2
        if D>=0:
            sqrtD=D**0.5
            return self.DoesIntersect([Transform(V(tr.pos.x+sqrtD,0),V(1,0),self.transform),Transform(V(tr.pos.x-sqrtD,0),V(1,0),self.transform)])
        else: return []
    def DoesIntersect(self,l):
        'overridden by the subclasses Ray and LineSegment'
        return l
class Ray(Line):
    'a ray (half-line) starting at the origin and continuing along the x-axis in the positive x direction, transformed by its transform'
    def __init__(self,transform):
        super().__init__(transform)
    def DoesIntersect(self, l):
        out = []
        for i in l:
            if 0<=i.pos.x:
                out.append(i)
        return out
class LineSegment(Line):
    'a line segment between the origin and the point (1,0), transformed by its transform'
    def __init__(self,transform):
        super().__init__(transform)
    def DoesIntersect(self, l):
        out = []
        for i in l:
            if 0<=i.pos.x<=1:
                out.append(i)
        return out

class Circle(Shape):
    'a circle with its center at the origin and its radius 1, transformed by its transform'
    def __init__(self,transform):
        assert isinstance(transform,Transform)
        self.transform=transform
    # def IntersectLine(self,line):
    #     line.IntersectCircle(self.transform,self.radius,True)
    def IsInside(self,transform):
        return self.transform.distance(transform) <= 1
    pass

class Transform:
    def __init__(self,pos:cv,rot:cv,parent=None):
        self.parent=parent
        self.pos=pos
        self.rot=rot
        self.world=None
    def detachFrom(self,parent):
        return Transform(parent.pos+self.pos*parent.rot,self.rot*parent.rot,parent.parent)
    def detachOnce(self):
        return self.detachFrom(self.parent)
    def detach(self,until=None): #probably needs optimization idk
        'gets the transform\'s world coordinates'
        c = self
        while c.parent!=until:
            c = c.detachOnce()
        return c
    def getWorld(self):
        'gets the transform\'s world coordinates. Also saves them for optimization purposes. \n WARNING: must be reset after an ancestor has moved.'
        if not self.world:
            if self.parent:
                self.world = self.detachFrom(self.parent.getWorld())
            else:
                self.world = self
        return self.world
    def Become(self,other):
        self.__dict__=other.__dict__
    def copy(self):
        return Transform(self.pos,self.rot,self.parent)
    def distance(self,other,ancestor=None):
        return abs(other.attach(self).pos)
    def attach(self,newParent,ancestor=None):
        'returns a new transform that has identical world coordinates but has newParent as parent'
        unattached=self.detach(ancestor)
        parent=newParent.detach(ancestor)
        # unattached.pos = parent.pos+self.pos*parent.rot
        # unattached.rot = self.rot*parent.rot
        # unattached.parent = parent.parent
        return Transform(
        (unattached.pos - parent.pos)/parent.rot,
        unattached.rot/parent.rot,
        newParent)
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