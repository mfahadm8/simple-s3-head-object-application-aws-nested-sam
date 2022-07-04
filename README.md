# AWS API with Proxy Integration to VPC Lambda using Nested Cloudformation (SAM)

This repo can be used to check if an object exists within specific specific bucket;

It creates
* An Api Gateway with Lambda Proxy Integration
* Dynamo Table 
* A VPC - 10.1.0.0/16
    * Two private subnets - 10.1.3.0/24 and 10.1.4.0/24 
    * Two public subnets - 10.1.1.0/24 and 10.1.2.0/24 
    * NatGatway, RouteTable Association etc.
    * Security Group 
    * A VPC Endpoint for S3
    * A VPC Endpoint for DynamoDB
* And of course the Lambda inside the VPC


The Lambda upon api call would write the transactions to dynamo Table

I am using Cloudformation (SAM) to deploy an AWS Lambda inside a VPC. All traffic stays within our custom VPC using VPC endpoints (Gateway - using Nat and not AWS PrivateLink). 

## Get Started

### Deploy

```sh
sam deploy  -t template.yaml  --stack-name test-stack  --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND --region us-east-1
```
:tada:

### Remove

You will need to delete the objects from the bucket, otherwise the stack will not be able to delete the bucket.

```sh
aws cloudformation delete-stack --stack-name test-stack 
```

## Api Endpoint
| Sr | Endpoint Url | Method |
| :-: | :-: | 
| 1 | https://uji57wdfx1.execute-api.us-east-1.amazonaws.com/dev | GET |

## Testing
 Please note that permission was only granted to bucket;
| Sr | Parameter Name | 
| :-: | :-: | 
| 1 | bucket_name  | 
| 2 | object_name  | 


### Test Cases

| Sr | bucket_name | object_name | Response
| :-: | :-: | :-: | :-: |
| 1 | teradata-test-bucket-alpha | blotch.jpg | 200 
| 2 | teradatea-test-bucket-alpha | blotch.jpg | 404 

## Explanation

To give Internet access to an AWS Lambda function that is linked to a VPC (eg to access DynamoDB endpoints), you will need one of the following:

   * The AWS Lambda function configured to use a Private Subnet that has a route table entry pointing to a NAT Gateway in the Public Subnet, OR
   * An Elastic IP address assigned to the Elastic Network Interface (ENI) of the Lambda function that appears in the VPC
 
## Attached Screenshots
![Object Found Case](screenshots/Screenshot1.png?raw=true "Object Found Case")

![Object Not Found Case](screenshots/Screenshot2.png?raw=true "Object Not Found Case")