from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty

import plotter
import random
import math
import slider2
    
import prey   
import inspect


class Model:
    def __init__(self, module):
        self.module=module
        self.sliders={}
    def make_sliders(self, widget, on_change):
        argspec=inspect.getargspec(self.module.model)
        for i,arg in enumerate(argspec.args):
            try:
                slider=slider2.Slider2(label=self.module.labels[arg], min=self.module.ranges[arg][0], 
                                max=self.module.ranges[arg][1], value1=argspec.defaults[i],
                                value2=argspec.defaults[i], size_hint=(None, 0.2), width=200)
            except KeyError:
                print 'Could not process parameter',arg
                continue
            self.sliders[arg]=slider
            widget.add_widget(slider)
            slider.bind(value1=on_change, value2=on_change)
    def generate_data(self):
        args={}
        for arg,slider in self.sliders.items():
            args[arg]=random.uniform(slider.value1,slider.value2)
        return self.module.model(**args)    
        
        


class MainView(Widget):
    scale = ListProperty([1.0, 1.0])
    
    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        
        self.model=Model(prey)
        self.model.make_sliders(self.sliders, self.on_slider_changed)
        

    
    def on_slider_changed(self,obj,value):
        pass
    


class PreyApp(App):

    def build(self):
        self.view=MainView()
        self.plotter = self.view.plotter
        Clock.schedule_interval(self.make_plot,0.5)
        return self.view
        
    def make_plot(self,dt):
        data=self.view.model.generate_data()
        #x0=random.uniform(self.view.x0.value1, self.view.x0.value2)
        #y0=random.uniform(self.view.y0.value1, self.view.y0.value2)
        #data=prey.model(x0=x0,y0=y0)
        self.plotter.axes.plot(data['x'], 0 ) 
        self.plotter.axes.plot(data['y'], 0.7 ) 
        
if __name__=='__main__':
    PreyApp().run()

