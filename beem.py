import sys
from math import *

from twisted.internet import reactor
from twisted.internet import task
from twisted.internet.defer import *
from twisted.python import log
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet.protocol import ReconnectingClientFactory
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
    listenWS


from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

from binascii import *
import treq
import socket

"""
BEEMO: TWISTED DEV SERVER
"""

#LOCAL_IP = "10.74.45.1" #"192.168.4.1"
class MeshLocalization(object):
    '''Mesh Server IP's are based off of the MAC address of that particular node.
    They follow the form:
        10.AA.BB.1
    By knowing our ip address we can replace the last value with a 1 and get the
    server IP. Boo Fucking Ya.
    '''
    app = None
    LOCAL_PORT = 18330

    def __init__(self,app):
        self.app = app

    @property
    def SERVER_IP(self):
        try: #Hail Marry
            gateway = '10.1.1.1'
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.01)
            s.connect_ex((gateway,80))
            this_ip = s.getsockname()[0]
            server_ip = '.'.join(this_ip.split('.')[:3]+['1'])
        except Exception as e:
            self.app.log( e )
            try:
                import netifaces
                server_ip = netifaces.gateways()['default'][netifaces.AF_INET][0]
            except:
                try:
                    server_ip = '.'.join(socket.gethostbyname( socket.gethostname() ).split('.')[:3]+['1'])
                except:
                    server_ip = '10.{}.{}.1'.format(random.randint(1,255),random.randint(1,255))
        if not server_ip.startswith('10.'):
            self.app.log('IP Not Of Mesh {}'.format(server_ip))
        return server_ip

    @property
    def HTTP_ID(self):
        return "http://{}:{}".format(self.SERVER_IP, self.LOCAL_PORT)
    @property
    def WEBSOCK_ID(self):
        return "ws://{}:{}/ws".format(self.SERVER_IP, self.LOCAL_PORT)


class BeemProtocol(WebSocketClientProtocol):

    def __init__(self, factory,**kwargs):
        super(BeemProtocol,self).__init__(**kwargs)
        self.factory = factory

    def onConnect(self, response):
        self.app.log("Beem Connected {0}".format(response.peer))
        self.factory.resetDelay()
        self.app.schedule_update()
        self.factory.addr_success = True

    def onMessage(self, message, isBinary):
        #Handle Websocket Responses... Reports, Verificaiton Ect
        if not isBinary:
            self.app.log('WS: {}'.format(message))

    def onClose(self, wasClean, code, reason):
        self.app.log("Connection Closed {0}".format(reason))

    @property
    def app(self):
        return self.factory.app


