# ReportFlow Project

ReportFlow is a data processing and reporting platform built with AWS Lambda, Redshift Serverless, and S3. It automates the extraction, transformation, and loading (ETL) of data, and generates reports stored in CSV files within an S3 bucket.

## Table of Contents

- [Project Overview](#project-overview)
- [Components](#components)
  - [Lambda Functions](#lambda-functions)
  - [Redshift Serverless](#redshift-serverless)
  - [S3 Bucket](#s3-bucket)
- [Environment Variables](#environment-variables)
- [Database Schema](#database-schema)
  - [Tables](#tables)
  - [Sample Data](#sample-data)
- [Deployment Instructions](#deployment-instructions)
- [CI/CD Pipeline](#cicd-pipeline)
- [Contributing](#contributing)

---

## Project Overview

ReportFlow automates the generation of business reports by querying data from Redshift, processing it, and saving the results in CSV format in an S3 bucket. The platform consists of two main Lambda functions that are triggered sequentially:

1. **reportflow_report_prep** - Prepares data by querying Redshift and loading the output into a report table.
2. **reportflow_report_file** - Reads the report table, processes the data, and stores the results as a CSV file in an S3 bucket.

---

## Components

### Lambda Functions

- **reportflow_report_prep**: 
  - Reads data from Redshift tables (`transactions`, `client`) and prepares the data for the report.
  - Saves the processed data into a report table in Redshift.
  
- **reportflow_report_file**: 
  - Reads the report table in Redshift.
  - Exports the results to a CSV file and uploads the file to an S3 bucket for access.

### Redshift Serverless

The project uses Redshift Serverless for data storage and query execution. It includes the following tables:

- **transactions**: Stores transaction data.
- **client**: Stores client information.
- **report_output**: Stores the final processed report data.

### S3 Bucket

The **ReportFlow** platform stores the output of the reports in an S3 bucket. The bucket stores the CSV files generated by `reportflow_report_file`.

---

## Environment Variables

The following environment variables are used by the Lambda functions:

- **REDSHIFT_DB**: The name of your Redshift database.
- **REDSHIFT_USER**: The user used to connect to Redshift.
- **REDSHIFT_SECRET_ARN**: ARN of the secret stored in AWS Secrets Manager to access Redshift credentials.
- **S3_BUCKET_NAME**: The name of the S3 bucket where the report CSV file will be stored.

---

## Database Schema

### Tables

#### `transactions`
Stores transaction data.

| Column            | Type     | Description                     |
|-------------------|----------|---------------------------------|
| `transaction_id`  | INT      | Primary key for the transaction |
| `client_id`       | INT      | Foreign key to the client       |
| `transaction_date`| DATE     | Date of the transaction         |
| `amount`          | DECIMAL  | Transaction amount              |

#### `client`
Stores client information.

| Column            | Type     | Description                  |
|-------------------|----------|------------------------------|
| `client_id`       | INT      | Primary key for the client   |
| `client_name`     | VARCHAR  | Name of the client           |

#### `report_output`
Stores the processed data for reports.

| Column            | Type     | Description                     |
|-------------------|----------|---------------------------------|
| `report_id`       | INT      | Unique report identifier        |
| `client_name`     | VARCHAR  | Name of the client             |
| `total_transactions` | INT    | Total number of transactions   |
| `total_amount`    | DECIMAL  | Total amount of transactions   |

### Sample Data

You can seed your Redshift tables with sample data using the SQL scripts stored in the `redshift/seed_data/` directory.

## Monitoring and Logging

The ReportFlow platform has a CloudWatch dashboard for monitoring Lambda functions and Redshift performance. It tracks execution times, invocations, and logs checkpoints.

For more details on the CloudWatch dashboard setup, refer to the [CloudWatch Dashboard Documentation](./docs/CloudWatch_Dashboard.md).

## Deployment Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/reportflow.git
   cd reportflow
