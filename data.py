# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 13:26:26 2017

@author: Cabin
"""

from kivy.lang import Builder
from plyer import gps
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *
from kivy.event import *
from kivy.clock import Clock, mainthread

from kivy.clock import Clock
from kivy.graphics import Color, Point, Mesh
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import *

from log import RingBuffer
from graph import Graph, MeshLinePlot, Plot, LinePlot

from kivy.graphics.context_instructions import *
import traceback



class RealTimeGraph(Widget):

    _max = 100
    _amin,_amax = -4, 4

    _ytick = 1


    def __init__(self,ymin=-1,ymax=1,pmax=1000,ytick = 1,**kwargs):
        super(RealTimeGraph,self).__init__(**kwargs)
        self._amin , self._amax = ymin, ymax
        self._max = pmax
        self._ytick= ytick
        self._inx = 0

        #self.bind(size = self.update_rect)

        self._buffer = RingBuffer(self._max)
        super(RealTimeGraph,self).__init__(**kwargs)
        self.graph =    Graph(xlabel='X', ylabel='Y', x_ticks_minor=self._max / 8,
                        x_ticks_major=self._max / 4, y_ticks_major=self._ytick, y_grid_label=True,
                        x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                        xmin=-0, xmax=self._max, ymin=self._amin, ymax=self._amax,
                        label_options = {'color': [0,0,0,1]})

#        with self.graph.canvas.before:
#            PushMatrix()
#            Rotate(angle=-90, origin=self.graph.pos)
#
#        with self.graph.canvas.after:
#            PopMatrix()

        self.bind(size = self.update_rect, pos = self.update_rect)

        self.graph.background_color = [1,1,1,1]
        self.graph.border_color = [0,0,0,1]
        self.graph.tick_color = [0.75,0.75,0.75,1]
        self.plot_x = MeshLinePlot(color=[0.3, 1, 0.3, 1])
        self.plot_x.mode ='points'
        self.plot_y = MeshLinePlot(color=[1, 0, 0.3, 1])
        self.plot_y.mode ='points'
        self.plot_z = MeshLinePlot(color=[0.3, 0, 1, 1])
        self.plot_z.mode = 'points'

        self.graph.add_plot(self.plot_x)
        self.graph.add_plot(self.plot_y)
        self.graph.add_plot(self.plot_z)

        self.add_widget(self.graph)

        for i in range(100):
            self.addData(i/100.0,-i/100.0+1,0)

    def update_rect(self,*args):
        self.graph.size = self.size
#        print self.size, self.graph.size
#        print self.center, self.graph.center
#        size = self.graph.size
#        self.graph.size = self.size[1],self.size[0]
#        self.graph.pos = self.pos[0]-self.graph.size[0],self.pos[1]#+self.graph.size[1]
#        print self.size, self.graph.size
#        print self.center, self.graph.center

    def addData(self,x,y,z):
        self._inx += 1
        if self._inx > self._max:
            self._inx = 0
        self._buffer.append( (self._inx, x, y, z) )

        i_,x_,y_,z_ = zip(*self._buffer.get())

        self.plot_x.points = zip(i_,x_)
        self.plot_y.points = zip(i_,y_)
        self.plot_z.points = zip(i_,z_)

Builder.load_string('''
<MotionData@Widget>:
    BoxLayout:
        id:lay
        orientation: 'vertical'
        Label:
            text: root.gps_location
        Label:
            height: 10
            text: root.gps_status
        Label:
            height: 10
            text: root.ble_string
        Label:
            height: 10
            text: root.cal_rssi
        Label:
            height: 10
            text: root.distance_str
        BoxLayout:
            size_hint_y: None
            height: '48dp'
            padding: '4dp'
            ToggleButton:
                text: 'Start' if self.state == 'normal' else 'Stop'
                on_state:
                    root.start(1000, 0) if self.state == 'down' else \
                    root.stop()
        BoxLayout:
            size_hint_y: None
            height: '48dp'
            padding: '4dp'
            ToggleButton:
                text: 'Calibrate'
                on_press:
                    root.calibrate_ble()

''')

class MotionData(Widget):

    #Utilities Logic
    gps_status = StringProperty()
    gps_active = False

    ble = ObjectProperty()
    bluetooth_active = False
    ble_poll = None

    #BLE Signal Strenght & Distance
    ble_rssi = NumericProperty()
    ble_string = StringProperty('BLE:')
    rssi_cal_m1 = NumericProperty(-45.0)


    #Motion Data:
    lat = NumericProperty()
    lon = NumericProperty()
    speed = NumericProperty()
    altitude = NumericProperty()
    bearing = NumericProperty()
    accuracy = NumericProperty()
    est_distance = NumericProperty()
    gps_location = StringProperty('GPS LOC:')
    distance_str = StringProperty('DIST:')
    cal_rssi = StringProperty('CAL:')

    GPS_RATE = 1000 #ms
    BLE_RATE = 10 #ms

    ENF = 2.0
    rssi_alpha = 0.975

    app = ObjectProperty()

    def __init__(self,app,**kwargs):
        super(MotionData,self).__init__(**kwargs)
        self.app = app
        try:
            #pyobjus.dylib_manager.load_framework('LibKivyBLE.framework')
            if platform == 'ios':
                import pyobjus
                pyobjus.dylib_manager.load_dylib('LibKivyBLE.dylib')
                kvble = pyobjus.autoclass('KivyBLE')
                self.ble = kvble.alloc().init()
                self.bluetooth_active = True
        except Exception as e:
            print e
            self.bluetooth_active = False
        try:
            gps.configure(on_location=self.on_location,
                          on_status=self.on_status)
            self.gps_active = True
        except NotImplementedError:
            print 'GPS is not implemented for your platform'
            self.gps_active = False

        self.lay = self.ids['lay']
        self.bind(size = self.update_rect, pos = self.update_rect)

    def poll_BLE_RSSI(self):
        self.ble_poll = Clock.schedule_interval(self.get_rssi, self.BLE_RATE/1000.0)


    def stop_BLE_Poll(self):
        Clock.unschedule( self.ble_poll )
        self.ble_poll = None

    def get_rssi(self,dt):
        rssi = self.ble.getFrisbeemRSSI()
        if rssi:
            new_rssi = float(rssi.doubleValue())

            #Use Low Pass Filter
            self.ble_rssi = self.rssi_alpha*self.ble_rssi + (1.0-self.rssi_alpha)*new_rssi

            #Calc Distance
            self.est_distance = 10.0**((self.rssi_cal_m1 - self.ble_rssi)/(10.0 * self.ENF))
            self.app.distance = self.est_distance

    def calibrate_ble(self):
        self.rssi_cal_m1 = self.ble_rssi
        self.cal_rssi = 'Calibrate Value: {}'.format(self.rssi_cal_m1)

    def on_ble_rssi(self,instance ,value):
        self.ble_string = "Frisbeem RSSI: {:3.4f}".format( value )

    def on_est_distance(self,instance,value):
        self.distance_str = "Frisbeem Dist: {:3.4f}".format( value )

    def on_rssi_cal_m1(self,instance,value):
        self.cal_rssi = "Cal RSSI: {:3.4f}".format( value )


    def start(self, minTime, minDistance):
        if self.gps_active:
            gps.start(minTime, minDistance)
        if self.bluetooth_active:
            self.ble.startTheScan()
            self.poll_BLE_RSSI()

    def stop(self):
        if self.gps_active:
            gps.stop()
        if self.bluetooth_active:
            self.ble.stopTheScan()
            self.stop_BLE_Poll()

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])
        if 'lat' in kwargs:
            self.lat = kwargs['lat']
        if 'lon' in kwargs:
            self.lon = kwargs['lon']
        if 'altitude' in kwargs:
            self.altitude = kwargs['altitude']
        if 'speed' in kwargs:
            self.speed = kwargs['speed']
        if 'bearing' in kwargs:
            self.bearing = kwargs['bearing']
        if 'accuracy' in kwargs:
            self.gps_accuracy = kwargs['accuracy']

        #Update App
        self.app.lat = self.lat
        self.app.lon = self.lon

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def on_pause(self):
        gps.stop()
        return True

    def on_resume(self):
        gps.start(1000, 0)
        pass

    def update_rect(self,instance,value):
        self.lay.size = self.size



if __name__ == '__main__':
    from math import sin
    from kivy.app import App

    class DataApp(App):
        time = 0
        x = 0
        def build(self):
            self.graph = RealTimeGraph()
            Clock.schedule_interval(self.updatePlot,1)

            return self.graph

        def updatePlot(self,dt):
            self.time += dt
            self.graph.addData( sin( (self.time/5.0) / 10.) , \
                                sin( (self.time/3.0) / 15.), \
                                sin( (self.time/7.0) / 15.))
            Clock.schedule_interval(self.updatePlot,0.1)

    DataApp().run()

#if __name__ == '__main__':
#    app = GpsTest()
#    app.run()