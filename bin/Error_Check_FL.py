########################################################################
#error_check.py										   14.12.09
#
#Description : Library of File Error check.
#			   Called in 
#			[1] Triple_filter.py
#
#########################################################################

#Function 01 : Input condition check ( option check )
#----------------------------------------------------
#If the following files are not given
#[1] [input file] ( n x 1 ) size. Where n is row(genes)
#[2] [topology file] ( n x 2 ) matrix. Where n is row(Edges)
#[3] [SNP file ] ( n x 2 ) matrix. where n is row(genes), columns is mutation rate ( fold change = KO / SNP )
#show error message.

def check_options(input_file, topology_file, snp_file, snp_rate):
	

	if input_file == None or topology_file == None or snp_file == None:
		print "[Error] Certain input is missing."
		print "[Notice] Minimun required files : Input file (DEG list), Topology, SNV."
		print "[Notice] -h for more information."
		quit()


	try : 
		snp_rate = float(snp_rate)

	except ValueError:

		print "[Error] SNV rate needs to be defined as numeric number "
		print "[Notice] -h for more information."
		quit()



#Function 02 : File format check
#----------------------------------------------------
#Check file format : tab seperated or comma seperated? 
	#Check file format 1 : For files that are bigger than ( n x 2 ) matrix. Available to determine whether the file is in tab, comma seperated file.
	#Check file format 2 : For files that are ( n x 1 ) matrix. Available to determine whether the file is in tab, comma, newline seperated.
	
#Check file matrix : Is the matrix in a correct size?
	#For files that are bigger than ( n x 2 ) matrix
	#[1] : Find as if there are any blanks

def check_file_format(input_file, topology_file, snp_file):


	print '\n>> CHECKING FILE FORMATS. '
	print '[NOTE] :TAB, SPACE, COMMA delimited files are only available.'

	#Check 01 : file format
	#----------------------
	#check input's format
	input_format = check_file_format_2(input_file, 'columns','Input file')    #Check file's delimiter

	#check topology file's format
	topology_format = check_file_format_1(topology_file, 'columns','edges','Topology file')    #Check file's delimiter

	#check snp file's format
	snp_format = check_file_format_1(snp_file, 'columns', 'genes', 'SNV file')

	#Check 02 : Is input matrix ( n x m ) matrix?
	#--------------------------------------------

	print '[File check] Checking matrix size of topology file'
	topology_matrix = check_input_matrix(topology_file,'topology file', topology_format)
	print '[File check] Checking matrix size of SNV file'
	snp_matrix = check_input_matrix(snp_file,'SNV file', snp_format)

	print '[NOTICE] No Format errors detected in given files'


	return input_format, topology_format, topology_matrix, snp_format, snp_matrix

#Function 02-1 : File format check
#----------------------------------------------------

#Daughter function of check_file_format
#Check file format 1 : For files that are bigger than ( n x 2 ) matrix. Available to determine whether the file is in tab, comma seperated file.

#Determines whether the file is tab seperated or , seperated.
#If both tab and comma is in the file. Error will happen.

def check_file_format_1(given_file, column, row, file_type):

	open_file = file(given_file)

	readlines = open_file.readlines()
	tab_check = 0
	comma_check = 0

	#Scaning whole context.
	for i in range(len(readlines)):
		read = readlines[i]
		if '\t' in read:
			tab_check = 1
		if ',' in read:
			comma_check = 1

	open_file.close()

	if tab_check == 1 and comma_check == 1:

		print "[Error] " + str(file_type) + " : [ comma, tab ] both format exists in file. Please check the file format."
		print "[Notice] Terminating program"
		quit()


	if tab_check == 1:
		print "[File check] " +str(file_type) + " : Format (tab seperated) detected."

		print "[File check] " +str(file_type) + " : Number of " + str(row) + " " + str(len(readlines))
		return 'tab'


	if comma_check == 1:
		print "[File check] " +str(file_type) + " : Format (comma seperated) detected."

		print "[File check] " +str(file_type) + " : Number of " + str(row) + " " + str(len(readlines))

		return 'comma'


#Function 02-2 : File format check
#----------------------------------------------------

#Daughter function of check_file_format
#Check file format 2 : For files that are ( n x 1 ) matrix. Available to determine whether the file is in tab, comma, newline seperated.


#For files of DEG list.

