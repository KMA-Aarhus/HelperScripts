# HelperScripts
Collection of small helper scripts

<h3>create_primer_files.py</h3>
<p>Creates primer.bed, insert.bed, amplicon.bed and json file from a .scheme.bed file such as that found on 
https://github.com/epi2me-labs/wf-artic/tree/master/data/primer_schemes/SARS-CoV-2/Midnight-ONT/V3</p>
<p>Run as:</p>
<code>python create_primer_files.py ".scheme.bed" "output location" </code>
<p>Example:</p>
<code>python create_primer_files.py Midnight-ONT-V3/SARS-CoV-2.scheme.bed Midnight-ONT-V3/ </code>

<h3>create_primer_json.py</h3>
<p>Creates a primer.json file from a primer.bed file</p>
<p>Run as:</p>
<code>python create_primer_json.py VarSkip/nCoV-2019.primer.bed VarSkip </code>

<p><strong>Additional things to remember when updating primers</strong></p>
<p>Rampart reads the primer names in pairs. Hence, if they are not formatted exactly as <primer-name>_LEFT and <primer-name>_RIGHT, Rampart will not recognise it. Additional information such as "_alt" following "_LEFT/_RIGHT" should be removed</p>

<h3>locate_move_vcf.py</h3>
<p>Locates and moves a set of .vcf files from a 'search_folder' and all nested folders within, to one 'target_folder'. Is useful for locating a certain set of output files, that is nested within some cluster output. This script was specifically used for illumina data, but can be tweaked to include non-illumina data. Can also be tweaked to locate and move another type of datatype.</p>
<p>Run as:</p>
<code>python locate_move_vcf.py idXXX.tsv /SEARCH_FOLDER/ /TARGET_FOLDER/</code>

<h3>find_overlap_accession.py</h3>
This script compares a number of result files from NCBI BLAST. This is used for checking if primer/probes share any off-target hits that may result in false positives.
The input is any number of Alignment Descriptions downloaded from the NCBI BLAST result page. The output is a csv files that contain the hits based on Scientific Name and Accession present in all input files.

<h3>find_pairwise_overlap.py</h3>
Works similarly to find_pverlap_accession but takes as input a directory of Alignment Description files from NCBI. It then does pairwise comparisons of all the input files. The outputs are csv files, one for each pair, that contain the hits based on Scientific Name and Accession present in both input files. Files should be named as following example: 222Z43AJ013-Alignment-Descriptions_IS481R.csv. Here "222Z43AJ013-Alignment-Descriptions" is an example of the naming from BLAST and "IS481R" is the primer/probe name.

<h3>files_for_pangenome.py</h3>
<p>This scripts takes as input a file of sample ids, one number per line, and finds the newest vcf and coverage mask files and copies them to a user specified location </p>
<p>Input:</p>
<p>One file containing sample ids</p>
<p>An output directory</p>
<p> Example usage:</p>
<code>python files_for_pangenome.py prøveliste.txt outdir</code>
<p>It looks through pappenheim_clean first in order to locate the correct directory in pappeneheim_raw. This is neccesary due to the very large amount of files present in the pappenheim_raw location which takes more than 2 minuter per sample if subdir is not specified. Also avoids causing slowdown in read/writing.</p>
  
<h3>pangenome.py</h3>
<p>This scripts greates a pangenome plot per gene for a patient that has had multiple samples taken across a span of time.</p> 
<p>Requires the genbank file to be present in the script directory: MN908947.3.gb. The file can be downloaded from https://www.ncbi.nlm.nih.gov/nuccore/MN908947.3/</p>
<p>Conda environment setup:</p>
<code>mamba create -n pangenome -c bioconda python pysam matplotlib pandas numpy vcf-annotator</code>
<p>Input:</p>
<p>One folder of .vcf and coverage mask files (assuming from Oxford Nanopore Sequencing reads)</p>
<p> Example usage:</p>
<code>python pangenome.py filedir</code>
<p>Assumes that the dates contained in the filenames is a close approximation to sample time. If not, rename files to reflect correct dates.</p>
