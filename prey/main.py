from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty

import plotter
import random
import math
import slider2
    
import model    

class MainView(Widget):
    scale = ListProperty([1.0, 1.0])
    
    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        
        self.x0=slider2.Slider2(label='x0', min=0, max=2, value1=1, value2=1, size_hint=(None, 0.2), width=200)
        self.sliders.add_widget(self.x0)      
        self.x0.bind(value1=self.on_slider_changed, value2=self.on_slider_changed)

        self.y0=slider2.Slider2(label='y0', min=0, max=2, value1=1, value2=1, size_hint=(None, 0.2), width=200)
        self.sliders.add_widget(self.y0)      
        self.y0.bind(value1=self.on_slider_changed, value2=self.on_slider_changed)

    
    def on_slider_changed(self,obj,value):
        pass
    


class PreyApp(App):

    def build(self):
        self.view=MainView()
        self.plotter = self.view.plotter
        Clock.schedule_interval(self.make_plot,0.5)
        return self.view
        
    def make_plot(self,dt):
        x0=random.uniform(self.view.x0.value1, self.view.x0.value2)
        y0=random.uniform(self.view.y0.value1, self.view.y0.value2)
        data=model.predator_prey(x0=x0,y0=y0)
        self.plotter.axes.plot(data['x'], 0 ) 
        self.plotter.axes.plot(data['y'], 0.7 ) 
        
if __name__=='__main__':
    PreyApp().run()

