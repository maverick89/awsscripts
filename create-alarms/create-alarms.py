###################################################################
# Description: Script to create High CPU Utilization alarm for all 
#			   running instances in a VPC.
#
# Author: Truptesh 
#
# Date: 05/09/2017
#
###################################################################

import boto3

ec2client = boto3.client('ec2')
cwclient = boto3.client('cloudwatch')

instance_id_list = []

vpcId = vpc-463a3523;
highCPUAlarm_Threshold = 70.0;
highCPUAlarm_period = 300;
highCPUAlarm_evaluationPeriod = 2;

ec2response = ec2client.describe_instances(
    Filters=[
        {
            'Name': 'vpc-id',
            'Values': [
                vpcId,
            ]
        },
    ]
)

for i in range (0,len(ec2response.get('Reservations'))):
	 instance_id_list.append(ec2response.get('Reservations')[i].get('Instances')[0].get('InstanceId'))

#print instance_id_list


for i in range (0,len(instance_id_list)):
	cwclient.put_metric_alarm(
	    AlarmName='CPUUtilization - ' + instance_id_list[i],
	    AlarmDescription='High CPUUtilization Alarm',
	    ActionsEnabled=True,
	    AlarmActions=[
	        'arn:aws:sns:us-east-1:397212192930:email',
	    ],
	    MetricName='CPUUtilization',
	    Namespace='AWS/EC2',
	    Statistic='Average',
	    Dimensions=[
	        {
	            'Name': 'InstanceId',
	            'Value': instance_id_list[i]
	        },
	    ],
	    Period=highCPUAlarm_period,
	    EvaluationPeriods=highCPUAlarm_evaluationPeriod,
	    Threshold=highCPUAlarm_Threshold,
	    ComparisonOperator='GreaterThanOrEqualToThreshold'
	)



