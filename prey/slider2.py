from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, AliasProperty, OptionProperty, \
        ReferenceListProperty, BoundedNumericProperty, StringProperty

from kivy.factory import Factory


class Slider2(Widget):
    label = StringProperty('')

    value1 = NumericProperty(0.)
    value2 = NumericProperty(0.)

    min = NumericProperty(0.)
    max = NumericProperty(100.)

    padding = NumericProperty(10)
    orientation = OptionProperty('horizontal', options=(
      'vertical', 'horizontal'))    

    range = ReferenceListProperty(min, max)
    step = BoundedNumericProperty(0, min=0)

    def get_norm_value1(self):
        vmin = self.min
        d = self.max - vmin
        if d == 0:
            return 0
        return (self.value1 - vmin) / float(d)

    def set_norm_value1(self, value):
        vmin = self.min
        step = self.step
        val = value * (self.max - vmin) + vmin
        if step == 0:
            self.value1 = val
        else:
            self.value1 = min(round((val - vmin) / step) * step, self.max) + vmin
            
        if self.value1>self.value2: self.value2=self.value1    
    value1_normalized = AliasProperty(get_norm_value1, set_norm_value1,
                                     bind=('value1', 'min', 'max', 'step'))


    def get_norm_value2(self):
        vmin = self.min
        d = self.max - vmin
        if d == 0:
            return 0
        return (self.value2 - vmin) / float(d)

    def set_norm_value2(self, value):
        vmin = self.min
        step = self.step
        val = value * (self.max - vmin) + vmin
        if step == 0:
            self.value2 = val
        else:
            self.value2 = min(round((val - vmin) / step) * step, self.max) + vmin
        if self.value2<self.value1: self.value1=self.value2    
    value2_normalized = AliasProperty(get_norm_value2, set_norm_value2,
                                     bind=('value2', 'min', 'max', 'step'))



    def get_value1_pos(self):
        padding = self.padding
        x = self.x
        y = self.y
        nval = self.value1_normalized
        if self.orientation == 'horizontal':
            return (x + padding + nval * (self.width - 2 * padding), y)
        else:
            return (x, y + padding + nval * (self.height - 2 * padding))

    def set_value1_pos(self, pos):
        x = min(self.right, max(pos[0], self.x))
        y = min(self.top, max(pos[1], self.y))
        if self.orientation == 'horizontal':
            if self.width == 0:
                self.value1_normalized = 0
            else:
                self.value1_normalized = (x - self.x) / float(self.width)
        else:
            if self.height == 0:
                self.value1_normalized = 0
            else:
                self.value1_normalized = (y - self.y) / float(self.height)
    value1_pos = AliasProperty(get_value1_pos, set_value1_pos,
                              bind=('x', 'y', 'width', 'height', 'min',
                                    'max', 'value1_normalized', 'orientation'))

    def get_value2_pos(self):
        padding = self.padding
        x = self.x
        y = self.y
        nval = self.value2_normalized
        if self.orientation == 'horizontal':
            return (x + padding + nval * (self.width - 2 * padding), y)
        else:
            return (x, y + padding + nval * (self.height - 2 * padding))

    def set_value2_pos(self, pos):
        x = min(self.right, max(pos[0], self.x))
        y = min(self.top, max(pos[1], self.y))
        if self.orientation == 'horizontal':
            if self.width == 0:
                self.value2_normalized = 0
            else:
                self.value2_normalized = (x - self.x) / float(self.width)
        else:
            if self.height == 0:
                self.value2_normalized = 0
            else:
                self.value2_normalized = (y - self.y) / float(self.height)
    value2_pos = AliasProperty(get_value2_pos, set_value2_pos,
                              bind=('x', 'y', 'width', 'height', 'min',
                                    'max', 'value2_normalized', 'orientation'))


    def find_closest_pos(self, x, y):
        x1,y1=self.value1_pos
        x2,y2=self.value2_pos
        dist1=(x-x1)**2+(y-y1)**2
        dist2=(x-x2)**2+(y-y2)**2
        if dist1<=dist2: return '1'
        else: return '2'

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            if touch.button=='scrolldown' or touch.button=='scrollup':
                touch.ud['item']=None
                v1=self.value1_normalized
                v2=self.value2_normalized
                vc=(v1+v2)/2
                dv=vc-v1
                if touch.button=='scrollup': 
                    dv-=0.1
                    if dv<0: dv=0
                elif touch.button=='scrolldown':
                    dv+=0.1
                    if dv>0.5: dv=0.5
                    if vc-dv<0: vc=dv
                    if vc+dv>1: vc=1-dv
                self.value1_normalized=vc-dv
                self.value2_normalized=vc+dv
                
            else:        
                touch.ud['item']=self.find_closest_pos(*touch.pos)
                    
                
            if touch.ud['item']=='1':
                self.value1_pos = touch.pos
            elif touch.ud['item']=='2':
                self.value2_pos = touch.pos
                            
            return True

    def on_touch_move(self, touch):
        if touch.grab_current == self:
            if touch.ud['item']=='1':
                self.value1_pos = touch.pos
            elif touch.ud['item']=='2':
                self.value2_pos = touch.pos
            return True

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            if touch.ud['item']=='1':
                self.value1_pos = touch.pos
            elif touch.ud['item']=='2':
                self.value2_pos = touch.pos
            return True
            

Factory.register('Slider2', Slider2)            

