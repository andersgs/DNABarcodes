#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
create_barcode_proj.py

'''
#import pdb; pdb.set_trace()
#import the necessary libraries
import sys, string, argparse, textwrap, os, time, shutil, re 
from dnabarcodes import dbcodeConfig
from dnabarcodes.dnabarcodes_class import DNABarcodes
from test_regex import validate_regex

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\

DNABarcodes
============

Process DNA barcodes through quality control and annotation steps.

	By
	Anders Goncalves da Silva and Rohan H. Clarke
	Monash University
	(C) 2014
			'''))

parser.add_argument('-c', metavar='FILENAME', type=argparse.FileType('r'), help='a config file')
            
args = parser.parse_args()

if args.c:
	cfg = dbcodeConfig.read(args.configfile)
elif os.path.isfile('dbcode.cfg'):
	cfg = dbcodeConfig.read('dbcode.cfg')
else:
	cfg = dbcodeConfig.create()


#########################################################################################
## Menu items ###########################################################################
#########################################################################################

def main_menu():
	global cfg
	while True:
		os.system('clear')
		print "#Welcome to DNABarcodes setup utility#"
		print "====================================="
		print "Version 0.1dev"
		print "Authors: Anders Goncalves da Silva and Rohan H. Clarke"
		print "Monash University"
		print "(C) 2014"
		print "Date: April 2014"
		print "-------------------------------------------------------"
		print ""
		print "Please select from one of the available options:"
		print ""
		print "(P)roject metadata"
		print "(T)asks setup"
		print "(R)eporting options"
		print "(S)ave configuration"
		print "(E)xecute DNAbarcodes"
		print "(Q)uit"
		print ""
		
		menu_item=raw_input('---> ')
		if menu_item not in ['P','T','S','R','E', 'Q']:
			print 'Please choose either P, T, R, S, E or Q...'
			print ''
			raw_input("Press any key to continue...")
			main_menu()
		if menu_item == 'Q':
			break
		if menu_item == 'P':
			metadata_menu()
		if menu_item == 'T':
			task_menu()
		if menu_item == 'R':
			reports_menu()
		if menu_item == 'S':
			fname = os.path.join(cfg.get('metadata','home_folder'),'dbcode.cfg')
			fh = open(fname,'wb')
			cfg.write(fh)
			fh.close()
			print 'Config file {} saved successfully'.format(fname)
			raw_input('Press any key to continue...')
		if menu_item == 'E':
			run = DNABarcodes(cfg)
			run.sync()
			break

