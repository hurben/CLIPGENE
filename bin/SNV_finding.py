#########################################################################
#SNV_finding.py													14.08.19 -> 15.03.17
#
#
#description : from snp file (VCF) :	handling VCF, or SNP information
#			[1] IF VCF:
#				1. make ANNOVAR ready form
#				2. Run ANNOVAR
#
#			[2] IF SNP information (ANNOVAR form)
#				1. Run ANNOVAR
#
#			#note : [1], [2] control , case each.
#
#			[3] ANNOVAR results to triple_filter snp information form.
#				
#
#command line : python SNV_finding.py -n normal.vcf -t tumor.vcf
#########################################################################


#Function 02 : RUN ANNOTATION
#-----------------------------------------------------
#Check file format
#	[1] if the file format is unknown -> ERROR, terminate program
#	[2] if the file format is VCF -> start parsing, make dictionary
#	[3] if the file format is ANNOVAR ready -> proceed next step
#		for annovar ready format. copy normal file and tumor file to 'annovar_ready.normal/tumor'



def annotation(normal_file_format, tumor_file_format, input_normal_file, input_tumor_file, program_dir):


	#open files 
	input_normal_open = file(input_normal_file)
	input_tumor_open = file(input_tumor_file)


	#buffer
	annovar_dir = str(program_dir) + '/annovar'



	########
	#normal#
	########
	print '[NOTICE] Proceeding normal file : ' + str(input_normal_file) 

	file_format = normal_file_format

	if file_format == 'unknown':
		print '[ERROR] Input file format unknown. Please check input file format.'
		print '[ERROR] This program supports VCF and ANNOVAR ready form'
		print '[Advice] Information of ANNOVAR ready form could by found : http://www.openbioinformatics.org/annovar/annovar_input.html'
		print '[NOTICE] Terminating program.'
		quit()

	if file_format == 'VCF':
		print '[NOTICE] Input file : VCF'
		print '[NOTICE] Making VCF file to ANNOVAR ready form'
		make_annovar_ready_form(file_format, input_normal_open, 'annovar_ready.normal')

		print '\n>> EXECUTING ANNOVAR.'
		annovar_cmd = annovar_dir +'/'+ 'annotate_variation.pl -out normal.annotation -build mm9 annovar_ready.normal ' + str(annovar_dir) +'/mousedb/'
		os.system(annovar_cmd)

		print '[NOTICE] ANNOVAR DONE (normal)'

	if file_format == 'ANNOVAR':
		print '[NOTICE] Input file : ANNOVAR'

		cmd = 'cp ' + str(input_normal_file) + ' annovar_ready.normal'
		os.system(cmd)

		#if modification of build is needed. EDIT this	
		print '\n>> EXECUTING ANNOVAR.'
		annovar_cmd = annovar_dir +'/'+ 'annotate_variation.pl -out normal.annotation -build mm9 annovar_ready.normal ' + str(annovar_dir) +'/mousedb/'
		os.system(annovar_cmd)
		os.system('rm annovar_ready.normal')
		print '[NOTICE] ANNOVAR DONE (normal)'




	#######
	#tumor#
	#######
	print '[NOTICE] Proceeding Tumor file : ' + str(input_tumor_file) 
	file_format = tumor_file_format

	if file_format == 'unknown':
		print '[ERROR] Input file format unknown. Please check input file format.'
		print '[ERROR] This program supports VCF and ANNOVAR ready form'
		print '[Advice] Information of ANNOVAR ready form could by found : http://www.openbioinformatics.org/annovar/annovar_input.html'
		print '[NOTICE] Terminating program.'
		quit()

	if file_format == 'VCF':
		print '[NOTICE] Input file : VCF'
		print '[NOTICE] Making VCF file to ANNOVAR ready form'
		make_annovar_ready_form(file_format,input_tumor_open, 'annovar_ready.tumor')

		print '\n>> EXECUTING ANNOVAR.'
		annovar_cmd = annovar_dir +'/'+ 'annotate_variation.pl -out tumor.annotation -build mm9 annovar_ready.tumor ' + str(annovar_dir) +'/mousedb/'
		os.system(annovar_cmd)

		print '[NOTICE] ANNOVAR DONE (tumor)'

	if file_format == 'ANNOVAR':
		print '[NOTICE] Input file : ANNOVAR'

		cmd = 'cp ' + str(input_tumor_file) + ' annovar_ready.tumor'
		os.system(cmd)


		print '\n>> EXECUTING ANNOVAR.'
		#if modification of build is needed. EDIT this	
		annovar_cmd = annovar_dir +'/'+ 'annotate_variation.pl -out tumor.annotation -build mm9 annovar_ready.tumor ' + str(annovar_dir) +'/mousedb/'
		os.system(annovar_cmd)
		os.system('rm annovar_ready.tumor')
		print '[NOTICE] ANNOVAR DONE (tumor)'
		
	

#Function 02-1 : Making ANNOVAR ready form from VCF file
#-----------------------------------------------------

