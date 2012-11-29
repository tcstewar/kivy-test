from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty

import plotter
import random
import math
import slider2
    

class MainView(Widget):
    scale = ListProperty([10.0, 10.0])
    
    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        self.slider.bind(value1=self.on_slider_changed, value2=self.on_slider_changed)
    
    def on_slider_changed(self,obj,value):
        self.scale[0]=self.slider.value1
        self.scale[1]=self.slider.value2
    


class PlotterApp(App):

    def build(self):
        self.view=MainView()
        self.plotter = self.view.plotter
        Clock.schedule_interval(self.make_plot,0.1)
        return self.view
        
    def make_plot(self,dt):
        scale=random.uniform(*self.view.scale)
        print self.view.scale
        data=[math.sin(t/scale) for t in range(100)]   
        self.plotter.axes.plot(data, 0 ) 
        
if __name__=='__main__':
    PlotterApp().run()

