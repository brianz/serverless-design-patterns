#!/bin/bash
if [[ ! "$1" ]]; then
    IMG="the-last-jedi-theatrical-poster-tall-A.jpg"
else
    IMG="$1"
fi

aws s3 cp "$IMG" s3://brianz-serverless-resize-dev/ --acl public-read
