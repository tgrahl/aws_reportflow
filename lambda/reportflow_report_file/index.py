import boto3
import csv
import os
import time

def lambda_handler(event, context):
    # Get environment variables
    workgroup_id = os.environ['REDSHIFT_WORKGROUP_ID']  # Workgroup ID for Serverless Redshift
    db_name = os.environ['REDSHIFT_DB']  # Database name
    secret_arn = os.environ['REDSHIFT_SECRET_ARN']  # ARN of the secret in Secrets Manager
    s3_bucket_name = os.environ['S3_BUCKET_NAME']  # S3 Bucket name to save the file

    # Initialize Redshift Data API client and S3 client
    client = boto3.client('redshift-data')
    s3_client = boto3.client('s3')

    # SQL Query to fetch data from the report_output table
    sql_statement = "SELECT * FROM report_output;"

    try:
        # Execute the query
        response = client.execute_statement(
            WorkgroupName=workgroup_id,  # Use Workgroup ID for Serverless
            Database=db_name,
            SecretArn=secret_arn,
            Sql=sql_statement
        )

        # Query execution ID
        query_id = response['Id']
        print(f"Query executed successfully, Query ID: {query_id}")

        # Wait for the query to finish (optional)
        time.sleep(5)

        # Fetch query results
        result = client.get_statement_result(Id=query_id)
        rows = result['Records']

        # If there are no records, raise an exception
        if not rows:
            print("No records found in report_output.")
            raise Exception("No records found in report_output.")

        # Convert the query results into CSV format
        csv_data = []
        headers = [column['name'] for column in result['ColumnMetadata']]
        csv_data.append(headers)  # Add headers to the CSV

        # Convert each row of results into a list of values
        for row in rows:
            csv_data.append([column['stringValue'] if 'stringValue' in column else '' for column in row])

        # Convert the CSV data into a string
        csv_file_content = '\n'.join([','.join(row) for row in csv_data])

        # Generate a unique file name for the CSV file (e.g., based on the timestamp)
        file_name = f"report_output_{int(time.time())}.csv"

        # Upload the CSV content to S3
        s3_client.put_object(
            Bucket=s3_bucket_name,
            Key=file_name,
            Body=csv_file_content
        )

        print(f"CSV file successfully uploaded to S3: {s3_bucket_name}/{file_name}")

        return {
            'statusCode': 200,
            'body': f"CSV file successfully created and uploaded to {s3_bucket_name}/{file_name}"
        }

    except Exception as e:
        print(f"Error: {e}")
        raise e
