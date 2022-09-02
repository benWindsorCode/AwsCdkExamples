# AwsCdkExamples
Worked examples of aws cdk usage. Note: you should use the usual cdk bootstrap and init. These projects just container the inner stack code.

Once setup run with 'cdk deploy' and kill with 'cdk destroy'.

# Project1 - Static Site in S3

Setup of:
- public bucket with index.html
- cloudfront cache in front of bucket (to save reads to bucket)
- (not complete) route53 facing the cloudfront cache for proper url

Problems: route53 certificate registration hangs for hours. Could sort manually but want a fully automated solution (see github issue linked in code)

# Project2 - Timed Event -> Sqs -> Lambda

Setup of:
- Timed event firing every minute
- Sqs taking the events into batches
- Lambda reading each batch when fired
