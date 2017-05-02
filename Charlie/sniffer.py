import sys
import pcapy
from struct import *
import socket
import os

# Rubo il file
f = open("sniffato.txt", "wb")
cap = pcapy.open_live("wlan0", 65536, 1, 0)
print "Listening on %s: net=%s, mask=%s, linktype=%d" % ('wlan0', cap.getnet(), cap.getmask(), cap.datalink())

while 1:
    (header, packet) = cap.next()
    eth_length = 14
    ip_header = packet[eth_length:eth_length + 20]
    iph = unpack('!BBHHHBBH4s4s', ip_header)
    version_ihl = iph[0]
    ihl = version_ihl & 0xF
    iph_length = ihl * 4
    if iph[6] == 17:
        d_addr = socket.inet_ntoa(iph[9])
        udph_length = 8
        u = iph_length + eth_length
        udp_header = packet[u:u + udph_length]
        udph = unpack('!HHHH', udp_header)
        offset = eth_length + udph_length + iph_length
        data = packet[offset:]
        if (udph[1] == 4000):
            f.write(data)
            print data
    elif (iph[6] == 6):
        t = iph_length + eth_length
        tcp_header = packet[t:t + 20]
        tcph = unpack('!HHLLBBHHH', tcp_header)
        sq = tcph[2]
        tcph_length = tcph[4] >> 4
        h_size = t + tcph_length * 4
        data = packet[h_size:]
        if ((tcph[1] == 4000)):
            f.write(data)
            print data
# Charlie incula il file verso Bob, calcola le frequenze della lingua utilizzata analizzando dei testi, calcola le frequenze del testo sniffato tra Alice e Bob e fa il mapping delle lettere in base alle frequenze

# FREQUENCY CALCULATION OF THE LANGUAGE

# FREQUENCY CALCULATION OF THE SNIFFED FILE

# CALCOLI VARI ED EVENTUALI TIPO % DI ERRORE ECC
