import os
try:
    user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
except KeyError:
    user_paths = []

print 'PYTHON PATH {}'.format( user_paths)

from kivy.support import install_twisted_reactor
install_twisted_reactor()

from zope.interface import implements, implementer, Interface

from twisted.internet import reactor
from twisted.internet import task
from twisted.protocols import basic
from twisted.cred import credentials
from twisted.internet.protocol import Protocol, ReconnectingClientFactory

from kivy.loader import Loader
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import *
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.settings import *
from kivy.uix.screenmanager import ScreenManager, Screen, FallOutTransition, \
                                    FadeTransition, RiseInTransition
from kivy.properties import *
from kivy.clock import Clock
from kivy.app import App
from kivy.config import ConfigParser, Config
from kivy.utils import *

#from kivy.garden.smaa import SMAA
#from navigationdrawer import NavigationDrawer

from config import *
from style import *
#from maps import *
from menus import *
from login import *
from modes import *
#from message import *
#from profiles import *
#from data import *
#from camera import *
from social_interface import *

from log import BufferLog
from beem import *


Loader.num_workers = 5

#class ProfileMenu(MenuBar):
#
#    def __init__(self,app,**kwargs):
#        super(ProfileMenu,self).__init__(app,**kwargs)
#
#        fref = weakref.ref(self.app.friends)
#        pref = weakref.ref(self.app.projects)
#
#        self.app.fbind('user_id',self.bind_profile_to_id)
#
#        self.profile = DetailedProfileView()
#        self.messages = UserListView(ref=fref)
#        self.roles =    UserListView(ref=fref)
#        self.projects = ProjectListView(ref=pref)
#        self.addMenuScreenWidget('overview',self.profile,**but_opt)
#        self.addMenuScreenWidget('roles',self.roles,**but_opt)
#        self.addMenuScreenWidget('projects',self.projects,**but_opt)
#        self.addMenuScreenWidget('messages',self.messages,**but_opt)
#
#    def bind_profile_to_id(self,inst,val):
#        self.profile.primary_key = val

#class ProjectsMenu(MenuBar):
#
#    def __init__(self,app,**kwargs):
#        super(ProjectsMenu,self).__init__(app,**kwargs)
#
#        fref = weakref.ref(self.app.friends)
#        pref = weakref.ref(self.app.projects)
#
#        lpref = weakref.ref(self.app.local_projects)
#
#        self.map = MapWidget(self)
#        self.local_proj_map_layer = ProjectMapView(maps = self.map,ref=lpref)
#
#
#        for screen in ('map','nearby','your projects','make'):
#            print screen
#            if screen == 'map':
#                self.addMenuScreenWidget(screen,self.map,**but_opt)
#            elif screen == 'your projects':
#                project_view = MenuTabSlider(self,size_hint=(1,1))
#                for _screen in ('overview','crew chat','crew list','auditions','edit'):
#                    if _screen in ('crew list','crew chat','auditioins'):
#                        project_view.addMenuScreenWidget(_screen,UserListView(ref=fref))
#                    else:
#                        project_view.addMenuScreenWidget(_screen,ProjectListView(ref=pref))
#                self.addMenuScreenWidget(screen,project_view,**but_opt)
#            else:
#                self.addMenuScreenWidget(screen,ProjectListView(ref=pref),**but_opt)
#




class SettingsWidget(MenuBar):

     pages = ['settings','log']

     _log = ObjectProperty(None)
     settings = ObjectProperty(None)

     def __init__(self,app,**kwargs):
         super(SettingsWidget,self).__init__(app,**kwargs)

         self.config = ConfigParser()
         self.config.read('myconfig.ini')
         self.build_config( self.config )

         self.addMenuScreenWidget('menu',self.app.open_settings,**self.app.settings.but_opt)

         self._log = BufferLog(self, 100)
         self._log.addText( 'hello beemo' )
         self.addMenuScreenWidget('log',self._log,**self.app.settings.but_opt)

         #self.sensors =  MotionData(self.app)
         #self.sensors.start(1000.0,0)
         #self.addMenuScreenWidget('Data',self.sensors,**self.app.settings.but_opt)

         #Add Button
         self.connect_button = Button(text = 'Connect', on_press = self.connect_to_server,size_hint=(1,0.1))
         self.add_widget(self.connect_button)


     def build_config(self, config):
         config.setdefaults('section1', {
             'key1': 'value1',
             'key2': '42'
         })

     def connect_to_server(self,*args):
         self.app.beem_client.retry_connection()

     def log(self, text):
         '''Call Back From BEEM'''
         #We add text to BufferLog
         self._log.addText( text )


