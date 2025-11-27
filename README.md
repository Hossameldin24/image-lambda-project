\# Image Lambda Processor



\## Overview

This project implements an AWS Lambda function to process images uploaded to S3 (e.g., resizing, watermarking).



\## Architecture

!\[Solution Architecture](docs/architecture.png)



\## Components

\- \*\*S3 Original Bucket\*\*: Receives user images.

\- \*\*AWS Lambda\*\*: Triggered by S3 uploads, applies processing.

\- \*\*S3 Processed Bucket\*\*: Stores processed images.

\- \*\*CloudWatch\*\*: Logs Lambda execution.



\## Deployment

1\. Upload Lambda package to AWS.

2\. Configure S3 triggers.

3\. Ensure IAM roles allow S3 read/write for Lambda.



\## Usage

```bash

aws s3 cp "image.jpg" s3://hossam-img-original-1234/

```

