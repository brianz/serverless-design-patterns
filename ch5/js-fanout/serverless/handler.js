'use strict';

var aws = require('aws-sdk');
var lambda = new aws.Lambda({
  region: 'us-west-2'
});


module.exports.imageUpload = (event, context, callback) => {
  const response = {
    statusCode: 200,
    body: JSON.stringify({
      message: 'resized successfully'
			, input: event
    }),
  };

  var params = {
    FunctionName: 'fanout-dev-Resize'
    , InvocationType: "Event"
  }

  var sizes = [128, 256, 1024];
  sizes = [512];

  console.log(JSON.stringify(event))


/*
  for (var i=0; i<sizes.length; i++) {

    params['Payload'] = JSON.stringify({"size": sizes[i]});

    lambda.invoke(params, function(error, data) {
      if (error) {
        console.log('error')
        console.log(error)
      } else {
        console.log('success')
        console.log(data)
      }
    });
  }
*/

  callback(null, response);
};


module.exports.resize = (event, context, callback) => {
  const response = {
    body: JSON.stringify({
      message: 'resizing image'
    }),
  };


  S3.getObject({Bucket: BUCKET, Key: originalKey}).promise()
    .then(data => Sharp(data.Body)
      .resize(width, height)
      .toFormat('png')
      .toBuffer()
    )
    .then(buffer => S3.putObject({
        Body: buffer,
        Bucket: BUCKET,
        ContentType: 'image/png',
        Key: key,
      }).promise()
    )
    .then(() => callback(null, {
        statusCode: '301',
        headers: {'location': `${URL}/${key}`},
        body: '',
      })
    )
    .catch(err => callback(err))

  console.log('Received event:', JSON.stringify(event, null, 2));
  console.log(response)
};