class FrisbeemHomeWidget(SocialHomeWidget):
    '''Manages Creen Widgets With Application Drawer'''

    app = None
    initialized = False

    info= ObjectProperty(None)
    games = ObjectProperty(None)
    settings = ObjectProperty(None)

    def __init__(self, app, **kwargs):
        self.touch_accept_width=50
        super(FrisbeemHomeWidget,self).__init__(app,**kwargs)


    def initialize(self):
        print 'initializing'

        #self.profile = ProfileMenu(self.app)
        #self.projects = ProjectsMenu(self.app)
        #self.casting = CastingMenu(self.app)
        self.games = ModesMenu(self.app)
        TESTGAMES = ['Flicker','Solid Color', 'Flash Lighting',\
                     'Dynamic Lighting','Gradient Lighting','Flicker Palette',\
                     'Press Flash']#,'Pattern','POV',]
        for game in TESTGAMES:
            if game == 'Solid Color':
                g = ColorPicking(self.app,self.games)
            elif game == 'Press Flash':
                g = Flash(self.app,self.games)
            elif game == 'Flicker':
                g = Flicker(self.app,self.games)
            elif game == 'Flicker Palette':
                g = FlickerPalette(self.app,self.games)
            elif game == 'Flash Lighting':
                g = ColorPicking(self.app,self.games)
            elif game == 'Dynamic Lighting':
                g = DynamicLighting(self.app,self.games)
            elif game == 'Gradient Lighting':
                g = GradientLighting(self.app,self.games)
            else:
                g = Mode(self.app,self.games)
            self.games.addMode(game,g)
        self.games.go_home()
        self.settings = SettingsWidget(self.app)
        #self.world =  MapWidget(self.app)
        #self.camera = CameraWidget()
        games_icon = CircularIcon(source=self.app.settings.GAMES_ICON,\
                                    **self.app.settings.icon_opt)
        # info_icon = CircularIcon(source=self.app.settings.INFO_ICON,\
        #                             **self.app.settings.icon_opt)
        settings_icon = CircularIcon(source=self.app.settings.SETTINGS_ICON,\
                                         **self.app.settings.icon_opt)
        logout_bttn = RoundedButton(text='logout',**self.app.settings.but_opt)
        self.addMenuScreenWidget('Modes',games_icon,self.games,**self.app.settings.font_opts)
        #self.addMenuScreenWidget('World',info_icon,self.world,**self.app.settings.font_opts)
        self.addMenuScreenWidget('Settings',settings_icon,self.settings,\
                                            **self.app.settings.font_opts)
        self.addMenuScreenWidget('',logout_bttn,Widget())


    def update_on_local_users(self,instance,local_users):
        pass

    def update_on_friends(self,instance,friends):
        pass

    def checkUidThenFire(self,instance,userId):
        pass

    def edit_user_info(self,*args,**kwargs):
        print 'hey hey whats going on...(im getting edited)'





