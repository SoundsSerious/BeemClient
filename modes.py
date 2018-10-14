# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 20:17:06 2017

@author: Cabin
"""

from kivy.app import App
from kivy.clock import *

from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import *
from kivy.uix.button import *
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *
from kivy.graphics import *
from kivy.graphics.texture import *
from kivy.graphics.vertex_instructions import *
from kivy.uix.behaviors import *

from menus import *
from kivy.uix.colorpicker import ColorPicker, ColorWheel

from kivy.lang import Builder
Builder.load_string('''

<-ModeTile@Button>:
    size_hint: 1,1
    background_color: app.settings.BACKGROUND
    tile_color: app.settings.LIGHT_GREY
    border_color: app.settings.GREY_COLOR
    radius: [25]
    border_width: 25
    edge_margin: 30
    canvas:
        Color:
            rgb: app.settings.OFFWHITE
        RoundedRectangle:
            size: self.size[0] -self.border_width*2, self.size[1]-self.border_width*2
            pos: self.center[0] - (self.size[0]-self.border_width*2)/2.0 ,self.center[1] - (self.size[1]-self.border_width*2)/2.0
            radius: self.radius
        Color:
            rgb: app.settings.LIGHT_GREY
        RoundedRectangle:
            size: self.size[0] -self.edge_margin*2, self.size[1]-self.edge_margin*2
            pos: self.center[0] - (self.size[0]-self.edge_margin*2)/2.0 ,self.center[1] - (self.size[1]-self.edge_margin*2)/2.0
            radius: self.radius

    Label:
        text: root.mode_text
        id: 'label'
        size: root.size
        pos_hint: {'center_x':0.5, 'center_y':0.5}

<-Mode@BoxLayout>:
    size_hint: 1,1
    background_color: app.settings.BACKGROUND
    orientation:'vertical'
    spacing:20

''')

class ModeTile(Button):
    mode_text = StringProperty("Mode Name")
    def __init__(self,title,menu,**kwargs):
        super(ModeTile,self).__init__(**kwargs)
        self.mode_text = title
        self.menu = menu

    def on_press(self):
        self.menu.go_screen(self.mode_text)

class Mode(BoxLayout):
    mode_name = StringProperty("Mode Name")
    bar_height = NumericProperty(50)
    mode = ObjectProperty(None)
    parent_menu = ObjectProperty(None)
    app = ObjectProperty(None)
    clock = ObjectProperty(None)
    def __init__(self,app,menu,**kwargs):
        super(Mode,self).__init__(**kwargs)
        self.app = app
        self.parent_menu = menu
        self.menu = FloatLayout(size_hint=(1,0.1))
        self.menu.orientation = 'horizontal'
        self.menu.height = self.bar_height
        self.backBtn = Button(text = 'Back',
                                     size_hint= (0.25,1),
                                     pos_hint = {'x': 0, 'center_y': .5})
        self.backBtn.bind( on_press = self.go_back )
        self.menu.add_widget( self.backBtn )
        self.add_widget(self.menu)

        self.bind( size = self.update_rect, pos = self.update_rect)

    def go_back(self,instance):
        self.parent_menu.go_home()
        self.clock.cancel()

    def activate(self):
        self.clock = Clock.schedule_interval(self.update_mode, 0.25)

    def update_mode(self,*args):
        #Override
        pass

    def update_rect(self,instance,value):
        if self.mode and hasattr(self.mode,'size'):
            self.mode.size = self.size

class ColorPicking(Mode):



    def __init__(self,app,menu,**kwargs):
        super(ColorPicking,self).__init__(app,menu,**kwargs)

        # self.power_text = Label(text = "Power", size_hint_max_y = 0.02 )
        # self.power = Switch(active = True, size_hint_y = 0.15)
        # self.power.bind(active = self.togglePower)

        self.in_col_text = Label(text = "Inside Color", size_hint_max_y = 0.02,size_hint_y = 0.02)
        self.color_in = AutonomousColorWheel()
        self.color_in.bind( _hsv = self.on_color )

        self.out_col_text = Label(text = "Outside Color", size_hint_max_y = 0.02,size_hint_y = 0.02)
        self.color_out = AutonomousColorWheel()
        self.color_out.bind( _hsv = self.on_color )

        self.speed_lay = BoxLayout( orientation = 'horizontal', size_hint_y = 0.1)
        self.speed_lab = Label(text = 'span', size_hint_x = 0.2)
        self.speed = Slider(min = 0, max = 10.0, value = 1.0 )
        self.speed._settings_index = 0 #This is important!!
        self.speed.bind(on_touch_up  = self.on_slider)
        self.speed_lay.add_widget( self.speed_lab)
        self.speed_lay.add_widget( self.speed)

        self.hold_lay = BoxLayout( orientation = 'horizontal', size_hint_y = 0.1)
        self.hold_lab = Label(text = 'hold', size_hint_x = 0.2)
        self.hold = Slider(min = 0, max = 1.0, value = 0.5 )
        self.hold._settings_index = 1 #This is important!!
        self.hold.bind(on_touch_up  = self.on_slider)
        self.hold_lay.add_widget( self.hold_lab)
        self.hold_lay.add_widget( self.hold)

        # self.add_widget( self.power_text )
        # self.add_widget( self.power )

        self.add_widget( self.in_col_text)
        self.add_widget( self.color_in )

        self.add_widget( self.out_col_text)
        self.add_widget( self.color_out )

        self.add_widget( self.speed_lay )
        self.add_widget( self.hold_lay )


    def on_color(self, instance, value):
        print 'Color Change '+str(instance) +"\t" +str(instance._hsv)
        if instance is self.color_in:
            self.applyColor(1, instance)
        if instance is self.color_out:
            self.applyColor(0, instance)

    def on_slider(self,instance,touch):
        if touch.grab_current != None:
            print 'Slider Change' + str(instance.value)
            val = int( ((instance.value - instance.min)/(instance.max - instance.min))*255 )
            self.app.beem_client.setModeSetting(instance._settings_index,val)

    def applyColor(self, index , colorWidget ):
        H,S,V = colorWidget._hsv[:3]
        H = int(H*255)
        S = int(S*255)
        V = int(V*255)
        print H,S,V
        self.app.beem_client.setColor(index, H,S,V)

    def update_mode_com(self,*args):
        pass


class Flicker(Mode):

    def __init__(self,app,menu,**kwargs):
        super(Flicker,self).__init__(app,menu,**kwargs)

        # self.power_text = Label(text = "Power", size_hint_max_y = 0.02 )
        # self.power = Switch(active = True, size_hint_y = 0.15)
        # self.power.bind(active = self.togglePower)

        self.col_text = Label(text = "Color", size_hint_max_y = 0.02,size_hint_y = 0.02)
        self.color = AutonomousColorWheel()
        self.color.bind( _hsv = self.on_color )

        #number of spark attempts
        self.nspk_lay = BoxLayout( orientation = 'horizontal', size_hint_y = 0.1)
        self.nspk_lab = Label(text = 'Chance', size_hint_x = 0.2)
        self.nspk = Slider(min = 0, max = 25.0, value = 8.0 )
        self.nspk._settings_index = 0 #This is important!!
        self.nspk.bind(on_touch_up  = self.on_slider_min_to_max)
        self.nspk_lay.add_widget( self.nspk_lab)
        self.nspk_lay.add_widget( self.nspk)

        #Sparking
        self.spk_lay = BoxLayout( orientation = 'horizontal', size_hint_y = 0.1)
        self.spk_lab = Label(text = 'Thresh', size_hint_x = 0.2)
        self.spk = Slider(min = 0, max = 1.0, value = 0.33 )
        self.spk._settings_index = 1 #This is important!!
        self.spk.bind(on_touch_up  = self.on_slider_scaled_u8max)
        self.spk_lay.add_widget( self.spk_lab)
        self.spk_lay.add_widget( self.spk)

        #Heating
        self.heat_lay = BoxLayout( orientation = 'horizontal', size_hint_y = 0.1)
        self.heat_lab = Label(text = 'Heat', size_hint_x = 0.2)
        self.heat = Slider(min = 0, max = 1.0, value = 0.25 )
        self.heat._settings_index = 2 #This is important!!
        self.heat.bind(on_touch_up  = self.on_slider_scaled_u8max)
        self.heat_lay.add_widget( self.heat_lab)
        self.heat_lay.add_widget( self.heat)

        #Cooling
        self.cool_lay = BoxLayout( orientation = 'horizontal', size_hint_y = 0.1)
        self.cool_lab = Label(text = 'Cool', size_hint_x = 0.2)
        self.cool = Slider(min = 0, max = 1.0, value = 0.111 )
        self.cool._settings_index = 3 #This is important!!
        self.cool.bind(on_touch_up  = self.on_slider_scaled_u8max)
        self.cool_lay.add_widget( self.cool_lab)
        self.cool_lay.add_widget( self.cool)


        self.add_widget( self.col_text)
        self.add_widget( self.color )

        self.add_widget( self.nspk_lay )
        self.add_widget( self.spk_lay )
        self.add_widget( self.heat_lay )
        self.add_widget( self.cool_lay )


    def on_color(self, instance, value):
        print 'Color Change '+str(instance) +"\t" +str(instance._hsv)
        self.applyColor(0, instance)

    def on_slider_scaled_u8max(self,instance,touch):
        if touch.grab_current != None:
            print 'Slider Change' + str(instance.value)
            val = int( ((instance.value - instance.min)/(instance.max - instance.min))*255 )
            self.app.beem_client.setModeSetting(instance._settings_index,val)

    def on_slider_min_to_max(self,instance,touch):
        if touch.grab_current != None:
            print 'Slider Change' + str(instance.value)
            val = int( instance.value )
            self.app.beem_client.setModeSetting(instance._settings_index,val)

    def applyColor(self, index , colorWidget ):
        H,S,V = colorWidget._hsv[:3]
        H = int(H*255)
        S = int(S*255)
        V = int(V*255)
        self.app.beem_client.setColor(index, H,S,V)

    def update_mode_com(self,*args):
        pass



class FlickerPalette(Mode):

    palettes = DictProperty({'HEAT':0,
                             'CLOUD':1,
                             'MAGMA':2,
                             'OCEAN':3,
                             'FOREST':4,
                             'RAINBOW':5,
                             'STRIPES':6,
                             'PARTY':7
                             })

    def __init__(self,app,menu,**kwargs):
        super(FlickerPalette,self).__init__(app,menu,**kwargs)

        # self.power_text = Label(text = "Power", size_hint_max_y = 0.02 )
        # self.power = Switch(active = True, size_hint_y = 0.15)
        # self.power.bind(active = self.togglePower)

        self.pal_text = Label(text = "Palette Select", size_hint_max_y = 0.02, size_hint_y = 0.02)
        self.palette = Spinner(text = 'HEAT',values = self.palettes.keys(),size_hint_y=0.15)
        self.palette.bind( text = self.on_palette )

        #number of spark attempts
        self.nspk_lay = BoxLayout( orientation = 'horizontal', size_hint_y = 0.1)
        self.nspk_lab = Label(text = 'Chance', size_hint_x = 0.2)
        self.nspk = Slider(min = 0, max = 25.0, value = 8.0 )
        self.nspk._settings_index = 0 #This is important!!
        self.nspk.bind(on_touch_up  = self.on_slider_min_to_max)
        self.nspk_lay.add_widget( self.nspk_lab)
        self.nspk_lay.add_widget( self.nspk)

        #Sparking
        self.spk_lay = BoxLayout( orientation = 'horizontal', size_hint_y = 0.1)
        self.spk_lab = Label(text = 'Thresh', size_hint_x = 0.2)
        self.spk = Slider(min = 0, max = 1.0, value = 0.33 )
        self.spk._settings_index = 1 #This is important!!
        self.spk.bind(on_touch_up  = self.on_slider_scaled_u8max)
        self.spk_lay.add_widget( self.spk_lab)
        self.spk_lay.add_widget( self.spk)

        #Heating
        self.heat_lay = BoxLayout( orientation = 'horizontal', size_hint_y = 0.1)
        self.heat_lab = Label(text = 'Heat', size_hint_x = 0.2)
        self.heat = Slider(min = 0, max = 1.0, value = 0.25 )
        self.heat._settings_index = 2 #This is important!!
        self.heat.bind(on_touch_up  = self.on_slider_scaled_u8max)
        self.heat_lay.add_widget( self.heat_lab)
        self.heat_lay.add_widget( self.heat)

        #Cooling
        self.cool_lay = BoxLayout( orientation = 'horizontal', size_hint_y = 0.1)
        self.cool_lab = Label(text = 'Cool', size_hint_x = 0.2)
        self.cool = Slider(min = 0, max = 1.0, value = 0.111 )
        self.cool._settings_index = 3 #This is important!!
        self.cool.bind(on_touch_up  = self.on_slider_scaled_u8max)
        self.cool_lay.add_widget( self.cool_lab)
        self.cool_lay.add_widget( self.cool)


        self.add_widget( self.pal_text )
        self.add_widget( self.palette )

        self.add_widget( self.nspk_lay )
        self.add_widget( self.spk_lay )
        self.add_widget( self.heat_lay )
        self.add_widget( self.cool_lay )

    def on_palette(self, instance, value):
        self.applyPalette(self.palettes[value])

    def on_color(self, instance, value):
        print 'Color Change '+str(instance) +"\t" +str(instance._hsv)
        self.applyColor(0, instance)

    def on_slider_scaled_u8max(self,instance,touch):
        if touch.grab_current != None:
            print 'Slider Change' + str(instance.value)
            val = int( ((instance.value - instance.min)/(instance.max - instance.min))*255 )
            self.app.beem_client.setModeSetting(instance._settings_index,val)

    def on_slider_min_to_max(self,instance,touch):
        if touch.grab_current != None:
            print 'Slider Change' + str(instance.value)
            val = int( instance.value )
            self.app.beem_client.setModeSetting(instance._settings_index,val)

    def applyColor(self, index , colorWidget ):
        H,S,V = colorWidget._hsv[:3]
        H = int(H*255)
        S = int(S*255)
        V = int(V*255)
        self.app.beem_client.setColor(index, H,S,V)

    def applyPalette(self, index ):
        self.app.beem_client.setPalette(index)

    def update_mode_com(self,*args):
        pass


class Flash(Mode):

    def __init__(self,app,menu,**kwargs):
        super(Flash,self).__init__(app,menu,**kwargs)

        self.out_col_text = Label(text = "Flash Color", size_hint_max_y = 0.02, size_hint_y = 0.02)
        self.color_out = AutonomousColorWheel()
        self.color_out.bind( _hsv = self.on_color )

        self.flash_button = RoundedButton( text = "Flash")
        self.flash_button.bind(on_press = self.activate_flash)
        self.flash_button.bind(on_release = self.deactivate_flash)

        self.add_widget( self.out_col_text)
        self.add_widget( self.color_out )
        self.add_widget( self.flash_button )
    def on_color(self, instance, value):
        print 'Color Change '+str(instance) +"\t" +str(instance._hsv)
        self.applyColor(0, instance)

    def applyColor(self, index , colorWidget ):
        H,S,V = colorWidget._hsv[:3]
        H = int(H*255)
        S = int(S*255)
        V = int(V*255)
        print H,S,V
        self.app.beem_client.setColor(index, H,S,V)

    def activate_flash( self, instance):
        self.app.beem_client.setModeSetting(0,1)

    def deactivate_flash( self, instance):
        self.app.beem_client.setModeSetting(0,0)

    def update_mode_com(self,*args):
        pass



class DynamicLighting(Mode):

    palettes = DictProperty({'HEAT':0,
                             'CLOUD':1,
                             'MAGMA':2,
                             'OCEAN':3,
                             'FOREST':4,
                             'RAINBOW':5,
                             'STRIPES':6,
                             'PARTY':7
                             })

    def __init__(self,app,menu,**kwargs):
        super(DynamicLighting,self).__init__(app,menu,**kwargs)

        # self.power_text = Label(text = "Power", size_hint_max_y = 0.02 )
        # self.power = Switch(active = True, size_hint_y = 0.15)
        # self.power.bind(active = self.togglePower)

        self.pal_text = Label(text = "Palette Select", size_hint_max_y = 0.02, size_hint_y = 0.02)
        self.palette = Spinner(text = 'HEAT',values = self.palettes.keys(),size_hint_y=0.15)
        self.palette.bind( text = self.on_palette )

        self.out_col_text = Label(text = "Outside Color", size_hint_max_y = 0.02, size_hint_y = 0.02)
        self.color_out = AutonomousColorWheel()
        self.color_out.bind( _hsv = self.on_color )

        # self.add_widget( self.power_text )
        # self.add_widget( self.power )

        self.add_widget( self.pal_text)
        self.add_widget( self.palette )

        self.add_widget( self.out_col_text)
        self.add_widget( self.color_out )

    def on_color(self, instance, value):
        print 'Color Change '+str(instance) +"\t" +str(instance._hsv)
        self.applyColor(0, instance)

    def on_palette(self, instance, value):
        print 'Palette Change '+str(instance) +"\t" +str(value)
        print self.palettes[value]
        self.applyPalette(self.palettes[value])

    def applyColor(self, index , colorWidget ):
        H,S,V = colorWidget._hsv[:3]
        H = int(H*255)
        S = int(S*255)
        V = int(V*255)
        print H,S,V
        self.app.beem_client.setColor(index, H,S,V)

    def applyPalette(self, index ):
        self.app.beem_client.setPalette(index)

    def update_mode_com(self,*args):
        pass

class GradientLighting(Mode):

    palettes = DictProperty({'HEAT':0,
                             'CLOUD':1,
                             'MAGMA':2,
                             'OCEAN':3,
                             'FOREST':4,
                             'RAINBOW':5,
                             'STRIPES':6,
                             'PARTY':7
                             })

    def __init__(self,app,menu,**kwargs):
        super(GradientLighting,self).__init__(app,menu,**kwargs)

        # self.power_text = Label(text = "Power", size_hint_max_y = 0.02 )
        # self.power = Switch(active = True, size_hint_y = 0.15)
        # self.power.bind(active = self.togglePower)

        self.pal_text = Label(text = "Palette Select", size_hint_max_y = 0.02, size_hint_y = 0.02)
        self.palette = Spinner(text = 'HEAT',values = self.palettes.keys(),size_hint_y=0.15)
        self.palette.bind( text = self.on_palette )

        self.out_col_text = Label(text = "Outside Color", size_hint_max_y = 0.02, size_hint_y = 0.02)
        self.color_out = AutonomousColorWheel()
        self.color_out.bind( _hsv = self.on_color )

        #Direction
        self.speed_lay = BoxLayout( orientation = 'horizontal', size_hint_y = 0.1)
        self.speed_lab = Label(text = 'speed', size_hint_x = 0.2)
        self.speed = Slider(min = -2.5, max = 2.5, value = 1.0 )
        self.speed.bind(on_touch_up  = self.on_speed)
        self.speed_lay.add_widget( self.speed_lab)
        self.speed_lay.add_widget( self.speed)
        # self.add_widget( self.power_text )
        # self.add_widget( self.power )

        self.add_widget( self.pal_text)
        self.add_widget( self.palette )

        self.add_widget( self.out_col_text)
        self.add_widget( self.color_out )

        self.add_widget(self.speed_lay)


    def on_color(self, instance, value):
        print 'Color Change '+str(instance) +"\t" +str(instance._hsv)
        self.applyColor(0, instance)

    def on_palette(self, instance, value):
        self.applyPalette(self.palettes[value])

    def on_speed(self,instance,touch):
        if touch.grab_current != None:
            val = int( ((self.speed.value - self.speed.min)/(self.speed.max - self.speed.min))*255 )
            self.app.beem_client.setModeSetting(0,val)


    def applyColor(self, index , colorWidget ):
        H,S,V = colorWidget._hsv[:3]
        H = int(H*255)
        S = int(S*255)
        V = int(V*255)
        print H,S,V
        self.app.beem_client.setColor(index, H,S,V)

    def applyPalette(self, index ):
        self.app.beem_client.setPalette(index)

    def update_mode_com(self,*args):
        pass


class DirectLighting(Mode):

    def __init__(self,app,menu,**kwargs):
        super(DirectLighting,self).__init__(app,menu,**kwargs)

        #Direction
        self.B_lay = BoxLayout( orientation = 'horizontal', size_hint_y = 0.1)
        self.B_lab = Label(text = 'Blue', size_hint_x = 0.2)
        self.B = Slider(min = 0, max = 255, value = 1.0 )
        self.B.bind(on_touch_up  = self.on_B)
        self.B_lay.add_widget( self.B_lab)
        self.B_lay.add_widget( self.B)

        self.R_lay = BoxLayout( orientation = 'horizontal', size_hint_y = 0.1)
        self.R_lab = Label(text = 'Red', size_hint_x = 0.2)
        self.R = Slider(min = 0, max = 255, value = 1.0 )
        self.R.bind(on_touch_up  = self.on_R)
        self.R_lay.add_widget( self.R_lab)
        self.R_lay.add_widget( self.R)

        self.G_lay = BoxLayout( orientation = 'horizontal', size_hint_y = 0.1)
        self.G_lab = Label(text = 'Green', size_hint_x = 0.2)
        self.G = Slider(min = 0, max = 255, value = 1.0 )
        self.G.bind(on_touch_up  = self.on_G)
        self.G_lay.add_widget( self.G_lab)
        self.G_lay.add_widget( self.G)

        self.W_lay = BoxLayout( orientation = 'horizontal', size_hint_y = 0.1)
        self.W_lab = Label(text = 'White', size_hint_x = 0.2)
        self.W = Slider(min = 0, max = 255, value = 1.0 )
        self.W.bind(on_touch_up  = self.on_W)
        self.W_lay.add_widget( self.W_lab)
        self.W_lay.add_widget( self.W)

        self.add_widget(self.B_lay)
        self.add_widget(self.R_lay)
        self.add_widget(self.G_lay)
        self.add_widget(self.W_lay)

    def on_B(self,instance,touch):
        if touch.grab_current != None:
            val = int( instance.value )
            self.app.beem_client.setModeSetting(0,val)

    def on_R(self,instance,touch):
        if touch.grab_current != None:
            val = int( instance.value )
            self.app.beem_client.setModeSetting(1,val)

    def on_G(self,instance,touch):
        if touch.grab_current != None:
            val = int( instance.value )
            self.app.beem_client.setModeSetting(2,val)

    def on_W(self,instance,touch):
        if touch.grab_current != None:
            val = int( instance.value )
            self.app.beem_client.setModeSetting(3,val)

    def update_mode_com(self,*args):
        pass


class ModesMenu( Widget ):
    modes = ListProperty()
    _modes = ListProperty()
    app = ObjectProperty()
    def __init__(self,app,**kwargs):
        super(ModesMenu,self).__init__()
        self.app = app
        self.menuSlider = MenuTabSlider(app)
        self.modeScreenManager = ScreenManager(transition=SwapTransition())

        screen = Screen(name = 'menu')
        screen.add_widget(self.menuSlider)

        self.modeScreenManager.add_widget( screen )
        self.add_widget( self.modeScreenManager )

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def go_home(self):
        self.modeScreenManager.current = 'menu'
        self.app.beem_client.setMode(-1)
        #self.app.sendCommand('GME','SEL','-1')

    def go_screen(self,name):
        self.modeScreenManager.current = name
        inx = self.modes.index( name )
        mode = self._modes[inx]
        #Start Dis Sheee
        if mode:
            mode.activate()
        self.app.beem_client.setMode(inx)
        #self.app.sendCommand('GME','SEL',str(inx))

    def addMode(self,modeName,mode):
        self.modes.append(modeName)
        self.menuSlider.addMenuScreenWidget(modeName,ModeTile(modeName,self))
        screen = Screen(name = modeName)
        screen.add_widget(mode)
        self._modes.append(mode)
        self.modeScreenManager.add_widget( screen )
        self.go_home()


    def update_rect(self, *args):
        self.modeScreenManager.pos = self.pos
        self.modeScreenManager.size = self.size


#if __name__ == '__main__':
#    TESTGAMES = ['Color','Pattern','POV','Position Mode']
#    from config import *
#    class Test(App):
#        settings = SocialSettings()
#        def build(self):
#            modes =  ModesMenu(self)
#            modes.addMode("Ring Of Fury",RingOfFury(self,modes))
#            modes.go_home()
#            return modes
#    tst = Test()
#    tst.run()
