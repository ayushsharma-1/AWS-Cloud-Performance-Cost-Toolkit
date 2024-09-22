# EC2 Cost Optimization and Right-Sizing Solution Documentation

## 1. Introduction

This document outlines a comprehensive solution for optimizing EC2 costs and automating the right-sizing of instances based on traffic and utilization metrics. The solution leverages AWS services, including Lambda, CloudWatch, and Auto Scaling, to ensure efficient resource usage and cost reduction.

---

## 2. Cost Analysis

### Key Cost Components

1. **Compute Cost**: Based on instance running time.
2. **Storage Cost**: Associated with EBS volumes attached.
3. **Data Transfer Cost**: Charges for outgoing data transfer.

### Resource Usage Breakdown

- **Total EC2 Bill**: $135.57
- **Instance Type**: Likely a `t3.medium` or `t3.large` instance with increased uptime.
- **Compute Usage**: 
  - `t3.medium` instance at approximately 2056 hours total (85.7 days of usage).
- **Storage**: Estimated at 100-150 GB EBS (gp2) storage, adding $10-$20 in costs.
- **Data Transfer**: Egress increased to around 600-700 GB, costing an additional $10-$20.

### Mathematical Breakdown of Total Costs

\[
\text{Total Cost} = \text{Compute Cost} + \text{Storage Cost} + \text{Data Transfer Cost}
\]
\[
= 85.57 + 15 + 45 = 135.57 \text{ USD/month}
\]

---

## 3. Solution Overview

### Automation Solution Components

1. **CloudWatch Metrics**: Monitoring EC2 instance metrics such as CPU utilization, network in/out, memory utilization, and disk I/O.
2. **Threshold-Based Scaling**: Define thresholds for scaling actions based on utilization.
3. **Lambda Function**: Automates instance resizing based on CloudWatch metrics.
4. **Auto Scaling Group Integration**: Ensures seamless scaling and automatic capacity adjustments.

---

## 4. Implementation Steps

### 4.1 CloudWatch Alarms Setup

- **Alarms**:
  - Trigger a **scale up** when CPU utilization exceeds 70% for more than 5 minutes.
  - Trigger a **scale down** when CPU utilization falls below 30% for more than 5 minutes.

### 4.2 Lambda Function Design

#### Flow Overview

1. **Trigger by CloudWatch Alarm**.
2. **Check Instance Usage**: Monitor CPU, memory, and I/O stats.
3. **Determine Right Instance Size**: Scale up or down based on utilization.
4. **Stop and Resize Instance**: Modify instance type and restart.
5. **Update Auto Scaling Group**: Adjust settings for future instance launches.
6. **Notification and Logging**: Log changes and notify stakeholders.

### 4.3 Sample Lambda Code

Here is the sample Python code using Boto3 for the Lambda function:

```python
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
```

### 4.4 CloudWatch Alarm Configuration

- Set up alarms for CPU utilization to invoke the Lambda function on scaling triggers.

---

## 5. Cost Optimization Strategies

To further reduce the EC2 bill from $135.57, consider the following strategies:

1. **Right-Sizing Instances**: Downgrade instances during low-traffic periods (e.g., from `t3.medium` to `t3.small`).
2. **Auto-Scaling**: Implement aggressive auto-scaling policies to shut down extra instances during off-peak hours.
3. **Data Transfer Optimization**: Utilize caching mechanisms (e.g., CloudFront) to reduce outgoing data transfer costs.
4. **Spot Instances**: Use Spot Instances for non-critical workloads to save on compute costs.
5. **Reserved Instances**: Commit to 1-year or 3-year Reserved Instances for predictable workloads to lock in savings.

---

## 6. Conclusion

This document provides a comprehensive approach to analyzing and optimizing EC2 costs while automating instance right-sizing using AWS Lambda, CloudWatch, and Auto Scaling. By implementing the outlined strategies and utilizing the provided code, organizations can achieve significant cost savings and improve resource efficiency.

---

## 7. Next Steps

1. **Define Thresholds**: Establish appropriate traffic thresholds for triggering scaling actions.
2. **Deploy Lambda Function**: Ensure it has the necessary permissions for EC2 management.
3. **Testing and Adjustment**: Test the solution in a controlled environment and adjust scaling policies as needed.
4. **Integrate with Auto Scaling**: Enhance handling of traffic spikes with Auto Scaling Groups.
