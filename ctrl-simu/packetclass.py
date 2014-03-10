#!/usr/bin/env python

import struct,socket,sys,time,ctypes
from config import *
from myTimer import *
from statistic import *

# ip header format
#0                   1                   2                   3   
#    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |Version|  IHL  |Type of Service|          Total Length         |
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |         Identification        |Flags|      Fragment Offset    |
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |  Time to Live |    Protocol   |         Header Checksum       |
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |                       Source Address                          |
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |                    Destination Address                        |
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |                    Options                    |    Padding    |
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

#udp header format
#0      7 8     15 16    23 24    31  
# +--------+--------+--------+--------+ 
# |     Source      |   Destination   | 
# |      Port       |      Port       | 
# +--------+--------+--------+--------+ 
# |                 |                 | 
# |     Length      |    Checksum     | 
# +--------+--------+--------+--------+ 
# |                                     
# |          data octets ...            
# +---------------- ...

Interval = int(confDict['Interval'])
ApNum = int(confDict['ApNum'])
ApOnlineSpeed = int(confDict['ApOnlineSpeed'])
FirstApMac = macs2a(confDict['FirstApMac'])
FirstApIp = socket.inet_aton(confDict['FirstApIp'])
ac_ip = confDict['ACIp']
ac_ip_net = struct.pack("!4s", socket.inet_aton(ac_ip))

StaNumPerAp = int(confDict['StaNumPerAp'])
StaOnlineSpeed = int(confDict['StaOnlineSpeed'])
FirstStaMac = macs2a(confDict['FirstStaMac'])
FirstStaIp = socket.inet_aton(confDict['FirstStaIp'])

PortalStaNum = int(confDict['PortalStaNum'])
PortalStaOnlineSpeed = int(confDict['PortalStaOnlineSpeed'])

HostIp = confDict['HostIp']
hostIP_net = struct.pack("!4s", socket.inet_aton(HostIp))
HostDev = confDict['HostDev']

apStat = ApStatClass()
staStat = StaStatClass()

md5 = ctypes.CDLL("./libmd5.so")

#create link layer raw socket
try:
    link_raw_sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.SOCK_RAW)
    link_raw_sock.bind((HostDev, socket.SOCK_RAW))
except socket.error , msg:
    print 'link_raw_sock could not create socket, error code: ' + str(msg[0]) + ' Message ' + msg[1] 
    sys.exit(-1)

HostMac = link_raw_sock.getsockname()[4]

#create network layer raw socket
try:
    network_raw_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    network_raw_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
except socket.error , msg:
    print 'network_raw_sock could not create socket, error code: ' + str(msg[0]) + ' Message ' + msg[1] 
    sys.exit(-1)

#ip header fields
def SetIpHeaders(ip_src_addr,ip_dst_addr,ip_ihl = 5,ip_ver = 4, ip_tos = 0,ip_tot_len = 0, ip_id = 1,ip_frag_off = 0,ip_ttl = 255, ip_proto = socket.IPPROTO_UDP,ip_check = 0):
    ''' set ip headers '''
    ihl_ver = (ip_ver << 4) | ip_ihl
    ip_header = struct.pack('!BBHHHBBH', ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, 0) + ip_src_addr + ip_dst_addr
    return ip_header

#udp header fields
def SetUdpHeaders(s_port, d_port, length, check):
    ''' set udp headers '''
    udp_header = struct.pack('!HHHH', s_port, d_port, (length + 8), check)
    return udp_header

#checksum
def CheckSum(msg):
    ''' calculate the checksum '''
    s = 0
    for i in struct.range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8)
        s = s + w

    s = (s>>16) + (s & 0xffff);
    s = s + (s >> 16);

    s = ~s & 0xffff

    return s

def Ip2Int(ip):
    ''' ip transfer to int '''
    return struct.unpack("!I", ip)[0]

def Int2Ip(i):
    ''' int transfer to ip '''
    return struct.pack("!I",i)
	
def CalculateIp(i, ip):
    return Int2Ip(ip + i)
	
