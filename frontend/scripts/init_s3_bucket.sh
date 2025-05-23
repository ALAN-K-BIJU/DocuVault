#!/bin/bash

aws s3api create-bucket --bucket your-dms-bucket --region us-east-1
aws s3api put-bucket-versioning --bucket your-dms-bucket --versioning-configuration Status=Enabled
