#################################################################
#CAFF-GENE-BEST_default.py									15.10.22
#
#
#
#description : Run CAFF-GENE-BEST with default options
#
#
#
#
#
##################################################################



if __name__ == '__main__':

	import sys
	import argparse
	import subprocess
	import os

	program_dir = os.path.split(os.path.realpath(__file__))
	lib_path = os.path.abspath(str(program_dir[0])+'/')

	network_file = str(lib_path) + 	'/bin/mmu10_normal_sample.topology' 
	pathway_type = 'STRING'

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', dest = 'input_file', help="Input file, a deg list")
	parser.add_argument('-s', '--snv', dest = 'snv_file', help="Input file, SNV rate file")
	parser.add_argument('-c', '--context', dest = 'context_aware', help="User's context of interest")
	parser.add_argument('-ko', '--knockout', dest = 'knockout_gene', help="Knocked out gene of the data")


	args= parser.parse_args()

	input_file = args.input_file
	snv_file = args.snv_file
	context_aware = args.context_aware
	ko_gene = args.knockout_gene
	

	CAFF_gene_cmd = 'python bin/CAFF_gene.py -t ' + str(network_file) + ' -p ' + str(pathway_type) + ' -i ' + str(input_file) + ' -s ' + str(snv_file)


	if snv_file == None or input_file == None or ko_gene == None:
		print '[Error] Essential input missing'
		print 'For more information, use help -h'
		quit()

	os.system(CAFF_gene_cmd)

	if context_aware == None:
		print '[Notice] Context not given. using non-context aware.'
		BEST_cmd = 'python3 bin/BEST_api.py -i CAFF_GENE.out -ko ' + str(ko_gene)
	if context_aware != None:
		print '[Notice] Given context : ' + str(context_aware)
		BEST_cmd = 'python3 bin/BEST_api.py -i CAFF_GENE.out -c ' +str(context_aware) + ' -ko ' + str(ko_gene)


	os.system(BEST_cmd)

	output_context = 'CAFF_GENE_BEST.initial.result.context'
	output_noncontext = 'CAFF_GENE_BEST.initial.result.noncontext'

	if context_aware != None:
		final_cmd = 'python bin/Final_ranking.py -i ' + str(output_context) + ' -g ' + str(ko_gene)
	if context_aware == None:
		final_cmd = 'python bin/Final_ranking.py -i ' + str(output_noncontext) + ' -g ' + str(ko_gene)

	os.system(final_cmd)







	


