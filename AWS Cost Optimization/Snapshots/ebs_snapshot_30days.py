import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Calculate the date 30 days ago
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    # Get all EBS snapshots
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Iterate through each snapshot and check last use
    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        start_time = snapshot['StartTime']

        # Check if the snapshot is older than 30 days
        if start_time < thirty_days_ago:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted EBS snapshot {snapshot_id} as it was not used in the last 30 days.")
