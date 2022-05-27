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

<h3>pangenome.py</h3>
<p>This scripts greates a pangenome plot for a patient that has had multiple samples taken across a span of time. </p>
<p>Input:</p>
<p>One folder of .vcf and coverage mask files (assuming from Oxford Nanopore Sequencing reads)</p>
<p> Example usage:</p>
<code>python pangenome.py filedir outdir</code>
<p>Assumes that the dates contained in the filenames is a close approximation to sample time. If not, rename files to reflect correct dates.</p>
