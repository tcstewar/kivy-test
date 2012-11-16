from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
import plotter
import random
import math

class MainView(Widget):
    pass


class PlotterApp(App):
    def build(self):
        view=MainView()
        self.plotter = view.plotter
        Clock.schedule_interval(self.make_plot,0.5)
        return view
        
    def make_plot(self,dt):
        scale=random.uniform(5,15)
        data=[math.sin(t/scale) for t in range(100)]   
        self.plotter.axes.plot(data, random.uniform(0,1) ) 
        
if __name__=='__main__':
    PlotterApp().run()

