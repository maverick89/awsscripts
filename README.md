# awsscripts

get-instance-list.py

Usage:

	usage: get-instance-list.py [-h] [-r REGION] [-v] [-c]

	optional arguments:
	-h, --help            show this help message and exit
	-r REGION, --region REGION
                        Name of the region
    -v, --verbose         increase output verbosity
    -c, --connect         Connect to EC2 instance

Default region is us-east-1

Lists the instance ids, type, IP addresses, name and instance type. You should have aws credentials setup before you can run this.

config.py 

This file should be setup to provide ssh keypair info.
