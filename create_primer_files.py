import os
import sys
import pandas as pd


def create_files(primer_scheme, outpath):
	prefix = primer_scheme.split("/")[-1].split(".")[0]
	primer_scheme = pd.read_csv(primer_scheme, sep='\t', header=None)
	#print(primer_scheme)

	primer_bed = primer_scheme.iloc[:, 0:4]
	primer_bed.sort_values(by=primer_bed.columns[1], inplace = True)
	primer_names = primer_bed[3].values.tolist()

	primer_bed[4] = [0 if int(p.split("_")[1]) % 2 == 1 else 1 for p in primer_names]
	primer_bed[5] = ["+" if "LEFT" in p else '-' for p in primer_names]

	#print(primer_bed)
	primer_bed.to_csv(outpath+"/"+prefix+".primer.bed", sep='\t', index=False, header=False)


	insert_dic = {}
	for index, row in primer_scheme.iterrows():
		primer = row[3].replace("_LEFT","").replace("_RIGHT","")
		if primer not in insert_dic:
			insert_dic[primer] = []
		pos_dict = {}

		if "LEFT" in row[3]:
			insert_dic[primer].append("MN908947.3")
			insert_dic[primer].append(row[2])
		elif "RIGHT" in row[3]:
			insert_dic[primer].append(row[1])
			if int(primer.split("_")[-1]) % 2 == 1:
				insert_dic[primer].append(1)
			else: 
				insert_dic[primer].append(2)
			insert_dic[primer].append("+")

	insert_bed = pd.DataFrame(insert_dic).transpose()
	insert_bed.to_csv(outpath+"/"+prefix+".insert.bed", sep='\t', index=False, header=False)

	amplicon_dic = {}
	for index, row in primer_scheme.iterrows():
		primer = row[3].replace("_LEFT","").replace("_RIGHT","")
		if primer not in amplicon_dic:
			amplicon_dic[primer] = []
		pos_dict = {}

		if "LEFT" in row[3]:
			amplicon_dic[primer].append("MN908947.3")
			amplicon_dic[primer].append(row[2])
		elif "RIGHT" in row[3]:
			amplicon_dic[primer].append(row[1])
			if int(primer.split("_")[-1]) % 2 == 1:
				amplicon_dic[primer].append(1)
			else: 
				amplicon_dic[primer].append(2)
			amplicon_dic[primer].append("+")

	amplicon_bed = pd.DataFrame(amplicon_dic).transpose()
	amplicon_bed.to_csv(outpath+"/"+prefix+".amplicon.bed", sep='\t', index=False, header=False)

	write_json(outpath+"/"+prefix+".primer.bed", outpath, prefix)

def write_json(primer_bed, outpath, prefix):
	primer_file = open(primer_bed, "r")
	version = outpath.split("/")[-1]
	outfilename = prefix + ".json"
	out_file = open(outpath+ "/"+outfilename, "w")

	out_file.write('{\n'+'\t'+'"name"' +
		': '+'"'+'nCoV2019 primer scheme '+version+'"'+',\n'+'\t'+'"amplicons"'+': [\n')		
	line = primer_file.readline()

	#out_file.write()
	c = 1
	while line != "":
		if c % 2 == 0 and c > 2:
			out_file.write(",\n")
		line_list = line.split()
		primer_name = line_list[3]
		if "LEFT" in primer_name:
			start = line_list[1]
		if "RIGHT" in primer_name:
			end = line_list[2]
			out_file.write("\t\t[" + str(start) + "," + str(end) + "]")
		line = primer_file.readline()
		c += 1

	out_file.write('\n\t]\n}')
	

if __name__ == '__main__':

	# Run as python files_from_pangenome.py ".txt list of sample IDs" "output path"
	primer_scheme = sys.argv[1]
	outpath = sys.argv[2]

	create_files(primer_scheme, outpath)