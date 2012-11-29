from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty
from kivy.factory import Factory
from kivy.graphics import Color, Ellipse, Line
from kivy.clock import Clock


class LineInfo:
    def __init__(self,axes,data,hue):
        self.axes=axes
        self.data=data
        self.color=Color(hue, 1, 1, mode='hsv')
        self.line=Line(points=self.compute_points(), width=2)
            
        axes.canvas.insert(axes.canvas.length()-1,self.line)
        axes.canvas.insert(axes.canvas.length()-1,self.color)
    def compute_points(self):
        pts=[]
        miny=self.axes.min_y
        maxy=self.axes.max_y
        for i,d in enumerate(self.data):
            x=float(i)/(len(self.data)-1)*(self.axes.width) + self.axes.x        
            y=(d-miny)/(maxy-miny)*self.axes.height + self.axes.y
            pts.extend((x,y))
        return pts
    def recompute(self):
        self.line.points=self.compute_points()
    def remove(self):
        self.axes.canvas.remove(self.line)    
        self.axes.canvas.remove(self.color)
        
    

class Axes(Widget):
    min_y = NumericProperty(0)
    max_y = NumericProperty(10)
    
    def __init__(self, **kwargs):
        super(Axes, self).__init__(**kwargs)
        self.lines = []
        Clock.schedule_interval(self.do_fade, 1.0/10)
        self.bind(size=self.recompute_lines)
        
    def plot(self, data, hue):
        self.lines.append(LineInfo(self, data, hue))
        
    def recompute_lines(self,width,height):
        for line in self.lines:
            line.recompute()
    
        
    def do_fade(self,dt):
        for line in self.lines[:-2]:
            line.color.s-=0.1
        while len(self.lines)>0 and self.lines[0].color.s<0.05:
            self.canvas.remove(self.lines[0].line)
            self.canvas.remove(self.lines[0].color)
            del self.lines[0]
        
        
        
Factory.register('Axes', Axes)            


class Plotter(Widget):
    pass

Factory.register('Plotter', Plotter)            
    
