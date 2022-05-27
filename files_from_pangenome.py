import os
import sys
import pandas as pd
import subprocess
import pathlib
from os.path import isfile, join
from os import listdir


def copy_files(samplefile, output):
	samples = open(samplefile, "r")
	sample = samples.readline().replace("\n","")
	while sample != "":	
		find_date_cmd = "find /faststorage/project/clinmicrocore/BACKUP/nanopore_sarscov2/pappenheim_clean/ -name \'*" + sample + ".consensus.fasta\' -exec cp \"{}\" " + output +  " \\;"
		os.system(find_date_cmd)
		sample = samples.readline().replace("\n","")
	consensus_files = [f for f in listdir(output) if ".consensus.fasta" in f]
	date_dict = {}
	for f in consensus_files:
		date = f.split("_")[0]
		sample = f.split("_")[1].split(".")[0]
		## If a sample has been run multiple times, only takes the newest
		if sample not in date_dict:
			date_dict[sample] = date
		elif int(date_dict[sample].split(".")[0]) < int(date.split(".")[0]):
			date_dict[sample] = date
		os.system("rm "+output+"/"+f)
	for sample in date_dict:
		if pathlib.Path("/faststorage/project/clinmicrocore/BACKUP/nanopore_sarscov2/pappenheim_clean/old_runs/clean_upload_"+date_dict[sample]+"/"+date_dict[sample]+"_final_summary.txt").exists:
			final_summary = open("/faststorage/project/clinmicrocore/BACKUP/nanopore_sarscov2/pappenheim_clean/old_runs/clean_upload_"+date_dict[sample]+"/"+date_dict[sample]+"_final_summary.txt", "r")
		elif pathlib.Path("/faststorage/project/clinmicrocore/BACKUP/nanopore_sarscov2/pappenheim_clean/clean_upload_"+date_dict[sample]+"/"+date_dict[sample]+"_final_summary.txt").exists:
			final_summary = open("/faststorage/project/clinmicrocore/BACKUP/nanopore_sarscov2/pappenheim_clean/clean_upload_"+date_dict[sample]+"/"+date_dict[sample]+"_final_summary.txt", "r")
		else:
			print("ERROR: no summary file found for ", date_dict[sample])
		summary_dict = {}
		
		l = final_summary.readline().replace("\n","")
		while l != "":
			var=l.split("=")[0]
			val=l.split("=")[1]
			summary_dict[var]=val
			l = final_summary.readline().replace("\n","")
		summary_dict['protocol_run_id']=summary_dict['protocol_run_id'].split("-")[0]
		dirname=date_dict[sample].replace('.', '_') + "_" + summary_dict["instrument"] + "_" + summary_dict["flow_cell_id"] + "_" + summary_dict['protocol_run_id']
		copy_vcf_cmd = "find /faststorage/project/clinmicrocore/BACKUP/nanopore_sarscov2/pappenheim_raw/"+ dirname + " -name \'*" + sample + ".merged.vcf\' -exec cp \"{}\" " + output +  " \\;"
		print(copy_vcf_cmd)
		os.system(copy_vcf_cmd)
		copy_cov_mask_cmd = "find /faststorage/project/clinmicrocore/BACKUP/nanopore_sarscov2/pappenheim_raw/"+ dirname + " -name \'*" + sample + ".coverage_mask.txt\' -exec cp \"{}\" " + output +  " \\;"
		print(copy_cov_mask_cmd)
		os.system(copy_cov_mask_cmd)

	

if __name__ == '__main__':

	# Run as python files_from_pangenome.py ".txt list of sample IDs" "output path"
	samples = sys.argv[1]
	output = sys.argv[2]

	copy_files(samples, output)
