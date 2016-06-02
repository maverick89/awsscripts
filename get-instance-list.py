import boto3
import sys


region = (sys.argv)

defaultRegion = "us-east-1"

listOfRegions = ["us-east-1","us-west-1","us-west-2","eu-west-1","eu-central-1","sa-east-1","ap-southeast-1","ap-southeast-2","ap-northeast-1","ap=northeasr-2"]

if len(region)==1:
	print "No region specified, using default region us-east-1"
	region.append(defaultRegion)

if len(region)>1:
	if region[1] not in listOfRegions:
		print "Unrecognised region name"
		sys.exit(0)

ec2 = boto3.resource("ec2",region_name=region[1])


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

print '\033[1m' + " ====================================================================================================================================================="
print "| " + '{:22}'.format("Instance Id")+"| "+'{:26}'.format("Name")+"| "+'{:16}'.format("Instance State")+" | "+'{:18}'.format("Public IP")+"| "+'{:18}'.format("Private IP")+"| "+'{:15}'.format("Instance Type")+"| "+'{:20}'.format("Key Name")+"|"
print " =====================================================================================================================================================" + '\033[0m'

for x in range(0,len(instanceList)):
	#print instanceList[x][6]["Name"]
	index = next(index for (index, d) in enumerate(instanceList[x][2]) if d["Key"] == "Name")

	print "| " + '{:22}'.format(instanceList[x][0]) + "| "+'{:26}'.format(instanceList[x][2][index]["Value"])+"| " +'{:16}'.format(instanceList[x][6]["Name"])+" | " +'{:18}'.format(instanceList[x][4])+"| "+'{:18}'.format(instanceList[x][3])+"| "+'{:15}'.format(instanceList[x][1])+"| "+'{:20}'.format(instanceList[x][5])+"|"

print '\033[1m' + " ====================================================================================================================================================="
print '\033[0m'

