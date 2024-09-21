import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('August Cost.csv')
data = data.fillna(0)

# List of columns to plot (ignoring 'Total costs($)' if you don't want to plot it)
columns_to_plot = ['Lambda($)', 'EC2-Instances($)', 'S3($)', 'CloudWatch($)', 'WAF($)',
                   'Elastic Load Balancing($)', 'VPC($)', 'EC2-Other($)', 'SES($)',
                   'X-Ray($)', 'CloudFront($)', 'SQS($)', 'Standup & Prosper($)',
                   'Step Functions($)', 'Amplify($)', 'Route 53($)', 'Secrets Manager($)',
                   'DynamoDB($)', 'Cost Explorer($)', 'EC2 Container Registry (ECR)($)',
                   'IoT($)', 'SNS($)']

# Loop through each column and plot it
for column in columns_to_plot:
    plt.figure(figsize=(10, 6))  # Create a new figure for each plot
    plt.plot(data[column], marker='o')  # Adding markers for better visibility
    
    # Set x-axis limits and ticks based on the number of data points
    plt.xlim(0, len(data)-1)
    plt.xticks(range(0, len(data)+1))  # Set x-ticks from 0 to the length of the data
    
    # Set y-ticks at intervals of 25
    y_ticks = range(0, int(max(data[column])) + 25, 25)
    plt.yticks(y_ticks)
    
    # Enable grid lines
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    
    # Add labels and title
    plt.title(f'{column} Costs Over Time')
    plt.xlabel('Index')
    plt.ylabel(column)
    
    # Show the plot for this column
    plt.show()
