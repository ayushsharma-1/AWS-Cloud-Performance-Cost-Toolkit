# AWS-Cloud-Performance-Cost-Toolkit
Comprehensive AWS cost optimization, monitoring, and CloudFront optimization for Next.js apps.

### 1. **AWS Cost Optimization (25 points)**

**Key Areas for Cost Reduction:**

1. **Lambda ($418.41):**
   - **Action**: Review and optimize function execution times and memory usage.
   - **Potential Savings**: By lowering allocated memory or optimizing execution times, costs can drop significantly. Consider reserving capacity for predictable workloads to achieve further savings. The trade-off here might be performance impact for latency-sensitive applications.

2. **EC2 Instances ($135.57):**
   - **Action**: Leverage EC2 instance right-sizing and spot instances for less critical workloads.
   - **Potential Savings**: By moving underutilized instances to smaller sizes or switching to spot instances, savings of up to 70% are possible. However, the trade-off would be potential instance termination in the case of spot instances.

3. **Snapshots:**
   - **Action**: Regularly review and delete outdated or unnecessary snapshots.
   - **Potential Savings**: Deleting unnecessary snapshots can lead to significant cost reductions in storage. Establishing a retention policy can help manage snapshot lifecycles effectively.

### 2. **Monitoring and Alerting (25 points)**

**CloudWatch Dashboard Design:**

A well-designed CloudWatch dashboard should provide real-time visibility into the health and performance of critical AWS services. Below is a mockup structure of a CloudWatch dashboard:

- **EC2 Monitoring:**
  - CPU Utilization
  - Network In/Out
  - Disk Read/Write
- **Lambda Monitoring:**
  - Invocations
  - Duration
  - Errors
- **S3 Monitoring:**
  - Bucket size by region
  - Request count
  - 4xx/5xx error rates

**Alarms:**

- **EC2 High CPU Alarm:**
  - **Metric**: `CPUUtilization > 85% for 5 minutes`
  - **Action**: Scale EC2 instances or investigate high-load applications.
  - **Notification**: Set up an AWS SNS notification to email or SMS when this threshold is breached.

- **Lambda Error Rate Alarm:**
  - **Metric**: `Errors > 5 within 1 minute`
  - **Action**: Trigger automatic rollback or scaling operations in case of high error rates.
  - **Notification**: AWS SNS notifications to inform developers of function errors.

**SNS Notification Setup:**
1. Create an SNS topic (e.g., "CriticalAlerts").
2. Subscribe team members via email or SMS.
3. Attach the SNS topic to CloudWatch alarms for real-time notifications.

### 3. **CloudFront Optimization for Next.js Application (50 points)**

**a) High Availability:**
   - **Strategy**: Use CloudFront's origin failover feature with multiple origins (primary: Lambda@Edge, secondary: static S3 bucket) to ensure availability.
   - **Testing**: Simulate failover by intentionally causing failure at the primary origin (Lambda@Edge) and ensuring requests are rerouted to the secondary (S3).
   - **Benefits**: Ensures uninterrupted service even if the main origin fails.

**b) Bot Attack Mitigation:**
   - **Method**: Implement AWS WAF (Web Application Firewall) with rate-limiting rules.
   - **Rate Limiting**: Set limits on the number of requests per IP (e.g., 100 requests per 5 minutes).
   - **Benefits**: Protects against denial-of-service (DoS) attacks and prevents overuse of resources.

**c) SEO Crawler Allowance:**
   - **Implementation**: Use AWS WAF to block malicious bots while allowing legitimate SEO crawlers by filtering User-Agent strings (e.g., "Googlebot", "Bingbot").
   - **IP List**: Maintain a list of allowed IPs for legitimate crawlers.
   - **Benefits**: Ensures SEO indexing while blocking unwanted traffic.

**d) Monitoring:**
   - **Key Metrics**:
     - Cache Hit Rate
     - Origin Latency
     - Request count
     - 4xx/5xx error rates
   - **Logging and Analysis**: Enable CloudFront access logs and integrate with AWS CloudWatch Logs for further analysis using AWS Athena.

**e) Site Loading Time Optimization:**
   - **Methods**:
     1. **Gzip Compression**: Enable Gzip compression in CloudFront to reduce the size of transmitted data.
     2. **Cache TTL Tuning**: Adjust Time-to-Live (TTL) values to cache content longer, reducing origin fetches.
     3. **Edge Locations**: Leverage all available CloudFront edge locations for quicker content delivery to users globally.
   - **Measurement**: Use Amazon CloudWatch and CloudFront logs to measure response times and overall load performance before and after optimization.
