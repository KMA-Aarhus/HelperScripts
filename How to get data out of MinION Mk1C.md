Connect the minion MK1C to the internet

## Via filezilla
In filezilla, set
Host: mc-113039
Username: minit
Password: minit
Port:22

## Via ssh
scp -R minit@mc-113039:/data/<run_dir> <destination>
