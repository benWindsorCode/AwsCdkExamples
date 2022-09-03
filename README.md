# AwsCdkExamples
Worked examples of aws cdk usage. Note: you should use the usual cdk bootstrap and init. These projects just container the inner stack code.

In an empty directory run
```shell
cdk init --language python
```
to setup the basic folder structure. You can then copy the project code into the parent and inner folders.
Once setup run with 'cdk deploy' and kill with 'cdk destroy'.

## Project1 - Static Site in S3

Setup of:
- public bucket with index.html
- cloudfront cache in front of bucket (to save reads to bucket)
- (not complete) route53 facing the cloudfront cache for proper url

Problems: route53 certificate registration hangs for hours. Could sort manually but want a fully automated solution (see github issue linked in code)

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