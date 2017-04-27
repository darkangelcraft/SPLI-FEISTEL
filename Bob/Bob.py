# coding=utf-8
import os
import glob

wlan = "eth0"
#devo configurarlo come host B
#os.system('ifconfig ' + wlan + ' 172.30.2.2/24')
#os.system('route add default gw 172.30.2.1')

###############################################################################

print'\033[94m#######   ######### ######## '
print'##     ## ##     ## ##     ##'
print'##     ## ##     ## ##     ##'
print'########  ##     ## ######## '
print'##     ## ##     ## ##     ##'
print'##     ## ##     ## ##     ##'
print'########   #######  ########\033[0m\n'


int_option2 = None
while int_option2 is None:

    print '1) receiv'
    print '2) decrypt'

    try:
        option2 = raw_input()
    except SyntaxError:
        int_option2 = None

    # RECEIVER
    if option2 == '1':
        print 'waiting...'
        os.system('nc -l -p 4000 | pv -rb > image_encrypted.txt')

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

    elif option2 == '2':
        print 'da implementare..'


