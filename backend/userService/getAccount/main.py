from boto3.dynamodb.conditions import Key
import json
import boto3

dynamodb_resource = boto3.resource("dynamodb", region_name='ca-central-1')
table = dynamodb_resource.Table("users-30144999") 

def handler(event, context):
    email = event["headers"]["email"]
    try:
        res = table.query(KeyConditionExpression=Key("email").eq(email))
        items = res["Items"]
        return {
            "statusCode": 200,
            "body": json.dumps(items)
        }
    except Exception as e:
        print(f"Exception: {e}")
        return {
            "statusCode": 500,
                "body": json.dumps({
                    "message": str(e)
                })     
        }

# Put email in headers:
# fetch('your-api-endpoint', {
#     method: 'GET',
#     headers: {
#         'Content-Type': 'application/json',
#         'email': email // Include email in headers
#     }
# })
