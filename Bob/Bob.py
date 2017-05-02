# coding=utf-8
import os
import glob
import defeistel
from defeistel import *

from bitstring import BitStream

wlan = "eth0"
#devo configurarlo come host B
#os.system('ifconfig ' + wlan + ' 172.30.2.2/24')
#os.system('route add default gw 172.30.2.1')

###############################################################################

# Input
key = BitStream('0b 0000 0000 0000 0111')

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
        os.system('nc -l -p 4000 | pv -rb > encrypted.jpg')

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

    elif option2 == '2':
        # Decryption
        print('\nDecryption is processing...')
        bit_enc = BitStream(filename='./encrypted.jpg')  # apro il file encrypted.raw in bit
        len_bit_enc = bit_enc.length
        quoziente = len_bit_enc / 512

        for i in range(quoziente):
            bit_enc.pos = len_bit_enc - (
                (
                i + 1) * 512)  # posiziono il cursore per la lettura in modo da leggere dall'ultimo blocco da 512 al primo
            chunk = BitStream(bin=bit_enc.read(
                'bin:512'))  # prendo un blocco da 512bit (il cursore si sposta automaticamente ogni volta che leggo)
            if bit_enc.pos == len_bit_enc:  # lettura ultimo blocco
                # print(i)
                defeist_chunk = BitStream(defeistel(chunk, key))
            # print(defeist_chunk)
            elif bit_enc.pos == 512:  # lettura primo blocco
                # defeist_chunk=defeist_chunk^chunk#Xor tra primo blocco feistelizzato e secondo blocco defeistelizzato
                original.prepend(defeist_chunk)
                defeist_chunk = defeistel(chunk, key)  # applico Feistel al blocco chunk con la chiave key
                # defeist_chunk=defeist_chunk^N#blocco_1 XOR bit a bit con N (512 bit random da noi scelti)
                original.prepend(defeist_chunk)  # inizializzo quello che sarà l'output
            else:  # lettura blocchi dall'ultimo al secondo
                # defeist_chunk=defeist_chunk^chunk
                if bit_enc.pos == len_bit_enc - 512:  # se sto considerando il penultimo blocco
                    original = defeist_chunk  # original è la variabile che conterrà i bit del file immagine che voglio ricostruire
                else:
                    original.prepend(defeist_chunk)
                defeist_chunk = defeistel(chunk, key)  # applico defeistel al blocco chunk con la chiave key
                # print(i)
                # print(defeist_chunk)

        # Scrittura su file
        print("\nDecryption Complete!\n")
        d = open('./decrypted.jpg', 'wb')
        BitStream(original).tofile(d)
        d.close()



