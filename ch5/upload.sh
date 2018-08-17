#!/bin/bash
: "${ENV:?Need to set ENV}"
: "${RESIZE_BUCKET_NAME:?Need to set RESIZE_BUCKET_NAME to your existing S3 bucket}"

if [[ ! "$1" ]]; then
    IMG="the-last-jedi-theatrical-poster-tall-A.jpg"
else
    IMG="$1"
fi

 aws s3 cp "$IMG" s3://$RESIZE_BUCKET_NAME-$ENV/ --acl public-read
