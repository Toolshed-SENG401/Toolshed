from main import *
import pytest
from moto import mock_aws
import boto3
import uuid

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    import os
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"

@mock_aws
def test_write_into_table():
    "Tests writing to DynamoDB table with valid input"
    dynamodb = boto3.resource('dynamodb', region_name='ca-central-1') 
    table_name = 'users-30144999'
    table = dynamodb.create_table(
        TableName = table_name, 
        KeySchema = [{'AttributeName': 'date', 'KeyType': 'HASH'}],
        AttributeDefinitions = [{'AttributeName': 'date', 'AttributeType': 'S'}],                      
    )
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
    
    event = {"body": '{"name": "John Doe", "email": "john@example.com", "rating": 5, "bio": "Sample bio", "location": "Sample location"}'}
    context = {}
    response = handler(event, context)

    assert response["statusCode"] == 200, "Status code should be 200 for successful execution"
    response = table.get_item(Key={'userID': json.loads(response['body'])['userID']})
    item_in_table = response.get('Item', {})

    inserted_item = json.loads(event['body'])
    for key, value in inserted_item.items():
        assert item_in_table.get(key) == value, f"Value for key {key} does not match in the DynamoDB table"


    



# def test_getUser_existing_data(mock_dynamodb):
#     mock_data = {
#         "email": ,
#         "name": "John Doe"
#     } 
#     mock_dynamodb.Table("users_dynamodb_table").put_item(Item=mock_data)

#     event = {"headers": {"email": "john.doe@example.com"}}

    