def CalculateMac(i, mac):
    ''' MAC add by step 1 '''
    a1,a2 = struct.unpack("!HI",mac)
    a2 = a2 + i
    return struct.pack("!HI", a1, a2)
	
def CalculateDiscoveryReqMsg(mac):
    return CWDisBuff[0:87] + mac + CWDisBuff[93:]

def CalculateJoinReqMsg(mac):
    return CWJoinBuff[0:87] + mac + CWJoinBuff[93:160] + mac + '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + CWJoinBuff[176:]

def CalculateKeepaliveMsg(apMac):
    return CWKeepalive + apMac + '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

def SendArpRequestMsg(i):
    ''' send arp msg '''
    try:
        SenderIp = CalculateIp(i, Ip2Int(FirstApIp))
        TargetIp = ac_ip_net
        packet = '\xff'*6 + HostMac + '\x08\x06' + ARPReqBuff[0:8] + HostMac + SenderIp + ARPReqBuff[18:24] + TargetIp + ARPReqBuff[28:]
        link_raw_sock.send(packet)
    except socket.error , msg:
        print 'link_raw_sock.send fail, error code: ' + str(msg[0]) + ' Messege ' + msg[1]
        sys.exit(-1)
		
def SendNetworkSockMsg(packet):
    ''' send msg '''
    try:
        network_raw_sock.sendto(packet, (ac_ip, 0))
    except socket.error , msg:
        print 'network_raw_sock.sendto fail, error code: ' + str(msg[0]) + ' Messege ' + msg[1]
        sys.exit(-1)

class CwPacket(object):
    "This is capwap msg class"

    def BuildDiscoveryRequestMsg(self, i):
        ap_ip = CalculateIp(i, Ip2Int(FirstApIp))
        ap_mac = CalculateMac(i, FirstApMac)
        payload = CalculateDiscoveryReqMsg(ap_mac)
        packet = ''
        totel_len = 8 + len(payload)
        packet = SetIpHeaders(ap_ip, ac_ip_net, 5, 4, 0, totel_len, 1, 0, 255, socket.IPPROTO_UDP, 0) + SetUdpHeaders(15246, 5246, len(payload), 0) + payload
        return packet

    def BuildJoinRequestMsg(self, ap_ip):
        i = Ip2Int(ap_ip) - Ip2Int(FirstApIp)
        ap_mac = CalculateMac(i, FirstApMac)
        payload = CalculateJoinReqMsg(ap_mac)
        packet = ''
        totel_len = 8 + len(payload)
        packet = SetIpHeaders(ap_ip, ac_ip_net, 5, 4, 0, totel_len, 1, 0, 255, socket.IPPROTO_UDP, 0) + SetUdpHeaders(15246, 5246, len(payload), 0) + payload
        return packet

    def BuildConfigRequestMsg(self, ap_ip):
        payload = CWConfigStat
        packet = ''
        totel_len = 8 + len(payload)
        packet = SetIpHeaders(ap_ip, ac_ip_net, 5, 4, 0, totel_len, 1, 0, 255, socket.IPPROTO_UDP, 0) + SetUdpHeaders(15246, 5246, len(payload), 0) + payload
        return packet

    def BuildChangeStateRequestMsg(self, ap_ip):
        payload = CWChangeStat
        packet = ''
        totel_len = 8 + len(payload)
        packet = SetIpHeaders(ap_ip, ac_ip_net, 5, 4, 0, totel_len, 1, 0, 255, socket.IPPROTO_UDP, 0) + SetUdpHeaders(15246, 5246, len(payload), 0) + payload
        return packet

    def BuildKeepaliveMsg(self, i):
        ap_ip = CalculateIp(i, Ip2Int(FirstApIp))
        ap_mac = CalculateMac(i, FirstApMac)
        payload = CalculateKeepaliveMsg(ap_mac)
        packet = ''
        totel_len = 8 + len(payload)
        packet = SetIpHeaders(ap_ip, ac_ip_net, 5, 4, 0, totel_len, 1, 0, 255, socket.IPPROTO_UDP, 0) + SetUdpHeaders(15247, 5247, len(payload), 0) + payload
        return packet

    def BuildEchoRequestMsg(self, i):
        ap_ip = CalculateIp(i, Ip2Int(FirstApIp))
        payload = CWEcho
        packet = ''
        totel_len = 8 + len(payload)
        packet = SetIpHeaders(ap_ip, ac_ip_net, 5, 4, 0, totel_len, 1, 0, 255, socket.IPPROTO_UDP, 0) + SetUdpHeaders(15246, 5246, len(payload), 0) + payload
        return packet

    def BuildConfigUpdateRspMsg(self, ap_ip, MsgSeq):
        payload = CWConfigUpdateRsp
        packet = ''
        totel_len = 8 + len(payload)
        packet = SetIpHeaders(ap_ip, ac_ip_net, 5, 4, 0, totel_len, 1, 0, 255, socket.IPPROTO_UDP, 0) + SetUdpHeaders(15246, 5246, len(payload), 0) + payload
        packet = packet[0:55] + MsgSeq + packet[56:]
        return packet

    def BuildWlanConfigRspMsg(self, ap_ip, MsgSeq):
        i = Ip2Int(ap_ip) - Ip2Int(FirstApIp)
        bssid = CalculateMac(i, FirstApMac)
        payload = CWWlanConfigRsp[0:30] + bssid
        packet = ''
        totel_len = 8 + len(payload)
        packet = SetIpHeaders(ap_ip, ac_ip_net, 5, 4, 0, totel_len, 1, 0, 255, socket.IPPROTO_UDP, 0) + SetUdpHeaders(15246, 5246, len(payload), 0) + payload
        packet = packet[0:55] + MsgSeq + packet[56:]
        return packet

    def BuildStationConfigRspMsg(self, ap_ip, MsgSeq):
        payload = CWStationConfigRsp
        packet = ''
        totel_len = 8 + len(payload)
        packet = SetIpHeaders(ap_ip, ac_ip_net, 5, 4, 0, totel_len, 1, 0, 255, socket.IPPROTO_UDP, 0) + SetUdpHeaders(15246, 5246, len(payload), 0) + payload
        packet = packet[0:55] + MsgSeq + packet[56:]
        return packet

    def send_echo_request(self, i, acMac):
        packet = self.BuildEchoRequestMsg(i)
