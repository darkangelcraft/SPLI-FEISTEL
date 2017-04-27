# coding=utf-8
import os
import glob
import json
import ast


wlan = "eth0"
#devo configurarlo come host A
#os.system('ifconfig ' + wlan + ' 172.30.1.2/24')
#os.system('route add default gw 172.30.1.1')

###############################################################################

images=[]
image_selected=0

###############################################################################

print'\033[94m#########  ##       ####  ######    ########'
print'##     ##  ##        ##   ##        ##'
print'##     ##  ##        ##   ##        ##'
print'##     ##  ##        ##   ##        ######'
print'#########  ##        ##   ##        ##'
print'##     ##  ##        ##   ##        ##'
print'##     ##  ######## ####  ########  ########\033[0m\n'

int_option1 = None
while int_option1 is None:

    print '1) select image'
    print '2) crypt'
    print '3) send'

    try:
        option1 = raw_input()
    except SyntaxError:
        int_option1 = None


    #seleziono il file
    if option1 == '1':

        images = glob.glob("image*")

        # stampo i file da selezionare
        i = 0
        for num in images:
            print '\t' + str(i) + ') ' + images[i]
            i = i + 1

        try:
            image_selected = raw_input()
        except SyntaxError:
            option = None

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

    # CIFRATURA
    elif option1 == '2':
        print 'da implementare..'

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

    # invio file cifrato con netcat
    elif option1 == '3':
        print 'sending image..'
        os.system('pv image_encrypted.gif | nc -w 1 172.30.2.2 4000')


