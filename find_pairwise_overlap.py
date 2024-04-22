import sys
import pandas as pd
import os

if len(sys.argv)>2:
	raise Exception("ERROR: Provide one directory only")

path = sys.argv[1]
print("This is the directory: ")
print(path)

files = [ fname for fname in os.listdir(sys.argv[1]) if fname.endswith('.csv')]
print(files)
processed = []
for f1 in files:
	f1_name = f1.split("_")[-1].split(".")[0]
	df1 = pd.read_csv(path+"\\"+f1, header=0, sep = ",")

	df1 = df1.rename(columns=lambda x: x.strip())

	df1 = df1[["Scientific Name","Query Cover","E value","Per. ident","Accession"]]

	df1 = df1.rename(columns={"Query Cover": f"Query Cover ({f1_name})", 
		"E value": f"E value ({f1_name})",
		"Per. ident": f"Per. ident ({f1_name})"})

	for f2 in files:
		f2_name = f2.split("_")[-1].split(".")[0]
		if f1_name != f2_name and f"{f2_name}_{f1_name}" not in processed:
			processed.append(f"{f2_name}_{f1_name}")
			processed.append(f"{f1_name}_{f2_name}")
			print("Processing:", f1, "and", f2)
		
			df2 = pd.read_csv(path+"\\"+f2, header=0, sep = ",")
			df2 = df2.rename(columns=lambda x: x.strip())
			df2 = df2[["Scientific Name","Query Cover","E value","Per. ident","Accession"]]
		
			df = pd.merge(df1, df2, on=["Accession","Scientific Name"], how='inner')
			df = df.rename(columns={"Query Cover": f"Query Cover ({f2_name})", 
				"E value": f"E value ({f2_name})",
				"Per. ident": f"Per. ident ({f2_name})"})

			filename = f1_name + "_" + f2_name+".xlsx"
			df.to_excel(filename)
		#if not df.empty:
		#	df.to_excel(filename)

print("  _                     ")
print(" | \\  _  ._   _    o \\  ")
print(" |_/ (_) | | (/_   o  | ")
print("                     /  ")



