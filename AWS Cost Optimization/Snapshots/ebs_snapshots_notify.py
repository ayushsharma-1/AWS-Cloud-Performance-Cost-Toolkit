import boto3
import json
from datetime import datetime, timedelta

# Initialize clients
ec2 = boto3.client('ec2')
sns = boto3.client('sns')
SNS_TOPIC_ARN = 'arn:aws:sns:YOUR_REGION:YOUR_ACCOUNT_ID:YOUR_SNS_TOPIC'

def lambda_handler(event, context):
    # Get all EBS snapshots
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Get all active EC2 instance IDs
    instances_response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    active_instance_ids = set()

    for reservation in instances_response['Reservations']:
        for instance in reservation['Instances']:
            active_instance_ids.add(instance['InstanceId'])

    snapshots_to_delete = []

    # Identify snapshots to delete
    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')

        if not volume_id:
            snapshots_to_delete.append(snapshot_id)
        else:
            try:
                volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
                if not volume_response['Volumes'][0]['Attachments']:
                    snapshots_to_delete.append(snapshot_id)
            except ec2.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                    snapshots_to_delete.append(snapshot_id)

    # Send notification for permission to delete
    if snapshots_to_delete:
        message = {
            'Snapshots': snapshots_to_delete,
            'Request': 'Permission to delete the following unused snapshots.',
        }
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=json.dumps(message),
            Subject='Request for Snapshot Deletion Permission'
        )
        print("Notification sent for deletion permission.")

