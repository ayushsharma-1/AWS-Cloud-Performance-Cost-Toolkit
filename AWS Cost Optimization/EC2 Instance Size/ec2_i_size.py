import boto3
import json
from datetime import datetime, timedelta

ec2_client = boto3.client('ec2')
cloudwatch_client = boto3.client('cloudwatch')

def lambda_handler(event, context):
    instance_id = event['detail']['instance-id']  # From CloudWatch event
    
    # Get CPU utilization
    cpu_util = get_instance_cpu_utilization(instance_id)
    
    if cpu_util > 70:
        new_instance_type = 't3.large'
    elif cpu_util < 30:
        new_instance_type = 't3.small'
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('Instance utilization is optimal')
        }
    
    # Stop the instance before resizing
    ec2_client.stop_instances(InstanceIds=[instance_id])
    waiter = ec2_client.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[instance_id])

    # Modify the instance type
    ec2_client.modify_instance_attribute(
        InstanceId=instance_id,
        InstanceType={'Value': new_instance_type}
    )
    
    # Restart the instance
    ec2_client.start_instances(InstanceIds=[instance_id])

    return {
        'statusCode': 200,
        'body': json.dumps(f'Instance resized to {new_instance_type}')
    }

def get_instance_cpu_utilization(instance_id):
    response = cloudwatch_client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=datetime.utcnow() - timedelta(minutes=10),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=['Average']
    )
    
    for datapoint in response['Datapoints']:
        return datapoint['Average']
    return 0