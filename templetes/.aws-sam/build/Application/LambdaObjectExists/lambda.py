import boto3
from botocore.errorfactory import ClientError
import json

dynamodb = boto3.resource('dynamodb')
eventsTable = dynamodb.Table('events')

def recordTransaction(client_ip,timestamp,code):
    eventsTable.put_item(Item={"client_ip":client_ip,"timestamp":timestamp,"status_code":code})

def getResponseObj(code):
    if code ==200:
        body = 'The object exists in the s3 bucket!'
    elif code==404:
        body={ "error": 'The object does not exist in s3 bucket!' }
    else:
        body={ "error": 'Bad request!' }
    return {
            "statusCode": code,
            "body": body ,
            "headers": {
                'Content-Type': 'application/json',
            }
        }

def lambda_handler(events,context=None):  #we could have used schema validation on events as decorator function
    client_ip=events['requestContext']['identity']['sourceIp']
    requestTimeEpoch=events['requestContext']['requestTimeEpoch']
    if events["httpMethod"] == "GET":
        s3_object_name = events["queryStringParameters"]["object_name"]
        bucket_name = events["queryStringParameters"]["bucket_name"]
    elif events["httpMethod"] == "POST":
        body=json.loads(events.get("body",""))
        s3_object_name=body.get("bucket_name","")
        bucket_name=body.get("object_name","")
    else:
        return context.fail(getResponseObj(400))

    s3=boto3.client("s3") 

    # Alternatively, a seperate asynchronous lambda invocation for logging records 
    # asynchronously in dynamodb could be performed to provide the user response with minimal latency
    # at the post of another invocation count; but since the operation is not time consuming; this approach was favored

    s3 = boto3.resource('s3')

    try:
        s3.Object(bucket_name, s3_object_name).load()  # performs head operation onto the object, alternatively boto3 client's head_object could have been used as well
        status_code='200'
        print(status_code)
        response=getResponseObj(status_code)
        recordTransaction(client_ip,requestTimeEpoch,status_code)
        return response
    except ClientError as e:
        status_code=int(e.response['Error']['Code'])
        response=getResponseObj(status_code)
        recordTransaction(client_ip,requestTimeEpoch,status_code)
        print(response,status_code)
        return response

if __name__=='__main__':
    event={'resource': '/', 'path': '/', 'httpMethod': 'GET', 'headers': None, 'multiValueHeaders': None, 'queryStringParameters': {'bucket_name': 'teradata-test-bucket-alpha', 'object_name': 'blotch.jpg'}, 'multiValueQueryStringParameters': {'bucket_name': ['teradata-test-bucket-alpha'], 'object_name': ['blotch.jpg']}, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': '5k604g9owc', 'resourcePath': '/', 'httpMethod': 'GET', 'extendedRequestId': 'UpgDzHzmoAMFToQ=', 'requestTime': '02/Jul/2022:17:02:16 +0000', 'path': '/', 'accountId': '188775091215', 'protocol': 'HTTP/1.1', 'stage': 'test-invoke-stage', 'domainPrefix': 'testPrefix', 'requestTimeEpoch': 1656781336200, 'requestId': '06be1353-d309-413c-90db-5b85363947ba', 'identity': {'cognitoIdentityPoolId': None, 'cognitoIdentityId': None, 'apiKey': 'test-invoke-api-key', 'principalOrgId': None, 'cognitoAuthenticationType': None, 'userArn': 'arn:aws:iam::188775091215:user/fahad.mustafa@geinac.com', 'apiKeyId': 'test-invoke-api-key-id', 'userAgent': 'aws-internal/3 aws-sdk-java/1.12.239 Linux/5.4.196-119.356.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.332-b08 java/1.8.0_332 vendor/Oracle_Corporation cfg/retry-mode/standard', 'accountId': '188775091215', 'caller': 'AIDASX467JQH6EUXFRE26', 'sourceIp': 'test-invoke-source-ip', 'accessKey': 'ASIASX467JQH6ZN2WV2O', 'cognitoAuthenticationProvider': None, 'user': 'AIDASX467JQH6EUXFRE26'}, 'domainName': 'testPrefix.testDomainName', 'apiId': 'qyz4z3fngf'}, 'body': None, 'isBase64Encoded': False}
    event2= {'resource': '/', 'path': '/', 'httpMethod': 'GET', 'headers': {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.5', 'Host': 'qyz4z3fngf.execute-api.us-east-1.amazonaws.com', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0', 'X-Amzn-Trace-Id': 'Root=1-62c0968c-3459c8a85b0113321a91c95d', 'X-Forwarded-For': '119.160.64.191', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'accept': ['text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'], 'accept-encoding': ['gzip, deflate, br'], 'accept-language': ['en-US,en;q=0.5'], 'Host': ['qyz4z3fngf.execute-api.us-east-1.amazonaws.com'], 'sec-fetch-dest': ['document'], 'sec-fetch-mode': ['navigate'], 'sec-fetch-site': ['none'], 'sec-fetch-user': ['?1'], 'upgrade-insecure-requests': ['1'], 'User-Agent': ['Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'], 'X-Amzn-Trace-Id': ['Root=1-62c0968c-3459c8a85b0113321a91c95d'], 'X-Forwarded-For': ['119.160.64.191'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': {'bucket_name': 'teradata-test-bucket-alpha', 'object_name': 'blotdch.jpg'}, 'multiValueQueryStringParameters': {'bucket_name': ['teradata-test-bucket-alpha'], 'object_name': ['blotch.jpg']}, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': '5k604g9owc', 'resourcePath': '/', 'httpMethod': 'GET', 'extendedRequestId': 'Upx2BHa0oAMFzyA=', 'requestTime': '02/Jul/2022:19:03:40 +0000', 'path': '/dev/', 'accountId': '188775091215', 'protocol': 'HTTP/1.1', 'stage': 'dev', 'domainPrefix': 'qyz4z3fngf', 'requestTimeEpoch': 1656788620765, 'requestId': '9751c144-8657-4377-8278-bfe3b0f7c34a', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '119.160.64.191', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0', 'user': None}, 'domainName': 'qyz4z3fngf.execute-api.us-east-1.amazonaws.com', 'apiId': 'qyz4z3fngf'}, 'body': None, 'isBase64Encoded': False}

    lambda_handler(event2)


