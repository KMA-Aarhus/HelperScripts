# HelperScripts
Collection of small helper scripts

<h3>create_primer_json.py</h3>
<p>Creates a primer.json file from a primer.bed file</p>
<p>Run as:</p>
<code>python create_primer_json.py VarSkip/nCoV-2019.primer.bed VarSkip </code>

<p><strong>Additional things to remember when updating primers</strong></p>
<p>Rampart reads the primer names in pairs. Hence, if they are not formatted exactly as <primer-name>_LEFT and <primer-name>_RIGHT, Rampart will not recognise it. Additional information such as "_alt" following "_LEFT/_RIGHT" should be removed</p>
