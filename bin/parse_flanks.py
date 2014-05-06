#!/usr/bin/env python

'''
parse_flanks.py in.fa out.fa leftflank_start leftflank_end rightflank_start rightflank_end

'''

import sys, re
from Bio import SeqIO

def usage():
	print "To use parse_flanks.py, type in the command line:"
	print ""
	print "> parse_flanks.py in.fa out.fa 0 234 714 0"
	print ""
	print "Where in.fasta is a fasta file containing aligned sequences"
	print "out.fa is the name of the output file"
	print ", 0 and 234 specify that one flank should contain the sequence from the "
	print "beginning of the sequence to, and including, base 234."
	print ", and 714 and 0 specify that other flank should include the sequence from"
	print "base 714 to the end of the sequence, not including base 714."
	print ""
	
def flanks(infile,outfile,lstart,lend,rstart,rend):
	seqs = []
	for recs in SeqIO.parse(infile,"fasta"):
		if lstart == 0:
			tmp = recs[:lend]
			tmp.id = tmp.id+"from 1..{}".format(lend)
			seqs.append(tmp)
		else:
			tmp = recs[lstart:lend]
			tmp.id = tmp.id+"from {}..{}".format(lstart,lend)
			seqs.append(tmp)
		
		if rend == 0:
			tmp = recs[rstart:]
			tmp.id = tmp.id+"from {}..{}".format(rstart,len(tmp))
			seqs.append(tmp)
		else:
			tmp = recs[rstart:rend]
			tmp.id = tmp.id+"from {}..{}".format(rstart,rend)
			seqs.append(tmp)
	SeqIO.write(seqs,outfile,"fasta")

def main():
	if len(sys.argv) != 7:
		usage()
	else:
		flanks(sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]))
		
if __name__=="__main__":
	main()
			