#        print 'send: echo req'
        SendNetworkSockMsg(packet)
        apStat.elemadd('echoreq')
	
        time.sleep(0.1)
        packet = ''
        packet = self.BuildKeepaliveMsg(i)
#        print 'send: keepalive req'
        SendNetworkSockMsg(packet)
        apStat.elemadd('keepalivereq')

    def HandleRcvMsg(self, buf):
        CW_MSG_TYPE_DISCOVERY_RSP = '\x00\x00\x00\x02'
        CW_MSG_TYPE_JOIN_RSP = '\x00\x00\x00\x04'
        CW_MSG_TYPE_CONFIG_STATUS_RSP = '\x00\x00\x00\x06'
        CW_MSG_TYPE_CHANGE_STATE_RSP = '\x00\x00\x00\x0c'
        CW_MSG_TYPE_ECHO_RSP = '\x00\x00\x00\x0e'
        CW_MSG_TYPE_ADD_WLAN = '\x00\x33\xdd\x01'
        CW_MSG_TYPE_CONFIG_UPDATE = '\x00\x00\x00\x07'
        CW_MSG_TYPE_ADD_STATION = '\x00\x00\x00\x19'

        apIp = buf[30:34]
        msg_type = buf[50:54]
        dataplane_keepalive = buf[50:56]
        #wlan request & config update request  need record its msg sequence
        MsgSeq = buf[55:56]

        if msg_type == CW_MSG_TYPE_DISCOVERY_RSP:
            apStat.elemadd('disrsp')
#            print 'recv: discovery rsp'
            packet = self.BuildJoinRequestMsg(apIp)
