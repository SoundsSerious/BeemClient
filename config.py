#Define EXP_PATH
import os
from kivy import resources
import random
from glob import glob
import sys
from kivy.loader import Loader
from kivy.utils import platform
from kivy.uix.image import Image

sys.path.append('../')

class SocialSettings(object):
    #CUR_URL = '127.0.0.1'
    #SOCIAL_PORT = 17776
    WEB_PORT = 8888

    SOCIAL_PORT = 18330
    CUR_URL = '192.168.4.1'

    SCREEN = {'width':324 , 'height': 640}
    SMALL_SCREEN = {'width':324 , 'height': 640}



    dropboxpath = os.path.join('Dropbox','workspace','Beem','Beem','code','BeemoClient_V1')
    if platform == 'macosx':
        HOME_URL = 'localhost'
        EXP_PATH = os.path.join(os.path.expanduser('~'),dropboxpath)
        ENG_STR = 'postgresql://Cabin@localhost:5432/postgis_test'
        USR_IMG = os.path.join(EXP_PATH,'user_images')
        APP_PATH = os.path.join(EXP_PATH,'app')
        SRV_PATH = os.path.join(EXP_PATH,'server')
    elif platform == 'win':
        usr = r'C:\Users\Sup'
        EXP_PATH = os.path.join(usr,dropboxpath)
        HOME_URL = 'localhost'
        ENG_STR = 'postgresql://exposureguy:Keavin#1123@localhost:5433/gistest'
        USR_IMG = os.path.join(EXP_PATH,r'user_images')
        APP_PATH = os.path.join(EXP_PATH,'app')
        SRV_PATH = os.path.join(EXP_PATH,'server')
    elif platform == 'linux':
        #Default to unix config
        HOME_URL = 'http://exposureapp.io'
        EXP_PATH = os.path.join(os.path.expanduser('~'),dropboxpath)
        ENG_STR = 'postgresql://Cabin@localhost:5432/postgis_test'
        USR_IMG = os.path.join(EXP_PATH,'user_images')
        APP_PATH = os.path.join(EXP_PATH,'app')
        SRV_PATH = os.path.join(EXP_PATH,'server')
    elif platform == 'ios':
        #Default to unix config
        HOME_URL = 'http://exposureapp.io'
        EXP_PATH = ''
        ENG_STR = 'postgresql://Cabin@localhost:5432/postgis_test'
        USR_IMG = os.path.join(EXP_PATH,'user_images')
        APP_PATH = ''#os.path.join(EXP_PATH,'app')
        SRV_PATH = ''#os.path.join(EXP_PATH,'server')

    STORE_URL = 'http://{}:{}'.format(HOME_URL,WEB_PORT)
    try:
        from sqlalchemy_imageattach.stores.fs import FileSystemStore
        STORE = FileSystemStore(USR_IMG,STORE_URL)
        print STORE_URL, STORE.base_url, STORE.path
    except Exception as e:
        print e


    DEFAULT_LOADING_IMAGE = os.path.join(EXP_PATH,'app','loading_apeture.png')
    from kivy.loader import Loader
    loadingImage = Loader.image(DEFAULT_LOADING_IMAGE)


    #LOCAL_IMAGE = os.path.join(APP_PATH,'Login_Image.jpg')
    LOCAL_IMAGE = os.path.join(APP_PATH,'Login_Image.jpg')
    MAP_ICON = os.path.join(APP_PATH,'resources','Beemo_CircleOnly_Med.png')
    LOGO_IMAGE = os.path.join(APP_PATH,'resources','Beemo_Logo.png')
    INFO_ICON = os.path.join(APP_PATH,'icons','globe.png')
    GAMES_ICON = os.path.join(APP_PATH,'icons','sparks.jpg')
    SETTINGS_ICON = os.path.join(APP_PATH,'icons','connected.png')
    #CAMERA_ICON = os.path.join(APP_PATH,'icons','photo-camera.png')
    RIBBON_ICON = os.path.join(APP_PATH,'resources','tabsliderarrow.png')
    ADDUSER_ICON = os.path.join(APP_PATH,'icons','uxpin-icon-set_add_user.png')
    RACK_ICON = os.path.join(APP_PATH,'icons','uxpin-icon-set_rack.png')
    LOADING_GIF = os.path.join(APP_PATH,'resources','Beemo_CircleOnly_Med_Rotate.gif')

    Loader.loading_image = Image(   source = LOADING_GIF, \
                                    size_hint = (0.5,0.5),
                                    pos_hint = {'center_x':0.5,'center_y':0.5}
                               )

    HEADER_FONT = os.path.join(APP_PATH,'fonts','hotel_font.ttf')
    MENU_FONT = os.path.join(APP_PATH,'fonts','Raleway-SemiBold.ttf')
    TITLE_FONT = os.path.join(APP_PATH,'fonts','Monument_Valley_1.2-Regular.ttf')

    #APP COLORS
    BEEMO_ORANGE = (247/255.,148/255.,30/255.,1)
    BEEMO_GREEN = (140/255.,198/255.,63/255.,1)
    BEEMO_BLUE = (37/255., 170/255., 225/255.,1)

    BEEMO_BLU_TRANSP = (37/255., 170/255., 225/255.,0.65)

    PRIMARY_COLOR = BEEMO_BLUE #(0.722,0.315,0.1,1)#(0.14901, 0.384313, 0.211764,1)#(0.722,0.315,0.1,1)
    SECONDARY_COLOR = BEEMO_ORANGE #(177/255.,144/255.,70/255.,1)
    OUTLINE_COLOR = BEEMO_BLUE#(0.2,0.2,0.2)
    DARKGREY_COLOR = (0.2,0.2,0.2,1)
    GREY_COLOR = (0.65,0.65,0.65,1)
    LIGHT_GREY = (0.9,0.9,0.9,1)
    BACKGROUND = (1,1,1,1)

    POPUPBACKGROUND = (1,1,1,0.9)
    OFFWHITE  = (0.95,0.95,0.95,1)

    BUTTONDOWN = OFFWHITE
    ERRORCOLOR =(0.62, 0.11, 0.20,1)

    SUCCESSCOLOR = [0.180, 0.545, 0.341,1]
    BTNBORDER = SECONDARY_COLOR

    font_opts = dict(   color=(0,0,0,1),text_size=(100,None),\
                        valign='bottom',halign='center',
                        font_size=25,
                        font_name=TITLE_FONT)
    icon_opt = dict(size_hint=(0.75,1))
    but_opt = dict(color_normal=(1,1,1,1),color_down=BUTTONDOWN,\
                    border_color=PRIMARY_COLOR,radius=0,\
                    color=(0,0,0,1),size_hint=(1,1),border_width=2,\
                    font_size=20,font_name=TITLE_FONT)


    resources.resource_add_path(os.path.join(APP_PATH,'resources'))


    settings_json = '''
    [
        {
            "type": "title",
            "title": "Reminders"
        },{
            "type": "options",
            "title": "Enable notifications",
            "desc": "Description of my first key",
            "section": "section1",
            "key": "key1",
            "options": ["value1", "value2", "another value"]
        },

        {
            "type": "numeric",
            "title": "My second key",
            "desc": "Description of my second key",
            "section": "section1",
            "key": "key2"
        }
    ]
    '''

    #Mock Data
    LAT,LONG = 26.7153, -80.053

    PRJ_DIR = os.path.join( EXP_PATH, 'project_images')
    PRJ_IMAGE = glob(PRJ_DIR+'/*.jpg')
    PROJECTS = [os.path.basename(prj).replace('.jpg','').replace('.',' ') \
                                        for prj in PRJ_IMAGE]
    PRJ_LOC = [(LONG+(random.random()-0.5)*0.1,LONG+(random.random()-0.5)*0.1)for prj in PROJECTS]

    USR_DIR = os.path.join( EXP_PATH, 'user_images')
    USR_IMAGE = glob(USR_DIR+'/*.jpg')
    USERS = [os.path.basename(prj).replace('.jpg','').replace('.',' ') \
                                        for prj in USR_IMAGE]
    N = len(USERS)
    USR_LOC = [(LAT+(random.random()-0.5)*0.1,LONG+(random.random()-0.5)*0.1) for prj in USERS]

    PRJ_MEMBERS = {prj: set([random.choice(USERS) for i in range(random.randint(1,N-3))]) \
                                                  for prj in PROJECTS}



def hello(self):
    print 'press my buttons baby'
