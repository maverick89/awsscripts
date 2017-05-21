import boto3
import sys
import subprocess
import argparse
import config

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r","--region", default="us-east-1",
                        help="Name of the region")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")
    parser.add_argument("-c","--connect", action="store_true", help="Connect to EC2 instance")
    args = parser.parse_args()
    
    listOfRegions = ["us-east-1",
                    "us-west-1",
                    "us-west-2",
                    "eu-west-1",
                    "eu-central-1",
                    "sa-east-1",
                    "ap-southeast-1",
                    "ap-southeast-2",
                    "ap-northeast-1",
                    "ap-northeast-2",
                    "ap-south-1",
                    "us-east-2",
                    "ca-central-1",
                    "eu-west-2"]
    
    mapRegionCodeToRegion = {"iad":"us-east-1",
                            "sfo":"us-west-1",
                            "pdx":"us-west-2",
                            "dub":"eu-west-1",
                            "fra":"eu-central-1",
                            "gru":"sa-east-1",
                            "sin":"ap-southeast-1",
                            "syd":"ap-southeast-2",
                            "nrt":"ap-northeast-1",
                            "icn":"ap-northeast-2",
                            "bom":"ap-south-1",
                            "cmh":"us-east-2",
                            "yul":"ca-central-1",
                            "lhr":"eu-west-2"}
    
    region = args.region
    
    if (region not in listOfRegions) and (region not in mapRegionCodeToRegion.keys()):
    	print "Unrecognised region name"
    	sys.exit(0)
    
    if len(region)==3:
        region=mapRegionCodeToRegion[region]
         
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
    
    listToPrint = []
    
    for x in range(0,len(instanceList)):
        temp = {}
        try:
            index = next(index for (index, d) in enumerate(instanceList[x][2]) if d["Key"] == "Name")
            temp.update({"instanceName": instanceList[x][2][index]["Value"]})
        except:
            temp.update({"instanceName":""}); 
    
        temp.update({"instanceID" : instanceList[x][0]})
        temp.update({"instanceState" : instanceList[x][6]["Name"]})
        temp.update({"publicIP" : instanceList[x][4]})
        temp.update({"privateIP": instanceList[x][3]})
        temp.update({"instanceType": instanceList[x][1]})
        temp.update({"keyName" : instanceList[x][5]})
    
        listToPrint.append(temp)
    
    lengthOfList = len(instanceList)
    
    print "Total Number of Instances: " + str(lengthOfList);
    
    if args.verbose:
    
    	print '\033[1m' + " ========================================================================================================================================================"
    	print "| " + '{:2}'.format("") + "|" +'{:22}'.format("Instance Id")+"| "+'{:26}'.format("Name")+"| "+'{:16}'.format("Instance State")+" | "+'{:18}'.format("Public IP")+"| "+'{:18}'.format("Private IP")+"| "+'{:15}'.format("Instance Type")+"| "+'{:20}'.format("Key Name")+"|"
    	print " ========================================================================================================================================================" + '\033[0m'
    
    	for idx, item in enumerate(listToPrint):
    
    		print "| " + '{:2}'.format(idx+1)+ "|" + '{:22}'.format(item["instanceID"]) + "| "+'{:26}'.format(item["instanceName"])+"| " +'{:16}'.format(item["instanceState"])+" | " +'{:18}'.format(item["publicIP"])+"| "+'{:18}'.format(item["privateIP"])+"| "+'{:15}'.format(item["instanceType"])+"| "+'{:20}'.format(item["keyName"])+"|"
    
    	print '\033[1m' + " ========================================================================================================================================================"
    	print '\033[0m'
    
    else:
    	print '\033[1m' + " ======================================================"
    	print "| " + '{:2}'.format("") + "|" +'{:22}'.format("Instance Id")+"| "+'{:26}'.format("Name")+"| "
    	print " ======================================================" + '\033[0m'
    
    	for idx, item in enumerate(listToPrint):
                print "| " + '{:2}'.format(idx+1)+ "|" + '{:22}'.format(item["instanceID"]) + "| "+'{:26}'.format(item["instanceName"])+"| "
    
    	print '\033[1m' + " ======================================================"
    	print '\033[0m'
    
    if args.connect:
        while (not index):
            index = raw_input('Enter instance number to connect: ')
        try:
            index = int(index) 
        except ValueError:
            print "Please enter an integer"

        if (index>=len(instanceList)+1):
    	    print "Invalid choice"
    	    sys.exit(0)
    
    	userName = raw_input('User name [ec2-user]: ') or "ec2-user"
    	print userName	
    	fName = (item for item in config.listOfKeys if item["region"] == region).next()
    	keyFile = config.baseDir+fName.get("fileName")
    	print 'ssh -i %s %s@%s'%(keyFile, userName, instanceList[index-1][4])
    	sshd='ssh -i %s %s@%s'%(keyFile, userName, instanceList[index-1][4])
    	subprocess.call(sshd,shell=True)
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")
