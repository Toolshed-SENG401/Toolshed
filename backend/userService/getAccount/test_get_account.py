from main import *
import pytest
from moto import mock_aws
import boto3

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    import os
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"

@pytest.fixture
def dynamodb_mock(aws_credentials):
    with mock_aws():
        yield boto3.resource('dynamodb', region_name='ca-central-1')

def test_get_user_from_table(dynamodb_mock):
    "Tests getting from DynamoDB table with valid input"
    table_name = 'users-30144999'
    dynamodb_mock.create_table(
        TableName = table_name, 
        KeySchema = [{'AttributeName': 'email', 'KeyType': 'HASH'}],
        AttributeDefinitions = [{'AttributeName': 'email', 'AttributeType': 'S'}],     
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    table = dynamodb_mock.Table(table_name)
    table.put_item(
        Item={
            "email": "john@example.com",
            "name": "John Doe",
            "rating": 5,
            "bio": "Sample bio",
            "location": "Sample location"
        }
    )

    event = {"headers": {"email": "john@example.com"}}
    context = {}
    response = handler(event, context)

    assert response["statusCode"] == 200, "Status code should be 200 for successful execution"
    response_body = json.loads(response['body'])
    assert len(response_body) == 1, "Expected only one item in the response"
    assert response_body[0]["email"] == "john@example.com", "Incorrect email returned"
    assert response_body[0]["name"] == "John Doe", "Incorrect name returned"
    assert response_body[0]["rating"] == 5, "Incorrect rating returned"
    assert response_body[0]["bio"] == "Sample bio", "Incorrect bio returned"
    assert response_body[0]["location"] == "Sample location", "Incorrect location returned"