def metadata_menu():
	global cfg
	
	while True:
		os.system('clear')
		print "Metadata menu"	
		print "============="
		print "(P)roject basename: {} [project basename]".format(cfg.get('metadata','project_basename'))
		print "(H)ome folder: {} [the location and name of the project's main folder]".format(cfg.get('metadata','home_folder'))
		print "(T)race data folder: {} ({}) [location of raw trace data (and trace file extension)]".format(cfg.get('metadata','traces_folder'),cfg.get('metadata','trace_ext'))
		print "(E)xpression: {} [regex to search for trace files]".format(cfg.get('metadata','regex'))
		print "(A)ssemblies folder: {} [folder where individual sample assemblies are stored]".format(cfg.get('metadata','barcodes_folder'))
		print "(O)utput folder: {} [folder where reports and QC'ed barcodes are stored]".format(cfg.get('metadata','reports_folder'))
		print "(R)eferences folder: {} [folder where reference FASTA files are kept]".format(cfg.get('metadata','ref_folder'))
		print "(C)opy existing phd files: {}".format(cfg.get('metadata','copy_phd'))
		print "(B)ack to main menu."
		print ""
		meta_menu_item=raw_input('--> ')
		
		if meta_menu_item not in ['P','H'',T','E','A','O','R','C','B']:
			print 'Please choose either T, E, H, R, ,C or B.'
			print ''
			raw_input("Press any key to continue...")
			metadata_menu()
		
		if meta_menu_item=='B':
			break
		
		if meta_menu_item=='P':
			print "Enter a new basename (leave blank for default: {}):".format(cfg.get('metadata','project_basename'))
			tmp=raw_input('--> ')
			if tmp=='':
				continue
			else:
				cfg.set('metadata','project_basename',tmp)
		
		if meta_menu_item=='E':
			print "Enter a new regex (leave blank for default):"
			tmp=raw_input('--> ')
			if tmp=='':
				pass
			else:
				cfg.set('metadata','regex',tmp)
			while True:
				print "Would you like to test the regex expression? [y/n]"
				ans = raw_input('--> ')
				if ans not in ['y','n']:
					print 'Please print y or n...'
					raw_input('Press any key to continue...')
					continue
				elif ans == 'n':
					print 'It is recommended you test your regex to ensure it is working before continuning'
					raw_input('Press any key to return to the menu...')
					break
				else:
					if validate_regex(cfg.get('metadata','regex'),cfg.get('metadata','traces_folder'),cfg.get('metadata','trace_ext')):
						print ""
						print "Your regex is finding a number of samples that match."
						print "Double check if it is finding the right number of files"
						raw_input('Press any key to continue...')
						break
					else:
						print ''
						print ''
						print "It seems the regex tester failed to find any matchs"
						print "Test it out out at http://regexpal.com."
						print "If it works on regexpal but not with DNABarcodes, email andersgs at googlemail dot com"
						print "Please send a test trace file and your regex."
						raw_input("Press any key to continue...")
						break
		
		if meta_menu_item=='H':
			while True:
				print "Enter a new home folder (leave blank for default):"
				tmp=raw_input('--> ')
				if tmp=='':
					pass
				else:
					home_folder=cfg.set('metadata','home_folder',os.path.abspath(tmp))
				if test_dir(cfg.get('metadata','home_folder')) =='break':
					break
		
		if meta_menu_item=='T':
			while True:
				print "Enter the name for the raw trace data folder for your project (leave blank for default)."
				print "If the folder does not exist, it will be created. If you already"
				print "have raw traces, you will have the opportunity to copy them over."
				tmp=raw_input('--> ')
				if tmp=='':
					pass
				else:
					raw_folder=cfg.set('metadata','traces_folder',os.path.join(cfg.get('metadata','home_folder'),tmp))
					print "Please type the extension to the trace files (if blank default=ab1)"
					tmp = raw_input('--> ')
					if tmp == '':
						continue
					else:
						cfg.set('metadata','trace_ext',tmp)
				if test_dir(cfg.get('metadata','traces_folder')) == 'break':
					traces = []
					for dr,dn,fn in os.walk(cfg.get('metadata','traces_folder')):
						for f in fn:
							if re.search(cfg.get('metadata','trace_ext'),f):
								traces.append(f)
					if os.listdir(cfg.get('metadata','traces_folder'))==[] or traces == []:
						print "It appears that your raw data folder is empty."
						print "Would you like to copy over sequencing data run folders now?[y/n]"
						while True:
							ans = raw_input('--> ')
							if ans not in ['y','n']:
								print "Answer should be 'y' or 'n'. Please try again"
								raw_input("Please press any to try again...")
							else:
								break
						if ans == 'n':
							break
						else:
							while True:
								print 'Please enter a folder path to the folder containing'
								print 'folders with sequencing trace data (one sub-folder per run)'
								while True:
									src = os.path.abspath(raw_input('--> '))
									total_runs = 0
									total_traces = 0
									if validate_dir(src):
										run_folders = os.listdir(src)
										for folder in run_folders:
											if folder[0] == '.':
												continue
											else:
												total_runs += 1
												trace_folder = os.path.join(src,folder)
												trace_files = [f for f in os.listdir(trace_folder) if re.search(cfg.get('metadata','trace_ext'),f)]
												if trace_files != []:
													total_traces += 1
													dest_folder = os.path.join(cfg.get('metadata','traces_folder'),folder)
													os.mkdir(dest_folder)
													for trace_file in trace_files:
														shutil.copy(os.path.join(trace_folder,trace_file),dest_folder)
										
										print "Successfully copied {} run folders, for a total {} traces.".format(total_runs,total_traces)
										raw_input('Press any key to return to the menu...')
										break
									else:
										print "Folder did not contain any trace files"
										print "Please enter a new folder name"
										run_input('Press any key to return to the menu...')
										break
								break
									
					else:
						print "It appears that your raw data folder already has some traces."
						print "Would you like to copy over sequencing data run folders now?[y/n]"
						while True:
							ans = raw_input('--> ')
							if ans not in ['y','n']:
								print "Answer should be 'y' or 'n'. Please try again"
								raw_input("Please press any to try again...")
							else:
								break
						if ans == 'n':
							break
						else:
							while True:
								print 'Please enter a folder path to the folder containing'
								print 'folders with sequencing trace data (one sub-folder per run)'
								while True:
									src = os.path.expanduser(raw_input('--> '))
									if validate_dir(src):
										run_folders = os.listdir(src)
										for folder in run_folders:
											if folder[0] == '.':
												continue
											else:
												trace_folder = os.path.join(src,folder)
												trace_files = [f for f in os.listdir(trace_folder) if re.search(cfg.get('metadata','trace_ext'),f)]
												if trace_files != '[]':
													dest_folder = os.path.join(cfg.get('metadata','traces_folder'),folder)
													os.mkdir(dest_folder)
													for trace_file in trace_files:
														shutil.copy(os.path.join(trace_folder,trace_file),dest_folder)
										break
									else:
										print "Folder did not contain any trace files"
										print "Please enter a new folder name"
										run_input('Press any key to return to the menu...')
										break
					break
				else:
					print 'Folder {} does not exist or could not be created.'.format(cfg.get('metadata','traces_folder'))
					print 'Please try again.'
					raw_input('Press any key to return to the menu')
					break
		
		if meta_menu_item=='A':
			while True:
				print "Please enter the full path for the assemblies folder"
				print "Default is {} - leave blank to accept the default".format(cfg.get('metadata','barcodes_folder'))
				tmp = raw_input('--> ')
				if tmp == '':
					if test_dir(cfg.get('metadata','barcodes_folder')) == 'break':
						break
				else:
					if test_dir(tmp) == 'break':
						cfg.set('metadata','barcodes_folder',tmp)
						break
		
		if meta_menu_item=='O':
			while True:
				print "Please enter the full path for the output folder"
				print "Default is {} - leave blank to accept the default".format(cfg.get('metadata','reports_folder'))
				tmp = raw_input('--> ')
				if tmp == '':
					if test_dir(cfg.get('metadata','reports_folder')) == 'break':
						break
				else:
					if test_dir(tmp) == 'break':
						cfg.set('metadata','reports_folder',tmp)
						break
		
		if meta_menu_item=='R':
			while True:
				print "Please enter the full path for the references folder"
				print "Default is {} - leave blank to accept the default".format(cfg.get('metadata','ref_folder'))
				tmp = raw_input('--> ')
				if tmp == '':
					if test_dir(cfg.get('metadata','ref_folder')) == 'break':
						break
				else:
					if test_dir(tmp) == 'break':
						cfg.set('metadata','ref_folder',tmp)
						break
		
		if meta_menu_item=='C':
			while True:
				print "Copy existing phd files ((T)rue or (F)alse) (Default: {}.".format(cfg.get('metadata','copy_phd'))
				print "By copying over phd files into phredPhrap assembly folders"
				print "You will skip Phred base-calling step."
				tmp=raw_input('--> ')
				if tmp=='':
					continue
				elif tmp not in ['T','F']:
					print "Please select: (T)rue or (F)alse."
					print ""
					raw_input("Press any key to continue...")
				else:
					if tmp =='T':
						cfg.set('metadata','copy_phd','True')
						while True:
							phd_files = []
							for dr,dn,fn in os.walk(cfg.get('metadata','traces_folder')):
								for f in fn:
									if re.search('phd',f):
										phd_files.append(f)
							if phd_files == []:
								print "There appears to be no phd files in your raw data folder."
								print "Would you like to copy them over from another file? [y/n]"
								while True:
									ans = raw_input('--> ')
									if ans not in ['y','n']:
										print 'Please answer y or n...'
										raw_input('Press any key to continue...')
									else:
										break
								if ans == 'n':
									print 'You have selected to copy phd files, yet there seems to be none in your raw data folder.'
									print 'This may lead to problems when running DNABarcodes.'
									print ' Please make sure to copy the phd files over before running the program'
									raw_input('Press any key to return to the menu...')
									break
								else:
									while True:
										print 'Please enter the path to the phd files folder.'
										print 'The path should be to a master folder containing sub-folders named by run'
										print 'As when copying over trace files'
										src = os.path.abspath(raw_input('--> '))
										if validate_dir(src):
											phd_folders = os.listdir(src)
											total_folders = 0
											total_files = 0
											for folder in phd_folders:
												if folder[0] == '.':
													continue
												total_folders += 1
												src_folder = os.path.join(src,folder)
												dest_folder = os.path.join(cfg.get('metadata','traces_folder'),folder)
												files = os.listdir(src_folder)
												for fi in files:
													if re.search('phd',fi):
														total_files += 1
														shutil.copy(os.path.join(src_folder,fi),dest_folder)
											if total_files == 0:
												print 'Found no phd files in {}'.format(src)
												print "Would you like to enter a new folder name? [y/n]"
												while True:
													ans = raw_input('--> ')
													if ans not in ['y','n']:
														print 'Please enter y or n'
														raw_input('Press any key to continue...')
													else:
														break
												if ans == 'y':
													continue
												else:
													print 'Please make sure to copy the phd files to their respective run folders'
													print 'in the {} folder before running DNABarcodes.'
													break																																	
											else:
												print "Copied {} phd files from {} folders".format(total_files,total_folders)
												raw_input('Press any key to continue')
												break
										else:
											print "Could find the folder {}".format(src)
											print "Would you like to enter a new folder name? [y/n]"
											while True:
												ans = raw_input('--> ')
												if ans not in ['y','n']:
													print 'Please enter y or n'
													raw_input('Press any key to continue...')
												else:
													break
											if ans == 'y':
												continue
											else:
												break
									break	
							else:
								print "Found phd files in your raw data folder."
								break	
						break
					else:
						cfg.set('metadata','copy_phd','False')
						break

