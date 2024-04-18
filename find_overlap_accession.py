import sys
import pandas as pd

if len(sys.argv)<3:
	raise Exception("ERROR: Provide at least 2 files")

print("These are the files: ")
print(sys.argv)

df = pd.read_csv(sys.argv[1], header=0, sep = ",")

df = df.rename(columns=lambda x: x.strip())

df = df[["Scientific Name","Query Cover","E value","Per. ident","Accession"]]


first_filename = sys.argv[1].split("/")[-1].split(".")[0]

df = df.rename(columns={"Query Cover": f"Query Cover ({first_filename})", 
		"E value": f"E value ({first_filename})",
		"Per. ident": f"Per. ident ({first_filename})"})

df.to_csv("test.csv", sep=",")
for f in sys.argv[2:]:
	filename = f.split("/")[-1].split(".")[0]
	tmp_df = pd.read_csv(f, header=0, sep = ",")
	tmp_df = tmp_df.rename(columns=lambda x: x.strip())
	tmp_df = tmp_df[["Scientific Name","Query Cover","E value","Per. ident","Accession"]]
	
	df = pd.merge(df, tmp_df, on=["Accession","Scientific Name"], how='inner')
	df = df.rename(columns={"Query Cover": f"Query Cover ({filename})", 
			"E value": f"E value ({filename})",
			"Per. ident": f"Per. ident ({filename})"})


df.to_csv("out.csv", sep=",")





