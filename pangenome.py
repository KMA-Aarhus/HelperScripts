import io
import os
import sys
import pysam
import numpy as np
import pandas as pd
import collections

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def parse_cov(cov_file):
	cov = open(cov_file, "r")
	l = cov.readline().replace("\n","")
	masked = []
	while l != "":	
		start = int(l.split()[1])
		end = int(l.split()[2])
		masked += range(start,end)

		l = cov.readline().replace("\n","")
	return masked

def read_vcf(v):
	# Annotates vcf with AA changes
	vcf_annotate_cmd = "vcf-annotator --output " + v + " " + v + " MN908947.3.gb"
	os.system(vcf_annotate_cmd)

	# Read in variant file
	vcf = pysam.VariantFile(v, 'r')
	v_dict = {}
	pos_dict = {}
	for var in vcf:
		if 'SupportFraction' not in var.info:
			print("SupportFraction not found. Is your vcf file generated from Illumina data?")
			break
		if 'AminoAcidChange' not in var.info:
			print("AminoAcidChange not found. Something likely went wrong in vcf-annotator")
			break
		if 'Gene' not in var.info:
			print("Gene not found. Something likely went wrong in vcf-annotator")
			break
		# Convoluted but working formatting of the AA and Gene strings
		AA = str(var.info['AminoAcidChange']).replace("('", "").replace("',)", "")
		gene = str(var.info['Gene']).replace("('", "").replace("',)", "")

		# Excludes synonymous/silent mutations, creates unique gene+AA identifier and saves frequency and position in separate dictionaries
		if AA != ".":			
			AA = gene+":"+AA
			v_dict[AA] = var.info['SupportFraction']
			pos_dict[AA] = var.pos
	# Variant dictionary contains a frequency for each AA change. Position dictionary contains a position for each AA change. Position is required to check for coverage.
	return v_dict, pos_dict


def get_allele_freq_subs(vcf_folder):
	# Create two lists of files, one for vcf files and one for coverage files.
	vcf_files = []
	cov_files = []
	for root, dirs, files in os.walk(vcf_folder):
		for file in files:
			if file.endswith(".vcf"):
				vcf_files.append(os.path.join(root, file))
			if file.endswith(".coverage_mask.txt"):
				cov_files.append(os.path.join(root, file))


	# Collects lists of missing coverage positions. 
	cov_dict = {}
	# Collects the AA changes and frequencies for each sample
	sample_dicts = {}
	# Combined dictionary of all AA changes and their nucleotide positions
	aa_pos = {}

	dates = []
	# Will contain final dictionary of variants and sample frequencies
	v_dict = {}

	# Parses coverage files and fills the missing coverage lists of nucleotide positions
	for cov_file in cov_files:
		date = str(cov_file.split("/")[-1].split(".")[0])
		masked = parse_cov(cov_file)
		cov_dict[date] = masked

	# Parses vcf files to dictionaries
	for v in vcf_files:
		tmp_dict, pos_dict = read_vcf(v)
		date = str(v.split("/")[-1].split(".")[0])
		dates.append(date)
		sample_dicts[date] = tmp_dict
		for key in tmp_dict:
			v_dict[key] = {}
		aa_pos.update(pos_dict)

	# Finally joins AA changes with corresponding nucleotide positions and frequency data for all samples. The dictionary is formatted as:
	# AAC1: {pos:nucleotide_position, sample1:freq, sample2:freq, sample3:freq}
	for var in v_dict:
		v_dict[var]["pos"] = int(aa_pos[var])
		for d in sample_dicts.keys():
			if var in sample_dicts[d]:
				v_dict[var][d] = sample_dicts[d][var]
				# For AA changes not observed in a given sample, we must determine if this is due to the variant not being present or just missing coverage
			else:				
				if v_dict[var]["pos"] not in cov_dict[d]:
					v_dict[var][d] = 0
				else:
					v_dict[var][d] = None
		
	return v_dict, dates

def create_gene_plot(df,gene,dates,vcf_folder):
	############
	# plotting #
	############
	# Reduces dataframe to one gene as we create one figure per gene to avoid crowding
	df = df[df["gene"] == gene]
	# Because of the way the dateframe is set up, it was easier to neccesary to iterate over the rows in the dataframe
	x_dates, frequencies, y_aa= ([] for i in range(3))

	for index, row in df.iterrows():
		for date in dates:
			x_dates.append(date)
			y_aa.append(row['AA'])
			frequencies.append(row[date])

	# To use as labels, get unique AA changes and dates. As we want to maintain the sort on nucleotide positions, we have to do this in a slightly complicated manner that maintains the ordering by index
	xlabs = [x_dates[index] for index in sorted(np.unique(x_dates, return_index=True)[1])]
	ylabs = [y_aa[index] for index in sorted(np.unique(y_aa, return_index=True)[1])]

	# set filename
	plt_filename = 'pangenome_plot_'+gene+'.png'

	# setting fixed plot size corresponding to A4 page
	plt.rcParams["figure.figsize"] = (8.27, 11.69)

	fig, ax = plt.subplots()

	# create gradient legend
	cm = plt.cm.get_cmap('coolwarm')
	sc = plt.scatter(x_dates, y_aa, c=frequencies, s=100, cmap=cm)
	plt.colorbar(sc, fraction=0.046, pad=0.04)

	# setting labels for x-axis and rotating
	#ax.set_xticks(list(range(len(set(x_dates)))))
	plt.xticks(ticks=range(len(xlabs)), labels=xlabs)


	#plt.yticks(ticks=range(len(y_aa_values)), labels=y_aa_values)

	#plt.xticks(rotation=300)

	# setting labels for y-axis
	plt.yticks(ticks=range(len(ylabs)), labels=ylabs)
	plt.gca().invert_yaxis()

	# saving loaded figure to filename given earlier
	plt.savefig(vcf_folder+"/"+plt_filename, bbox_inches='tight')
	plt.close()
	return


def pangenome_plots(vcf_folder):

	v_dict, dates = get_allele_freq_subs(vcf_folder)
	# Convert the dictionary containing AA changes and frequencies to a dataframe for plotting
	df = pd.DataFrame(data=v_dict)
	df = df.transpose()
	df = df.astype({'pos':'int'})
	df["gene"] = [var.split(":")[0] for var in df.index]
	df["AA"] = [var.split(":")[1] for var in df.index]
	# Sort the dataframe to keep ordering based on positions
	df = df.sort_values(by =["pos"])
	# create dataset for plotting
	for gene in set(df["gene"]):
		print("Creating figure for ", gene, "gene")
		create_gene_plot(df,gene, dates,vcf_folder)

if __name__ == '__main__':
	################################################################################
	# Description:
	# - This scripts greates a pangenome plot for a patient that 
	#	has had multiple samples taken across a span of time. 
	#
	# Input:
	# - One folder of .vcf and coverage mask files (assuming from Oxford Nanopore Sequencing reads)
	#
	# Example usage:
	# - python pangenome.py filedir outdir
	# 
	#	Assumes that the dates contained in the filenames is a close approximation to sample time. If not, rename files to reflect correct dates.
	
	vcf_folder = sys.argv[1]

	pangenome_plots(vcf_folder)