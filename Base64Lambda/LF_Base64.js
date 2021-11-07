const AWS = require('aws-sdk');
var s3 = new AWS.S3();

exports.handler = async (event) => {
    // TODO implement
    console.info(JSON.stringify(event));
    let buff = Buffer.from(event.body, "base64");
    let eventBodyStr = buff.toString('UTF-8');
    console.log(eventBodyStr);
    let decodedImage = Buffer.from(eventBodyStr, 'base64');
    var filePath = event.queryStringParameters.item;
    var bucket = event.queryStringParameters.bucket;
    var labels = event.queryStringParameters.customer_labels;
    var params = {
        "Body": decodedImage,
        "Bucket": bucket,
        "Key": filePath,
        "Metadata": {
            'customLabels': labels
        }
    };

    try {
        let uploadOutput = await s3.upload(params).promise();
        let response = {
            "statusCode": 200,
            "body": JSON.stringify(uploadOutput),
            "isBase64Encoded": false,        
            header : {
            'Access-Control-Allow-Origin' : '*'
            }
        };
        return response;
    }
    catch (err) {
        let response = {
            "statusCode": 500,
            "body": JSON.stringify(err),
            "isBase64Encoded": false,
            header : {
            'Access-Control-Allow-Origin' : '*'
            }
        };
        return response;
    }
    //console.info(eventBody);
    const response = {
        header : {
            'Access-Control-Allow-Origin' : '*'
        },
        statusCode: 200,
        body: JSON.stringify(event),
    };
    return response;
};
