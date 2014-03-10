#!/usr/bin/env python

class ApStatClass(object):
    'this is Ap statistic class'
    packageDict = {'disreq':0, 'disrsp':0, 'joinreq':0, 'joinrsp':0, 'confstatreq':0, 'confstatrsp':0,\
                'changereq':0, 'changersp':0, 'confupreq':0, 'confuprsp':0, 'staconfreq':0, 'staconfrsp':0,\
                'wlanconfreq':0, 'wlanconfrsp':0, 'keepalivereq':0, 'keepaliversp':0, 'echoreq':0, 'echorsp':0}
    packageDictTmp = {'disreq':0, 'disrsp':0, 'joinreq':0, 'joinrsp':0, 'confstatreq':0, 'confstatrsp':0,\
                'changereq':0, 'changersp':0, 'confupreq':0, 'confuprsp':0, 'staconfreq':0, 'staconfrsp':0,\
                'wlanconfreq':0, 'wlanconfrsp':0, 'keepalivereq':0, 'keepaliversp':0, 'echoreq':0, 'echorsp':0}
    def reset(self):
        for i in self.packageDict:
            self.packageDict[i] = 0
        for i in self.packageDictTmp:
            self.packageDictTmp[i] = 0

    def elemadd(self, name):
        self.packageDict[name] = self.packageDict[name] + 1
		
    def selfprint(self, tile):
        print tile.center(100, '-')
        print 'Discover Req:'.ljust(20, ' ') + str(self.packageDict['disreq'] - self.packageDictTmp['disreq']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['disreq']).ljust(10, ' ') + \
              'Discover Rsp:'.ljust(20, ' ') + str(self.packageDict['disrsp'] - self.packageDictTmp['disrsp']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['disrsp']).ljust(10, ' ')
        self.packageDictTmp['disreq'] = self.packageDict['disreq']
        self.packageDictTmp['disrsp'] = self.packageDict['disrsp']
        print 'Join Req:'.ljust(20, ' ') + str(self.packageDict['joinreq'] - self.packageDictTmp['joinreq']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['joinreq']).ljust(10, ' ') + \
              'Join Rsp:'.ljust(20, ' ') + str(self.packageDict['joinrsp'] - self.packageDictTmp['joinrsp']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['joinrsp']).ljust(10, ' ')
        self.packageDictTmp['joinreq'] = self.packageDict['joinreq']
        self.packageDictTmp['joinrsp'] = self.packageDict['joinrsp']
        print 'ConfState Req:'.ljust(20, ' ') + str(self.packageDict['confstatreq'] - self.packageDictTmp['confstatreq']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['confstatreq']).ljust(10, ' ') + \
              'ConfState Rsp:'.ljust(20, ' ') + str(self.packageDict['confstatrsp'] - self.packageDictTmp['confstatrsp']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['confstatrsp']).ljust(10, ' ')
        self.packageDictTmp['confstatreq'] = self.packageDict['confstatreq']
        self.packageDictTmp['confstatrsp'] = self.packageDict['confstatrsp']
        print 'Change Req:'.ljust(20, ' ') + str(self.packageDict['changereq'] - self.packageDictTmp['changereq']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['changereq']).ljust(10, ' ') + \
              'Change Rsp:'.ljust(20, ' ') + str(self.packageDict['changersp'] - self.packageDictTmp['changersp']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['changersp']).ljust(10, ' ')
        self.packageDictTmp['changereq'] = self.packageDict['changereq']
        self.packageDictTmp['changersp'] = self.packageDict['changersp']
        print 'ConfUpStat Req:'.ljust(20, ' ') + str(self.packageDict['confupreq'] - self.packageDictTmp['confupreq']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['confupreq']).ljust(10, ' ') + \
              'ConfUpStat Rsp:'.ljust(20, ' ') + str(self.packageDict['confuprsp'] - self.packageDictTmp['confuprsp']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['confuprsp']).ljust(10, ' ')
        self.packageDictTmp['confupreq'] = self.packageDict['confupreq']
        self.packageDictTmp['confuprsp'] = self.packageDict['confuprsp']
        print 'StaConf Req:'.ljust(20, ' ') + str(self.packageDict['staconfreq'] - self.packageDictTmp['staconfreq']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['staconfreq']).ljust(10, ' ') + \
              'StaConf Rsp:'.ljust(20, ' ') + str(self.packageDict['staconfrsp'] - self.packageDictTmp['staconfrsp']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['staconfrsp']).ljust(10, ' ')
        self.packageDictTmp['staconfreq'] = self.packageDict['staconfreq']
        self.packageDictTmp['staconfrsp'] = self.packageDict['staconfrsp']
        print 'WlanConf Req:'.ljust(20, ' ') + str(self.packageDict['wlanconfreq'] - self.packageDictTmp['wlanconfreq']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['wlanconfreq']).ljust(10, ' ') + \
              'WlanConf Rsp:'.ljust(20, ' ') + str(self.packageDict['wlanconfrsp'] - self.packageDictTmp['wlanconfrsp']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['wlanconfrsp']).ljust(10, ' ')
        self.packageDictTmp['wlanconfreq'] = self.packageDict['wlanconfreq']
        self.packageDictTmp['wlanconfrsp'] = self.packageDict['wlanconfrsp']
        print 'Keepalive Req:'.ljust(20, ' ') + str(self.packageDict['keepalivereq'] - self.packageDictTmp['keepalivereq']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['keepalivereq']).ljust(10, ' ') + \
              'Keepalive Rsp:'.ljust(20, ' ') + str(self.packageDict['keepaliversp'] - self.packageDictTmp['keepaliversp']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['keepaliversp']).ljust(10, ' ')
        self.packageDictTmp['keepalivereq'] = self.packageDict['keepalivereq']
        self.packageDictTmp['keepaliversp'] = self.packageDict['keepaliversp']
        print 'Echo Req:'.ljust(20, ' ') + str(self.packageDict['echoreq'] - self.packageDictTmp['echoreq']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['echoreq']).ljust(10, ' ') + \
              'Echo Rsp:'.ljust(20, ' ') + str(self.packageDict['echorsp'] - self.packageDictTmp['echorsp']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['echorsp']).ljust(10, ' ')
        self.packageDictTmp['echoreq'] = self.packageDict['echoreq']
        self.packageDictTmp['echorsp'] = self.packageDict['echorsp']
        print '-' * 100

