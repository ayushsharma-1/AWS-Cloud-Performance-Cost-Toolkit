### AWS Cost Optimization

1. **EC2 Instances ($135.57)**
   - **Optimization Suggestion**: Consider **Right-Sizing** EC2 instances by evaluating the performance metrics. If the current instances are underutilized, downgrade to smaller instance types or switch to **Spot Instances** for non-critical workloads.
   - **Potential Savings**: Up to 30-50% for Spot Instances or right-sizing instances to match actual resource needs.
   - **Trade-Off**: Spot Instances can be interrupted, so they are not suitable for all workloads. Right-sizing requires performance monitoring to ensure applications are still running efficiently.

2. **Lambda Functions ($418.41)**
   - **Optimization Suggestion**: Optimize function code to reduce execution time, increase memory efficiency, and eliminate idle periods. Use **AWS Lambda Power Tuning** to find the optimal memory configuration.
   - **Potential Savings**: Reducing function execution time and adjusting memory can lead to savings of 20-30%.
   - **Trade-Off**: This requires performance testing and might involve reworking existing function logic.

3. **Snapshots Cleanup & Optimization**
   - **Optimization Suggestion**: Remove outdated EC2 and S3 snapshots or move them to cheaper storage tiers such as S3 Glacier for long-term retention.
   - **Potential Savings**: Potential savings of 40-50% by deleting unnecessary snapshots or archiving them in lower-cost storage solutions like S3 Glacier.
   - **Trade-Off**: Deleting snapshots or moving them to cold storage may delay access to backups, impacting recovery time in the event of system failures or data restoration needs.
