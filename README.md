# AwsCdkExamples
Worked examples of aws cdk usage. Note: you should use the usual cdk bootstrap and init. These projects just container the inner stack code.

In an empty directory run
```shell
cdk init --language python
```
to setup the basic folder structure. You can then copy the project code into the parent and inner folders.
Once setup run with 'cdk deploy' and kill with 'cdk destroy'.

## Project1 - Static Site in S3 -> Cloudfront -> Route53

Prerequisites (one time setup - not all possible/easy with cdk):
- domain name 
- hosted zone in aws, with name servers matching the domain name name servers
- certificate in us-east-1 (for cloudfront) that is registered in the hosted zone

Setup of:
- public bucket with index.html
- cloudfront cache in front of bucket (to save reads to bucket)
- route53 facing the cloudfront cache for proper url

Programatic certificate request is possible, but slow, if needed use (but unsure how to get it in us-east-1):
```python
    my_dns_certificate = aws_certificatemanager.Certificate(
        self,
        "Certificate",
        domain_name=url,
        validation=aws_certificatemanager.CertificateValidation.from_dns(hosted_zone)
    )
```
## Project2 - Timed Event -> Sqs -> Lambda

Setup of:
- Timed event firing every minute
- Sqs taking the events into batches
- Lambda reading each batch when fired


## Project3 - API Gateway -> Lambda Backed Endpoints

Setup of:
- 3 different lambdas
- API gateway with each endpoint routed via a lambda

## Project4 - S3 Object Creation -> Lambda (with requirements.txt)

Setup of:
- lambda taking deps from a requirements.txt
- S3 bucket
- S3 bucket object creation triggers lambda
- template for opensearch cluster creation too if wanted

## Project5 - AWS S3 -> Glue Crawler -> Athena

Setup of:
- s3 buckets for input and output
- AWS glue crawler
- Athena queries
- ETL jobs

## Project6 - AWS Gateway -> Route53

Setup of:
- lambda backed api gateway
- example of environment vars for lambda 
- timeout and resource plan of api gateway
- route53 front to api gateway