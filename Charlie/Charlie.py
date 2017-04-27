# coding=utf-8
import glob
import json
import ast
import time
import os

wlan = "eth0"
#devo configurarlo come gateway C

# impostazione indirizzi IP
# os.system('sudo ifconfig -v ' + wlan + ':1 172.30.1.1/24')
# os.system('sudo ifconfig -v ' + wlan + ':2 172.30.2.1/24')
#
# # cancella le route di default
# os.system('sudo route del default')
#
# # aggiunge route per vedere le reti
# os.system('sudo route add -net 172.30.1.0 netmask 255.255.255.0 gw 172.30.1.1 dev ' + wlan + ':1')
# os.system('sudo route add -net 172.30.2.0 netmask 255.255.255.0 gw 172.30.2.1 dev ' + wlan + ':2')
#
# # abilitare il forwarding dei pacchetti
# os.system('sudo sysctl -w net.ipv4.ip_forward=1')
#
# # disabilita ICMP redirect
# os.system('sudo sysctl -w net.ipv4.conf.all.accept_redirects=0')
# os.system('sudo sysctl -w net.ipv4.conf.all.send_redirects=0')
#
# # default
# os.system('sudo sysctl -w net.ipv4.conf.default.accept_redirects=0')
# os.system('sudo sysctl -w net.ipv4.conf.default.send_redirects=0')
#
# # dev wlan
# os.system('sudo sysctl -w net.ipv4.conf.' + wlan + '.accept_redirects=0')
# os.system('sudo sysctl -w net.ipv4.conf.' + wlan + '.send_redirects=0')
#
# # lo
# os.system('sudo sysctl -w net.ipv4.conf.lo.accept_redirects=0')
# os.system('sudo sysctl -w net.ipv4.conf.lo.send_redirects=0')

###############################################################################

print'\033[94m######   ##     ##    ###    ########  ##       #### ########'
print'##    ## ##     ##   ## ##   ##     ## ##        ##  ##       '
print'##       ##     ##  ##   ##  ##     ## ##        ##  ##       '
print'##       ######### ##     ## ########  ##        ##  ######   '
print'##       ##     ## ######### ##   ##   ##        ##  ##       '
print'##    ## ##     ## ##     ## ##    ##  ##        ##  ##       '
print'######   ##     ## ##     ## ##     ## ######## #### ######## \033[0m\n'

int_option3 = None
while int_option3 is None:

    print "1) sniffing packet"

    try:
        option3 = raw_input()
    except SyntaxError:
        int_option3 = None

    if option3 == '1':
        os.chdir("../")
        os.system('python sniffer.py')
