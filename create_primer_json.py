import sys

def write_json():
	primer_file = open(sys.argv[1], "r")
	version = sys.argv[2]
	outfilename = sys.argv[1].replace(".primer.bed", ".json")
	out_file = open(outfilename, "w")

	out_file.write('{\n'+'\t'+'"name"' +
		': '+'"'+'nCoV2019 primer scheme v'+version+'"'+',\n'+'\t'+'"amplicons"'+': [\n')
		

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

if __name__ == "__main__":
	write_json()


