# AWS VPC Lambda with serverless

This repo can be used to check if an object exists within specific specific bucket;

It creates
* An Api Gateway with Lambda Proxy Integration
* Dynamo Table 
*
* A VPC - 10.1.0.0/16
    * Two private subnets - 10.192.0.0/26 and 10.192.0.64/26
    * Security Group 
    * A VPC Endpoint for S3
    * A VPC Endpoint for Dynamo
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

## Explanation

To give Internet access to an AWS Lambda function that is linked to a VPC (eg to access DynamoDB endpoints), you will need one of the following:

   * The AWS Lambda function configured to use a Private Subnet that has a route table entry pointing to a NAT Gateway in the Public Subnet, OR
   * An Elastic IP address assigned to the Elastic Network Interface (ENI) of the Lambda function that appears in the VPC

This would avoid the need for you to configure a VPC Endpoint for DynamoDB.
