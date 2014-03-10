#!/usr/bin/python
#Filename: start.py

import sys, time, thread, os
from packetclass import *

cw_msg = CwPacket() 
open_sta_msg = OpenStaPacket()
peap_sta_msg = PeapStaPacket()
radius_msg = RadiusPacket()
portal_msg = PortalPacket()

PORTAL_PORT = '\x07\xd0'
AUTH_PORT = '\x07\x14'
CWCTRL_PORT = '\x14\x7e'
CWDATA_PORT = '\x14\x7f'

PROTOCAL_TYPE_ARP = '\x08\x06'

#create thread 1: recv msg 
def recv_msg():
    print 'execute recv_msg thread ...'
    while True:
        buf = link_raw_sock.recvfrom(65535)[0]
        IpSrcPort = buf[34:36]
        IpDstPort = buf[36:38]
        protocal = buf[12:14]

        if protocal == PROTOCAL_TYPE_ARP:
            if buf[28:32] == ac_ip_net and buf[20:22] == '\x00\x01':
#                print 'recv: arp request msg'
                packet = buf[6:12] + HostMac + buf[12:20] + '\x00\x02' + HostMac + buf[38:42] + buf[6:12] + buf[28:32] + buf[42:]
                link_raw_sock.send(packet)
        elif IpSrcPort == CWCTRL_PORT:
            cw_msg.HandleRcvMsg(buf)
        elif IpSrcPort == CWDATA_PORT:
            Header = buf[43:47]
            if Header == '\x20\x83\x20\x00':
                open_sta_msg.HandleRcvMsg(buf)
            else :
                cw_msg.HandleRcvMsg(buf)
        elif IpSrcPort == PORTAL_PORT:
            portal_msg.HandleRcvMsg(buf)

#send arp request
def start_ap_arp():
    for i in range(ApNum):
#        print 'send: arp req'
        SendArpRequestMsg(i)
        if ((i+1) % 1500 == 0:
            time.sleep(1)
			
#start ap
def start_ap():
    for i in range(ApNum):
        packet = cw_msg.BuildDiscoveryRequestMsg(i)
#        print 'send: discover req'
        SendNetworkSockMsg(packet)
        apStat.elemadd('disreq')
        if ((i+1) % ApOnlineSpeed) == 0:
            time.sleep(1)
'''
    for i in range(ApNum):
        packet = cw_msg.BuildJoinRequestMsg(i)
        SendNetworkSockMsg(packet)
        if (i % ApOnlineSpeed) == 0:
            time.sleep(1)
    for i in range(ApNum):
        packet = cw_msg.BuildConfigRequestMsg(i)
        SendNetworkSockMsg(packet)
        if (i % ApOnlineSpeed) == 0:
            time.sleep(1)
    for i in range(ApNum):
        packet = cw_msg.BuildChangeStateRequestMsg(i)
        SendNetworkSockMsg(packet)
        if (i % ApOnlineSpeed) == 0:
            time.sleep(1)
    for i in range(ApNum):
        packet = cw_msg.BuildKeepaliveMsg(i)
        SendNetworkSockMsg(packet)
        if (i % ApOnlineSpeed) == 0:
            time.sleep(1)
    for i in range(ApNum):
        packet = cw_msg.BuildEchoRequestMsg(i)
        SendNetworkSockMsg(packet)
        if (i % ApOnlineSpeed) == 0:
            time.sleep(1)
'''
def start_open_sta():
    for i in range(ApNum):
        for j in range(StaNumPerAp):
            k = j + (i * StaNumPerAp)
            packet = open_sta_msg.BuildOpenStaAuthMsg(i, k)
#            print 'send: open station auth req'
            SendNetworkSockMsg(packet)
            staStat.elemadd('openauthreq')

            if ((k+1) % StaOnlineSpeed) == 0:
                time.sleep(1)

def start_portal_sta():
    for i in range(PortalStaNum):
        packet = open_sta_msg.BuildArpReqMsg(i)
        link_raw_sock.send(packet)
    time.sleep(5)
    for i in range(PortalStaNum):
        packet = portal_msg.BuildChallengeReq(i)
        SendNetworkSockMsg(packet)
		
        if ((i+1)%PortalStaOnlineSpeed) == 0:
            time.sleep(1)

def printStat(interval):
    print 'execute printStat thread ...'
    tmp = myTimer(interval, printStatAll, [apStat, staStat, interval])
    tmp._run()

def main():

    thread.start_new_thread(recv_msg, ())

    start_ap_arp()
    time.sleep(1)

    thread.start_new_thread(printStat, (Interval,))

    start_ap()
    time.sleep(20)

    start_open_sta()
    time.sleep(10)
	
    start_portal_sta()

    while True:
        time.sleep(1000)
        pass

main()