def task_menu():
	global cfg
	
	while True:
		os.system('clear')
		print "Tasks menu"	
		print "============="
		print "(P)hredPhrap: {} [run phredPhrap]".format(cfg.get('tasks','run_phredphrap'))
		print "(V)ector/flank region database: {} [database for use with cross_match]".format(cfg.get('tasks','vector_db'))
		print "(N)CBI Blast: {} ({}) [run NCBI Blast (with database)]".format(cfg.get('tasks','run_wwwBlast'),cfg.get('tasks','wwwBlast_db'))
		print "(L)ocal Blast: {} ({}) [run local Blast (with database)]".format(cfg.get('tasks','run_localBlast'),cfg.get('tasks','localBlast_db'))
		print "(C)orrect reading frame: {} ({}) [correct reading frame (with protein database)]".format(cfg.get('tasks','correct_readingFrame'),cfg.get('tasks','localBlastX_db'))
		print "(B)ack to main menu."
		print ""
		task_menu_item=raw_input('--> ')
		
		if task_menu_item not in ['P','V','N','L','C','B']:
			print 'Please choose either P, N, L, C, B..'
			print ''
			raw_input("Press any key to continue...")
			task_menu()
		
		if task_menu_item=='B':
			break
		
		if task_menu_item=='P':
			while True:
				print "Run phredPhrap ((T)rue or (F)alse) (Default {}):".format(cfg.get('tasks','run_phredphrap'))
				tmp=raw_input('--> ')
				if tmp=='':
					break
				elif tmp not in ['T','F']:
					print "Please select: (T)rue or (F)alse."
					print ""
					raw_input("Press any key to continue...")
				else:
					if tmp =='T':
						cfg.set('tasks','run_phredphrap','True')
					else:
						cfg.set('tasks','run_phredphrap','False')
						print "*****WARNING*****"
						print "By not running phredPhrap, the rest of DNA Barcodes"
						print " might not work properly."
						print "*****WARNING*****"
						raw_input("Press any key to continue...")
					break
		
		if task_menu_item=='V':
			while True:
				print "Please give the full path to the FASTA file containing flanking regions to the barcode for use in cross_match"
				print "Default is {} - leave blank for default".format(cfg.get('tasks','vector_db'))
				tmp = raw_input('--> ')
				if tmp == '':
					break
				else:
					if os.path.isfile(tmp):
						cfg.set('tasks','vector_db',tmp)
					else:
						print "File {} does not exist in this path.".format(tmp)
						print "Do you wish to accept this filename [y] or do you wish to enter a new one [n] or accept the default [c]?"
						ans = raw_input('--> ')
						if tmp == 'y':
							print "Ok, but make sure that it exists before running dnabarcodes."
							raw_input("Press any key to continue...")
							break
						elif tmp == 'n':
							continue
						elif tmp == 'c':
							print "Accepting default {}.".format(cfg.get('tasks','cfg'))
							raw_input('Press any key to continue')
							break
						else:
							continue
		
		if task_menu_item=='N':
			while True:
				print "Run NCBI BLAST ((T)rue or (F)alse) (Default: {} with db {}):".format(cfg.get('tasks','run_wwwBlast'),cfg.get('tasks','wwwBlast_db'))
				tmp=raw_input('--> ')
				if tmp=='':
					break
				elif tmp not in ['T','F']:
					print "Please select: (T)rue or (F)alse."
					print ""
					raw_input("Press any key to continue...")
				else:
					if tmp == 'T':
						cfg.set('tasks','run_wwwBlast','True')
					else:
						cfg.set('tasks','run_wwwBlast','False')
					if run_wwwBlast:
						while True:
							print "Please name the BLAST database (nr,nt - leave blank for default {}):".format(cfg.get('tasks','wwwBlast_db'))
							tmp = raw_input('--> ')
							if tmp=='':
								break
							elif tmp not in ['nr','nt']:
								print "Please select either nr or nt"
								print ""
								raw_input("Press any key to continue...")
							else:
								cfg.set('tasks','rwwwBlast_db',tmp)
								break
					break
		
		if task_menu_item=='L':
			while True:
				print "Run local BLAST ((T)rue or (F)alse) (Default: {} with db {}:".format(cfg.get('tasks','run_localBlast'),cfg.get('tasks','localBlast_db'))
				tmp=raw_input('--> ')
				if tmp=='':
					break
				elif tmp not in ['T','F']:
					print "Please select: (T)rue or (F)alse."
					print ""
					raw_input("Press any key to continue...")
				else:
					if tmp == 'T':
						cfg.set('tasks','run_localBlast','True')
					else:
						cfg.set('tasks','run_localBlast','False')
					if run_localBlast:
						while True:
							print "Type to the path to the local BLAST database (leave blank for default):"
							tmp = raw_input('--> ')
							if tmp=='':
								print "Please type in the location of a FASTA file with reference nucleotide sequences"
							else:
								cfg.set('tasks','localBlast_db',tmp)
								if os.path.isfile(cfg.get('tasks','localBlast_db')):
									break
								else:
									print "The file {} does seem to exist".format(cfg.get('tasks','localBlast_db'))
									print "Please try again..."
									if raw_input("Please press 'c' to cancel, or any key to try again...") == 'c':
										break
									else:
										continue
					break
		
		if task_menu_item=='C':
			while True:
				print "Ensure that all barcodes are in the same reading frame ((T)rue or (F)alse) (Default: {}):".format(cfg.get('tasks','correct_readingFrame'),cfg.get('task','localBlastX_db'))
				tmp=raw_input('--> ')
				if tmp=='':
					break
				elif tmp not in ['T','F']:
					print "Please select: (T)rue or (F)alse."
					print ""
					raw_input("Press any key to continue...")
				else:
					if tmp == 'T':
						cfg.set('tasks','correct_readingFrame','True')
					else:
						cfg.set('tasks','correct_readingFrame','False')
					if correct_readingFrame:
						while True:
							print "Please type the path to the BLASTX database (leave blank for default):"
							tmp = raw_input('--> ')
							if tmp=='':
								print "Please type in the location of a FASTA file with reference protein sequences"
							else:
								cfg.set('tasks','localBlastX_db',os.path.abspath(tmp))
								if os.path.isfile(cfg.get('tasks','localBlastX_db')):
									break
								else:
									print "The file {} does seem to exist".format(cfg.get('tasks','localBlastX_db'))
									print "Please try again..."
									if raw_input("Please press 'c' to cancel, or any key to try again...") == 'c':
										break
									else:
										continue

					break

