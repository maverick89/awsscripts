import boto3
import sys
import subprocess
import argparse
import config

parser = argparse.ArgumentParser()
parser.add_argument("-r","--region", default="us-east-1",
                    help="Name of the region")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
parser.add_argument("-c","--connect", action="store_true", help="Connect to EC2 instance")
args = parser.parse_args()

#defaultRegion = "us-east-1"

listOfRegions = ["us-east-1","us-west-1","us-west-2","eu-west-1","eu-central-1","sa-east-1","ap-southeast-1","ap-southeast-2","ap-northeast-1","ap-northeast-2"]

region = args.region

if region not in listOfRegions:
	print "Unrecognised region name"
	sys.exit(0)

ec2 = boto3.resource("ec2",region_name=region)


try:
	instances = ec2.instances.filter()

except botocore.exceptions.EndpointConnectionError:
	print "Could not connect to endpoint"
	sys.exit(0)	

instanceList = []
for instance in instances:
	templist = [instance.id, instance.instance_type, instance.tags, instance.private_ip_address, instance.public_ip_address, instance.key_name, instance.state]
	instanceList.append(templist)


lengthOfList = len(instanceList)

print "Total Number of Instances: " + str(lengthOfList);

if args.verbose:

	print '\033[1m' + " ========================================================================================================================================================"
	print "| " + '{:2}'.format("") + "|" +'{:22}'.format("Instance Id")+"| "+'{:26}'.format("Name")+"| "+'{:16}'.format("Instance State")+" | "+'{:18}'.format("Public IP")+"| "+'{:18}'.format("Private IP")+"| "+'{:15}'.format("Instance Type")+"| "+'{:20}'.format("Key Name")+"|"
	print " ========================================================================================================================================================" + '\033[0m'

	for x in range(0,len(instanceList)):
		#print instanceList[x][6]["Name"]
		index = next(index for (index, d) in enumerate(instanceList[x][2]) if d["Key"] == "Name")

		print "| " + '{:2}'.format('%s'%(x))+ "|" + '{:22}'.format(instanceList[x][0]) + "| "+'{:26}'.format(instanceList[x][2][index]["Value"])+"| " +'{:16}'.format(instanceList[x][6]["Name"])+" | " +'{:18}'.format(instanceList[x][4])+"| "+'{:18}'.format(instanceList[x][3])+"| "+'{:15}'.format(instanceList[x][1])+"| "+'{:20}'.format(instanceList[x][5])+"|"

	print '\033[1m' + " ========================================================================================================================================================"
	print '\033[0m'

else:
	print '\033[1m' + " ======================================================"
	print "| " + '{:2}'.format("") + "|" +'{:22}'.format("Instance Id")+"| "+'{:26}'.format("Name")+"| "
	print " ======================================================" + '\033[0m'

	for x in range(0,len(instanceList)):
		#print instanceList[x][6]["Name"]
		index = next(index for (index, d) in enumerate(instanceList[x][2]) if d["Key"] == "Name")

		print "| " + '{:2}'.format('%s'%(x))+ "|" + '{:22}'.format(instanceList[x][0]) + "| "+'{:26}'.format(instanceList[x][2][index]["Value"])+"| " 

	print '\033[1m' + " ======================================================"
	print '\033[0m'

if args.connect:
	index = input('Enter instance number to connect: ')
	if (index>=len(instanceList)):
		print "Invalid choice"
		sys.exit(0)

	userName = raw_input('User name [ec2-user]: ') or "ec2-user"
		
	fName = (item for item in config.listOfKeys if item["region"] == args.region).next()
	keyFile = config.baseDir+fName.get("fileName")
	sshd='ssh -i %s %s@%s'%(keyFile, userName, instanceList[index][4])
	subprocess.call(sshd,shell=True)


