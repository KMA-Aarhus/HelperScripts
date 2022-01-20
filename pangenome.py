import io
import os
import sys
import numpy as np
import pandas as pd

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def read_vcf(path):
	# pretty self-explanatory
    with open(path, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]
    return pd.read_csv(
        io.StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
               'QUAL': str, 'FILTER': str, 'INFO': str},
        sep='\t'
    ).rename(columns={'#CHROM': 'CHROM'})


def get_allele_freq_subs(vcf_folder):
	# handle allele frequency from .vcf files
	vcf_files = []
	for root, dirs, files in os.walk(vcf_folder):
		for file in files:
			if file.endswith(".vcf"):
				vcf_files.append(os.path.join(root, file))

	vcf_files.sort()
	al_freqs = []
	subs = []
	for v in vcf_files:
		df = read_vcf(v)
		df_subs = df[['POS', 'REF', 'ALT']]
		df = df['INFO']
		
		for i in range(len(df)):
			tmp = df[i]
			tmp = tmp.split(';')

			for j in range(len(tmp)):
				if tmp[j][:3] == 'DP=':
					dp_val = int(tmp[j][3:])
				elif tmp[j][:3] == 'AD=':
					# this stunt is used since we are handling illumina reads
					# if not, then it is possible to reduce the lines to one
					ap_val = tmp[j][3:]
					ap_val = ap_val.split(',')
					ap_val = int(ap_val[0]) + int(ap_val[1])

			al_freqs.append(ap_val/dp_val)

		tmp_subs = df_subs['REF'] + df_subs['POS'].astype(str) + df_subs['ALT']
		subs.append(','.join(tmp_subs.tolist()))

	return al_freqs, pd.DataFrame(subs)


def pangenome_plot(vcf_folder, id_file):

	al_freqs, subs = get_allele_freq_subs(vcf_folder)

	# handle substitution and dates
	df2 = pd.read_csv(id_file, sep='\t')
	n2, m2 = df2.shape
	dates = df2['sampling_date']

	# looks wierd, but is necessary
	# overwrites the substitutions noted in the .tsv file
	df2['substitutions'] = subs
	subs = df2['substitutions']


	# handling overlapping dates
	# only works if there are only two dates overlapping
	unique_dates = []
	i = 0
	while i < len(dates)-1:
		if dates[i] == dates[i+1]:
			unique_dates.append(dates[i] + '(1)')
			unique_dates.append(dates[i] + '(2)')
			i += 2
		else:
			unique_dates.append(dates[i])
			i += 1

	# special case: if we end on a unique date
	if i < len(dates):
		unique_dates.append(dates[i])

	dates = unique_dates
	df2['sampling_date'] = unique_dates

	# finding unique substitutions for y-axis labels
	pre_suf_dict = {}
	cleaned_subs = []

	for i in range(n2):
		tmp_sub = subs[i].split(',')

		for j in range(len(tmp_sub)):
			clean_sub = tmp_sub[j][1:-1]
			cleaned_subs.append(int(clean_sub))

			if clean_sub not in pre_suf_dict.keys():
				pre_suf_dict[clean_sub] = tmp_sub[j][0] + tmp_sub[j][-1]

	cleaned_subs = list(set(cleaned_subs))
	cleaned_subs.sort()
	cleaned_subs = [str(cleaned_subs[i]) for i in range(len(cleaned_subs))]

	sub_dict = {cleaned_subs[i]: i for i in range(0, len(cleaned_subs))}

	# finding unique dates for x-axis labels
	cleaned_dates = []

	for i in range(n2):
		cleaned_dates.append('-'.join(dates[i].split('-')[-2:]))

	cleaned_dates = list(set(cleaned_dates))
	cleaned_dates.sort()
	cleaned_dates = [cleaned_dates[i].replace('-', '/') for i in range(len(cleaned_dates))]

	date_dict = {cleaned_dates[i]: i for i in range(0, len(cleaned_dates))}

	# create dataset for plotting
	x_vals = []
	y_vals = []

	for i in range(n2):
		tmp_sub = subs[i].split(',')

		for j in range(len(tmp_sub)):
			clean_sub = tmp_sub[j][1:-1]
			clean_date = '-'.join(dates[i].split('-')[-2:])
			clean_date = clean_date.replace('-', '/')

			x_vals.append(date_dict[clean_date])
			y_vals.append(sub_dict[clean_sub])

	# recreate substitutions for labeling the y-axis
	new_y_axis = []

	for i in range(len(cleaned_subs)):
		tmp = cleaned_subs[i]
		pre_suf = pre_suf_dict[tmp]

		new_y_axis.append(pre_suf[0] + tmp + pre_suf[1])

	############
	# plotting #
	############

	# setting file name (assumes that it is called idXXX.tsv)
	plt_filename = 'pangenome_' + id_file[:5] + '.png'

	# setting fixed plot size corresponding to A4 page
	plt.rcParams["figure.figsize"] = (8.27, 11.69)

	fig, ax = plt.subplots()

	# create gradient legend
	cm = plt.cm.get_cmap('RdYlBu')
	sc = plt.scatter(x_vals, y_vals, c=al_freqs, s=100, cmap=cm)
	plt.colorbar(sc, fraction=0.046, pad=0.04)

	# setting labels for x-axis and rotating
	ax.set_xticks(list(range(len(cleaned_dates))))
	ax.set_xticklabels(cleaned_dates)
	plt.xticks(rotation=300)

	# setting labels for y-axis
	ax.set_yticks(list(range(len(cleaned_subs))))
	ax.set_yticklabels(new_y_axis)
	plt.gca().invert_yaxis()

	# saving loaded figure to filename given earlier
	plt.savefig(plt_filename, bbox_inches='tight')
	plt.close()
	return


if __name__ == '__main__':
	################################################################################
	# Description:
	# - This scripts greates a pangenome plot for a patient that 
	#	has had multiple samples taken across a span of time. It 
	#	was specifically used for 4 samples that all had the naming 
	#	format idXXX. Furthermore, a .tsv file was included which
	# 	had metadata for the tests taken. This was used for the x-axis
	# 	labels. The .tsv file also included the substitutions, but
	#	there were less noted than in the .vcf files. Therefore the 
	#	substitutions noted in the .vcf files were used.
	#
	# Input:
	# - One folder of .vcf files (assuming illumina reads)
	# - One .tsv file with dates of samples (metadata)
	#
	# Example usage:
	# - python pangenome.py idXXX/ idXXX/idXXX.tsv
	# 
	# 	If id of patient is not in format idXXX, of alot of indices above breaks.
	# 	If date is not noted in format 'YYYY-MM-DD', the above breaks as well.
	#	Assumes that the .vcf and .tsv files are orderered by sample_id, and 
	#	therefore also ordered by date. Good luck!
	
	vcf_folder = sys.argv[1]
	id_file = sys.argv[2]

	pangenome_plot(vcf_folder, id_file)
