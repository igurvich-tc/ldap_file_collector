# ldap file collector
Used to collect files from openstack insances for the purposes of an LDAP groups audit.
Please follow the provided config.conf file as an example to fill your maintenance node name, the project namespace and the instances running within it.
The script will then ssh into the maint node and from it will ssh into the other instances provided to collect the files needed.
The files will be saved into a folder named after the project namespace.
