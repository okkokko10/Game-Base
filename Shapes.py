from Screen import *
from Transform import Transform
import math
def sign(x):
    return math.copysign(1,x)
class Shape:
    def Intersect(self,other):
        return []
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
    def IntersectCircle(self,circle,ancestor=None):
        'returns the points at which the circle intersects the line. returns None if it doesn\'t'
        assert isinstance(circle,Circle)
        tr=circle.transform.attach(self.transform,ancestor)
        D=tr.rot.lengthSq()-tr.pos.y**2
        if D>=0:
            sqrtD=D**0.5
            return self.DoesIntersect([Transform(V(tr.pos.x+sqrtD,0),V(1,0),self.transform),Transform(V(tr.pos.x-sqrtD,0),V(1,0),self.transform)])
        else: return []
    def IntersectLine(self,line,ancestor=None):
        'returns a list containing a single transform with the position at the intersection. Works with rays and line segments, and returns an empty list if the lines are parallel or do not intersect due to being line segments/rays'
        assert isinstance(line,Line)
        tr=line.transform.attach(self.transform,ancestor)
        px,py=tr.pos
        vx,vy=tr.rot
        if vy==0:
            return []
        out=Transform(V(px-py*vx/vy),V(1,0),self.transform)
        if self.DoesIntersectSingle(out) and line.DoesIntersectSingle(out.attach(tr,self.transform)):
            return [out]
        else: return []
    def DoesIntersect(self,l):
        return [t for t in l if self.DoesIntersectSingle(t)]
    def DoesIntersectSingle(self,t):
        'overridden by the subclasses Ray and LineSegment'
        return True
class Ray(Line):
    'a ray (half-line) starting at the origin and continuing along the x-axis in the positive x direction, transformed by its transform'
    def __init__(self,transform):
        super().__init__(transform)
    def DoesIntersectSingle(self, t):
        return 0<=t.pos.x
class LineSegment(Line):
    'a line segment between the origin and the point (1,0), transformed by its transform'
    def __init__(self,transform):
        super().__init__(transform)
    def DoesIntersectSingle(self, t):
        return 0<=t.pos.x<=1

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

class Polygon(Shape):
    def __init__(self,transform,points):
        self.transform=transform
        self.points=points
        self.genLines()
    def genLines(self):
        self.lines=[]
        for i in len(self.points):
            self.lines.append(
            LineSegment(
            Transform(
            self.points[i],
            self.points[i-1]-self.points[i],
            self.transform
            )))
    def IsInside(self,transform):
        'inverted if the origin is outside. is not yet foolproof.'
        assert isinstance(transform,Transform)
        tr = transform.attach(self.transform)
        between=LineSegment(Transform(V(0,0),tr.pos,self.transform))
        passes=0
        for s in self.lines:
            assert isinstance(s,LineSegment)
            passes+= bool(s.IntersectLine(between,self.transform))
        if passes&1:
            return False
        else:
            return True
    def Intersect(self, other):
        out=[]
        indices=[]
        for i in range(len(self.lines)):
            a=self.lines[i].Intersect(other)
            if a:
                out+=a
        return out

