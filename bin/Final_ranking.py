#########################################################################
#final_ranking.py											 15.05.02
#
#
#description : from best result file
#			 [2] calculate shortest path of each gene.
#				
#
#command line : python final_ranking.py -i [best result]
#########################################################################


#SHORTEST PATH FROM SSLIM (RECIEVED AT 15.05.01)
#MODIFIED 15.05.02 BY BENJAMIN
import networkx as nx

def main(sKOGene, sQueryGeneListFileName, output):
	lQueryGeneList	=	Call_QueryGenes(sQueryGeneListFileName)
	gPPI			=	Call_PPINetwork()
	dPathDict		=	Calculate_ShortestPath(sKOGene, lQueryGeneList, gPPI)
	Print_Result(dPathDict, output)

def Print_Result(dPathDict, output):
	fOutFile = file(str(output),'w')

#MEMO:
#sKey[0] = KOGene
#sKey[1] = QueryGene
#nLength
#data_dict[sKey[1]][1] = best score


	sp_dict = {}
	sp_rank_dict = {}

	rank_sum_dict = {}
	rank_sum_rank_dict = {}

	#value 
	for sKey in dPathDict:
		nLength		=	len(dPathDict[sKey]) - 1
		gene = sKey[1]
		best_score = data_dict[gene][1]

		if gene in sp_dict:
			"something Wrong. duplicated gene names exist"
		if gene not in sp_dict:
			sp_dict[gene] = nLength
		
	
	#calculate rank

	
	sorted_sp_list = sorted(sp_dict.items(), key=lambda x: x[1])



#initial
	rank = 1
	boolean_sp = sp_dict[sorted_sp_list[0][0]]
	for i in range(1, len(sorted_sp_list)):

		gene = sorted_sp_list[i][0]
		current_sp = sp_dict[gene]

		if current_sp > boolean_sp:
			rank += 1
			boolean_sp = current_sp

		sp_rank_dict[gene] = rank
		


	for gene in data_dict.keys():
		best_rank = int(data_dict[gene][0])
		best_rank += 1

		try : 
			sp_rank = sp_rank_dict[gene]
			Rank_sum = best_rank + sp_rank
			rank_sum_dict[gene] = Rank_sum

		except KeyError:
		
			continue


	#print rank_sum_dict
	sorted_ranksum_list = sorted(rank_sum_dict.items(), key=lambda x:x[1])


#	fOutFile.write('RANK\tQueryGene\tPath_Length\tPPI_RANK\tBEST_SCORE\tBEST_RANK\tFinal_Score(BordaCount)\n')
	fOutFile.write('RANK(Borda_count)\tCandiateGene\tPPI_RANK\tBEST_RANK\n')

	for i in range(len(sorted_ranksum_list)):
		gene = sorted_ranksum_list[i][0]
		rank = i
		fOutFile.write(str(i) + '\t' + str(gene) + '\t' + str(sp_rank_dict[gene]) + '\t' + str(data_dict[gene][0]) +'\n')
	

	fOutFile.close()
	print 'Done'

		

def Calculate_ShortestPath(sKOGene, lQueryGeneList, gPPI):
	dPathDict	=	{}

	for sGene in lQueryGeneList:
		try:
			lPath	=	nx.shortest_path(gPPI, source = sKOGene, target = sGene)
			dPathDict[sKOGene, sGene]	=	lPath
		except :
			print str(sGene) + ' not in PPI info.'
			continue

	return dPathDict

def Call_PPINetwork():
	STRING_PPI_FILE = 'bin/PPI/STRING_PPI_Mus_musculus_Symbol.txt'
	fPPIFile			=	file(str(STRING_PPI_FILE),'r')

	lPPIRead			=	[x.replace('\n','').split('\t') for x in fPPIFile.readlines()]
	gPPI				=	nx.Graph()
	for lLine in lPPIRead:
		sGene1, sGene2	=	lLine[0], lLine[1]
		nWeight			=	int(lLine[2])
		gPPI.add_edge(sGene1, sGene2, weight = nWeight)
	print 'Import STRING database completed'
	print 'The number of edges in the DB: ', len(gPPI.edges())

	return gPPI


def Call_QueryGenes(sQueryGeneListFileName):

	lQueryGeneList = []

	fGeneFile		=	file(sQueryGeneListFileName,'r')
	file_readlines = fGeneFile.readlines()

	for i in range (1, len(file_readlines)):
		read = file_readlines[i]
		read = read.replace('\n','')
		token = read.split('\t')

		gene = token[1]
		initial_rank = token[0]
		best_score = token[2]

		data_dict[gene] = [initial_rank, best_score]
		lQueryGeneList.append(gene)
		
	return lQueryGeneList





#Starting Program : 
if __name__ == '__main__':

	import sys
	import argparse
	import subprocess
	import os


	program_dir = os.path.split(os.path.realpath(__file__))[0]
	lib_path = os.path.abspath(str(program_dir[0])+'/')

	print lib_path





	#Using Argparse for Option retrival
	parser = argparse.ArgumentParser()  #initialize argparse

	#Note : n = row, m = column
	parser.add_argument('-i','--input', dest = 'input', help="Assign input file(best result)")
	parser.add_argument('-g','--gene', dest = 'gene', help="")
	parser.add_argument('-o','--output', dest = 'output_file', help = "Assign certain rated SNP , n X 1 matrix " ) #Gene list of certain rate of SNPs, the genes will be removed lat

	args= parser.parse_args()


	#Defining argument variables
	input_file = args.input
	ko_gene = args.gene
	output = args.output_file

	if output == None:
		output = 'CAFF_GENE_BEST.final.result'


	data_dict = {}

	print '#################################################'
	print '#                                               #'
	print '#              CAFF-GENE-BEST 1.0               #'
	print '#      ::      FINAL GENE RANKING       ::      #'
	print '#                                               #'
	print '#################################################'





	#STARTING FUNCTION
	sKOGene					=	ko_gene
	sQueryGeneListFileName	=	input_file

	main(sKOGene, sQueryGeneListFileName, output)


