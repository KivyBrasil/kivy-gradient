# https://stackoverflow.com/questions/60736027/how-to-set-text-color-to-gradient-texture-in-kivy

from kivy.lang import Builder
from kivy.graphics.texture import Texture
from kivy.properties import (
    ObjectProperty, ListProperty, NumericProperty, 
    StringProperty, OptionProperty
)
from kivy.uix.label import Label
from kivy.uix.button import Button

from itertools import chain
from colors import hexs
from random import choice, random

class LabelGradient(Label):
    grad = ObjectProperty(None)
    color = ListProperty([1,1,1,1])
    bg_color = ListProperty([0, 0, 0, 255])
    radius = ListProperty([10,])
    gradient = ListProperty([[]])
    gradient_orientation = OptionProperty('vertical', options = ['horizontal', 'vertical'])

    def __init__(self, **kwargs):
        super(LabelGradient, self).__init__(**kwargs)
        Builder.load_string('''
<LabelGradient>:
    canvas.before:
        # draw the gradient below the normal Label Texture
        Color:
            rgba: 1,1,1,1
        RoundedRectangle:
            texture: root.grad
            size: root.size
            pos: root.pos#int(root.center_x - root.texture_size[0] / 2.), int(root.center_y - root.texture_size[1] / 2.)
            radius: root.radius
''')
        Clock.schedule_once(self.start)

    def start(self, evt):
        # create a 64x64 texture, defaults to rgba / ubyte
        if self.gradient_orientation == 'horizontal':
            self.grad = Texture.create(size=(len(self.gradient), 1))
        elif self.gradient_orientation == 'vertical':
            self.grad = Texture.create(size=(1, len(self.gradient)))
        
        buf = [str(int(v * 255)) for v in chain(*self.gradient)]
        buf = b"".join(map(lambda x: hexs[x], buf))

        # then blit the buffer
        self.grad.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')

class ButtonGradient(Button):
    background_normal = ''
    background_down = ''
    background_color = [0,0,0,0]
    grad = ObjectProperty(None)
    radius = ListProperty([10])
    color = ListProperty([1,1,1,1])
    gradient = ListProperty([[]])
    gradient_orientation = OptionProperty('vertical', options = ['horizontal', 'vertical'])

    def __init__(self, **kwargs):
        super(ButtonGradient, self).__init__(**kwargs)
        Builder.load_string('''
<ButtonGradient>:
    text_size: self.size
    halign: 'center'
    valign: 'middle'
    canvas.before:
        # draw the gradient below the normal Label Texture
        Color:
            rgba: 1,1,1,1
        RoundedRectangle:
            texture: root.grad
            size: root.texture_size
            pos: int(root.center_x - root.texture_size[0] / 2.), int(root.center_y - root.texture_size[1] / 2.)
            radius: root.radius
''')
        Clock.schedule_once(self.start)

    def start(self, evt):
        # create a 64x64 texture, defaults to rgba / ubyte
        if self.gradient_orientation == 'horizontal':
            self.grad = Texture.create(size=(len(self.gradient), 1))
        elif self.gradient_orientation == 'vertical':
            self.grad = Texture.create(size=(1, len(self.gradient)))

        self.buf_normal = [str(int(v * 255)) for v in chain(*self.gradient)]
        self.buf_normal = b"".join(map(lambda x: hexs[x], self.buf_normal))

        self.buf_down = [str(int(v * 200)) for v in chain(*self.gradient)]
        self.buf_down = b"".join(map(lambda x: hexs[x], self.buf_down))

        # then blit the buffer
        self.grad.blit_buffer(self.buf_normal, colorfmt='rgba', bufferfmt='ubyte')
    
    def on_press(self):
        # print(self.text)
        self.grad.blit_buffer(self.buf_down, colorfmt='rgba', bufferfmt='ubyte')

    def on_release(self):
        # then blit the buffer
        self.grad.blit_buffer(self.buf_normal, colorfmt='rgba', bufferfmt='ubyte')

if __name__ == '__main__':
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.clock import Clock
    
    class GradientApp(App):
        def build(self):
            kv = Builder.load_string('''
#;import Texture kivy.graphics.texture.Texture
BoxLayout:
    orientation: "vertical"
    ScrollView:
        BoxLayout:
            id: container
            orientation: "vertical"
            size_hint: 1, None
            height: self.minimum_height
            padding: dp(5)
            spacing: dp(5)
            ButtonGradient:
                text: "Kivy Brazil \\o/"
                size_hint: [1, None]
                height: 80
                font_size: 20
                gradient_orientation: 'vertical'
                gradient: [[0,.5,0,1], [1,1,0,1], [0,0,1,1]]
                on_release:
                    print(self.text)
            LabelGradient:
                text: "Kivy Brazil :)"
                size_hint: [1, None]
                height: 80
                font_size: 20
                gradient_orientation: 'horizontal'
                gradient: [[0,.5,0,1], [1,1,0,1], [0,0,1,1]]
''')
            for wid in range(5):
                kv.ids.container.add_widget(
                    LabelGradient(
                        text = f"{wid} Gradient Label", 
                        size_hint = [1, None],
                        height = 80,
                        font_size = 20,
                        gradient_orientation = choice(['vertical', 'horizontal']),
                        gradient = [[random(),random(),random(),1], 
                                    [random(),random(),random(),1], 
                                    [random(),random(),random(),1]]))
            for wid in range(5):
                kv.ids.container.add_widget(
                    ButtonGradient(
                        text = f"{wid+5} Gradient Button", 
                        size_hint = [1, None],
                        height = 80,
                        font_size = 20,
                        gradient_orientation = choice(['vertical', 'horizontal']),
                        gradient = [[random(),random(),random(),1], 
                                    [random(),random(),random(),1], 
                                    [random(),random(),random(),1]]))
            return kv
    
GradientApp().run()