#########################################################################
#SNV_rate_recalculation_for_biorep.py													14.08.19 -> 15.03.17
#
#
#description : from multiple snp rate file , DONE by SNV_finding.py
#
#			  Among two different files, use the biggest SNV rate. 
#			  As we intend to exclude every possible noise. A single biggest SNV rate will be exclude in the future.
#				
#
#command line : python SNV_rate_recalculation_for_biorep.py [File1] [File2]
#########################################################################


def file_to_dict(input_file, rate_dict):

	input_file_open = file(input_file,'r')
	input_readlines = input_file_open.readlines()

	
	for i in range(len(input_readlines)):
		read = input_readlines[i]
		read = read.replace('\n','')
		
		token = read.split('\t')
		gene = token[0]
		rate = token[1]
		rate = float(rate)
	
		if gene not in rate_dict.keys():
			rate_dict[gene] = rate
		else:
			if rate_dict[gene] < rate:
#				print gene
#				print rate_dict[gene], rate
				rate_dict[gene] = rate

	
	print "Total SNV contents at " , str(input_file) ," :",len(rate_dict.keys())
		
def dict_to_text(rate_dict, output_text):

	txt = file(str(output_text),'w')
	
	for gene in rate_dict.keys():
		rate= rate_dict[gene]
		txt.write(str(gene)+'\t' + str(rate)+'\n')







#Starting Program : SNV_rate_recalculation_for_biorep.py
if __name__ == '__main__':


	import sys
	import argparse
	import subprocess
	import os


	program_dir = os.path.split(os.path.realpath(__file__))[0]


	#Using Argparse for Option retrival
	parser = argparse.ArgumentParser()	#initialize argparse

	#Note : n = row, m = column
	parser.add_argument('-i1','--input1', dest = 'input_1_file', help="Assign input first file")	
	parser.add_argument('-i2','--input2', dest = 'input_2_file', help="Assign input second file")	
	parser.add_argument('-o','--output', dest = 'output_file', help = "")

	args= parser.parse_args()


	#Defining argument variables
	input_1_file = args.input_1_file
	input_2_file = args.input_2_file
	output = args.output_file


	#buffer
	rate_dict = {}

	if output == None:
		output = str(input_1_file) + '_' + str(input_2_file) + '.out'

	print '#################################################'
	print '#                                               #'
	print '#               PRE-CAFF_GENE  1.0              #'
	print '#   integrating multiple biorep snvrate file    #'
	print '#                                               #'
	print '#################################################'

	#FUnction starts
	file_to_dict(input_1_file, rate_dict)
	file_to_dict(input_2_file, rate_dict)
	dict_to_text(rate_dict, output)



