# CloudWatch Dashboard for ReportFlow

## Overview

This document describes the setup and configuration of the **CloudWatch Dashboard** used for monitoring the performance of the **ReportFlow** platform. The dashboard is designed to track key metrics, including Lambda function performance, query execution times, and checkpoints for each report generation process.

## Dashboard Setup

The dashboard consists of multiple widgets to visualize various aspects of the reporting pipeline. These widgets include metrics for Lambda function performance, execution durations, and logs of key events.

### Step 1: Create CloudWatch Custom Metrics for Lambda Functions

Custom metrics are added to the Lambda functions (`reportflow_report_prep` and `reportflow_report_file`) to track performance. These metrics include:
- Invocation count
- Execution duration

Lambda functions are configured to send these metrics using the `PutMetricData` API call.

### Step 2: Create CloudWatch Dashboard

To visualize the Lambda metrics and logs, a CloudWatch dashboard is created with the following widgets:

### Step 3: Widget Details

#### Widget 1: Lambda Execution Metrics

**Widget Type:** Line  
**Data Type:** Metric  
**Purpose:** Display the execution duration of `reportflow_report_prep` and `reportflow_report_file` Lambda functions.  
**Metrics Tracked:**
- `Duration` (time taken for the function to execute)

#### Widget 2: Lambda Invocation Count

**Widget Type:** Line  
**Data Type:** Metric  
**Purpose:** Display the number of invocations for both Lambda functions.  
**Metrics Tracked:**
- `Invocations` (count of function executions)

#### Widget 3: Query Execution Time

**Widget Type:** Line  
**Data Type:** Metric  
**Purpose:** Display the time taken by the Redshift queries executed within the Lambda functions (`reportflow_report_prep`).  
**Metrics Tracked:**
- Query execution time (custom metric created in the Lambda function code)

#### Widget 4: Logs Insights Widget

**Widget Type:** Logs Table  
**Data Type:** Logs  
**Purpose:** Display logs from both Lambda functions with a focus on key checkpoints.  
**Query Example:**
```sql
fields @timestamp, @message
| filter @message like /Checkpoint/
| sort @timestamp desc
| limit 10
