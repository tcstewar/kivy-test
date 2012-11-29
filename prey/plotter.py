from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty
from kivy.factory import Factory
from kivy.graphics import Color, Ellipse, Line
from kivy.clock import Clock


class LineInfo:
    def __init__(self,axes,data,hue):
        self.removed=False
        self.axes=axes
        self.data=data
        self.color=Color(hue, 1, 1, 0, mode='hsv')
        self.line=Line(points=self.compute_points(), width=2)
            
        axes.canvas.add(self.color)
        axes.canvas.add(self.line)
        #axes.canvas.insert(axes.canvas.length()-1,self.line)
        #axes.canvas.insert(axes.canvas.length()-1,self.color)
        
        
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
        self.removed=True
    

class Axes(Widget):
    min_y = NumericProperty(0)
    max_y = NumericProperty(10)
    
    def __init__(self, **kwargs):
        super(Axes, self).__init__(**kwargs)
        self.lines = []
        self.fade_in = []
        self.fade_out = []
        self.fade_down = []
        Clock.schedule_interval(self.do_fade, 0.05)
        self.bind(size=self.recompute_lines)
        
    def plot(self, data, hue):
        lineinfo=LineInfo(self, data, hue)
        self.lines.append(lineinfo)
        self.fade_in.append(lineinfo)
        return lineinfo
        
    def recompute_lines(self,width,height):
        for line in self.lines:
            line.recompute()
    
    def remove_plot(self,lineinfo):
        if lineinfo in self.fade_in: self.fade_in.remove(lineinfo)
        if lineinfo in self.fade_down: self.fade_down.remove(lineinfo)
        self.fade_out.append(lineinfo)
        
    def fade(self,lineinfo):
        if lineinfo in self.fade_in: self.fade_in.remove(lineinfo)
        self.fade_down.append(lineinfo)
    
    def do_fade(self, dt):
        for line in self.fade_in[:]:
            line.color.a+=0.1
            if line.color.a>=0.95:
                self.fade_in.remove(line)
        
        faded=0.3
        for line in self.fade_down[:]:
            if line.color.a>faded: 
                line.color.a-=0.1
                if line.color.a<=faded: self.fade_down.remove(line)
            elif line.color.a<faded: 
                line.color.a+=0.1
                if line.color.a>=faded: self.fade_down.remove(line)

        
        for line in self.fade_out[:]:
            line.color.a-=0.1
            if line.color.a<=0.05:
                self.lines.remove(line)
                line.remove()
                self.fade_out.remove(line)
        
        
        
Factory.register('Axes', Axes)            


class Plotter(Widget):
    pass

Factory.register('Plotter', Plotter)            
    