class StaStatClass(object):
    'this is station statisitc class'
    packageDict = {'openauthreq':0, 'openauthrsp':0, 'openassoreq':0, 'openassorsp':0}
    packageDictTmp = {'openauthreq':0, 'openauthrsp':0, 'openassoreq':0, 'openassorsp':0}
	
    def reset(self):
        for i in self.packageDict:
            self.packageDict[i] = 0
        for i in self.packageDictTmp:
            self.packageDictTmp[i] = 0

    def elemadd(self, name):
        self.packageDict[name] = self.packageDict[name] + 1

    def selfprint(self, tile):
        print tile.center(100, '-')
        print 'OpenAuth Req:'.ljust(20, ' ') + str(self.packageDict['openauthreq'] - self.packageDictTmp['openauthreq']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['openauthreq']).ljust(10, ' ') + \
              'OpenAuth Rsp:'.ljust(20, ' ') + str(self.packageDict['openauthrsp'] - self.packageDictTmp['openauthrsp']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['openauthrsp']).ljust(10, ' ')
        self.packageDictTmp['openauthreq'] = self.packageDict['openauthreq']
        self.packageDictTmp['openauthrsp'] = self.packageDict['openauthrsp']
        print 'OpenAsso Req:'.ljust(20, ' ') + str(self.packageDict['openassoreq'] - self.packageDictTmp['openassoreq']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['openassoreq']).ljust(10, ' ') + \
              'OpenAsso Rsp:'.ljust(20, ' ') + str(self.packageDict['openassorsp'] - self.packageDictTmp['openassorsp']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['openassorsp']).ljust(10, ' ')
        self.packageDictTmp['openassoreq'] = self.packageDict['openassoreq']
        self.packageDictTmp['openassorsp'] = self.packageDict['openassorsp']
        print '-' * 100

class PeapStatClass(object):
    'this is peap statisitc class'
    packageDict = {'peapauthreq':0, 'peapauthrsp':0, 'peapassoreq':0, 'peapassorsp':0}
    packageDictTmp = {'peapauthreq':0, 'peapauthrsp':0, 'peapassoreq':0, 'peapassorsp':0}
	
    def reset(self):
        for i in self.packageDict:
            self.packageDict[i] = 0
        for i in self.packageDictTmp:
            self.packageDictTmp[i] = 0

    def elemadd(self, name):
        self.packageDict[name] = self.packageDict[name] + 1

    def selfprint(self, tile):
        print tile.center(100, '-')
        print 'PeapAuth Req:'.ljust(20, ' ') + str(self.packageDict['peapauthreq'] - self.packageDictTmp['peapauthreq']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['peapauthreq']).ljust(10, ' ') + \
              'PeapAuth Rsp:'.ljust(20, ' ') + str(self.packageDict['peapauthrsp'] - self.packageDictTmp['peapauthrsp']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['peapauthrsp']).ljust(10, ' ')
        self.packageDictTmp['peapauthreq'] = self.packageDict['peapauthreq']
        self.packageDictTmp['peapauthrsp'] = self.packageDict['peapauthrsp']
        print 'PeapAuth Req:'.ljust(20, ' ') + str(self.packageDict['peapassoreq'] - self.packageDictTmp['peapassoreq']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['peapassoreq']).ljust(10, ' ') + \
              'PeapAuth Rsp:'.ljust(20, ' ') + str(self.packageDict['peapassorsp'] - self.packageDictTmp['peapassorsp']).ljust(10, ' ') + \
              '[total]:' + str(self.packageDict['peapassorsp']).ljust(10, ' ')
        self.packageDictTmp['peapassoreq'] = self.packageDict['peapassoreq']
        self.packageDictTmp['peapassorsp'] = self.packageDict['peapassorsp']
        print '-' * 100

def printStatAll(apObj, staObj, interval):
    apObj.selfprint('AP STATISTIC  (interval:  ' + str(interval) + 's)')
    staObj.selfprint('STA STATISTIC  (interval:  ' + str(interval) + 's)')
	