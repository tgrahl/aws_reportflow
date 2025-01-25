import boto3
import os

# Initialize the Redshift Data API client
client = boto3.client('redshift-data')

def lambda_handler(event, context):
    # Get environment variables
    redshift_cluster_id = os.getenv("REDSHIFT_CLUSTER_ID")  # Redshift Serverless cluster ID
    workgroup_id = os.environ['REDSHIFT_WORKGROUP_ID']  # Workgroup ID for Serverless Redshift
    redshift_db = os.getenv("REDSHIFT_DB")  # Database name
    redshift_user = os.getenv("REDSHIFT_USER")  # User for Redshift
    
    # SQL query to insert data into report_output
    insert_sql = """
    INSERT INTO report_output (transaction_id, transaction_date, amount, currency, description, client_name, country)
    SELECT 
        t.transaction_id, 
        t.transaction_date, 
        t.amount, 
        t.currency, 
        t.description, 
        c.client_name, 
        c.country
    FROM transactions t
    JOIN clients c 
    ON t.client_id = c.client_id;
    """

    try:
        # Run the SQL statement using the Redshift Data API
        response = client.execute_statement(
            WorkgroupName=workgroup_id,
            Database=redshift_db,
            SecretArn=os.getenv("REDSHIFT_SECRET_ARN"),  # Secret ARN for credentials
            Sql=insert_sql
        )

        # Get the statement ID and wait for the query to complete
        statement_id = response['Id']
        print(f"Query started with statement ID: {statement_id}")

        # Check for the status of the query
        result = client.describe_statement(Id=statement_id)
        while result['Status'] not in ['FINISHED', 'FAILED']:
            print("Waiting for query to finish...")
            result = client.describe_statement(Id=statement_id)

        if result['Status'] == 'FINISHED':
            print("Data inserted into report_output table successfully.")
        else:
            print(f"Query failed: {result['Error']}")
            raise Exception(f"Query failed: {result['Error']}")

    except Exception as e:
        print(f"Error occurred: {e}")
        raise

    return {
        "statusCode": 200,
        "body": "Data insertion completed."
    }
