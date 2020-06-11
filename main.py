# https://stackoverflow.com/questions/60736027/how-to-set-text-color-to-gradient-texture-in-kivy
# https://gist.github.com/tshirtman/4247921

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.properties import (
    ObjectProperty, ListProperty, NumericProperty, 
    StringProperty, OptionProperty, BooleanProperty
)

from kivy.clock import Clock
from kivy.factory import Factory

from itertools import chain
from random import choice, random, randint

# hex bynary numbers
hexs = {
        '0': b'\x00', '1': b'\x01', '2': b'\x02', '3': b'\x03', '4': b'\x04', '5': b'\x05', '6': b'\x06', '7': b'\x07', '8': b'\x08', '9': b'\x09', 
        '10': b'\x0a', '11': b'\x0b', '12': b'\x0c', '13': b'\x0d', '14': b'\x0e', '15': b'\x0f', '16': b'\x10', '17': b'\x11', '18': b'\x12', '19': b'\x13', 
        '20': b'\x14', '21': b'\x15', '22': b'\x16', '23': b'\x17', '24': b'\x18', '25': b'\x19', '26': b'\x1a', '27': b'\x1b', '28': b'\x1c', '29': b'\x1d', 
        '30': b'\x1e', '31': b'\x1f', '32': b'\x20', '33': b'\x21', '34': b'\x22', '35': b'\x23', '36': b'\x24', '37': b'\x25', '38': b'\x26', '39': b'\x27', 
        '40': b'\x28', '41': b'\x29', '42': b'\x2a', '43': b'\x2b', '44': b'\x2c', '45': b'\x2d', '46': b'\x2e', '47': b'\x2f', '48': b'\x30', '49': b'\x31', 
        '50': b'\x32', '51': b'\x33', '52': b'\x34', '53': b'\x35', '54': b'\x36', '55': b'\x37', '56': b'\x38', '57': b'\x39', '58': b'\x3a', '59': b'\x3b', 
        '60': b'\x3c', '61': b'\x3d', '62': b'\x3e', '63': b'\x3f', '64': b'\x40', '65': b'\x41', '66': b'\x42', '67': b'\x43', 
        '68': b'\x44', '69': b'\x45', '70': b'\x46', '71': b'\x47', '72': b'\x48', '73': b'\x49', '74': b'\x4a', '75': b'\x4b', 
        '76': b'\x4c', '77': b'\x4d', '78': b'\x4e', '79': b'\x4f', '80': b'\x50', '81': b'\x51', '82': b'\x52', '83': b'\x53', 
        '84': b'\x54', '85': b'\x55', '86': b'\x56', '87': b'\x57', '88': b'\x58', '89': b'\x59', '90': b'\x5a', '91': b'\x5b', 
        '92': b'\x5c', '93': b'\x5d', '94': b'\x5e', '95': b'\x5f', '96': b'\x60', '97': b'\x61', '98': b'\x62', '99': b'\x63', 
    '100': b'\x64', '101': b'\x65', '102': b'\x66', '103': b'\x67', '104': b'\x68', '105': b'\x69', '106': b'\x6a', '107': b'\x6b', 
    '108': b'\x6c', '109': b'\x6d', '110': b'\x6e', '111': b'\x6f', '112': b'\x70', '113': b'\x71', '114': b'\x72', '115': b'\x73', 
    '116': b'\x74', '117': b'\x75', '118': b'\x76', '119': b'\x77', '120': b'\x78', '121': b'\x79', '122': b'\x7a', '123': b'\x7b', 
    '124': b'\x7c', '125': b'\x7d', '126': b'\x7e', '127': b'\x7f', '128': b'\x80', '129': b'\x81', '130': b'\x82', '131': b'\x83', 
    '132': b'\x84', '133': b'\x85', '134': b'\x86', '135': b'\x87', '136': b'\x88', '137': b'\x89', '138': b'\x8a', '139': b'\x8b', 
    '140': b'\x8c', '141': b'\x8d', '142': b'\x8e', '143': b'\x8f', '144': b'\x90', '145': b'\x91', '146': b'\x92', '147': b'\x93', 
    '148': b'\x94', '149': b'\x95', '150': b'\x96', '151': b'\x97', '152': b'\x98', '153': b'\x99', '154': b'\x9a', '155': b'\x9b', 
    '156': b'\x9c', '157': b'\x9d', '158': b'\x9e', '159': b'\x9f', '160': b'\xa0', '161': b'\xa1', '162': b'\xa2', '163': b'\xa3', 
    '164': b'\xa4', '165': b'\xa5', '166': b'\xa6', '167': b'\xa7', '168': b'\xa8', '169': b'\xa9', '170': b'\xaa', '171': b'\xab', 
    '172': b'\xac', '173': b'\xad', '174': b'\xae', '175': b'\xaf', '176': b'\xb0', '177': b'\xb1', '178': b'\xb2', '179': b'\xb3', 
    '180': b'\xb4', '181': b'\xb5', '182': b'\xb6', '183': b'\xb7', '184': b'\xb8', '185': b'\xb9', '186': b'\xba', '187': b'\xbb', 
    '188': b'\xbc', '189': b'\xbd', '190': b'\xbe', '191': b'\xbf', '192': b'\xc0', '193': b'\xc1', '194': b'\xc2', '195': b'\xc3', 
    '196': b'\xc4', '197': b'\xc5', '198': b'\xc6', '199': b'\xc7', '200': b'\xc8', '201': b'\xc9', '202': b'\xca', '203': b'\xcb', 
    '204': b'\xcc', '205': b'\xcd', '206': b'\xce', '207': b'\xcf', '208': b'\xd0', '209': b'\xd1', '210': b'\xd2', '211': b'\xd3', 
    '212': b'\xd4', '213': b'\xd5', '214': b'\xd6', '215': b'\xd7', '216': b'\xd8', '217': b'\xd9', '218': b'\xda', '219': b'\xdb', 
    '220': b'\xdc', '221': b'\xdd', '222': b'\xde', '223': b'\xdf', '224': b'\xe0', '225': b'\xe1', '226': b'\xe2', '227': b'\xe3', 
    '228': b'\xe4', '229': b'\xe5', '230': b'\xe6', '231': b'\xe7', '232': b'\xe8', '233': b'\xe9', '234': b'\xea', '235': b'\xeb', 
    '236': b'\xec', '237': b'\xed', '238': b'\xee', '239': b'\xef', '240': b'\xf0', '241': b'\xf1', '242': b'\xf2', '243': b'\xf3', 
    '244': b'\xf4', '245': b'\xf5', '246': b'\xf6', '247': b'\xf7', '248': b'\xf8', '249': b'\xf9', '250': b'\xfa', '251': b'\xfb', 
    '252': b'\xfc', '253': b'\xfd', '254': b'\xfe', '255': b'\xff'
}