class BeemoClient(WebSocketClientFactory, ReconnectingClientFactory):

    protocol = BeemProtocol
    utf8validateIncoming = False
    app = None
    client = None #Single Client For Now .. one primary connection
    mesh_loc = None
    addr_success = False
    _http_addr = None
    attm_connector = None
    def __init__(self, kivy_app,mesh_loc,**kwargs):
        self.mesh_loc = mesh_loc
        WebSocketClientFactory.__init__(self,self.mesh_loc.WEBSOCK_ID,**kwargs)
        self.app = kivy_app
        self.app.beem_client = self
        self.utf8validateIncoming = False
        # reactor.callLater(5,self.getHeapSize)
        # reactor.callLater(5,self.sendTelemetry)
    @property
    def http_addr(self):
        if self.attm_connector:
            ipadr =  "http://{}:{}".format(self.attm_connector.host, self.attm_connector.port)
            #self.app.log('Using {}'.format(ipadr))
            return ipadr
        else:
            return self.mesh_loc.HTTP_ID

    def startedConnecting(self, connector):
        self.app.log('Started to connect. {}'.format( self.mesh_loc.WEBSOCK_ID))
        self.attm_connector = connector
        self._http_addr = connector.getDestination()

    def buildProtocol(self, addr):
        self.client = self.protocol(self)
        return self.client

    def clientConnectionFailed(self, connector, reason):
        self.app.log("Client connection failed .. {}".format(reason))
        self.client = None
        self.addr_success = False
        self.attm_connector = None
        ReconnectingClientFactory.clientConnectionFailed(self,connector,reason)


    def clientConnectionLost(self, connector, reason):
        self.app.log("Client connection lost .. {}".format(reason))
        self.client = None
        self.addr_success = False
        self.attm_connector = None
        ReconnectingClientFactory.clientConnectionLost(self,connector,reason)
        #self.getHeapSize()

    def retry_connection(self,*args):
        if self.connector:
            self.resetDelay()
            self.retry()

    @inlineCallbacks
    def getMeshReport(self,*args):
        if self.client and self.client.connected:
            try:
                resp = yield treq.get(self.http_addr+'/mesh/report')
                #yield resp.text()
            except  Exception, e:
                print str(e)

    @inlineCallbacks
    def getSettings(self,*args):
        if self.client and self.client.connected:
            try:
                resp = yield treq.get(self.http_addr+'/lights/settings/get')
                content = yield resp.text()
                yield self.app.applySettings( content )
            except  Exception, e:
                print str(e)



    @inlineCallbacks
    def setSettings(self,power,temp,brightness):
        if self.client and self.client.connected:
            yield treq.get(self.http_addr+'/lights/settings/set',   params = {  'temp': str(temp),
                                                                    'power': str(power),
                                                                    'brightness': str(brightness)
                                                                    })

    @inlineCallbacks
    def setColor(self,I=0,H=10,S=0,V=70):
        if self.client and self.client.connected:
            yield treq.get(self.http_addr+'/mode/color/set',   params = {  'I': str(I),
                                                                    'H': str(H),
                                                                    'S': str(S),
                                                                    'V': str(V)})

    @inlineCallbacks
    def setMode(self,INDEX):
        if self.client and self.client.connected:
            try:
                yield treq.get(self.http_addr+'/mode/select/', params={'INDEX': str(INDEX)})
            except  Exception, e:
                print str(e)

    @inlineCallbacks
    def setPalette(self,index):
        print "Setting Palette "+ str(index)
        if self.client and self.client.connected:
            try:
                yield treq.get(self.http_addr+'/mode/palette/set', params={'I': str(index)})
            except  Exception, e:
                print str(e)

    @inlineCallbacks
    def setModeSetting(self,index,value):
        print 'Mode Setting ' + str(index) + ' To ' + str(value)
        if self.client and self.client.connected:
            try:
                yield treq.get(self.http_addr+'/mode/settings/set', params={'INX': str(index),
                                                                     'SET': str(int(value))})
            except  Exception, e:
                print str(e)

    @inlineCallbacks
    def turnOn(self):
        if self.client and self.client.connected:
            try:
                yield treq.get(self.http_addr+'/lights/on', params = {})
            except  Exception, e:
                print str(e)

    @inlineCallbacks
    def turnOff(self):
        if self.client and self.client.connected:
            try:
                yield treq.get(self.http_addr+'/lights/off', params = {})
            except  Exception, e:
                print str(e)

    def _cb_print(self,msg,pretext='LOG:'):
        self.app.log( str(msg))

if __name__ == '__main__':

    import sys

    class MockApp:

        def log(self,*args):
            print 'LOG :'+ str(args[0])


    app = MockApp()

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    meshLocalizatoin = MeshLocalization(app)
    factory = BeemoClient(app,meshLocalizatoin)
    factory.utf8validateIncoming = False

    lc = task.LoopingCall( factory.getMeshReport )
    lc.start(30.0)

    reactor.connectTCP(meshLocalizatoin.SERVER_IP, meshLocalizatoin.LOCAL_PORT, factory)
    reactor.run()


#def broadcast(reactor, regtype, port, name=None):
#    def _callback(sdref, flags, errorCode, name, regtype, domain):
#        if errorCode == pybonjour.kDNSServiceErr_NoError:
#            d.callback((sdref, name, regtype, domain))
#        else:
#            d.errback(errorCode)
#
#    d = Deferred()
#    sdref = pybonjour.DNSServiceRegister(name = name,
#                                        regtype = regtype,
#                                        port = port,
#                                        callBack = _callback)
#
#    reactor.addReader(MDNS_ServiceDescriptor(sdref))
#    return d

#
#def broadcasting(args):
#    global sdref
#    sdref  = args[0]
#    log.msg('Broadcasting %s.%s%s' % args[1:])
#
#def failed(errorCode):
#    log.err(errorCode)
#
#class MDNS_ServiceDescriptor(object):
#
#    interface.implements(IReadDescriptor)
#
#    def __init__(self, sdref):
#        self.sdref = sdref
#
#    def doRead(self):
#        #pybonjour.DNSServiceProcessResult(self.sdref)
#        pass
#
#    def fileno(self):
#        return self.sdref.fileno()
#
#    def logPrefix(self):
#        return "bonjour"
#
#    def connectionLost(self, reason):
#        self.sdref.close()
#
#
#class Beem(LineReceiver):
#
#    it = True
#
#    def __init__(self, factory):
#        self.factory = factory
#
#    def connectionMade(self):
#        self.factory.app.log( 'Connection Made Sending Resp.' )
#        self.sendLine("What's your name?")
#        self.factory.app.on_connection(self)
#
#    def lineReceived(self, line):
#        self.factory.app.log( line )
#