def reports_menu():
	global cfg
	global out_barcodes
	global bcode_format
	global bcode_fname
	global bcode_minQ
	global bcode_minQP

	while True:
		os.system('clear')
		print "Reports menu"	
		print "============="
		print "(O)utput barcodes: {} [should a barcodes file be outputted]".format(cfg.get('reports','out_barcodes'))
		print "(D)NA Barcodes format: {} [output barcodes in what format]".format(cfg.get('reports','bcode_format'))
		print "(F)ilename for barcodes file: {} [barcode filename without extension]".format(cfg.get('reports','bcode_fname'))
		print "(M)inimum Phred-base quality to accept base-call: {} [default=20]".format(cfg.get('reports','bcode_minQ'))
		print "(P)roportion of bases with at least minimum quality: {} [default=0.975]".format(cfg.get('reports','bcode_minQP'))		
		print "(B)ack to main menu."
		print ""
		reports_menu_item=raw_input('--> ')

		if reports_menu_item not in ['O','D','F','M','P','B']:
			print 'Please choose either O, D, F, M, P, B..'
			print ''
			raw_input("Press any key to continue...")
			reports_menu()
		
		if reports_menu_item=='B':
			break

		if reports_menu_item=='O':
			while True:
				print "Output a barcodes file to the reporting directory ((T)rue or (F)alse) (Default: {}):".format(cfg.get('reports','out_barcodes'))
				tmp=raw_input('--> ')
				if tmp=='':
					break
				elif tmp not in ['T','F']:
					print "Please select: (T)rue or (F)alse."
					print ""
					raw_input("Press any key to continue...")
				else:
					if tmp == 'T':
						cfg.set('reports','out_barcodes','True')
					else:
						cfg.set('reports','out_barcodes','False')
					break

		if reports_menu_item=='D':
			while True:
				print "Output barcodes in what format (fa:fasta or fq:fastq) (Default: {}):".format(cfg.get('reports','bcode_format'))
				tmp=raw_input('--> ')
				if tmp=='':
					break
				elif tmp not in ['fa','fasta','fq','fastq']:
					print "Please select: fa for FASTA or fq for FASTQ."
					print ""
					raw_input("Press any key to continue...")
				else:
					if tmp in ['fa','fasta']:
						cfg.set('reports','bcode_format','fasta')
					else:
						cfg.set('reports','bcode_format','fastq')
					break

		if reports_menu_item=='F':
			print "Type in a DNA barcodes filename (without extension) (Default: {}):".format(cfg.get('reports','bcode_fname'))
			tmp=raw_input('--> ')
			if tmp=='':
				continue
			else:
				cfg.set('reports','bcode_fname',tmp)
				break

		if reports_menu_item=='M':
			while True:
				print "Choose a minimum Phred base-quality score to filter barcodes (default={}).".format(cfg.get('reports','bcode_minQ'))
				print "Acceptable values are integers between 0 and 126."
				print "A value of zero means no filtering."
				tmp=raw_input('--> ')
				try:
					tmp=int(tmp)
				except:
					print "Please select an integer value between 1 and 126."
					print ""
					raw_input("Press any key to continue...")
					continue					
				if tmp=='':
					break
				elif tmp < 0 or tmp > 126:
					print "Please select an integer value between 1 and 126."
					print ""
					raw_input("Press any key to continue...")
					continue
				else:
					cfg.set('reports','bcode_minQ',str(tmp))
					break

		if reports_menu_item=='P':
			while True:
				print "Choose a minimum proportion of bases with the minimum Phred base-quality"
				print "score to filter barcodes (default={}).".format(cfg.get('reports','bcode_minQP'))
				print "Acceptable values are floats between 0 and 1."
				print "A value of zero means no filtering."
				print "A value of 1 means 100% of bases must have a base-quality score" 
				print "equal to or larger than the minimum value of {}.".format(cfg.get('reports','bcode_minQ'))
				tmp=raw_input('--> ')
				try:
					tmp=float(tmp)
				except:
					print "Please select float between 0 and 1 (e.g., 0.5)."
					print ""
					raw_input("Press any key to continue...")
					continue					
				if tmp=='':
					break
				elif tmp < 0 or tmp > 1:
					print "Please select float between 0 and 1 (e.g., 0.5)."
					print ""
					raw_input("Press any key to continue...")
					continue
				else:
					cfg.set('reports','bcode_minQP',str(tmp))
					break

