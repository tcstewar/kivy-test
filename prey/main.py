from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty
from kivy.animation import Animation
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
        self.lines=[]
        self.seed=0
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
    def generate_data(self, seed):
        random.seed(seed)
        args={}
        for arg,slider in self.sliders.items():
            args[arg]=random.uniform(slider.value1,slider.value2)
        return self.module.model(**args)

    def add_dataset(self,axes):
        data=self.generate_data(self.seed)
        lines={}
        for key, hue in self.module.colors.items():
            li=axes.plot(data[key],hue)
            lines[key]=li
        self.lines.append((self.seed, lines))    
        self.seed+=1
        
        if len(self.lines)>1:
            for li in self.lines[-2][1].values():
                axes.fade(li)
            
        
        if len(self.lines)>3:
            for li in self.lines[-4][1].values():
                axes.remove_plot(li)
                
            while (self.lines[0][1].values()[0].removed):
                del self.lines[0]
        
    def recompute(self):
        for seed, lines in self.lines:
            data=self.generate_data(seed)
            for key,line in lines.items():
                line.data=data[key]
                line.recompute()
                
        


class MainView(Widget):
    scale = ListProperty([1.0, 1.0])
    change_timer = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        
        self.model=Model(prey)
        self.model.make_sliders(self.sliders, self.on_slider_changed)
        

    
    def on_slider_changed(self,obj,value):
        self.model.recompute()
        self.change_timer=1
        Animation(change_timer=0, duration=2.0).start(self)
    


class PreyApp(App):

    def build(self):
        self.view=MainView()
        self.plotter = self.view.plotter
        Clock.schedule_interval(self.make_plot,0.5)
        return self.view
        
    def make_plot(self,dt):
        if self.view.change_timer==0:
            self.view.model.add_dataset(self.plotter.axes)
        
if __name__=='__main__':
    PreyApp().run()

