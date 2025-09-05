# Event-Driven ETL Automation

An AWS-based event-driven ETL (Extract, Transform, Load) pipeline that automatically processes shipping data through a series of transformations and analytics queries.

## Architecture Overview

This project implements a serverless ETL pipeline using AWS services to process shipping data in real-time. The system follows an event-driven architecture where data processing is triggered automatically when new files are uploaded to S3.

### System Flow

```
S3 Landing Bucket → Lambda Trigger → Step Functions → AWS Glue Jobs → S3 Staging → Athena Query → SNS Notification
```

## Components

### 1. Data Generation (`runtime/shipping_schedule_application.py`)
- **Purpose**: Generates synthetic shipping data for testing and demonstration
- **Functionality**: 
  - Creates fake shipping records with customer information, shipping costs, distances, and quantities
  - Uploads data to S3 landing bucket with timestamped filenames
  - Uses Faker library for realistic data generation

### 2. Event Trigger (`runtime/startStepFunction.py`)
- **Purpose**: Lambda function that triggers the ETL pipeline when new files are uploaded
- **Functionality**:
  - Monitors S3 bucket for new file uploads
  - Automatically starts the Step Functions state machine
  - Handles S3 event notifications

### 3. Step Functions Orchestration (`stepFunction/stepfunction.json`)
- **Purpose**: Orchestrates the entire ETL workflow
- **Workflow Steps**:
  1. **Convert JSON to Parquet**: Runs `JSON2Parquet-job` Glue job
  2. **Create Raw Data Catalog**: Starts Glue crawler for raw data
  3. **Process Data**: Runs `data-normalization-job` Glue job
  4. **Create Processed Data Catalog**: Starts Glue crawler for processed data
  5. **Query Processed Data**: Executes Athena query for analytics
  6. **SNS Publish**: Sends results via SNS notification

### 4. ETL Jobs (`glueETL/`)

#### JSON2Parquet-job.py
- **Purpose**: Converts JSON data to Parquet format for better performance
- **Functionality**:
  - Reads JSON files from S3 landing bucket
  - Applies data type mappings
  - Writes transformed data to S3 staging bucket

#### data-normalization-job.py
- **Purpose**: Normalizes and cleans the processed data
- **Functionality**:
  - Reads from the transformed data catalog
  - Removes sensitive fields (customer_name)
  - Writes normalized data to final S3 location

## Data Flow

1. **Data Ingestion**: Synthetic shipping data is generated and uploaded to S3 landing bucket
2. **Event Trigger**: S3 event triggers Lambda function to start Step Functions
3. **Data Transformation**: 
   - JSON files are converted to Parquet format
   - Data is normalized and cleaned
4. **Data Cataloging**: Glue crawlers create/update data catalogs
5. **Analytics**: Athena query calculates shipping metrics
6. **Notification**: Results are published via SNS

## Data Schema

### Input Data (JSON)
```json
{
  "shipping_id": 12345,
  "shipping_date": "2024/01/15",
  "customer_name": "John Doe",
  "street_address": "123 Main St",
  "destination_city": "serverless_island",
  "shipping_cost": 1500.0,
  "shipping_distance": 50.0,
  "quantity": 2500.0,
  "product_id": 67890
}
```

### Output Analytics Query
The system calculates:
- Total shipping costs
- Total shipping distances
- Total fuel quantities

## AWS Services Used

- **S3**: Data storage (landing and staging buckets)
- **Lambda**: Event processing and data generation
- **Step Functions**: Workflow orchestration
- **AWS Glue**: ETL processing and data cataloging
- **Athena**: Analytics queries
- **SNS**: Notifications
- **CloudWatch**: Logging and monitoring

## Prerequisites

- AWS CLI configured with appropriate permissions
- Python 3.x with required packages:
  - `boto3`
  - `faker`
  - `urllib3`

## Setup Instructions

1. **Deploy AWS Resources**:
   - Create S3 buckets for landing and staging data
   - Set up Glue jobs with the provided scripts
   - Create Glue crawlers for data cataloging
   - Deploy Lambda functions
   - Create Step Functions state machine
   - Set up SNS topic

2. **Configure Environment Variables**:
   - `BUCKET_NAME`: S3 landing bucket name
   - `STATE_MACHINE_ARN`: Step Functions state machine ARN

3. **Set up S3 Event Notifications**:
   - Configure S3 bucket to trigger Lambda function on object creation

## Usage

1. **Generate Test Data**:
   ```python
   # Run the shipping_schedule_application.py Lambda function
   # This will generate and upload synthetic shipping data
   ```

2. **Monitor Pipeline**:
   - Check Step Functions console for execution status
   - Monitor CloudWatch logs for detailed processing information
   - Review SNS notifications for final results

## File Structure

```
Event-Driven ETL Automation/
├── glueETL/
│   ├── data-normalization-job.py    # Data cleaning and normalization
│   └── JSON2Parquet-job.py          # JSON to Parquet conversion
├── runtime/
│   ├── shipping_schedule_application.py  # Data generation Lambda
│   └── startStepFunction.py              # Event trigger Lambda
└── stepFunction/
    ├── stepfunction.json            # Step Functions definition
    └── Capture.PNG                  # Architecture diagram
```

## Monitoring and Troubleshooting

- **CloudWatch Logs**: Check Lambda function logs for errors
- **Step Functions Console**: Monitor workflow execution status
- **Glue Console**: Review job runs and crawler status
- **S3 Console**: Verify data files are being created and processed

## Security Considerations

- Customer names are removed during normalization for privacy
- IAM roles should follow least privilege principle
- S3 buckets should have appropriate access controls
- Consider encryption at rest and in transit

## Cost Optimization

- Glue jobs use serverless pricing model
- Step Functions charges per state transition
- S3 storage costs vary by data volume
- Consider data lifecycle policies for cost management

## Future Enhancements

- Add error handling and retry mechanisms
- Implement data quality checks
- Add more sophisticated analytics queries
- Consider real-time streaming with Kinesis
- Add monitoring dashboards with CloudWatch