class HoverBehavior:
    hovered = BooleanProperty(False)
    border_point = ObjectProperty(None)
    '''Contains the last relevant point received by the Hoverable. This can
    be used in `on_enter` or `on_leave` in order to know where was dispatched the event.
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return  # do proceed if I'm not displayed <=> If have no parent
        pos = args[1]
        # Next line to_widget allow to compensate for relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            # We have already done what was needed
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self):
        pass

    def on_leave(self):
        pass

class LabelGradient(Factory.Label):
    grad = ObjectProperty(None)
    color = ListProperty([1,1,1,1])
    radius = ListProperty([10,])
    gradient = ListProperty([[]])
    gradient_orientation = OptionProperty('vertical', options = ['horizontal', 'vertical'])

    def __init__(self, **kwargs):
        super(LabelGradient, self).__init__(**kwargs)
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
        self.canvas.ask_update()

class ButtonGradient(Factory.Button):
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
        self.blitter(self.buf_normal)
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.blitter(self.buf_down)
            return True
        return super(ButtonGradient, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.blitter(self.buf_normal)
            return True
        return super(ButtonGradient, self).on_touch_up(touch)

    # blit the buffer and update the canvas
    def blitter(self, buf):
        self.canvas.ask_update()
        self.grad.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.canvas.ask_update()

class HoverGradient(HoverBehavior, Factory.Label):
    grad = ObjectProperty(None) # texture object
    radius = ListProperty([10]) # canvas curvature
    color = ListProperty([1,1,1,1]) # text color
    gradient = ListProperty([[]]) # list of lists with the colors in rgba % 100
    gradient_orientation = OptionProperty('vertical', options = ['horizontal', 'vertical'])

    def __init__(self, *args, **kwargs):
        super(HoverGradient, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.start)

    def start(self, evt):
        # change the gradient orientation
        if self.gradient_orientation == 'horizontal':
            # create the texture accordling with colors quantity
            self.grad = Texture.create(size = (len(self.gradient), 1))
        elif self.gradient_orientation == 'vertical':
            self.grad = Texture.create(size = (1, len(self.gradient)))

        # normalize the rgba to pattern 
        self.buf_normal = [str(int(v * 255)) for v in chain(*self.gradient)]
        self.buf_normal = b"".join(map(lambda x: hexs[x], self.buf_normal))

        self.buf_down = [str(int(v * 230)) for v in chain(*self.gradient)]
        self.buf_down = b"".join(map(lambda x: hexs[x], self.buf_down))

        # then blit the buffer
        self.blitter(self.buf_normal)

    def on_enter(self):
        self.blitter(self.buf_down)

    def on_leave(self):
        self.blitter(self.buf_normal)

    def blitter(self, buf):
        self.grad.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.canvas.ask_update()

class RandomGradient(Factory.Label):
    grad = ObjectProperty(None)
    color = ListProperty([1,1,1,1])
    radius = ListProperty([10,])
    texture_x = NumericProperty(3)
    texture_y = NumericProperty(3)

    def __init__(self, *args, **kwargs):
        super(RandomGradient, self).__init__(*args, **kwargs)
        Clock.schedule_interval(self.random_gradient, 1)

    def random_gradient(self, evt):
        self.grad = Texture.create(size=(self.texture_x, self.texture_y), colorfmt='rgba')
        colors = list()
        for x in range(0, self.texture_x):
            for y in range(0, self.texture_y):
                colors.append([randint(0, 255), randint(0, 255), randint(0, 255), 255])

        # get all colors generated and appended in colors 
        # and transform in one list with all numbers like string
        self.buf_normal = [str(c) for c in chain(*colors)]
        # convert the buf_normal to bytes
        self.buf_normal = b"".join(map(lambda x: hexs[x], self.buf_normal))
        # blit the buffer
        self.grad.blit_buffer(self.buf_normal, colorfmt='rgba', bufferfmt='ubyte')

class RadialHoverGradient(HoverBehavior, Factory.Label):
    grad = ObjectProperty(None) # texture object
    radius = ListProperty([10]) # canvas curvature
    color = ListProperty([1,1,1,1]) # text color
    radial = NumericProperty(32)
    border_color_normal = ListProperty([0, 0.7, 0.7, 1]) # get the colors in rgba%
    center_color_normal = ListProperty([1, 1, 0, 1]) # get the colors in rgba%

    def __init__(self, *args, **kwargs):
        super(RadialHoverGradient, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.start)

    def start(self, evt):
        # change the radial
        size = (self.radial, self.radial)
        self.grad = Texture.create(size = size, colorfmt = 'rgba')
        # color normalize
        self.border_color_normal = [int(v * 255) for v in self.border_color_normal]
        self.center_color_normal = [int(v * 255) for v in self.center_color_normal]
        # get the colors in down|enter depending of the behavior choosed
        self.border_color_down = [c - 10 if c >= 10 else 0 for c in self.border_color_normal]
        self.center_color_down = [c - 10 if c >= 10 else 0 for c in self.center_color_normal]
        # instacialize the buffers
        self.buf_normal = list()
        self.buf_down = list()
        # get the center of the radial
        sx_2 = size[0] // 2
        sy_2 = size[1] // 2
        
        for x in range(-sx_2, sx_2):
            for y in range(-sy_2, sy_2):
                a = x / (1.0 * sx_2)
                b = y / (1.0 * sy_2)
                d = (a ** 2 + b ** 2) ** .5

                for c in (0, 1, 2, 3):
                    self.buf_normal.append(str( max(0, min(255, int(self.center_color_normal[c] * (1 - d)) + int(self.border_color_normal[c] * d)))))
                    self.buf_down.append(str( max(0, min(255, int(self.center_color_down[c] * (1 - d)) + int(self.border_color_down[c] * d)))))
        # This assign a bytes string to the buffers 
        self.buf_normal = b"".join(map(lambda x: hexs[x], self.buf_normal))
        self.buf_down = b"".join(map(lambda x: hexs[x], self.buf_down))
        # then blit the buffer
        self.blitter(self.buf_normal)

    def on_enter(self):
        self.blitter(self.buf_down)

    def on_leave(self):
        self.blitter(self.buf_normal)

    def blitter(self, buf):
        self.grad.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.canvas.ask_update()

Builder.load_string("""
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

<HoverGradient>:
    canvas.before:
        Color:
            rgba: [1,1,1,1]
        RoundedRectangle:
            texture: root.grad
            size: root.size
            pos: root.pos
            radius: root.radius

<RandomGradient>:
    canvas.before:
        Color:
            rgba: [1,1,1,1]
        RoundedRectangle:
            texture: root.grad
            size: root.size
            pos: root.pos
            radius: root.radius

<RadialHoverGradient>:
    canvas.before:
        Color:
            rgba: [1,1,1,1]
        RoundedRectangle:
            texture: root.grad
            size: root.size
            pos: root.pos
            radius: root.radius
""")

if __name__ == '__main__':
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.clock import Clock
    
    class GradientApp(App):
        def build(self):
            kv = Builder.load_string('''
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
''')

            kv.ids.container.add_widget(
                LabelGradient(
                    text = f"Gradient Label", size_hint = [1, None],
                    height = 80, font_size = 20,
                    gradient_orientation = choice(['vertical', 'horizontal']),
                    gradient = [[random(),random(),random(),1], 
                                [random(),random(),random(),1], 
                                [random(),random(),random(),1]]))
            kv.ids.container.add_widget(
                ButtonGradient(text = f"Gradient Button", 
                    size_hint = [1, None], height = 80, font_size = 20,
                    gradient_orientation = choice(['vertical', 'horizontal']),
                    gradient = [[random(),random(),random(),1], 
                                [random(),random(),random(),1], 
                                [random(),random(),random(),1]]))
            kv.ids.container.add_widget(
                HoverGradient(
                    text = f"Hover Gradient", size_hint = [1, None],
                    height = 80, font_size = 20,
                    gradient_orientation = choice(['vertical', 'horizontal']),
                    gradient = [[random(),random(),random(),1], 
                                [random(),random(),random(),1], 
                                [random(),random(),random(),1]]))
            kv.ids.container.add_widget(
                RandomGradient(
                    text = f"Random Gradient", size_hint = [1, None],
                    height = 80, font_size = 20
                ))
            kv.ids.container.add_widget(
                RadialHoverGradient(
                    text = f"Radial Hover Gradient", size_hint = [1, None],
                    border_color_normal = [0,.7,.7,1],
                    center_color_normal = [.3,.3,.3,1],
                    height = 300, font_size = 20
                ))

            return kv

    GradientApp().run()