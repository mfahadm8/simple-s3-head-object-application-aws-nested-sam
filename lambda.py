import boto3
from botocore.errorfactory import ClientError
import json

dynamodb = boto3.resource('dynamodb')
eventsTable = dynamodb.Table('events')

def recordTransaction(client_ip,timestamp,code):
    eventsTable.put_item(Item={"client_ip":client_ip,"timestamp":timestamp,"status_code":code})

def getResponseObj(code):
    if code ==200:
        body = { 'success': True,'message':'The object exists in the s3 bucket!'}
    elif code==404:
        body={ "error": 'The object does not exist in s3 bucket!' }
    else:
        body={ "error": 'Bad request!' }
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body),
        "isBase64Encoded": False
    }
    

def lambda_handler(events,context=None):  #we could have used schema validation on events as decorator function
    print(events)
    client_ip=events['requestContext']['identity']['sourceIp']
    requestTimeEpoch=events['requestContext']['requestTimeEpoch']
    try:
        if events["httpMethod"] == "GET":
            s3_object_name = events["queryStringParameters"]["object_name"]
            bucket_name = events["queryStringParameters"]["bucket_name"]
        elif events["httpMethod"] == "POST":
            body=json.loads(events.get("body",""))
            s3_object_name=body.get("bucket_name","")
            bucket_name=body.get("object_name","")
        else:
            return getResponseObj(400)
    except:
        return getResponseObj(400)

    print(bucket_name,s3_object_name)
    # Alternatively, a seperate asynchronous lambda invocation for logging records 
    # asynchronously in dynamodb could be performed to provide the user response with minimal latency
    # at the post of another invocation count; but since the operation is not time consuming; this approach was favored

    s3 = boto3.resource('s3')

    try:
        s3.Object(bucket_name, s3_object_name).load()  # performs head operation onto the object, alternatively boto3 client's head_object could have been used as well
        status_code=200
        print(status_code)
        response=getResponseObj(status_code)
        recordTransaction(client_ip,requestTimeEpoch,status_code)
        return response
    except ClientError as e:
        status_code=int(e.response['Error']['Code'])
        print(status_code)
        response=getResponseObj(status_code)
        recordTransaction(client_ip,requestTimeEpoch,status_code)
        print(response,status_code)
        return response
