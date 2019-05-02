########################################################################
#CAFF_gene.py										14.12.09 -> 15.03.17 -> 15.06.22
#
#
#description : main body of the package(?)
#			   first attemption of using python opt parse.
#			   probably initial step of all process
#
#command line : python CAFF_gene.py -i [DEG list] -t [topology file] -s [snv file] -r [certain snv rate (default 2)] -o [output name]
#########################################################################



#Function 01 : CAFF_gene main function
#-----------------------------------------
#PROCESS STEP
#[1] MAKE gene lists that corresponds to the biological pathway.
#[2] MAKE gene lists from DEG file.


def CAFF_gene_filter(input_file, input_format, topology_matrix, snv_matrix, snv_rate, string_db_dir):

	print '\n>> STARTING CAFF-GENE PROCESS'

	#MAKING, CHECKING GENE LIST, DICTIONARY : START

	#[1] MAKE gene lists that corresponds to the biological pathway.
	string_genes_list = genes_to_list(string_db_dir, 'newline')

	#[2] MAKE gene lists from DEG file.
	DEG_list = genes_to_list(input_file, input_format)

	#[3] Matrix of topology is done from the previous step

	#[4] Matrix of SNV is done from the previous step

	#MAKING, CHECKING GENE LIST, DICTIONARY : END

	print '[NOTICE] Given number of DEGs : ' + str(len(DEG_list))

	#APPLY FIRST FILTER : DEGs filtered by topology
	filtered_list = first_filter(DEG_list, topology_matrix)

	print '[NOTICE] APPLIED 1st FILTER : filtering by GRN : ' + str(len(filtered_list)) + ' remained'

	#APPLY SECOND FILTER : topology filterd DEGs filtered by PATHWAY
	filtered_list = second_filter(filtered_list, string_genes_list)
	print '[NOTICE] APPLIED 2nd FILTER : filtering by STRING DB : ' + str(len(filtered_list)) + ' remained'


	filtered_list = third_filter(filtered_list, snv_matrix, snv_rate)
	print '[NOTICE] APPLIED 3rd FILTER : filtering by SNV : ' + str(len(filtered_list)) + ' remained'

	return filtered_list
	



#Function 01-1 : gene files (DEG, STRING db) to  list
#----------------------------------------------------

#[1]Making string DB's gene list
#string DB's gene list was from mmu.genes, mmu.pathway.genes

#[2]Making DEG's gene list


def genes_to_list(gene_file, file_format):

	if file_format == 'comma':
		file_format = ','
	if file_format == 'tab':
		file_format = '\t'
		
	gene_file = file(gene_file)
	gene_readlines = gene_file.readlines()

	gene_list = []
	
	for i in range(len(gene_readlines)):
		read = gene_readlines[i]
		read = read.replace('\n','')
		read = read.replace('\r','')

		if file_format == "newline":
			gene_list.append(read)
		else:
			token = read.split(file_format)
			for i in range(len(token)):
				gene_list.append(token[i])

	return gene_list
		
		

#Function 01-2 : FIRST FILTERING OPTION
#----------------------------------------------------

#[1] FROM topology matrix, find if TF (first column = key) and TG (second column = value ) are in the DEG list
#If TRUE : parse DEGs
#If false : do not pares DEGs

#[2] make union list.


def first_filter(DEG_list, topology_matrix):

	#DEG list that have been filtered by topology.	
	filtered_list = []

	for TF in topology_matrix.keys():

		TF_check = 0

		if TF in DEG_list:

			TF_check = 1
			TG_check = 0
			
			TGs = topology_matrix[TF]  #Note : TGs indicate multiple TGs. not single TG.

			for i in range(len(TGs)):
				TG = TGs[i]
				
				if TG in DEG_list:

					TG_check = 1
					filtered_list.append(TG)

			if TF_check == 1 and TG_check == 1:
				filtered_list.append(TF)

	unique_filtered_list = list(set(filtered_list))

	return unique_filtered_list

					
#Function 01-3 : SECOND FILTERING OPTION
#----------------------------------------------------

#[1] FROM topology filtered DEG list, find if DEG list are in STRING list
#If TRUE : parse DEGs
#If false : do not pares DEGs


def second_filter(DEG_list, string_list):
	
	filtered_list = []

	for DEG in DEG_list:
		if DEG in string_list:
			filtered_list.append(DEG)

	return filtered_list

#Function 01-4 : THIRD FILTERING OPTION
#----------------------------------------------------

#[1] FROM topology filtered DEG list, find if DEG list are in string list
#If TRUE : parse DEGs
#If false : do not pares DEGs


