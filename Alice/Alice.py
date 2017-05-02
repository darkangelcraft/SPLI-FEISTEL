# coding=utf-8
import os
import glob
import json
import ast

import sys
from bitstring import BitStream
import feistel
from feistel import *

wlan = "eth0"
#devo configurarlo come host A
os.system('ifconfig ' + wlan + ' 172.30.1.2/24')
os.system('route add default gw 172.30.1.1')

###############################################################################

images=[]
image_selected=0

# COSTANTE che indica il numero di bit di cui e' composto un chunk
CHUNK_DIM = 512

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
        # Apro l'immagine che voglio criptare
        try:
            # A BitStream is a mutable container of bits with methods and properties that allow it to be parsed as a stream of bits.
            # Both the BitArray and the ConstBitStream classes are base classes for BitStream and so all of their methods are also available for
            # BitStream objects.
            # 	image = BitStream(filename = './lena256.raw')
            image = BitStream(filename="./image.jpg")
        except IOError:
            print('image not found')
            sys.exit(0)

        # restituisce la lunghezza in bit dell'oggetto bitstring
        image_len = image.length
        print("image to cipher is:"+str("image")+" , \ndimensione %d Bits (%d Bytes)," % (image_len, image_len / 8))

        # controllo di quanti chunk e' formata l'immagine
        num_chunk = image_len / CHUNK_DIM
        print('formate da: %d chunk esatti' % num_chunk)

        # controllo di quanti chunk e' formata l'immagine
        num_chunk = image_len / CHUNK_DIM
        print('formed by: %d chunk' % num_chunk)

        # controllo che l'immagine binaria sia multiplo di 512 bit
        # se non e' multipla , ciclo quanto basta per aggiungere alla fine dell'immagine degli zeri per renderla multipla
        resto = image_len % CHUNK_DIM
        if (resto != 0):
            for i in range(CHUNK_DIM - resto):  # i=0, ..., x
                image.append('0b 0')
            image_len = image.length
            print('The image has been edited!')
            print("Image : %d Bits" % image_len)

        ###########################################
        # METTERE LA PARTE INERENTE LA FUNZIONE F
        ###########################################

        # key ="0000000000000011"	#chiave a 16 bit = 3(10)
        # key=BitStream(bin=key)
        key = BitStream('0b 0000 0000 0000 0111')
        # N=BitStream('0b 01010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101')
        # print ("Chiave di cifratura: %d, N: %d" % (key.int, N.int))
        print ("Encryption key: %d" % (key.int))

        # comincio a prelevare chunk e a compiere la cifratura
        for i in range(num_chunk):  # i=0, ..., 1024
            chunk = BitStream(bin=image.read('bin:512'))  # prelevo un chunk dalla immagine per la prima lettura
            if i == 0:
                print ("i: %d chunk: " % i)
                print chunk
            if image.pos == 512:
                # chunk = chunk^N #faccio lo XOR con un N deciso da noi
                cifrato = BitStream(feistel(chunk, key))
                old_chunk = cifrato
            # per le altre letture
            else:
                # chunk = chunk ^ old_chunk
                feist_chunk = feistel(chunk, key)
                cifrato.append(feist_chunk)
                old_chunk = feist_chunk

        print('Cipher completed!')
        critto_image_path = open('./encrypted.jpg', 'wb')
        BitStream(cifrato).tofile(critto_image_path)
        critto_image_path.close()

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

    # invio file cifrato con netcat
    elif option1 == '3':
        print 'sending image..'
        os.system('pv encrypted.jpg | nc -w 1 172.30.2.2 4000')