#            print 'send: join req'
            SendNetworkSockMsg(packet)
            apStat.elemadd('joinreq')
        elif msg_type == CW_MSG_TYPE_JOIN_RSP:
            apStat.elemadd('joinrsp')
#            print 'recv: join rsp'
            packet = self.BuildConfigRequestMsg(apIp)
#            print 'send: config status req'
            SendNetworkSockMsg(packet)
            apStat.elemadd('confstatreq')
        elif msg_type == CW_MSG_TYPE_CONFIG_STATUS_RSP:
            apStat.elemadd('confstatrsp')
#            print 'recv: config status rsp'
            packet = self.BuildChangeStateRequestMsg(apIp)
#            print 'send: change state req'
            SendNetworkSockMsg(packet)
            apStat.elemadd('changereq')
        elif msg_type == CW_MSG_TYPE_CHANGE_STATE_RSP:
            apStat.elemadd('changersp')
#            print 'recv: change state rsp'
            i = Ip2Int(apIp) - Ip2Int(FirstApIp)
            tmp = myTimer(30, self.send_echo_request, [i, buf[6:12]])
            tmp._run()
        elif msg_type == CW_MSG_TYPE_ECHO_RSP:
            apStat.elemadd('echorsp')
#            print 'recv: echo rsp'
        elif msg_type == CW_MSG_TYPE_ADD_WLAN:
            apStat.elemadd('wlanconfreq')
#            print 'recv: wlan configuration req' 
            packet = self.BuildWlanConfigRspMsg(apIp, MsgSeq)
#            print 'send: wlan configuration rsq'
            SendNetworkSockMsg(packet)
            apStat.elemadd('wlanconfrsp')
        elif msg_type == CW_MSG_TYPE_CONFIG_UPDATE:
            apStat.elemadd('confupreq')
#            print 'recv: config update req'
            packet = self.BuildConfigUpdateRspMsg(apIp, MsgSeq)
#            print 'send: config update rsp'
            SendNetworkSockMsg(packet)
            apStat.elemadd('confuprsp')
        elif msg_type == CW_MSG_TYPE_ADD_STATION:
            apStat.elemadd('staconfreq')
#            print 'recv: add station req'
            packet = self.BuildStationConfigRspMsg(apIp, MsgSeq)
#            print 'send: station config rsp'
            SendNetworkSockMsg(packet)
            apStat.elemadd('staconfrsp')
        elif dataplane_keepalive == '\x00\x16\x00\x23\x00\x10' and buf[26:30] == ac_ip_net:
            apStat.elemadd('keepaliversp')
#            print 'recv: keepalive rsp'

def CalculateAuthMsg(ap_mac, sta_mac, bssid, payload):
    return payload[0:20] + ap_mac + sta_mac + bssid + payload[38:]
    
def CalculateAssociateMsg(ap_mac, sta_mac, bssid, payload):
    return payload[0:20] + ap_mac + sta_mac + bssid + payload[38:]
	
class OpenStaPacket(object):
    "This is open sta msg class"
     
    def BuildOpenStaAuthMsg(self, i, j):
        ap_ip = CalculateIp(i, Ip2Int(FirstApIp))
        ap_mac = CalculateMac(i, FirstApMac)
        bssid = ap_mac
        sta_mac = CalculateMac(j, FirstStaMac)
        payload = CalculateAuthMsg(ap_mac, sta_mac, bssid, OpenStaAuth)
        totel_len = 8 + len(payload)
        packet = ''
        packet = SetIpHeaders(ap_ip, ac_ip_net, 5, 4, 0, totel_len, 1, 0, 255, socket.IPPROTO_UDP, 0) + SetUdpHeaders(15247, 5247, len(payload), 0) + payload
        return packet
		
    def BuildOpenStaAssociateReqMsg(self, i, j):
        ap_ip = CalculateIp(i, Ip2Int(FirstApIp))
        ap_mac = CalculateMac(i, FirstApMac)
        bssid = CalculateMac(i, FirstApMac)
        sta_mac = CalculateMac(j, FirstStaMac)
        payload = CalculateAssociateMsg(ap_mac, sta_mac, bssid, OpenStaAssociateReq)
        totel_len = 8 + len(payload)
        packet = ''
        packet = SetIpHeaders(ap_ip, ac_ip_net, 5, 4, 0, totel_len, 1, 0, 255, socket.IPPROTO_UDP, 0) + SetUdpHeaders(15247, 5247, len(payload), 0) + payload
        return packet
		
    def BuildArpReqMsg(self, i):
        staMac = CalculateMac(i, FirstStaMac)
        staIp = CalculateIp(i, Ip2Int(FirstStaIp))
        TargetIp = ac_ip_net
        packet = '\xff'*6 + staMac + '\x08\x06' + ARPReqBuff[0:8] + staMac + staIp + ARPReqBuff[18:24] + TargetIp + ARPReqBuff[28:]
        return packet
		
    def HandleRcvMsg(self, buf):
        apIp = buf[30:34]
        flag = buf[58:60]
        if flag == '\xb0\x00' and buf[68:74] == buf[74:80]:
            staStat.elemadd('openauthrsp')
