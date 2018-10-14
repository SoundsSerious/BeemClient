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
#import netifaces

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
    
    @property
    def SERVER_IP(self):
        server_ip = '.'.join(socket.gethostbyname( socket.gethostname() ).split('.')[:3]+['1'])
        print server_ip
        #server_ip = netifaces.gateways()['default'][netifaces.AF_INET][0]
        #gateway = '10.0.0.1'
        #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #s.connect((gateway,0))
        #this_ip = s.getsockname()[0]
        #server_ip = '.'.join(this_ip.split('.')[:3]+['1'])
        return server_ip
    LOCAL_PORT = 18330
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
        self.app.log("COM: CON: {0}".format(response.peer))
        self.factory.resetDelay()


    # def onOpen(self):
    #     self.app.log("COM: OPN:")
    #
    #     def hello():
    #         self.sendMessage(u"Hello, world!".encode('utf8'))
    #         self.sendMessage(b"\x00\x01\x03\x04", isBinary=True)
    #         self.factory.reactor.callLater(1, hello)
    #
    #     # start sending messages every second ..
    #     hello()

    # def onMessage(self, payload, isBinary):
    #     if payload:
    #         if isBinary:
    #             #print("Binary message received: {0} bytes".format(len(payload)))
    #             self.app.log("COM: BIN: {0} ".format(b2a_uu(payload)))
    #         else:
    #             if "TEL"in payload and "POS" in payload and payload.endswith(";"):
    #                 pre, pos_data = payload.split("POS:\t")
    #                 self.app.log("KALMAN POSITION: {}".format(pos_data))
    #                 self.app.kalman_pos = sqrt(sum([float(v.replace(';', ''))**2 for v in pos_data.split(',')]))
    #             self.app.log("COM: TXT: {}".format(payload))

    def onClose(self, wasClean, code, reason):
        self.app.log("COM: CLO: {0}".format(reason))

    @property
    def app(self):
        return self.factory.app


class BeemoClient(WebSocketClientFactory, ReconnectingClientFactory):

    protocol = BeemProtocol
    utf8validateIncoming = False
    app = None
    client = None #Single Client For Now .. one primary connection
    mesh_loc = None
    def __init__(self, kivy_app,mesh_loc,**kwargs):
        self.mesh_loc = mesh_loc
        WebSocketClientFactory.__init__(self,self.mesh_loc.WEBSOCK_ID,**kwargs)
        self.app = kivy_app
        self.app.beem_client = self
        self.utf8validateIncoming = False
        # reactor.callLater(5,self.getHeapSize)
        # reactor.callLater(5,self.sendTelemetry)

    def startedConnecting(self, connector):
        self.app.log('Started to connect. {}'.format( self.mesh_loc.WEBSOCK_ID))

    def buildProtocol(self, addr):
        self.client = self.protocol(self)
        return self.client

    def clientConnectionFailed(self, connector, reason):
        self.app.log("Client connection failed .. {}".format(reason))
        self.client = None
        self.retry(connector)


    def clientConnectionLost(self, connector, reason):
        self.app.log("Client connection lost .. {}".format(reason))
        self.client = None
        self.retry(connector)
        #self.getHeapSize()

    @inlineCallbacks
    def getSettings(self,*args):
        if self.client and self.client.connected:
            try:
                resp = yield treq.get(self.mesh_loc.HTTP_ID+'/lights/settings/get')
                content = yield resp.text()
                yield self.app.applySettings( content )
            except  Exception, e:
                print str(e)

    @inlineCallbacks
    def setSettings(self,power,temp,brightness):
        if self.client and self.client.connected:
            yield treq.get(self.mesh_loc.HTTP_ID+'/lights/settings/set',   params = {  'temp': str(temp),
                                                                    'power': str(power),
                                                                    'brightness': str(brightness)
                                                                    })

    @inlineCallbacks
    def setColor(self,I=0,H=10,S=0,V=70):
        if self.client and self.client.connected:
            yield treq.get(self.mesh_loc.HTTP_ID+'/mode/color/set',   params = {  'I': str(I),
                                                                    'H': str(H),
                                                                    'S': str(S),
                                                                    'V': str(V)})

    @inlineCallbacks
    def setMode(self,INDEX):
        if self.client and self.client.connected:
            try:
                yield treq.get(self.mesh_loc.HTTP_ID+'/mode/select/', params={'INDEX': str(INDEX)})
            except  Exception, e:
                print str(e)

    @inlineCallbacks
    def setPalette(self,index):
        print "Setting Palette "+ str(index)
        if self.client and self.client.connected:
            try:
                yield treq.get(self.mesh_loc.HTTP_ID+'/mode/palette/set', params={'I': str(index)})
            except  Exception, e:
                print str(e)

    @inlineCallbacks
    def setModeSetting(self,index,value):
        print 'Mode Setting ' + str(index) + ' To ' + str(value)
        if self.client and self.client.connected:
            try:
                yield treq.get(self.mesh_loc.HTTP_ID+'/mode/settings/set', params={'INX': str(index),
                                                                     'SET': str(int(value))})
            except  Exception, e:
                print str(e)

    @inlineCallbacks
    def turnOn(self):
        if self.client and self.client.connected:
            try:
                yield treq.get(self.mesh_loc.HTTP_ID+'/lights/on', params = {})
            except  Exception, e:
                print str(e)

    @inlineCallbacks
    def turnOff(self):
        if self.client and self.client.connected:
            try:
                yield treq.get(self.mesh_loc.HTTP_ID+'/lights/off', params = {})
            except  Exception, e:
                print str(e)

    def _cb_print(self,msg,pretext='LOG:'):
        self.app.log( str(msg))

if __name__ == '__main__':

    import sys

    class MockApp:

        def log(self,*args):
            print 'LOG :'+ str(args[0])

    meshLocalizatoin = MeshLocalization()

    app = MockApp()

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = BeemoClient(app,meshLocalizatoin)
    factory.utf8validateIncoming = False

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
