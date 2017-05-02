###########################################
#
#		RETE DI FEISTEL
#
###########################################


import bitstring
from bitstring import *

import hashlib
from hashlib import *



def feistel_block(chunk, chiave):
	chunk  = BitStream(chunk) #lo ripassiamo in BitStream ma non e' essenziale
	chiave = BitStream(chiave) #stesso discorso

	left_chunk = BitStream(bin = chunk.read('bin: 256')) #leggo i primi 256 bit del chunk
	chiave = chiave * 16 #duplico la mia chiave in modo che sia da 128 bit
	#comincio a leggere i primi 128 bit del chunk di destra
	right_chunk = BitStream(bin = chunk.read('bin:256'))
	right_chunk_with_key = BitStream(right_chunk ^ chiave)
	right_chunk_md5 = hashlib.sha256() #inizializzo l'md5
	right_chunk_md5.update( right_chunk_with_key.read('bin:256'))
	right_chunk_md5_part1 = BitStream(bytes = right_chunk_md5.digest())
	
	#leggo i rimanenti 128 bit del chunk di destra
	#right_chunk = BitStream(bin = chunk.read('bin:128'))
	#right_chunk_with_key = BitStream(right_chunk ^ chiave)
	#right_chunk_md5 = hashlib.md5() #inizializzo l'md5
	#right_chunk_md5.update( right_chunk_with_key.read('bin:128'))
	#right_chunk_md5_part2 = BitStream(bytes = right_chunk_md5.digest())
	
	#concateno i due right
	#right_chunk_md5_part1.append(right_chunk_md5_part2) 
	new_right = left_chunk ^ right_chunk_md5_part1 # Ri+1 = Li XOR Ri_md5 
	
	chunk.pos = 256 #mi metto in posizione 256, cosi da leggere la right al passo dopo 
	feist_block = BitStream(bin = chunk.read('bin:256')) # Li+1 = Ri
	feist_block.append(new_right) # Ri+1 = Li XOR new_right
	return feist_block


def feistel(chunk, key):#funzione che applica gli 8 blocchi feistel al blocco da 512bit (chunk) con la chiave key
	key=BitStream(key)
	chunk=BitStream(chunk)
	key_rev=key
	key_rev.reverse()#chiave invertita
	key1=~key#chiave negata
	key2=key&key_rev
	key3=key|key_rev
	key4=key^key_rev
	key5=~key_rev
	key6=~(key&key_rev)
	key7=~(key|key_rev)
	key8=~(key^key_rev)

	chunk=BitStream(feistel_block(chunk, key1))#processo il chunk col blocco 1
	chunk=BitStream(feistel_block(chunk, key2))#processo il risultato del blocco 1 col blocco 2
	chunk=BitStream(feistel_block(chunk, key3))#processo il risultato del blocco 2 col blocco 3
	chunk=BitStream(feistel_block(chunk, key4))#processo il risultato del blocco 3 col blocco 4
	chunk=BitStream(feistel_block(chunk, key5))#processo il risultato del blocco 4 col blocco 5
	chunk=BitStream(feistel_block(chunk, key6))#processo il risultato del blocco 5 col blocco 6
	chunk=BitStream(feistel_block(chunk, key7))#processo il risultato del blocco 6 col blocco 7
	chunk=BitStream(feistel_block(chunk, key8))#processo il risultato del blocco 7 col blocco 8
	return chunk

	
