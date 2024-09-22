# Cost Reduction by Automating the Deletion Process of Unused EBS Snapshots Using AWS Lambda

## Introduction
This document outlines a strategy for cost reduction in AWS by automating the deletion of unused EBS snapshots using AWS Lambda functions. The implementation leverages Python 3.10 or 3.12 and the Boto3 library. The goal is to minimize unnecessary costs associated with orphaned snapshots while ensuring that operational integrity is maintained through a systematic review process.

## Overview of EBS Snapshots and Costs
Elastic Block Store (EBS) snapshots serve as backups for EBS volumes stored in Amazon S3. While they provide valuable data recovery options, orphaned snapshots (those without associated volumes or instances) lead to ongoing costs that can inflate monthly AWS bills. Therefore, it is essential to implement a solution that identifies and deletes these orphaned snapshots systematically.

## Proposed Solution Using AWS Lambda

### Lambda Function Deployment
1. **Deployment**: Create an AWS Lambda function that will periodically check for orphaned EBS snapshots. The function can be triggered using CloudWatch Events to run at specified intervals (e.g., daily or weekly).

### Scripts Overview
Three scripts will be utilized in this process:

1. **Script 1: Direct Deletion of Orphaned Snapshots**
2. **Script 2: Sending SNS Notifications for Approval Before Deletion**
3. **Script 3: Deleting Snapshots Older than 30 Days Without Usage**

### Script 1: Direct Deletion of Orphaned Snapshots

```python
import boto3

def delete_orphaned_snapshots(event, context):
    ec2 = boto3.client('ec2')
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
    
    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot['VolumeId']
        
        # Check if the snapshot is associated with any active volumes
        volumes = ec2.describe_volumes(VolumeIds=[volume_id])
        if not volumes['Volumes']:
            # Delete orphaned snapshot
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted orphaned snapshot: {snapshot_id}")
```

### Script 2: Sending SNS Notifications for Approval Before Deletion

```python
import boto3

def notify_for_snapshot_deletion(event, context):
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')
    
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
    orphaned_snapshots = []
    
    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']
        volumes = ec2.describe_volumes(VolumeIds=[snapshot['VolumeId']])
        if not volumes['Volumes']:
            orphaned_snapshots.append(snapshot_id)

    if orphaned_snapshots:
        message = f"Orphaned snapshots identified for deletion: {', '.join(orphaned_snapshots)}"
        response = sns.publish(
            TopicArn='arn:aws:sns:region:account-id:topic-name',
            Message=message,
            Subject='Snapshot Deletion Approval Needed'
        )
        print("Notification sent for approval.")
```

### Script 3: Deleting Snapshots Older than 30 Days Without Usage

```python
import boto3
from datetime import datetime, timedelta

def delete_old_snapshots(event, context):
    ec2 = boto3.client('ec2')
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
    threshold_date = datetime.now() - timedelta(days=30)

    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']
        start_time = snapshot['StartTime'].replace(tzinfo=None)

        if start_time < threshold_date:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted snapshot older than 30 days: {snapshot_id}")
```

## Cost Monitoring
Integrate cost monitoring solutions, such as AWS Cost Explorer, to assess savings achieved through the deletion of unused snapshots. Regularly review the cost reports to evaluate the effectiveness of the implemented solution.

## Benefits of the Approach
- **Cost Reduction**: By removing unnecessary snapshots, organizations can significantly lower their AWS bills.
- **Automated Management**: Automating the identification and deletion process reduces manual oversight and operational overhead.
- **Improved Resource Management**: Maintaining an optimal number of snapshots enhances data management practices and ensures efficient utilization of storage resources.

## Conclusion
By implementing AWS Lambda to manage EBS volume snapshots, organizations can proactively reduce unnecessary costs associated with orphaned snapshots. This automated approach leads to immediate cost savings, improved resource management, and promotes accountability in cloud resource utilization. Regular audits and notifications ensure operational integrity while maintaining cost-effectiveness.
