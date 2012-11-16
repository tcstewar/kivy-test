from kivy.app import App
from kivy.clock import Clock
import plotter
import random
import math


class PlotterApp(App):
    def build(self):
        self.plotter = plotter.Plotter()
        Clock.schedule_interval(self.make_plot,0.5)
        #Clock.schedule_interval(self.plotter.axes.do_fade,0.01)
        return self.plotter
        
    def make_plot(self,dt):
        scale=random.uniform(5,15)
        data=[math.sin(t/scale) for t in range(100)]   
        self.plotter.axes.plot(data, random.uniform(0,1) ) 
        
if __name__=='__main__':
    PlotterApp().run()

