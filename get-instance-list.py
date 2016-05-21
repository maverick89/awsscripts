import boto3
import sys


region = (sys.argv)

defaultRegion = "us-east-1"

if len(region)==1:
	region.append(defaultRegion)

try:
	ec2 = boto3.resource("ec2",region_name=region[1])

except ValueError:
	print "Invalid region name"
	sys.exit(0)


try:
	instances = ec2.instances.filter()

except botocore.exceptions.EndpointConnectionError:
	print "Could not connect to endpoint"
	sys.exit(0)	

instanceList = []
i =0
for instance in instances:
	templist = [instance.id, instance.instance_type, instance.tags, instance.private_ip_address, instance.public_ip_address, instance.key_name]

	instanceList.append(templist)
	i = i+1
#print instanceList[0][0]

lengthOfList = len(instanceList)
print "Total Number of Instances: " + str(lengthOfList);

print '\033[1m' + " ======================================================================================================================================"
print "| " + '{:22}'.format("Instance Id")+"| "+'{:30}'.format("Name")+"| "+'{:18}'.format("Public IP")+"| "+'{:18}'.format("Private IP")+"| "+'{:15}'.format("Instance Type")+"| "+'{:20}'.format("Key Name")+"|"
print " ======================================================================================================================================" + '\033[0m'

for x in range(0,len(instanceList)):

	print "| " + '{:22}'.format(instanceList[x][0]) + "| "+'{:30}'.format(instanceList[x][2][0]["Value"])+"| " +'{:18}'.format(instanceList[x][4])+"| "+'{:18}'.format(instanceList[x][3])+"| "+'{:15}'.format(instanceList[x][1])+"| "+'{:20}'.format(instanceList[x][5])+"|"

print '\033[1m' + " ======================================================================================================================================"
print '\033[0m'

