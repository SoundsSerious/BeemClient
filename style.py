# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 22:54:02 2016

@author: Sup

'''#Default KV Image Definition
<Image,AsyncImage>:
    canvas:
        Color:
            rgba: self.color
        Rectangle:
            texture: self.texture
            size: self.norm_image_size
            pos: self.center_x - self.norm_image_size[0] / 2., self.center_y - self.norm_image_size[1] / 2.

#RoundedLabel
        Color:
            rgba:  self.background_color
        RoundedRectangle:
            size: self.texture_size
            pos: self.center[0] - self.texture_size[0]/2.0,self.center[1] - self.texture_size[1]/2.0
            radius: self._radius
        Color:
            rgba:  self.font_color
        Rectangle:
            texture: self.texture
            size: self.texture_size
            pos: self.center[0] - self.texture_size[0]/2.0,self.center[1] - self.texture_size[1]/2.0
            radius: self._radius
'''
"""

from __future__ import absolute_import

from kivy.app import App
from kivy.uix.button import *
from kivy.uix.label import *
from kivy.uix.widget import *
from kivy.uix.boxlayout import *
from kivy.uix.floatlayout import *
from kivy.graphics import *
from kivy.graphics.texture import *
from kivy.graphics.vertex_instructions import *
from kivy.uix.behaviors import *
from kivy.uix.image import *
from kivy.uix.colorpicker import *
from kivy.uix.colorpicker import _ColorArc
from kivy.uix.effectwidget import *
from kivy.core.text import Label as CoreLabel
from kivy.graphics.svg import Svg
from kivy.properties import *
from kivy.graphics.opengl import glFinish
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from math import cos, sin, pi, sqrt, atan


from time import time

from config import *

# -*- coding: utf-8 -*-
from kivy.lang import Builder




Builder.load_string(
'''
<ColorWheel>:
    _origin: self.center
    _radius: 0.45 * min(self.size)

<RoundedButton>:
    border_color: app.settings.BEEMO_BLUE
    background_color: app.settings.OFFWHITE
    canvas.before:
        Color:
            rgb: self.border_color
        RoundedRectangle:
            size: self.size
            pos: self.center[0] - self.size[0]/2.0,self.center[1] - self.size[1]/2.0
            radius: self.radius
        Color:
            rgb: self.background_color

        StencilPush
        RoundedRectangle:
            size: self.size[0]-self.border_width*2, self.size[1]-self.border_width*2
            pos: self.center[0] - (self.size[0]-self.border_width*2)/2.0,self.center[1] - (self.size[1]-self.border_width*2)/2.0
            radius: self.radius
        StencilUse

    canvas.after:
        StencilUnUse
        RoundedRectangle:
            size: self.size[0]-self.border_width*2, self.size[1]-self.border_width*2
            pos: self.center[0] - (self.size[0]-self.border_width*2)/2.0,self.center[1] - (self.size[1]-self.border_width*2)/2.0
            radius: self.radius
        StencilPop

<-RoundedImage>:
    canvas:
        Color:
            rgb: (1, 1, 1)

        StencilPush
        RoundedRectangle:
            size: self.norm_image_size
            pos: self.center[0] - self.norm_image_size[0]/2.0,self.center[1] - self.norm_image_size[1]/2.0
            radius: self._radius
        StencilUse
        Rectangle:
            texture: self.texture
            size: self.norm_image_size
            pos: self.center[0] - self.norm_image_size[0]/2.0,self.center[1] - self.norm_image_size[1]/2.0
        StencilUnUse
        RoundedRectangle:
            size: self.norm_image_size
            pos: self.center[0] - self.norm_image_size[0]/2.0,self.center[1] - self.norm_image_size[1]/2.0
            radius: self._radius
        StencilPop

<-RoundedExpandingImage>:
    canvas:
        Color:
            rgb: (1, 1, 1)

        StencilPush
        RoundedRectangle:
            size: self.size
            pos: self.center[0] - self.size[0]/2.0,self.center[1] - self.size[1]/2.0
            radius: self._radius
        StencilUse
        Rectangle:
            texture: self.texture
            size: self.exp_image_size
            pos: self.center[0] - self.exp_image_size[0]/2.0,self.center[1] - self.exp_image_size[1]/2.0
        StencilUnUse
        RoundedRectangle:
            size: self.size
            pos: self.center[0] - self.size[0]/2.0,self.center[1] - self.size[1]/2.0
            radius: self._radius
        StencilPop

<-SquareExpandingImage>:
    canvas:
        Color:
            rgb: (1, 1, 1)
        #Rectangle:
        #    size: self.size
        #    pos: self.center[0] - self.exp_image_size[0]/2.0,self.center[1] - self.exp_image_size[1]/2.0
        StencilPush
        Rectangle:
            size: self.min_size
            pos: self.center[0] - self.min_size[0]/2.0,self.center[1] - self.min_size[1]/2.0
        StencilUse

        Rectangle:
            texture: self.texture
            size: self.exp_image_size
            pos: self.center[0] - self.exp_image_size[0]/2.0,self.center[1] - self.exp_image_size[1]/2.0

        StencilUnUse
        Rectangle:
            size: self.min_size
            pos: self.center[0] - self.min_size[0]/2.0,self.center[1] - self.min_size[1]/2.0
        StencilPop

<-ExpandingImage>:
    canvas:
        Color:
            rgb: (1, 1, 1)
        #Rectangle:
        #    size: self.size
        #    pos: self.center[0] - self.exp_image_size[0]/2.0,self.center[1] - self.exp_image_size[1]/2.0
        StencilPush
        Rectangle:
            size: self.size
            pos: self.center[0] - self.size[0]/2.0,self.center[1] - self.size[1]/2.0
        StencilUse

        Rectangle:
            texture: self.texture
            size: self.exp_image_size
            pos: self.center[0] - self.exp_image_size[0]/2.0,self.center[1] - self.exp_image_size[1]/2.0

        StencilUnUse
        Rectangle:
            size: self.size
            pos: self.center[0] - self.size[0]/2.0,self.center[1] - self.size[1]/2.0
        StencilPop


<-ExpandingWebImage>:
    canvas:
        Color:
            rgb: (1, 1, 1)
        #Rectangle:
        #    size: self.size
        #    pos: self.center[0] - self.exp_image_size[0]/2.0,self.center[1] - self.exp_image_size[1]/2.0
        StencilPush
        Rectangle:
            size: self.size
            pos: self.center[0] - self.size[0]/2.0,self.center[1] - self.size[1]/2.0
        StencilUse

        Rectangle:
            texture: self.texture
            size: self.exp_image_size
            pos: self.center[0] - self.exp_image_size[0]/2.0,self.center[1] - self.exp_image_size[1]/2.0

        StencilUnUse
        Rectangle:
            size: self.size
            pos: self.center[0] - self.size[0]/2.0,self.center[1] - self.size[1]/2.0
        StencilPop

<-SquareExpandingWebImage>:
    canvas:
        Color:
            rgb: (1, 1, 1)
        #Rectangle:
        #    size: self.exp_image_size
        #    pos: self.center[0] - self.exp_image_size[0]/2.0,self.center[1] - self.exp_image_size[1]/2.0
        StencilPush
        Rectangle:
            size: self.min_size
            pos: self.center[0] - self.min_size[0]/2.0,self.center[1] - self.min_size[1]/2.0
        StencilUse

        Rectangle:
            texture: self.texture
            size: self.exp_image_size
            pos: self.center[0] - self.exp_image_size[0]/2.0,self.center[1] - self.exp_image_size[1]/2.0

        StencilUnUse
        Rectangle:
            size: self.min_size
            pos: self.center[0] - self.min_size[0]/2.0,self.center[1] - self.min_size[1]/2.0
        StencilPop

<-RoundedWebImage>:
    canvas:
        Color:
            rgb:  self.color
        StencilPush
        RoundedRectangle:
            size: self.norm_image_size
            pos: self.center[0] - self.norm_image_size[0]/2.0,self.center[1] - self.norm_image_size[1]/2.0
            radius: self._radius
        StencilUse
        Rectangle:
            texture: self.texture
            size: self.norm_image_size
            pos: self.center[0] - self.norm_image_size[0]/2.0,self.center[1] - self.norm_image_size[1]/2.0
        StencilUnUse
        RoundedRectangle:
            size: self.norm_image_size
            pos: self.center[0] - self.norm_image_size[0]/2.0,self.center[1] - self.norm_image_size[1]/2.0
            radius: self._radius
        StencilPop

<-CircleWebImage>:
    canvas:
        Color:
            rgb:  self.borderColor
        Ellipse:
            size: min(self.norm_image_size), min(self.norm_image_size)
            pos: self.center[0] - min(self.norm_image_size)/2.0,self.center[1] - min(self.norm_image_size)/2.0
        Color:
            rgb:  self.color
        StencilPush
        Ellipse:
            size: min(self.norm_image_size)-self.borderSize, min(self.norm_image_size)-self.borderSize
            pos: self.center[0] - (min(self.norm_image_size)-self.borderSize)/2.0,self.center[1] - (min(self.norm_image_size)-self.borderSize)/2.0
        StencilUse
        Rectangle:
            texture: self.texture
            size: self.norm_image_size[0]-self.borderSize, self.norm_image_size[1] -self.borderSize
            pos: self.center[0] - (self.norm_image_size[0]-self.borderSize)/2.0,self.center[1] - (self.norm_image_size[1]-self.borderSize)/2.0
        StencilUnUse
        Ellipse:
            size: min(self.norm_image_size)-self.borderSize, min(self.norm_image_size)-self.borderSize
            pos: self.center[0] - (min(self.norm_image_size)-self.borderSize)/2.0,self.center[1] - (min(self.norm_image_size)-self.borderSize)/2.0
        StencilPop



<-Icon@ButtonBehavior+SquareExpandingImage>:
    background_color: [1,1,1,1]
    pos_hint: {'center_x':0.5,'bottom':1}
    size: root.size
    size_hint: 1,1
    canvas:
        Color:
            rgba: root.background_color
        Rectangle:
            texture: root.texture
            size: self.norm_image_size
            pos: self.pos[0]+self.width/2 -self.norm_image_size[1]/2 , \
                 self.pos[1]+self.height/2 -self.norm_image_size[1]/2

<-CircularIcon@Icon>:
    edge_color: [0,0,0,1]
    edge_width: 1.5
    background_color: [1,1,1,1]
    pos_hint: {'center_x':0.5,'bottom':1}
    size: root.size
    size_hint: 1,1
    canvas:
        StencilPush
        Ellipse:
            size:root.min_side*2, root.min_side*2
            pos: self.x+(self.max_side-self.min_side*2)/2,self.y-self.height/2
        StencilUse
        Color:
            rgba: root.background_color
        Rectangle:
            texture: root.texture
            size: self.exp_image_size
            pos: self.pos[0]+self.width/2 -self.exp_image_size[1]/2 , \
                 self.pos[1]+self.height/2 -self.exp_image_size[1]/2
        StencilUnUse
        Ellipse:
            size:root.min_side*2, root.min_side*2
            pos: self.x+(self.max_side-self.min_side*2)/2,self.y-self.height/2
        StencilPop
        Color:
            rgba: (0,0,0,0)# root.edge_color
        Line:
            circle: root.center_x-root.edge_width/2,\
                    root.center_y-root.edge_width/2,\
                    root.min_side+root.edge_width
            width: root.edge_width

<MenuPanel@BoxLayout>:
    orientation:'vertical'
    background_color: [1,1,1,1]
    size_hint: 1,1
    width: 120
    spacing:20
    canvas:
        Color:
            rgba: self.background_color
        Rectangle:
            size: self.size
            pos: self.pos

<-RoundedAlighnedTextInput@AlignedTextInput>:
    canvas:
        StencilPush
        RoundedRectangle:
            size: self.size
            pos: self.center[0] - self.size[0]/2.0,self.center[1] - self.size[1]/2.0
            radius: self._radius
        StencilUse
        Color:
            rgba:  self.background_color
        Rectangle:
            size: self.size[0]-self.borderSize, self.size[1] -self.borderSize
            pos: self.center[0] - (self.size[0]-self.borderSize)/2.0,self.center[1] - (self.size[1]-self.borderSize)/2.0
        StencilUnUse
        RoundedRectangle:
            size: self.size
            pos: self.center[0] - self.size[0]/2.0,self.center[1] - self.size[1]/2.0
            radius: self._radius
        StencilPop

<ColorDropDown>:

        ''')

class ColorDownButton(Button):
    """
    Button with a possibility to change the color on on_press (similar to background_down in normal Button widget)
    """
    background_color_normal = ListProperty([1, 1, 1, 0.5])
    background_color_down = ListProperty([1, 1, 1, 1])
    background_color = ListProperty([1,1,1,1])
    text = StringProperty('ColorButton')
    def __init__(self, **kwargs):
        super(ColorDownButton, self).__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color_down = kwargs.get('color_down',self.background_color_down)
        self.background_color_normal = kwargs.get('color_normal',self.background_color_normal)
        self.text = kwargs.get('text','ColorButton')
        self.background_color = self.background_color_normal
        Label.__init__(self,**kwargs)

        #self.bind( size=self.update_rect )

    def _do_press(self):
        super(ColorDownButton, self)._do_press()
        self.background_color = self.background_color_down

    def _do_release(self, *args):
        super(ColorDownButton, self)._do_release(*args)
        self.background_color = self.background_color_normal

    def update_rect(self,*args):
        #print self.size, self.background_color
        pass

class RoundedButton(ColorDownButton):
    '''In which we make a damn button with rounded corners'''

    _radius = ListProperty([20])
    border_width = NumericProperty(5)
    border_color = ListProperty([0.8,0.8,1,1])
    def __init__(self, **kwargs):
        self.border_color = kwargs.get('border_color',[0.8,0.8,1,1])
        self.border_width = kwargs.get('border_width',5)
        self._radius = [float(kwargs.get('radius',20))]*4
        super(RoundedButton,self).__init__(**kwargs)

    @property
    def radius(self):
        return self._radius

class ExpandingImage(Image):

    def get_norm_image_size(self):
        if not self.texture:
            return self.size
        ratio = self.image_ratio
        w, h = self.size
        tw, th = self.texture.size

        # ensure that the width is always maximized to the containter width
        if self.allow_stretch:
            if not self.keep_ratio:
                return w, h
            iw = w
        else:
            iw = min(w, tw)
        # calculate the appropriate height
        ih = iw / ratio
        # if the height is too higher, take the height of the container
        # and calculate appropriate width. no need to test further. :)
        if ih > h:
            if self.allow_stretch:
                ih = h
            else:
                ih = min(h, th)
            iw = ih * ratio

        return iw, ih

    norm_image_size = AliasProperty(get_norm_image_size, None, bind=(
        'texture', 'size', 'image_ratio', 'allow_stretch'))

    def get_exp_background_size(self):
        w,h = self.size
        WT,HT = self.get_norm_image_size()
        if not self.texture:
            return self.size
        wt, ht = self.texture.size

        if HT == 0:
            AR = 1
        else:
            AR = WT/HT
            if AR == 0: AR = 1
        XMx,YMx = max(w,WT),max(h,HT)

        checkPoint = lambda points: all([p<=0 for p in points])
        pointMag = lambda points: min(points[0],0) * min(points[1],0) if checkPoint(points) else 99999999999

        x1 = YMx/AR +1
        y1 = x1/AR +1
        dX1 = (XMx-x1)
        dY1 = (YMx-y1)
        P1 = (dX1,dY1)
        mtch1 = pointMag(P1)

        x2 = XMx+1
        y2 = x2/AR +1
        dX2 = (XMx-x2)
        dY2 = (YMx-y2)
        P2 = (dX2,dY2)
        mtch2 = pointMag(P2)

        y3 = YMx+1
        x3 = y3*AR + 1
        dX3 = (XMx-x3)
        dY3 = (YMx-y3)
        P3 = (dX3,dY3)
        mtch3 = pointMag(P3)

        y4 = XMx/AR + 1
        x4 = y4*AR + 1
        dX4 = (XMx-x4)
        dY4 = (YMx-y4)
        P4 = (dX4,dY4)
        mtch4 = pointMag(P4)

        points = [(x1,y1),(x2,y2),(x3,y3),(x4,y4)]
        dSize = [mtch1,mtch2,mtch3,mtch4]
        index = dSize.index(min(dSize))
        selectedSize = points[index]
        return selectedSize

    exp_image_size = AliasProperty(get_exp_background_size, None, bind=(
        'texture', 'size', 'image_ratio', 'allow_stretch'))

    @property
    def min_side(self):
        mn = min(self.size)
        return mn

    def min_size(self):
        ms = self.min_side
        return ms,ms

    min_size = AliasProperty(min_size, None, bind=(
        'texture', 'size', 'image_ratio', 'allow_stretch'))

class ExpandingWebImage( AsyncImage ):

    def get_norm_image_size(self):
        if not self.texture:
            return self.size
        ratio = self.image_ratio
        w, h = self.size
        tw, th = self.texture.size

        # ensure that the width is always maximized to the containter width
        if self.allow_stretch:
            if not self.keep_ratio:
                return w, h
            iw = w
        else:
            iw = min(w, tw)
        # calculate the appropriate height
        ih = iw / ratio
        # if the height is too higher, take the height of the container
        # and calculate appropriate width. no need to test further. :)
        if ih > h:
            if self.allow_stretch:
                ih = h
            else:
                ih = min(h, th)
            iw = ih * ratio

        return iw, ih

    norm_image_size = AliasProperty(get_norm_image_size, None, bind=(
        'texture', 'size', 'image_ratio', 'allow_stretch'))

    def get_exp_background_size(self):
        w,h = self.size
        WT,HT = self.get_norm_image_size()

        if HT == 0:
            AR = 1
        else:
            AR = WT/HT
            if AR == 0: AR = 1
        XMx,YMx = max(w,WT),max(h,HT)

        checkPoint = lambda points: all([p<=0 for p in points])
        pointMag = lambda points: min(points[0],0) * min(points[1],0) if checkPoint(points) else 99999999999

        x1 = YMx/AR +1
        y1 = x1/AR +1
        dX1 = (XMx-x1)
        dY1 = (YMx-y1)
        P1 = (dX1,dY1)
        mtch1 = pointMag(P1)

        x2 = XMx+1
        y2 = x2/AR +1
        dX2 = (XMx-x2)
        dY2 = (YMx-y2)
        P2 = (dX2,dY2)
        mtch2 = pointMag(P2)

        y3 = YMx+1
        x3 = y3*AR + 1
        dX3 = (XMx-x3)
        dY3 = (YMx-y3)
        P3 = (dX3,dY3)
        mtch3 = pointMag(P3)

        y4 = XMx/AR + 1
        x4 = y4*AR + 1
        dX4 = (XMx-x4)
        dY4 = (YMx-y4)
        P4 = (dX4,dY4)
        mtch4 = pointMag(P4)

        points = [(x1,y1),(x2,y2),(x3,y3),(x4,y4)]
        dSize = [mtch1,mtch2,mtch3,mtch4]
        index = dSize.index(min(dSize))
        selectedSize = points[index]
        return selectedSize

    exp_image_size = AliasProperty(get_exp_background_size, None, bind=(
        'texture', 'size', 'image_ratio', 'allow_stretch'))

    @property
    def min_side(self):
        mn = min(self.size)
        return mn

    def min_size(self):
        ms = self.min_side
        return ms,ms

    min_size = AliasProperty(min_size, None, bind=(
        'texture', 'size', 'image_ratio', 'allow_stretch'))

class SquareExpandingImage(ExpandingImage):
    pass

class SquareExpandingWebImage(ExpandingWebImage):
    pass


class Icon(ButtonBehavior,SquareExpandingImage):
    background_color = ListProperty([1,1,1,1])
    source = StringProperty('icons/uxpin-icon-set_chemistry.png')

    def min_side(self):
        return min(self.size)
    min_side = AliasProperty(min_side,bind=['size'])

    def min_size(self):
        sz = self.min_side
        return (sz,sz)
    min_size = AliasProperty(min_size,bind=['size'])

    def max_side(self):
        return max(self.size)
    max_side = AliasProperty(max_side,bind=['size'])

    def max_size(self):
        sz = self.max_side
        return (sz,sz)
    max_size = AliasProperty(max_size,bind=['size'])

    def __init__(self,**kwargs):
        sc = kwargs.get('source')
        if sc: self.source = sc
        bg = kwargs.get('background_color')
        if bg: self.background_color = bg

        super(Icon,self).__init__(**kwargs)
        SquareExpandingImage.__init__(self,mipmap=True,**kwargs)

        self.bind( size = self.update_rect)

    def update_rect(self,*args):
        #print self.size, self.min_side
        pass




class RoundedImage(Image):

    _radius_pct = 0.2
    _radius = ListProperty([20])

    def __init__(self,**kwargs):
        self._radius_pct = kwargs.get('radius_pct',0.1)
        self.radius_cmd()
        super(RoundedImage,self).__init__(**kwargs)
        self.bind(size = self.radius_cmd)

    def center_image(self, *args):
        print 'centering'
        x,y = self.center
        self.pos =   x - self.norm_image_size[0]/2.0,\
                    y - self.norm_image_size[1]/2.0

    def radius_cmd(self,*args):
        self._radius = [self.height * self._radius_pct]


class RoundedExpandingImage(RoundedImage):

    def get_exp_background_size(self):
        w,h = self.size
        WT,HT = self.get_norm_image_size()

        if HT == 0:
            AR = 1
        else:
            AR = WT/HT
            if AR == 0: AR = 1
        XMx,YMx = max(w,WT),max(h,HT)

        checkPoint = lambda points: all([p<=0 for p in points])
        pointMag = lambda points: min(points[0],0) * min(points[1],0) if checkPoint(points) else 99999999999

        x1 = YMx/AR +1
        y1 = x1/AR +1
        dX1 = (XMx-x1)
        dY1 = (YMx-y1)
        P1 = (dX1,dY1)
        mtch1 = pointMag(P1)

        x2 = XMx+1
        y2 = x2/AR +1
        dX2 = (XMx-x2)
        dY2 = (YMx-y2)
        P2 = (dX2,dY2)
        mtch2 = pointMag(P2)

        y3 = YMx+1
        x3 = y3*AR + 1
        dX3 = (XMx-x3)
        dY3 = (YMx-y3)
        P3 = (dX3,dY3)
        mtch3 = pointMag(P3)

        y4 = XMx/AR + 1
        x4 = y4*AR + 1
        dX4 = (XMx-x4)
        dY4 = (YMx-y4)
        P4 = (dX4,dY4)
        mtch4 = pointMag(P4)

        points = [(x1,y1),(x2,y2),(x3,y3),(x4,y4)]
        dSize = [mtch1,mtch2,mtch3,mtch4]
        index = dSize.index(min(dSize))
        selectedSize = points[index]
        return selectedSize


    exp_image_size = AliasProperty(get_exp_background_size, None, bind=(
        'texture', 'size', 'image_ratio', 'allow_stretch'))


class RoundedWebImage(AsyncImage):

    _radius_pct = 0.5
    _radius = [20]

    def __init__(self,**kwargs):
        super(RoundedWebImage,self).__init__(**kwargs)
        self.bind(size = self.radius_cmd)

    def center_image(self, *args):
        print 'centering'
        x,y = self.center
        self.pos =   x - self.norm_image_size[0]/2.0,\
                    y - self.norm_image_size[1]/2.0

    def radius_cmd(self,*args):
        #if self.height:
        self._radius = [self.height * self._radius_pct]
        #else:
        #    return [10]



#
class CircleWebImage(AsyncImage):

    _radius_pct = 0.5
    _radius = [20]

    borderColor = (1,1,1)
    borderSize = 5

    def __init__(self,**kwargs):
        super(CircleWebImage,self).__init__(**kwargs)
        self.bind(size = self.radius_cmd)

    def center_image(self, *args):
        print 'centering'
        x,y = self.center
        self.pos =   x - self.norm_image_size[0]/2.0,\
                    y - self.norm_image_size[1]/2.0

    def radius_cmd(self,*args):
        #if self.height:
        self._radius = [self.height * self._radius_pct]


class RoundedLabel(Label):
    _radius_pct = 0.8
    _radius = [10]
    maxrad = 10

    _font_color = None
    _background_color = None

    _max_width = 300

    def __init__(self,**kwargs):
        super(RoundedLabel,self).__init__(size_hint=(1,1),**kwargs)

        #Get Some Inputs
        self._max_width = kwargs.get('max_width',300)
        self._background_color = kwargs.get('background_color',(0,0.2,0.4,1))
        self._font_color = kwargs.get('font_color',(0.8,1,1,1))

        #Set Some Defaults
        self.size_hint_y =  None
        self.text_size = self._max_width, None
        self.height =  self.texture_size[1]

        #Canvas FTW
        with self.canvas:
            Color(*self._background_color)
            self.rect = RoundedRectangle(size = self.box_size,pos= self.box_pos,\
                                        radius = self._radius)
            Color(*self._font_color)
            self.text_rect = Rectangle( texture = self.texture, size = self.texture_size,\
                                   pos = self.txt_pos)

        #callbacks, to be binded
        self.bind(pos = self.update_rect,
                  size = self.update_rect)

        self.update_rect()

    @property
    def justified_x(self):
        if self.halign == 'right':
            val =  self.width - (self.texture_size[0]+self._radius[0])
        elif self.halign == 'center':
            val  =  0
        elif self.halign == 'left':
            val =  2
        return val

    @property
    def box_size(self):
        return self.texture_size[0] + self._radius[0]- 2,\
                  self.texture_size[1] + self._radius[0] -2

    @property
    def box_pos(self):
        val =  self.justified_x  ,\
                 self.center[1] - self.texture_size[1]/2.0
        return val

    @property
    def txt_pos(self):
        val = self.justified_x  + self._radius[0]/2.0,\
                 self.center[1] - self.texture_size[1]/2.0 + self._radius[0]/2.0
        return val

    def update_rect(self,*args):
        self.texture_update()
        self.height =  self.texture_size[1] + self._radius[0]
        rad = self.texture_size[1] * self._radius_pct
        if rad > self.maxrad:
            self.rect.radius = [self.maxrad]
        else:
            self.rect.radius = [rad]
        self.rect.size = self.box_size
        self.rect.pos =  self.box_pos

        self.text_rect.pos = self.txt_pos
        self.text_size = self._max_width , None
        self.text_rect.size = self.texture_size
        self.text_rect.texture = self.texture
        #print self.size, self.pos, self
        #print self.text_rect.size, self.text_rect.pos,self.txt_pos,self.texture_size,  repr(self.text)
        #print self.rect.size, self.rect.pos, self.box_pos, self.box_size, repr(self.text)


DEFAULT_PADDING = 0
class AlignedTextInput(TextInput):

    halign = StringProperty('left')
    valign = StringProperty('top')

    def __init__(self, **kwargs):
        self.halign = kwargs.get("halign", "left")
        self.valign = kwargs.get("valign", "top")

        self.bind(on_text=self.on_text)
        self.bind(focus=self.on_focus)
        super(AlignedTextInput,self).__init__(**kwargs)

    def on_text(self, instance, value):
        self.redraw()

    def on_size(self, instance, value):
        self.redraw()

    def on_focus(self,instance,value):
        self.redraw()

    @property
    def max_size(self):

#        if self.focus:
#            return max(self._lines_rects, key=lambda r: r.size[0]).size
        if self.text != '':
            return max(self._lines_rects, key=lambda r: r.size[0]).size
        else:
            return max(self._hint_text_rects, key=lambda r: r.size[0]).size


    def redraw(self):
        """
        Note: This methods depends on internal variables of its TextInput
        base class (_lines_rects and _refresh_text())
        """
        self._refresh_text(self.text)

        num_lines = len(self._lines_rects)

        px = [DEFAULT_PADDING, DEFAULT_PADDING]
        py = [DEFAULT_PADDING, DEFAULT_PADDING]

        if self.halign == 'center':
            d = (self.width - self.max_size[0]) / 2.0 - DEFAULT_PADDING
            px = [d, d]
        elif self.halign == 'right':
            px[0] = self.width - self.max_size[0] - DEFAULT_PADDING

        if self.valign == 'middle':
            d = (self.height - self.max_size[1] * num_lines) / 2.0 - DEFAULT_PADDING
            py = [d, d]
        elif self.valign == 'bottom':
            py[0] = self.height - self.max_size[1] * num_lines - DEFAULT_PADDING

        self.padding_x = px
        self.padding_y = py

class AutonomousColorWheel(ColorWheel):
    _piece_divisions = NumericProperty(20)
    _pieces_of_pie = NumericProperty(40)
    _min_radius = NumericProperty(5)
    def __init__(self, **kwarg):
        pdv = self._piece_divisions
        self.sv_s = [(float(x) / pdv, 1) for x in range(pdv)] + [
            (1, float(y) / pdv) for y in reversed(range(pdv))]
        super(AutonomousColorWheel, self).__init__(**kwarg)
        self.init_wheel(dt = 0)

        self.bind(on_size = self.update_rect, \
                  on_pos = self.update_rect)

    def on__origin(self, instance, value):
        #App.get_running_app().log('On Origin {}'.format(value))
        self.init_wheel(None)

    def on__radius(self, instance, value):
        #App.get_running_app().log('On Radius {}'.format(value))
        self.init_wheel(None)

    def init_wheel(self, dt):
        # initialize list to hold all meshes
        self.canvas.clear()
        self.arcs = []
        self.sv_idx = 0
        pdv = self._piece_divisions
        ppie = self._pieces_of_pie

        for r in range(pdv):
            for t in range(ppie):
                if r == 0:
                    self.arcs.append(
                        _ColorArc(
                            self._radius * (float(r) / float(pdv)),
                            self._min_radius + self._radius * (float(r + 1) / float(pdv)),
                            2 * pi * (float(t) / float(ppie)),
                            2 * pi * (float(t + 1) / float(ppie)),
                            origin=self._origin,
                            color=(float(t) / ppie,
                                   self.sv_s[self.sv_idx + r][0],
                                   self.sv_s[self.sv_idx + r][1],
                                   1)))
                else:
                    self.arcs.append(
                        _ColorArc(
                            self._min_radius + self._radius * (float(r) / float(pdv)),
                            self._min_radius + self._radius * (float(r + 1) / float(pdv)),
                            2 * pi * (float(t) / float(ppie)),
                            2 * pi * (float(t + 1) / float(ppie)),
                            origin=self._origin,
                            color=(float(t) / ppie,
                                   self.sv_s[self.sv_idx + r][0],
                                   self.sv_s[self.sv_idx + r][1],
                                   1)))

                self.canvas.add(self.arcs[-1])

    def update_rect(self,instance,value):
        w,h = self.size
        x,y = self.pos


        self._origin = (x + w/2, y+h/2)
        self._radius = min([(w/2),(h/2)])

        #App.get_running_app().log('Update Rect: {},{},{},{}'.format(x,y,w,h))

    # def on__hsv(self, instance, value):
    #     super(AutonomousColorWheel, self).on__hsv(instance, value)


class CircularIcon(Icon):
    pass

class MenuPanel(BoxLayout):
    pass

class RoundedAlighnedTextInput(AlignedTextInput):
    _radius = [20]
    border_Size=1
    pass

app = None

def halowarld(*args):
    print 'helllllloo {}'.format(args)

if __name__ == '__main__':
    global app
    class KivyApp(App):
        def build(self):
            tex = 'Some Text '*10+'\n'
            tex *= 5
            lay = BoxLayout(orientation='vertical')
            with lay.canvas:
                Color(1,1,1,1)
                Rectangle(size=lay.size)
            lay.add_widget(CircularIcon(source=r'C:\Users\Sup\Dropbox\workspace\Exposure\app\icons\uxpin-icon-set_add_user.png'))
#            lay.add_widget(RoundedLabel(text = 'Hey Hey How Are You?',halign='right',\
#                                        background_color = (1,1,1,0.8),\
#                                        font_color = (0,0.2,0.5)))
#            lay.add_widget(RoundedLabel(text = 'Hey Hey How Are You?',halign='left',\
#                                        background_color = (1,1,1,0.8),\
#                                        font_color = (0,0.2,0.5)))
#            lay.add_widget(RoundedLabel(text = 'Hey Hey How Are You?',halign='left',\
#                            background_color = (1,1,1,0.8),\
#                            font_color = (0,0.2,0.5)))
            buton = RoundedButton(text='ehhhelloo')
            buton.bind(on_press =halowarld)
            #lay.add_widget(buton)
            return lay

    app = KivyApp()
    app.run()

#TEXTURE = 'kiwi.jpg'
#YELLOW = (1, .7, 0)
#ORANGE = (1, .45, 0)
#RED = (1, 0, 0)
#WHITE = (1, 1, 1)

#class Theme(object):
#    '''In Which We Color Our Application'''
#    pass
#
#
#class Style(object):
#    font_size = 100
#    font_color = (1,1,1)
#
#class RadialGradientStyleist(Style):
#    '''In Which We Color Objects With A Radial Gradient'''
#
#    _color1 = (1, 1, 0)
#    _color2 = (1, 0, 0)
#    _tex_size = (64, 64)
#    _shader = '''
#        $HEADER$
#        uniform vec3 border_color;
#        uniform vec3 center_color;
#        void main (void) {
#            float d = clamp(distance(tex_coord0, vec2(0.5, 0.5)), 0., 1.);
#            gl_FragColor = vec4(mix(center_color, border_color, d), 1);
#        }
#        '''
#
#    @property
#    def radial_gradient(self):
#
#        fbo = Fbo(size=self._tex_size)
#        fbo.shader.fs = self._shader
#
#        # use the shader on the entire surface
#        fbo['border_color'] = map(float, self._color1)
#        fbo['center_color'] = map(float, self._color2)
#        with fbo:
#            Color(1, 1, 1)
#            Rectangle(size=self._tex_size)
#        fbo.draw()
#
#        return fbo.texture
#
#    def __call__(self):
#        return self.radial_gradient
#
#class StyleUnit(object):
#    '''In Which We Color Objects'''
#
#    _styleist = None
#    _style = None
#    def initalizeStyle(self):
#        if self._styleist:
#            glFinish()
#            self._style = self._styleist()
#            glFinish()
