from ShapeDraw import *

class ChopPolygon(Polygon):
    def Cut(self,line:Line):
        newVertices=[]
        indices=[]
        indices1=[]
        for i in range(len(self.lines)):
            newVertices.append(self.lines[i].transform)
            indices.append(0)
            a = self.lines[i].IntersectLine(line)
            if a:
                indices1.append(len(indices))
                indices.append(1)
                b=a[0]
                newVertices.append(b)
        if indices1<=2:
            return [self]
        def sortkey(k):
            return newVertices[k].pos.x
        indices2=sorted(indices1,sortkey)
        for i in range(len(indices2)):
            indices[indices2[i]]=i+1
        
        groups=[[]]
        for i in range(len(indices)):
            groups[-1].append(i)
            if indices[i]:
                groups.append([i])
        if len(groups)>1:
            groups[0]=groups[-1]+groups[0]
            del groups[-1]

            def opposite(e):
                return e-1+2*(e&1)
            def continuation(e):
                a=opposite(indices[e[-1]])
                for i in range(len(groups)):
                    if indices[groups[i][0]]==a:
                        return i
            links=[]
            for k in groups:
                links.append([continuation(k),True])
            linked=[]
            for i in range(len(links)):
                if links[i][1]:
                    linked.append([])
                i=a
                while links[a][1]:
                    linked[-1].append(a)
                    links[a][1]=False
                    a=links[a][0]
            cutGroups=[]
            for i in range(len(linked)):
                cutGroups.append([])
                for k in linked[i]:
                    cutGroups[-1].extend(groups[k])
            groups = cutGroups
        
        groupVertices=[]
        for k in groups:
            groupVertices.append([])
            for k1 in k:
                v=newVertices[k1].detach(self.transform)
                groupVertices[-1].append(v.pos)
        newPolygons=[]
        for k in groupVertices:
            newPolygons.append(ChopPolygon(self.transform.copy(),groupVertices))
        return newPolygons
class ChopPolygonGameObject(ShapeObject):
    def __init__(self, polygon,color):
        self.shape=polygon
        self.color=color
    def Update(self, scene):
        return super().Update(scene)

if __name__=='__main__':
    tr=Transform(V(0,0),V(1/100,0))
    a=Scene(TrCanvas(V(800,800),tr))
    b=Display(V(800,800))
    col=(100,100,100)
    a.AddObject(ShapeObject(Circle(Transform(V(1,1),V(1,0))),col))
    a.AddObject(ShapeObject(LineSegment(Transform(V(2,1),V(1,0))),col))
    a.AddObject(MoveCamera())

    b.Loop(a.ScreenUpdate)        
        