def make_annovar_ready_form(file_format,input_file, output_file):

	#open and readlines
	input_readlines = input_file.readlines()
	output_txt = file(str(output_file),'w')

	#buffers
	annovar_dict = {}

	for i in range(len(input_readlines)):
		read = input_readlines[i]
		read = read.replace('\n','')

		if read[0] != '#':
			token = read.split('\t')

			contig = token[0]
			position = token[1]

			ref_nucleotide = token[3]
			alt_nucleotide = token[4]

			if len(ref_nucleotide) == 1:
				if len(alt_nucleotide) == 1:
					annovar_dict[contig,position] = [ref_nucleotide, alt_nucleotide]
					
	for key in annovar_dict.keys():
		contig = key[0]

		if 'chr' not in contig:
			contig = 'chr' + str(contig)

		position = key[1]
		ref_nuc = annovar_dict[key][0]
		alt_nuc = annovar_dict[key][1]
		output_txt.write(str(contig) + '\t' + str(position) + '\t' + str(position) +'\t' + str(ref_nuc) +'\t' + str(alt_nuc) + '\tNULL\n')

	output_txt.close()






#Function 03 : MAKE TRIPLE FILTER ready form, from annotation results
#-----------------------------------------------------

def	make_triple_filter_ready_form():
	
	#open and readlines
	normal_annotation_file = file('normal.annotation.variant_function')
	normal_annotation_readlines = normal_annotation_file.readlines()

	tumor_annotation_file = file('tumor.annotation.variant_function')
	tumor_annotation_readlines = tumor_annotation_file.readlines()

	#buffer
	mutation_rate_dict = {}

	#Using function 03-1
	normal_annotation_dict = annotation_file_to_dict(normal_annotation_readlines)
	tumor_annotation_dict = annotation_file_to_dict(tumor_annotation_readlines)
	


	#note: beware, normal dict and tumor dict may have different keys.
	#therefore, need pseudo count for non-consensus keys

	for gene in normal_annotation_dict.keys():
		if gene not in tumor_annotation_dict.keys():
			tumor_annotation_dict[gene] = 1

	for gene in tumor_annotation_dict.keys():
		if gene not in normal_annotation_dict.keys():
			normal_annotation_dict[gene] = 1


	for gene in normal_annotation_dict.keys():

		if float(tumor_annotation_dict[gene]) >= float(normal_annotation_dict[gene]):
			mutation_rate = float(tumor_annotation_dict[gene]) / float(normal_annotation_dict[gene])
		if float(normal_annotation_dict[gene]) > float(tumor_annotation_dict[gene]):
			mutation_rate = float(normal_annotation_dict[gene]) / float(tumor_annotation_dict[gene])

		mutation_rate_dict[gene] = mutation_rate
#		print tumor_annotation_dict[gene], normal_annotation_dict[gene], mutation_rate
			
	return mutation_rate_dict



#Function 03-1 : making dictionary from annotation files
#-------------------------------------------------------

def annotation_file_to_dict(annotation_readlines):

	annotation_dict = {}

	for i in range(len(annotation_readlines)):
		read = annotation_readlines[i]
		read = read.replace('\n','')
		token = read.split('\t')

		if 'dist' not in token[1]:
			
			gene = token[1].split('(')[0]
			gene = gene.split(',')[0]

			try : annotation_dict[gene] += 1
			except KeyError : annotation_dict[gene] = 2

	return annotation_dict
	

#Function 04 : Write final results
#-------------------------------------------------------

def dict_to_text(result_dict,output):
	
	text = file(str(output),'w')

	for key in result_dict.keys():
		text.write(str(key) + '\t' + str(result_dict[key]) + '\n')



#Starting Program : SNP_finding
if __name__ == '__main__':


	import sys
	import argparse
	import subprocess
	import os


	program_dir = os.path.split(os.path.realpath(__file__))[0]


	#call library path & function : error_check
	lib_path = os.path.abspath(str(program_dir[0])+'/')
	import Error_Check_FL


	#Using Argparse for Option retrival
	parser = argparse.ArgumentParser()	#initialize argparse

	#Note : n = row, m = column
	parser.add_argument('-n','--normal', dest = 'input_normal_file', help="Assign input file(normal)")	
	parser.add_argument('-t','--tumor', dest = 'input_tumor_file', help="Assign input file(tumor)")	
	parser.add_argument('-o','--output', dest = 'output_file', help = "Assign certain rated SNP , n X 1 matrix " ) #Gene list of certain rate of SNPs, the genes will be removed later.

	args= parser.parse_args()


	#Defining argument variables
	input_normal_file = args.input_normal_file
	input_tumor_file = args.input_tumor_file
	output = args.output_file


	print '#################################################'
	print '#                                               #'
	print '#               PRE-CAFF_GENE  1.0              #'
	print '#      Preprocess : Listing SNV frequency       #'
	print '#                                               #'
	print '#################################################'




	Error_Check_FL.option_check(input_normal_file,input_tumor_file)


	print '\n>> CHECKING FILE FORMAT. Normal'
	normal_file_format = Error_Check_FL.check_file_format_for_snv(input_normal_file)
	print '\n>> CHECKING FILE FORMAT. Tumor'
	tumor_file_format = Error_Check_FL.check_file_format_for_snv(input_tumor_file)
	annotation(normal_file_format, tumor_file_format, input_normal_file, input_tumor_file, program_dir)

	#if annotation is done. Each file will saved as
	#normal.annotation.variant_function
	#tumor.annotation.variant_function
	#Files will be moved to log/ after every process is done.

	print '\n[NOTICE] Calculating mutation rate between normal and tumor'
	mutation_rate_dict = make_triple_filter_ready_form()

	if output == None:
		output = 'snp_rate.txt'


	print '[NOTICE] Making results at ' + str(output)
	dict_to_text(mutation_rate_dict,output)
	print '[NOTICE] Every process succesfully DONE'




