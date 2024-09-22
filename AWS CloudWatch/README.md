# AWS CloudWatch Monitoring Documentation

## 1. CloudWatch Dashboard Design

The proposed CloudWatch dashboard will provide an overview of critical metrics for AWS resources, specifically EC2 instances, Lambda functions, and S3 buckets. This will help you quickly assess performance and detect potential issues.

### 1.1 Dashboard Widgets Configuration

Below is a JSON configuration for the dashboard widgets. Each widget will visualize specific metrics for monitoring performance.

```json
{
  "widgets": [
    {
      "type": "metric",
      "x": 0,
      "y": 0,
      "width": 6,
      "height": 6,
      "properties": {
        "metrics": [
          ["AWS/EC2", "CPUUtilization", "InstanceId", "i-0123456789abcdef0"]
        ],
        "period": 60,
        "stat": "Average",
        "region": "us-east-1",
        "title": "EC2 CPU Utilization"
      }
    },
    {
      "type": "metric",
      "x": 6,
      "y": 0,
      "width": 6,
      "height": 6,
      "properties": {
        "metrics": [
          ["AWS/EC2", "NetworkIn", "InstanceId", "i-0123456789abcdef0"],
          [".", "NetworkOut", ".", "."]
        ],
        "period": 300,
        "stat": "Sum",
        "region": "us-east-1",
        "title": "EC2 Network In/Out"
      }
    },
    {
      "type": "metric",
      "x": 0,
      "y": 6,
      "width": 6,
      "height": 6,
      "properties": {
        "metrics": [
          ["AWS/EC2", "DiskReadOps", "InstanceId", "i-0123456789abcdef0"],
          [".", "DiskWriteOps", ".", "."]
        ],
        "period": 300,
        "stat": "Sum",
        "region": "us-east-1",
        "title": "EC2 Disk Read/Write Ops"
      }
    },
    {
      "type": "metric",
      "x": 6,
      "y": 6,
      "width": 6,
      "height": 6,
      "properties": {
        "metrics": [
          ["AWS/EC2", "StatusCheckFailed", "InstanceId", "i-0123456789abcdef0"]
        ],
        "period": 60,
        "stat": "Minimum",
        "region": "us-east-1",
        "title": "EC2 Status Check Failed"
      }
    },
    {
      "type": "metric",
      "x": 0,
      "y": 12,
      "width": 6,
      "height": 6,
      "properties": {
        "metrics": [
          ["AWS/S3", "BucketSizeBytes", "BucketName", "your-bucket-name", "StorageType", "Standard"]
        ],
        "period": 86400,
        "stat": "Average",
        "region": "us-east-1",
        "title": "S3 Bucket Size"
      }
    },
    {
      "type": "metric",
      "x": 6,
      "y": 12,
      "width": 6,
      "height": 6,
      "properties": {
        "metrics": [
          ["AWS/S3", "NumberOfObjects", "BucketName", "your-bucket-name", "StorageType", "AllStorageTypes"]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "S3 Number of Objects"
      }
    },
    {
      "type": "metric",
      "x": 0,
      "y": 18,
      "width": 6,
      "height": 6,
      "properties": {
        "metrics": [
          ["AWS/S3", "4xxErrors", "BucketName", "your-bucket-name"],
          [".", "5xxErrors", ".", "."]
        ],
        "period": 300,
        "stat": "Sum",
        "region": "us-east-1",
        "title": "S3 4xx/5xx Errors"
      }
    },
    {
      "type": "metric",
      "x": 6,
      "y": 18,
      "width": 6,
      "height": 6,
      "properties": {
        "metrics": [
          ["AWS/S3", "BytesDownloaded", "BucketName", "your-bucket-name"],
          [".", "BytesUploaded", ".", "."]
        ],
        "period": 300,
        "stat": "Sum",
        "region": "us-east-1",
        "title": "S3 Data Transfer"
      }
    },
    {
      "type": "metric",
      "x": 0,
      "y": 24,
      "width": 6,
      "height": 6,
      "properties": {
        "metrics": [
          ["AWS/Lambda", "Invocations", "FunctionName", "your-lambda-function"]
        ],
        "period": 60,
        "stat": "Sum",
        "region": "us-east-1",
        "title": "Lambda Invocations"
      }
    },
    {
      "type": "metric",
      "x": 6,
      "y": 24,
      "width": 6,
      "height": 6,
      "properties": {
        "metrics": [
          ["AWS/Lambda", "Errors", "FunctionName", "your-lambda-function"]
        ],
        "period": 60,
        "stat": "Sum",
        "region": "us-east-1",
        "title": "Lambda Errors"
      }
    },
    {
      "type": "metric",
      "x": 0,
      "y": 30,
      "width": 6,
      "height": 6,
      "properties": {
        "metrics": [
          ["AWS/Lambda", "Duration", "FunctionName", "your-lambda-function"]
        ],
        "period": 60,
        "stat": "Average",
        "region": "us-east-1",
        "title": "Lambda Duration"
      }
    },
    {
      "type": "metric",
      "x": 6,
      "y": 30,
      "width": 6,
      "height": 6,
      "properties": {
        "metrics": [
          ["AWS/Lambda", "Throttles", "FunctionName", "your-lambda-function"]
        ],
        "period": 60,
        "stat": "Sum",
        "region": "us-east-1",
        "title": "Lambda Throttles"
      }
    },
    {
      "type": "text",
      "x": 12,
      "y": 0,
      "width": 6,
      "height": 6,
      "properties": {
        "markdown": "# Alarm Status\n\n| Alarm Name | State |\n|------------|-------|\n| High CPU   | ALARM |\n| S3 Errors  | OK    |\n"
      }
    }
  ]
}
```

