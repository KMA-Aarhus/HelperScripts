## First time setup on ubuntu machines - installing samba
<code>sudo apt install smbclient cifs-utils</code>

## Mounting the transfering data
<p>Plug the MinION to an ethernet connection. Get IP from the MinION itself. Resets if the devide has been disconnected. Check that connection works</p>
<code>smbclient -L xx.xx.xx.xx -U minit </code>
<p>Mount drive:</p>

<code>sudo mount -t cifs -o vers=3.0,username=minit '//10.31.73.66/data' /mnt </code>
<p>You can now view and copy from all data found in the data dir on the MinION</p>
