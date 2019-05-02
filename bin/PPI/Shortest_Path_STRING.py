# QueryGeneListFile Format (All Official gene Symbols ONLY)
#	Gene_1\n
#	Gene_2\n
#	...
#	Gene_n\n
##################
# Path_length is equal to the number of edges between the two selected nodes
# ex)  gene1 - gene2 - gene3 - gene4 - gene5
#	Path_length(gene1,gene5) = 4
#	Path_length(gene2,gene4) = 2

import sys, os
import networkx as nx

def main(sKOGene, sQueryGeneListFileName):
	lQueryGeneList	=	Call_QueryGenes(sQueryGeneListFileName)
	gPPI			=	Call_PPINetwork()
	dPathDict		=	Calculate_ShortestPath(sKOGene, lQueryGeneList, gPPI)
	Print_Result(dPathDict)

def Print_Result(dPathDict):
	fOutFile		=	file(os.getcwd() + '/Shortest_Path_Result.txt','w')
	fOutFile.write('KOGene\tQueryGene\tPath_Length\tGenes_on_the_Path\n')
	for sKey in dPathDict:
		nLength		=	len(dPathDict[sKey]) - 1
		lTemp		=	[sKey[0],sKey[1], nLength] + dPathDict[sKey]
		fOutFile.write('\t'.join(map(str,lTemp))+'\n')
		print 'The Length of Shortest Path between ', sKey[0], 'and', sKey[1], 'is: ', str(nLength)

def Calculate_ShortestPath(sKOGene, lQueryGeneList, gPPI):
	dPathDict	=	{}
	for sGene in lQueryGeneList:
		lPath	=	nx.shortest_path(gPPI, source = sKOGene, target = sGene)
		dPathDict[sKOGene, sGene]	=	lPath
	return dPathDict

def Call_PPINetwork():
#	fPPIFile			=	file('/data/project/sslim/STRING/Mus_musculus/STRING_PPI_Mus_musculus_Symbol.txt','r')
	fPPIFile			=	file('STRING_PPI_Mus_musculus_Symbol.txt','r')

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
	fGeneFile		=	file(sQueryGeneListFileName,'r')
	lQueryGeneList	=	[x.replace('\n','') for x in fGeneFile.readlines()]
	return lQueryGeneList

if __name__ == '__main__':
	sKOGene					=	sys.argv[1]
	sQueryGeneListFileName	=	sys.argv[2]
	main(sKOGene, sQueryGeneListFileName)