### Explanation of Key Metrics

- **EC2 CPU Utilization**: Measures the percentage of allocated EC2 compute units used by the instance. High utilization can indicate that the instance may require scaling.
  
- **EC2 Network In/Out**: Monitors the amount of data received and sent by the instance. This helps assess network load and bandwidth requirements.
  
- **Disk Read/Write Operations**: Tracks the number of read and write operations on the instance’s disks, helping in understanding disk performance and I/O bottlenecks.

- **S3 Bucket Size**: Displays the total size of the specified S3 bucket, allowing for cost management related to storage.

- **S3 Number of Objects**: Counts the total number of objects in the S3 bucket, useful for understanding data usage and organization.

- **Lambda Function Invocations and Errors**: Monitors the number of times the Lambda function is invoked and the number of errors encountered, helping to ensure function reliability and performance.

## 2. CloudWatch Alarms

### 2.1 High CPU Usage Alarm for EC2 Instances

**Purpose**: To notify when CPU utilization exceeds a specified threshold, indicating potential performance issues.

- **Metric**: `CPUUtilization`
- **Threshold**: Trigger an alarm if CPU utilization exceeds **80%** for **5 consecutive minutes**.
- **Period**: 1 minute.
- **Evaluation Periods**: 3 consecutive periods (totaling 3 minutes).
- **Action**: Notify via SNS.

```json
{
  "AlarmName": "High CPU Usage on EC2",
  "MetricName": "CPUUtilization",
  "Namespace": "AWS/EC2",
  "Statistic": "Average",
  "Threshold": 80.0,
  "ComparisonOperator": "GreaterThanThreshold",
  "EvaluationPeriods": 3,
  "Period": 60,
  "ActionsEnabled": true,
  "AlarmActions": ["arn:aws:sns:region:account-id:HighCPUNotifications"]
}
```

### 2.2 Lambda Function Errors Alarm

**Purpose**: To alert when the number of errors in the Lambda function exceeds a set limit, ensuring reliability in serverless operations.

- **Metric**:

 `Errors`
- **Threshold**: Trigger an alarm if the number of errors exceeds **5** within **5 minutes**.
- **Period**: 1 minute.
- **Evaluation Periods**: 5 consecutive periods (totaling 5 minutes).
- **Action**: Notify via SNS.

```json
{
  "AlarmName": "Lambda Function Error Alarm",
  "MetricName": "Errors",
  "Namespace": "AWS/Lambda",
  "Statistic": "Sum",
  "Threshold": 5,
  "ComparisonOperator": "GreaterThanThreshold",
  "EvaluationPeriods": 5,
  "Period": 60,
  "ActionsEnabled": true,
  "AlarmActions": ["arn:aws:sns:region:account-id:LambdaErrorNotifications"]
}
```

## 3. SNS Notification Setup

To set up notifications for the CloudWatch alarms using Amazon Simple Notification Service (SNS), follow these steps:

### Step 1: Create an SNS Topic
1. **Log into the AWS Management Console**.
2. Navigate to **Amazon SNS**.
3. Click on **Topics** in the left menu, then select **Create topic**.
4. Choose **Standard** as the type.
5. Enter a **name** for your topic (e.g., `HighCPUNotifications` or `LambdaErrorNotifications`).
6. Optionally, provide a display name for SMS notifications.
7. Click **Create topic**.

### Step 2: Subscribe to the SNS Topic
1. After creating the topic, you will see it in the list. Click on the topic name.
2. Click on **Create subscription**.
3. Choose the **protocol** for notifications (e.g., Email, SMS, HTTP/S).
4. Enter the **endpoint** (e.g., your email address for Email subscriptions).
5. Click **Create subscription**.
6. If you chose Email, check your inbox for a confirmation email from AWS and confirm the subscription.

### Step 3: Set Up CloudWatch Alarms with SNS Actions
Now, you can attach the SNS topic to your CloudWatch alarms:

1. Go to the **CloudWatch** service in the AWS Management Console.
2. Click on **Alarms** in the left menu and select **Create alarm**.
3. Choose the metric for which you want to create an alarm (e.g., `CPUUtilization` for EC2 or `Errors` for Lambda).
4. Follow the wizard to configure your alarm settings, such as threshold, evaluation periods, etc.
5. In the **Notification** section:
   - Under **Alarm state trigger**, choose the state for which you want notifications (e.g., "ALARM").
   - Select the SNS topic you created earlier (e.g., `HighCPUNotifications` or `LambdaErrorNotifications`) from the dropdown menu.
6. Review your settings and click **Create alarm**.

### Step 4: Test the Alarm and Notification
- To ensure everything is working correctly, you can temporarily set a lower threshold for the alarm and trigger it by simulating high CPU usage on an EC2 instance or causing errors in a Lambda function.
- Monitor your email or SMS for notifications from the SNS topic when the alarm goes into the ALARM state.


## 4. Conclusion

This documentation provides a comprehensive guide to setting up an effective AWS CloudWatch monitoring system. By utilizing dashboards, alarms, and notifications, you can gain real-time insights into your AWS resources and proactively respond to potential issues. 