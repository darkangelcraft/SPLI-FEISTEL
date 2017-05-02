import sys
import time
import bitstring
from bitstring import *
import hashlib
from hashlib import *

ORIGINAL_FILE="./original.jpg"
ENCRYPTED_FILE="./encrypted.jpg"
DECRYPTED_FILE="./decrypted_image.jpg"
CHUNK_LEN=512#bit

#APPLICAZIONE DI DEFEISTEL AD UN SINGOLO CHUNK
def single_iteration_defeistel(chunk, key_i):
    #ripeto la chiave 16 volte (sono necessari 256 bit di chiave per effettuare lo XOR)
    key_i = key_i*16
    chunk.pos=0

    #funzione f
    left_part=BitStream(bin=chunk.read('bin:'+str(CHUNK_LEN/2)))
    left_partXOR=BitStream(left_part^key_i)
    left_part_sha256=hashlib.sha256()
    left_part_sha256.update(left_partXOR.read('bin:'+str(CHUNK_LEN/2)).encode('utf-8'))
    left_part_sha256=BitStream(bytes=left_part_sha256.digest())
    right_part=BitStream(bin=chunk.read('bin:'+str(CHUNK_LEN/2)))
    Li=left_part_sha256^right_part

    #attacco Li davanti ad Ri (mediante prepend)
    chunk.pos=0
    defeist_block=BitStream(bin=chunk.read('bin:'+str(CHUNK_LEN/2)))#Ri
    defeist_block.prepend(Li)

    return defeist_block


#CHIAMO 8 VOLTE IN CASCATA LA FUNZIONE "single_iteration_defeistel" PER RESTITUIRE UN CHUNK DECRIPTATO
def decrypt(chunk, key):
    key=BitStream(key)
    chunk=BitStream(chunk)

    #creazione delle 8 chiavi a partire da quella base
    key_rev=key
    key_rev.reverse()
    key1=~key
    key2=key&key_rev
    key3=key|key_rev
    key4=key^key_rev
    key5=~key_rev
    key6=~(key&key_rev)
    key7=~(key|key_rev)
    key8=~(key^key_rev)

    #ottengo ogni chunk mediante l'invocazione della funzione passandogli il vecchio valore del chunk e la giusta chiave
    chunk=BitStream(single_iteration_defeistel(chunk, key8))
    chunk=BitStream(single_iteration_defeistel(chunk, key7))
    chunk=BitStream(single_iteration_defeistel(chunk, key6))
    chunk=BitStream(single_iteration_defeistel(chunk, key5))
    chunk=BitStream(single_iteration_defeistel(chunk, key4))
    chunk=BitStream(single_iteration_defeistel(chunk, key3))
    chunk=BitStream(single_iteration_defeistel(chunk, key2))
    chunk=BitStream(single_iteration_defeistel(chunk, key1))

    return chunk


#CONTROLLO SULLA CORRETTEZZA DELL'IMMAGINE DECIFRATA
def corrected_decryption(decrypted_image):
    original_image=BitStream(filename=ORIGINAL_FILE)
    if original_image==decrypted_image:
        return True
    else:
        print"Incorrect key\n"
        return False



#DECRIPTAZIONE IMMAGINE CIFRATA
def bruteforce_attack():
    key=BitStream('0b 0000 0000 0000 0001')
    i=0
    c=1
    chunks=[]
    decrypted_chunks=[]
    flag=False
    tmp_flag=True
    t1=time.time()
    try:
        image=BitStream(filename=ENCRYPTED_FILE)
    except IOError:
        print('Image not found\n')
        sys.exit(-1)

    image_len=image.length
    num_chunk=image_len / CHUNK_LEN
    print"Encrypted image read - (%d Bytes) - %d chunks" % (image_len / 8, num_chunk)

    chunks=[None]*num_chunk
    decrypted_chunks=[None]*num_chunk
    while flag==False:
        print"Attempt to decrypt #%d\nKey used ---> %d" % (c, key.uint)
        for i in range(num_chunk):
            chunks[i]=BitStream(bin=image.read('bin:'+str(CHUNK_LEN)))
            if(i==0):
                final_image=decrypt(chunks[i], key)
            else:
                decrypted_chunks[i]=decrypt(chunks[i],key)
                final_image.append(decrypted_chunks[i])

        flag=corrected_decryption(final_image)

        if flag == True:
            print"Key found ---> %d"%key.uint

            #scrittura su file del contenuto decriptato
            try:
                f=open(DECRYPTED_FILE, 'wb')
                BitStream(final_image).tofile(f)
                f.close()
                break
            except IOError:
                print("Cannot save the decrypted file\n'")
                sys.exit(-3)
        #aggiustamento parametri per iterazione successiva
        c+=1
        key=key.uint + 1
        key=BitStream(uint=key, length=16)
        image.pos=0

    t2=time.time()
    elapsed_time=(t2-t1)
    print"time spent:%.3f seconds"%elapsed_time
    print"\n==================================================================="
    print"Attack finished! You can now open the decrypted image\n===================================================================\n\n\n"


#=================================INIZIO "MAIN"=================================
print "\n\n\t|---------------------------|"
print "\t|Bruteforce Attack - Feistel|"
print "\t|---------------------------|\n\n"

print"\tMAIN MENU"
print"\n1) Start bruteforce attack"
print"2) exit"
selection=raw_input()
if int(selection)==1:
    bruteforce_attack()
elif int(selection)==2:
    sys.exit(0)
else:
    print"wrong input\n"