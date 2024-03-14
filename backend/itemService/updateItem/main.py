import boto3
import requests
import json
import hashlib
import base64

def get_dynamodb_table(table_name):
    """Initialize a DynamoDB resource and get the table."""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    return table

def parse_event_body(event_body):
    """Parse the event body, converting from JSON string to dictionary if necessary."""
    if isinstance(event_body, str):
        return json.loads(event_body)
    return event_body

def update_item_in_table(table, newData):
    """Update an item in the DynamoDB table."""
    response = table.put_item(
        Item=newData,
        ReturnValues='ALL_OLD'
    )
    return response

def post_image(image):
    # Get the credentials from AWS Parameter Store
    ssm = boto3.client('ssm')
    parameter_names = []
    key_string = ssm.get_parameter(
        Name="CloudinaryKey",
        WithDecryption=True
    )["Parameter"]["Value"]

    keys = key_string.split(",")

    cloud_name = keys[0]
    api_key = keys[1]
    api_secret = keys[2]

    url = f'https://api.cloudinary.com/v1_1/{cloud_name}/image/upload/'

    # Set up the payload
    payload = {
        'api_key': api_key,
    }
    file = {
        'file': image
    }
    payload["signature"] = create_signature(payload, api_secret)
    res = requests.post(url, files=file, data=payload)
    return res.json()

def create_signature(body, api_secret):
    exclude = ["api_key", "resource_type", "cloud_name"]
    sorted_body = sort_dict(body, exclude)
    query_string = create_query_string(sorted_body)
    query_string = f"{query_string}{api_secret}"
    hashed = hashlib.sha1(query_string.encode("utf-8")).hexdigest()
    return hashed

def sort_dict(dict, exclude):
    myKeys = list(dict.keys())
    myKeys.sort()
    for i in range(len(exclude)):
        if exclude[i] in myKeys:
            myKeys.remove(exclude[i])

    return {i: dict[i] for i in myKeys}

def create_query_string(dict):
    query_string = ""
    for ind, (key, value) in enumerate(dict.items()):
        query_string = f"{key}={value}" if ind == 0 else f"{query_string}&{key}={value}"
    return query_string

def handler(event, context):
    try:
        # Get the table and retrieve the old values
        table_name = 'items-30144999'
        table = get_dynamodb_table(table_name)
        item = table.get_item(Key={"itemID": itemID})["Item"]
        
        old_image_hashes = item["imageHashes"]
        timestamp = item["timestamp"]
        lenderID = item["lenderID"]

        # Parse the event body
        body = parse_event_body(event["body"])
        itemID = body["itemID"]

        # Get the new values
        itemName = body["name"]
        description = body["description"]
        condition = body["condition"]
        location = body["location"]
        tags = body["tags"]

        # Get the image and hashes
        raw_images = body["images"]
        image_urls = []
        image_hashes = []
        for raw_image in raw_images:
            image_bytes = base64.b64decode(raw_image)
            new_image_hash = hashlib.sha256(image_bytes).hexdigest()
            
            # If the image has changed, upload it to Cloudinary, and update the image URL and hash
            if new_image_hash not in old_image_hashes:
                response = post_image(image_bytes)
                image_url = response["secure_url"]
                image_hash = new_image_hash
                
            # If the image has not changed, use the old image URL and hash
            else:
                image_url = table.get_item(Key={"itemID": itemID})["Item"]["image"]
                image_url = table.get_item(Key={"itemID": itemID})["Item"]["image"]

                i = old_image_hashes.index(new_image_hash)
                image_hash = old_image_hashes[i]

            image_urls.append(image_url)
            image_hashes.append(image_hash)

        # Create a new item object
        newInfo = {
            'itemID': itemID,
            'itemName': itemName,
            'condition': condition,
            'description': description,
            'tags': tags,
            'location': location,
            'images': image_urls,
            'imageHashes': image_hashes,
            'lenderID': lenderID,
            'timestamp': timestamp,
            'borrowerID': None
        }


        # Update the item in the table
        response = update_item_in_table(table, newInfo)
        
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }

