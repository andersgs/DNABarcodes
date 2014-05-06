#!/usr/bin/env python

'''
test_regex.py

'''

import sys, argparse, textwrap, re, os

###########################
### The validation function
###########################

def validate_regex(pat,raw_data_path,chrom_type):
	'''
	validate_regex: takes a pat(tern) plus an input directory, and a chromatogram extension (e.g., .ab1), and outputs how many files match the regex.
	
	The test is based on the traces found in the test folder of the package.
	The first test will give 10 out of 10, and the second only 8 out of 10, as 
	 the trace files with a band ID beginning with K won't be matched.
	
	>>> validate_regex("B_((K[0-9]{6})|([0-9]{3}-[0-9]{5}))_[0-9]{2}", "../dnabarcodes/test/test_traces/",".ab1")
	Found 10 files matching the regex out of 10 trace files.
	Done!
	>>> validate_regex("B_(([0-9]{3}-[0-9]{5}))_[0-9]{2}", "../dnabarcodes/test/test_traces/",".ab1")
	Found 8 files matching the regex out of 10 trace files.
	Done!
	'''
	#load up all the trace files in the infolder according to the extension into a list
	fnames = []
	for root,dirs,files in os.walk(raw_data_path):
		for f in files:
			if re.search(chrom_type,f):
				fnames.append(os.path.join(root,f))
	#count how many trace files match the regex
	count = 0
	for f in fnames:
		if re.search(pat,f):
			count += 1
	#raise an exception if the count is zero
	if count == 0:
		print "The pattern {} does not seem to match any files in {}.\nPlease check your expression using a regex tester online.".format(pat,raw_data_path)
		return False
	
	#if count is larger than zero, print out the number of matches compared to the number
	# of traces. They should be the same.
	print "Found {} files matching the regex out of {} trace files.".format(count,len(fnames))
	print 'Done!'
	return True
	
def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\

	A regex tester, suitable to test if a particular regex is capable of returning all the trace files in a raw data file. 

	Output: Count of files that match the regex expression.

	'''))

	###########################
	### Setting up the options
	###########################

	parser.add_argument('infolder', metavar='FOLDER', help='folder with trace files [default=\'.\']',default='.')

	parser.add_argument('regex', action='store',type=str,metavar='STR', help='regex expression')

	parser.add_argument('ext', action='store',type=str,metavar='STR', help='file extenstion of the trace files (e.g., .ab1 for ABI trace files)')

	parser.add_argument('-d', action='store_true', help='run in debug mode')

	parser.add_argument('-t', action='store_true', help='run in test mode')


	###########################
	### Loading the options
	###########################

	args = parser.parse_args()

	infolder = args.infolder
	regex = args.regex
	ext = args.ext
	
	###########################
	### Validate
	###########################
	#if in debug mode, just print out the arguments
	if args.d:
		print args
	
	#if in test mode, run the test in the docstring
	elif args.t:
		import doctest
		doctest.testmod()
	
	#else, run the function
	else:
		validate_regex(regex,infolder,ext)

if __name__=="__main__":
	#the main function
	main()