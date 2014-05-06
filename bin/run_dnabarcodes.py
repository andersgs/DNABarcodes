#!/usr/bin/env python

'''
run_dnabarcodes.py

'''

import sys, argparse, textwrap
from dnabarcodes.dnabarcodes_class import DNABarcodes
from dnabarcodes import dbcodeConfig

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\

DNABarcodes
============

Process DNA barcodes through quality control and annotation steps.

	By
	Anders Goncalves da Silva and Rohan H. Clarke
	Monash University
	(C) 2014
			'''))

parser.add_argument('c', metavar='FILENAME', type=argparse.FileType('rb'), help='the configuration file')

parser.add_argument('-minQ','--min_quality', action='store',type=float,metavar='INT', help='minimum acceptable base quality')

parser.add_argument('-minQP','--min_quality_prop', action='store', type=float,metavar='FLOAT', help='minimum acceptable proportions of bases with minimum base quality')     

#parser.add_argument('-r','--raw', action='store_true', default='store_false', help='output raw DNA barcodes to a FASTA file [or FASTQ file if -fq is selected]')

parser.add_argument('-fq','--fastq', action='store_true', default='store_false',help='output DNA barcodes into a FASTQ formatted file')            

args = parser.parse_args()

def main():
	if args.cfgfile:
		cfg=dbcodeConfig.read(args.c)
	else:
		cfg=dbcodeConfig.create()

	if args.min_quality != None:
		cfg.set('reports','bcode_minQ',str(args.minQ))

	if args.min_quality_prop != None:
		cfg.set('reports','bcode_minQP',str(args.minQP))

	if args.raw:
		cfg.set('tasks','correct_readingFrame','False')

	if args.fastq:
		cfg.set('reports','bcode_format','fastq')

	run = DNABarcodes(cfg)
	run.sync()

if __name__=='__main__':
	main()