def third_filter(DEG_list, snv_matrix, snv_rate):

	filtered_list = []

	for DEG in DEG_list:
		if DEG in snv_matrix.keys():

			DEG_snv_rate = snv_matrix[DEG][0]
	
	
#			if float(DEG_snv_rate) < float(snv_rate):
			if float(DEG_snv_rate) <= float(snv_rate):

				filtered_list.append(DEG)

		if DEG not in snv_matrix.keys():
			filtered_list.append(DEG)

	return filtered_list

	
#Function 02 : Creating OUTPUT file
#----------------------------------------------------

def generate_output(filtered_list, output_file):

	print '[NOTICE] Creating result file of ' + str(len(filtered_list)) + ' genes at ' + str(output_file)

	output_text = file(output_file,'w')

	for gene in filtered_list:
		output_text.write(str(gene) + '\n')


#Starting Program : CAFF-GENE filter
if __name__ == '__main__':

	import sys
	import argparse
	import subprocess
	import os

	program_dir = os.path.split(os.path.realpath(__file__)) #location of bin folder
	#kegg_db_file = str(program_dir[0]) + '/Kegg_DB/mmu.pathway.genes'
	#Kegg DB's gene list was from mmu.genes, mmu.pathway.genes
	#Only genes that have a corresponded pathway to KEGG is in the list.
	#Gene list was made in 14.06.18 (In the future, the possibility of outdate exists)
	
	string_db_file = str(program_dir[0]) + '/PPI/STRING_PPI.uniq.list'
	kegg_file = str(program_dir[0]) + '/Kegg_DB/mmu.pathway.genes'
	


	#call library path & function : error_check
	lib_path = os.path.abspath(str(program_dir[0])+'/')
	print lib_path
	import Error_Check_FL

	#Using Argparse for Option retrival
	parser = argparse.ArgumentParser()	#initialize argparse

	#Note : n = row, m = column
	parser.add_argument('-i','--input', dest = 'input_file', help="Input file : A list of genes that represents DEGs")	
	parser.add_argument('-t','--topology', dest = 'topology_file', help="Specify certian gene regulatory network (GRN) to use. User can provide their own gene regulatory network.")
	parser.add_argument('-p','--pathway', dest = 'pathway_type', help="Choose pathway type to use. STRING or KEGG") 
	parser.add_argument('-s','--snv', dest = 'snv_file', help = "Assign certain rated SNV" ) #Gene list of certain rate of SNVs, the genes will be removed later.
	parser.add_argument('-r','--snv_rate', dest = 'snv_rate', help = "Assign the rate of SNV" ) #Gene list of certain rate of SNVs, the genes will be removed later.
	parser.add_argument('-o','--output', dest = 'output_file', help = "Assign certain rated SNV , n X 1 matrix " ) #Gene list of certain rate of SNVs, the genes will be removed later.

	args= parser.parse_args()



	#Defining argument variables
	input_file = args.input_file
	topology_file = args.topology_file
	pathway_type = args.pathway_type
	snv_file = args.snv_file
	snv_rate = args.snv_rate
	output_file = args.output_file




	print '-------------------------------------'
	print ':                                   :'
	print ':                                   :'
	print ':  ::         CAFF-GENE         ::  :'
	print ':                                   :'
	print ':                             1.0.1 :'
	print '-------------------------------------'

	if snv_rate == None:
		print "[Notice] SNV rate not given. Using default mutation rate."
		snv_rate = 2.0

	#Check input options. If missing options exists, terminate the program
	Error_Check_FL.check_options(input_file, topology_file, snv_file, snv_rate)

	if pathway_type == None:
		print '[Error] Pathway type not given. Please define which pathway DB to use'
		quit()

	if pathway_type =='STRING' or pathway_type == 'string':
		pathway_file = string_db_file
		print '[Notice] Using STRING DB'
	if pathway_type =='KEGG' or pathway_type == 'kegg':
		pathway_file = kegg_file 
		print '[Notice] Using KEGG DB'
		

	
	#Check input formats & create dictionary of several matrices.	
	input_format, topology_format, topology_matrix, snv_format, snv_matrix = Error_Check_FL.check_file_format(input_file, topology_file, snv_file)

	snv_rate = float(snv_rate)

	filtered_list = CAFF_gene_filter(input_file, input_format, topology_matrix, snv_matrix, snv_rate, pathway_file)

	if output_file == None:
		output_file = 'CAFF_GENE.out'

	generate_output(filtered_list, output_file)

	print '[NOTICE] CAFF-GENE DONE !'