#            print 'recv: open station auth rsp'
            i = Ip2Int(apIp) - Ip2Int(FirstApIp)
            j = Ip2Int(buf[64:68]) - Ip2Int(FirstStaMac[2:])
            packet = self.BuildOpenStaAssociateReqMsg(i, j)
#            print 'send: open station associate req'
            SendNetworkSockMsg(packet)
            staStat.elemadd('openassoreq')
        elif flag == '\x10\x00':
            staStat.elemadd('openassorsp')
#            print 'recv: open station associate rsp'
    
class PeapStaPacket(object):
    "This is peap sta msg class"

class RadiusPacket(object):
    "This is radius msg class"

class PortalPacket(object):
    'This is portal msg class'
    def BuildChallengeReq(self, i):
        staIp = CalculateIp(i, Ip2Int(FirstStaIp))
        payload = PortalChallengeReq[:8] + staIp + PortalChallengeReq[12:]
        totel_len = 8 + len(payload)
        packet = ''
        packet = SetIpHeaders(hostIP_net, ac_ip_net, 5, 4, 0, totel_len, 1, 0, 255, socket.IPPROTO_UDP, 0) + SetUdpHeaders(22000, 2000, len(payload), 0) + payload + '\x00\x00'
        return packet

    def BuildAuthReq(self, staIp, reqId, challenge):
        challengePwd = '0123456789abcdef'
        pwd = '\x31'
        challengeId = reqId[1:2]
        md5.md5_challengePwd(challengeId, pwd, challenge, challengePwd)

        payload = PortalAuthReq[:6] + reqId + staIp + PortalAuthReq[12:21] + challengePwd
        totel_len = 8 + len(payload)
        packet = ''
        packet = SetIpHeaders(hostIP_net, ac_ip_net, 5, 4, 0, totel_len, 1, 0, 255, socket.IPPROTO_UDP, 0) + SetUdpHeaders(22000, 2000, len(payload), 0) + payload
        return packet

    def BuildAuthAff(self, staIp, reqId):
        payload = PortalAuthAff[:6] + reqId + staIp + PortalAuthAff[12:]
        totel_len = 8 + len(payload)
        packet = ''
        packet = SetIpHeaders(hostIP_net, ac_ip_net, 5, 4, 0, totel_len, 1, 0, 255, socket.IPPROTO_UDP, 0) + SetUdpHeaders(22000, 2000, len(payload), 0) + payload
        return packet

    def HandleRcvMsg(self, buf):
        staIp = buf[50:54]
        msgType = buf[43:44]
        reqId = buf[48:50]
        errCode = buf[56:57]
        if errCode != '\x00':
            return 
        if msgType == '\x02':
            challenge = buf[60:]
            packet = self.BuildAuthReq(staIp, reqId, challenge)
            SendNetworkSockMsg(packet)
        elif msgType == '\x04':
            packet = self.BuildAuthAff(staIp, reqId)
            SendNetworkSockMsg(packet)