#Determines whether the file is tab seperated or , seperated.
#if tab or , is not in the file, identify it as newline seperated.
#If both tab and comma is in the file. Error will happen.


def check_file_format_2(given_file, row, file_type):

	open_file = file(given_file)


	readlines = open_file.readlines()

	tab_check = 0
	comma_check = 0

	for i in range(len(readlines)):
		read = readlines[i]
		if '\t' in read:
			tab_check = 1
		if ',' in read:
			comma_check = 1

	open_file.close()

	if tab_check == 1 and comma_check == 1:

		print "[Error] " + str(file_type) + " : [ comma, tab ] both format exists in file. Please check the file format."
		print "[Notice] Terminating program"
		quit()

	if comma_check == 1:
		print "[File check] " +str(file_type) + " : Format (comma seperated) Detected."
		print "[File check] " +str(file_type) + " : Number of " + str(row) + ' '+ str(len(readlines[0].split(',')))
		return 'comma'

	if tab_check == 1:
		print "[File check] " +str(file_type) + " : Format (tab seperated) Detected."
		print "[File check] " +str(file_type) + " : Number of " + str(row) + ' '+ str(len(readlines[0].split('\t')))
		return 'tab'

	if tab_check == 0 and comma_check == 0:
		print "[File check] " + str(file_type) + " : Format (tab, comma seperated) is not Detected."
		print "[File check] " + str(file_type) + " : [Alternative] using (new line) seperate."
		print "[File check] " +str(file_type) + " : Number of " + str(row) + ' '+str(len(readlines[0]))
		return 'newline'


#Function 02-3 : Check input matrix
#--------------------------------------------------------

#Check file matrix : Is the matrix in a correct size?
#For files that are bigger than ( n x 2 ) matrix
#[1] : Find as if there are any blanks



#checking as if the matrix is ( n x m ) size.
#Missing values are not allowed.


def check_input_matrix(given_file, file_type, file_format):

	if file_format == 'comma':
		file_format = ','
	if file_format == 'tab':
		file_format = '\t'

	open_file = file(given_file)
	readlines = open_file.readlines()

	check_dict =  {}

	token_size = len(readlines[0].split(file_format))

	#check
	for i in range(len(readlines)):
		read = readlines[i]
		read = read.replace('\n','')
		token = read.split(file_format)
		if token_size == len(token):

			if '' not in token:
				pass

			else:
				print '[Error] The matrix size is not constant. Please check as if the matrix is correct.'
				quit()
			
		else:
			print '[Error] The matrix size is not constant. Please check as if the matrix is correct.'
			quit()
	


	#IF matrix is correct, make dictionary.
	for i in range(len(readlines)):
		read = readlines[i]
		read = read.replace('\n','')
		token = read.split(file_format)
		key = token[0]
		for j in range(1, len(token)):
			try : check_dict[key].append(token[j])
			except KeyError: check_dict[key] = [token[j]]

	return check_dict

#################################################
#FILE CHECK FUNCTIONS : END
#################################################


#Function 00 : option check
#---------------------------
#Check input options
#if normal and tumor file(or vcf file) is Null
#terminate program


def option_check(input_normal_file, input_tumor_file):

	print '\n>> CHECKING OPTIONS.'

	if input_normal_file == None:
		print '[ERROR] Input file : Normal VCF or Annovar ready file is missing.'
		print '[Error] Terminating program'
		quit()

	if input_tumor_file == None:
		print '[ERROR] Input file : Tumor VCF or Annovar ready file is missing.'
		print '[Error] Terminating program'
		quit()
	print '[NOTICE] Input options are correctly given.'




#Function 01 : Check file format
#--------------------------------
#Check whether file is in VCF format or ANNOVAR ready format.
#VCF format is checked by the header ##fileformat=VCFvX.X
#ANNOVAR format is checked by 5 columns
#ANNOVAR format checking will be strict.

def check_file_format_for_snv(input_file):


	#open and readlines
	input_file_open = file(input_file)
	input_readlines = input_file_open.readlines()

	file_format = 'unknown'

	if '##fileformat' in input_readlines[0]:
		if 'VCF' in input_readlines[0]:
			file_format = 'VCF'

	else:
		token = input_readlines[0].split('\t')
		if len(token) >= 5 and len(token) <= 6:
			file_format = 'ANNOVAR'

	print '[File check] Input file : ' + str(file_format) + ' Detected.'

	return file_format