class FrisbeemApp(SocialApp):

    #User Private Relationships
    friends = ListProperty(None)
    projects = ListProperty(None)

    #User Public Relationships
    local_users = ListProperty(None)
    local_projects = ListProperty(None)

    distance = NumericProperty()
    kalman_pos = NumericProperty()
    lat = NumericProperty()
    lon = NumericProperty()

    beem_client = ObjectProperty(None)
    socialWidget = ObjectProperty(None)

    _mesh_locilization = None

    def auth_handler(self, *args):
        if self.authenticated == False:
            self.loginScreenManager.current = 'login'
        else:
            self.loginScreenManager.current = 'app'
            #reactor.callLater(1,self.startUpdate)


    def setupMainScreen(self):
        self.loginScreenManager = ScreenManager(transition=FadeTransition())

        self.loginScreen = Screen(name = 'login')
        self.login = Login(self, self.settings.LOCAL_IMAGE, require_login= False)
        self.loginScreen.add_widget(self.login)

        self.appScreen = Screen(name = 'app')

        self.loginScreenManager.add_widget( self.loginScreen)
        self.loginScreenManager.add_widget( self.appScreen)

        self.loginScreenManager.current = 'login'
        self.bind(authenticated = self.auth_handler)
        self.bind(social_client = self.on_social_client)
        #Kickoff
        self.auth_handler()

        self.socialWidget = FrisbeemHomeWidget(self)
        self.appScreen.add_widget(self.socialWidget)

        return self.loginScreenManager

    def update_client(self,deffered):
        self.log('updating client')
        #Pass User Id
        deffered.addCallback(self.get_user_info)
        deffered.addCallback(self.get_friends)
        deffered.addCallback(self.get_local_users)
        deffered.addCallback(self.get_local_projects)
        deffered.addCallback(self.get_projects)

    def schedule_update(self,*args):
        '''Gets Called After Connection To Beem'''
        Clock.schedule_once(self.get_beem_config_settings,2.5)

        self._mesh_reporter = task.LoopingCall( self.beem_client.getMeshReport )
        self._mesh_reporter.start(10.0)

    def log(self, text):
        '''Call Back From BEEM'''
        #We add text to BufferLog
        pre = 'LOG: {}'
        if self.socialWidget:
            self.socialWidget.settings.log( text )
        else:
            pre = 'NO LOG: {}'
        print pre.format(text)

    def connectToServer(self):
        #Call back cus argument
        reactor.connectTCP(self._mesh_locilization.SERVER_IP, self._mesh_locilization.LOCAL_PORT, self.beem_client)

    def build_config(self, config):
        config.setdefaults('light', {'power': 1,'temp': 5500,'brightness':50} )

    def build_settings(self, settings):
        settings.add_json_panel("Beem Settings", self.config, data="""
        [
            {"type": "bool",
            "title": "Power",
            "section": "light",
            "key": "power",
            "true": "auto"
            },
            {"type": "numeric",
            "title": "Temperature [1900-10000]",
            "section": "light",
            "key": "temp"
            },
            {"type": "numeric",
            "title": "Brightness [0-100]",
            "section": "light",
            "key": "brightness"
            }
        ]"""
        )

    def on_config_change(self, config, section, key, value):
        self.send_beem_config_settings()

    def send_beem_config_settings(self):
        power = self.config.getint('light','power')
        brightness = self.config.getint('light','brightness')
        temp = self.config.getint('light','temp')
        self.beem_client.setSettings(power,temp,brightness)

    def get_beem_config_settings(self,*args):
        self.beem_client.getSettings()

    def applySettings(self,settingsText):
        settings = json.loads( settingsText )
        self.config.set('light', 'brightness', int(100 * settings['brightness']))
        self.config.set('light', 'temp', settings['temp'])
        self.config.set('light', 'power',  settings['power'])

    def setupNetworkServices(self):
        self.log( "starting rectors capin\'")

        self._mesh_locilization = MeshLocalization(self)

        self.beem_client = BeemoClient( self, self._mesh_locilization)
        self.beem_client.utf8validateIncoming = False
        #reactor.connectTCP(self._mesh_locilization.SERVER_IP, self._mesh_locilization.LOCAL_PORT, self.beem_client)
        #self.log('Starting MDNS Name Service')
        #d = broadcast(reactor, "_beem._tcp", PORT+1, "beemo_dev")
        #d.addCallback(broadcasting)
        #d.addErrback(failed)



if __name__ == '__main__':
    app = FrisbeemApp()

    #Do App Setup Stuff
    Config.set('graphics','resizable',0)
    Config.set('graphics', 'width', str(app.settings.SCREEN['width']))
    Config.set('graphics', 'height', str(app.settings.SCREEN['height']))
    #Import Window Right Before Use
    from kivy.core.window import Window
    print Window.size

    if platform in ('win','linux','macosx'):
        Window.size = (app.settings.SCREEN['width'],app.settings.SCREEN['height'])
    else:
        Window.size = (app.settings.SCREEN['width'],app.settings.SCREEN['height'])
    print Window.size

    app.run()
