import sys

genes = sys.argv[1]
genes_pathway = sys.argv[2]


genes_file = file(genes)
genes_pathway_file = file(genes_pathway)


genes_file_readlines = genes_file.readlines()
genes_pathway_file_readlines = genes_pathway_file.readlines()


genes_dict = {}
genes_pathway_list = []

for i in range(len(genes_file_readlines)):
	read = genes_file_readlines[i]
	read = read.replace('\n','')

	if ';' in read:

		first_token = read.split(';')[0]
		token = first_token.split('\t')

		mmu_gene_id = token[0]
		gene_symbol = token[1].split(',')[0]

		genes_dict[mmu_gene_id] = gene_symbol

for i in range(len(genes_pathway_file_readlines)):
	read = genes_pathway_file_readlines[i]
	read = read.replace('\n','')

	gene_id = read.split('\t')[0]
	genes_pathway_list.append(gene_id)


unique_genes_pathway_list = list(set(genes_pathway_list))


txt = file('result.txt','w')

for key in genes_dict.keys():
	if key in unique_genes_pathway_list:
		txt.write(str(genes_dict[key]) + '\n')






