from Screen import *
from Shapes import *
from TransformCanvas import *
from GetTextures import GetTexture
class C_DrawShape(Component):
    active:bool
    def __init__(self,shape,color):
        self.shape=shape
        self.color=color
        super().__init__()
    def O_OnDraw(self,canvas):
        if isinstance(self.shape,Circle):
            canvas.DrawCircle(self.shape.transform,self.color)
        elif isinstance(self.shape,Line):
            canvas.DrawLine(self.shape.transform,self.color)
        elif isinstance(self.shape,Polygon):
            for line in self.shape.lines:
                canvas.DrawLine(line.transform,self.color)
        super().O_OnDraw(canvas)
class C_DrawTexture(Component):
    def __init__(self,transform,number) -> None:
        self.number=number
        self.transform=transform
        super().__init__()
    def O_OnDraw(self, canvas:TrCanvas):
        canvas.DrawSurface(GetTexture(self.number),self.transform)
        return super().O_OnDraw(canvas)
    pass
# if __name__=='__main__':
#     tr=Transform(V(0,0),V(1/100,0))
#     a=Scene(TrCanvas(V(800,800),tr))
#     b=Display(V(800,800))
#     col=(100,100,100)
#     a.AddObject(ShapeObject(Circle(Transform(V(1,1),V(1,0))),col))
#     a.AddObject(ShapeObject(LineSegment(Transform(V(2,1),V(1,0))),col))
#     a.AddObject(MoveCamera())

#     b.Loop(a.ScreenUpdate)