#########################################################################################
## Auxiliary functions ##################################################################
#########################################################################################
def validate_dir(path):
	'''
	Check if a directory exists
	'''
	if os.path.exists(os.path.abspath(path)):
		return True
	else:
		return False

def test_dir(path):
	'''
	test if directory exists, if not create it
	'''
	path = os.path.expanduser(path)
	dir = validate_dir(path)
	if dir:
		print "Congratulations, the folder {} exists.".format(path)
		print "Please make sure you are not overriding any pre-existing projects."
		raw_input("Please press any key to continue...")
		return 'break'
	else:
		print "Folder {} does not exist".format(path)
		print "Would you like to create it? [y/n]"
		while True:
			ans = raw_input("--> ")
			if ans not in ['y','n']:
				print "Answer should be 'y' or 'n'. Please try again"
				raw_input("Please press any to try again...")
			else:
				break
		if ans =='n':
			print 'Could not create folder {}, please try again.'.format(path)
			raw_input("Please press any key to continue...")
			return 'break'
		else:
			try:
				os.mkdir(path)
				print "Successfully created folder {}.".format(path)
				raw_input("Please press any key to continue...")
				return 'break'
			except:
				print "You do not seem to have sufficient priviledges to create this directory"
				print "or, there was something wrong with your path"
				print "Would you like to try again? [y/n]"
				while True:
					ans = raw_input("--> ")
					if ans not in ['y','n']:
						print "Answer should be 'y' or 'n'. Please try again"
					else:
						break
				if ans =='y':
					return 'continue'
				else:
					return 'break'

#########################################################################################
## Main function ########################################################################
#########################################################################################


def main():
	'''
	Create a new project from a parameter file or from interaction with the user
	'''
	main_menu()
			
if __name__=="__main__":
	main()			