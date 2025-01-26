# IAM Roles for ReportFlow

## Overview
This document outlines the IAM roles required for the `ReportFlow` project. These roles ensure secure access to AWS services and resources used by the Lambda functions and Step Functions state machine.

---

## IAM Role: `reportflow_lambda_role`

### Purpose
This role is shared by both Lambda functions:  
- `reportflow_report_prep`  
- `reportflow_report_file`  

It provides permissions for the Lambda functions to interact with Redshift, Secrets Manager, and S3.

### Permissions
The following permissions are attached to the `reportflow_lambda_role`:

#### **Amazon Redshift Data API**
- `redshift-data:ExecuteStatement`  
  Allows executing SQL statements on the Redshift database.  
- `redshift-data:GetStatementResult`  
  Allows fetching results from Redshift queries.

#### **AWS Secrets Manager**
- `secretsmanager:GetSecretValue`  
  Allows retrieving Redshift credentials stored securely in Secrets Manager.

#### **Amazon S3**
- `s3:PutObject`  
  Allows writing the generated CSV files to the designated S3 bucket.

### Trust Relationship
This IAM role is trusted by the **Lambda service** (`lambda.amazonaws.com`).

---

## IAM Role: `reportflow_stepfunctions_role`

### Purpose
This role provides the Step Functions state machine with the ability to invoke the Lambda functions and log execution details.

### Permissions
The following permissions are attached to the `reportflow_stepfunctions_role`:

#### **AWS Lambda**
- `lambda:InvokeFunction`  
  Allows the Step Functions state machine to invoke the following Lambda functions:
  - `reportflow_report_prep`
  - `reportflow_report_file`

#### **Amazon CloudWatch Logs**
- `logs:CreateLogGroup`  
  Allows creating new log groups for Step Functions executions.  
- `logs:CreateLogStream`  
  Allows creating new log streams for each Step Functions execution.  
- `logs:PutLogEvents`  
  Allows publishing execution logs to CloudWatch.

### Trust Relationship
This IAM role is trusted by the **Step Functions service** (`states.amazonaws.com`).

---

## Security Best Practices
1. **Least Privilege Access**  
   Ensure each IAM role only has the minimum permissions required to perform its tasks.
2. **Role Rotation**  
   Regularly review and update IAM roles to remove unused permissions.
3. **Monitoring**  
   Use AWS CloudTrail and CloudWatch Logs to monitor usage of these IAM roles.

---

## Additional Notes
- Both IAM roles are crucial for the operation of the `ReportFlow` project and must be properly configured during setup.  
- The roles are referenced directly in the Lambda and Step Functions configurations.  
- Ensure that the policies attached to the roles are updated if additional features or services are introduced in the project.

