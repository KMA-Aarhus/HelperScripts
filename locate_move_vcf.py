import os
import sys
import numpy as np
import pandas as pd
from shutil import copyfile


def move_vcf(local_path, target_path):

	copyfile(local_path, target_path)

	return


def locate_move_vcf_internal(tsv_file, search_path, target_path):

	df1 = pd.read_csv(tsv_file, sep='\t')
	df1 = df1['raw_filename'].astype(str)

	search_list = []

	for i in range(len(df1)):
		tmp = df1[i].split(';')[0]
		tmp = tmp.split('_')
		tmp = '_'.join(tmp[0:2])
		search_list.append(tmp)

	print(search_list)
	subdirs = os.listdir(search_path)

	for t in search_list:
		for s in subdirs:
			sp = search_path  + t + '/aligned/' + t + '_bcftools.vcf'
			tp = target_path + t + '.vcf'
			move_vcf(sp, tp)
			break

	return


if __name__ == '__main__':
	################################################################################
	# Description:
	# - This scripts is for locating and moving files from a set of folders,
	#	to one specific folder of choice. Basically gathering the necessary 
	#	files that is wanted. Can be tweaked to not only work on .vcf files.
	#	This specific script was used to locate the output af an illumina
	#	read_aligner. So it is assumed that there are two files noted in the
	#	'raw_filename' column. This can also be tweaked if is not the case.
	#
	# Input:
	# - One .tsv file with metadata of samples
	# - One folder where the wanted files are in nested folder within (search_path)
	# - One folder where the wanted files are to be transfered to (target_path)
	#
	# Example usage:
	# - python locate_move_vcf.py idXXX.tsv /SEARCH_FOLDER/ /TARGET_FOLDER/

	tsv_file = sys.argv[1]
	search_path = sys.argv[2]
	target_path = sys.argv[3]

	locate_move_vcf_internal(tsv_file, search_path, target_path)
	